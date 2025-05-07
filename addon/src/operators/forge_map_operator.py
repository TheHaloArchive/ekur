# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
import re
import urllib.error
import urllib.request
import bpy

from pathlib import Path
from typing import final
from bpy.types import (
    Collection,
    Context,
    Mesh,
    Object,
    Operator,
)
from mathutils import Matrix, Quaternion, Vector

from .material_operator import import_materials
from ..ui.forge_map_options import get_forge_map_options
from ..ui.material_options import get_material_options
from ..constants import BLOCKER_MATERIAL, INCORRECT_RTGOS
from ..model.importer.model_importer import ModelImporter
from ..json_definitions import ForgeMaterial, ForgeObjectDefinition, ForgeObjectRepresentation

from ..madeleine.forge_level_reader import ForgeFolder, ForgeLevel, get_forge_map
from ..utils import get_data_folder, read_json_file


def apply_rtgo_transform(
    pos: list[float],
    offset: Vector,
    scale: list[float],
    rotation: Quaternion,
) -> list[float]:
    scaled_offset = Vector(
        (
            offset[0] * scale[0],
            offset[1] * scale[1],
            offset[2] * scale[2],
        )
    )
    scaled_offset.rotate(rotation)  # pyright: ignore[reportUnknownMemberType]
    new_axis: list[float] = [
        pos[0] + scaled_offset[0],
        pos[1] + scaled_offset[1],
        pos[2] + scaled_offset[2],
    ]
    return new_axis


@final
class ForgeMapOperator(Operator):
    bl_idname = "ekur.importforgemap"
    bl_label = "Import"
    bl_options = {"REGISTER", "UNDO"}

    _geometry_cache: dict[str, list[Object]] = {}

    def __init__(self, *args, **kwargs) -> None:  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        super().__init__(*args, **kwargs)
        self.index: int = 0

    def _get_or_create_geometry(self, global_id: str, style: int) -> list[Object]:
        if global_id in self._geometry_cache or bpy.context.scene is None:
            return self._geometry_cache[global_id]

        data = get_data_folder()
        props = get_material_options()
        path = f"{data}/models/{global_id}.ekur"
        if not Path(path).exists():
            path = f"{data}/runtime_geo/{global_id}.ekur"
        geo_importer = ModelImporter()
        imported_objects = geo_importer.start_import(path, bones=False)

        master_collection = bpy.data.collections.get("Master Geometries")
        if not master_collection:
            master_collection = bpy.data.collections.new("Master Geometries")
            bpy.context.scene.collection.children.link(master_collection)  # pyright: ignore[reportUnknownMemberType]

        source_objects = imported_objects
        for source_object in source_objects:
            if source_object.name in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.unlink(source_object)  # pyright: ignore[reportUnknownMemberType]
            master_collection.objects.link(source_object)  # pyright: ignore[reportUnknownMemberType]
            source_object.select_set(True)  # pyright: ignore[reportUnknownMemberType]
            if bpy.context.view_layer:
                bpy.context.view_layer.objects.active = source_object
            props.use_default_coating = False
            props.coating_id = str(style)
            import_materials()
            source_object.select_set(False)  # pyright: ignore[reportUnknownMemberType]

        self._geometry_cache[global_id] = source_objects
        return source_objects

    def create_categories(
        self, category: ForgeFolder, parent: Collection, is_subcat: bool = False
    ) -> tuple[Collection, list[tuple[ForgeFolder, Collection]]]:
        category_collection = bpy.data.collections.new(category.name)
        parent.children.link(category_collection)  # pyright: ignore[reportUnknownMemberType]
        if is_subcat:
            return category_collection, []
        subcats: list[tuple[ForgeFolder, Collection]] = []
        for subcat in category.subcategories:
            if subcat.parent == category.id:
                subcats.append(
                    (subcat, self.create_categories(subcat, category_collection, True)[0])
                )
        return category_collection, subcats

    def get_waypoint_version(self) -> str:
        options = get_forge_map_options()
        try:
            with (
                urllib.request.urlopen(options.url) as response,  # pyright: ignore[reportAny]
            ):
                html: str = response.read().decode("utf-8")  # pyright: ignore[reportAny]
                match = re.search(
                    r"""VersionId"\s*:\s*"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})""",
                    html,
                )
                if match:
                    return match.group(1)
        except urllib.error.HTTPError as e:
            logging.error(f"Failed to download waypoint html: {e.status}")
        return ""

    def get_asset_version(self, split: list[str]) -> tuple[str, str]:
        options = get_forge_map_options()
        asset, version = "", ""
        if not options.use_file:
            if split[2] == "cylix.guide":
                asset, version = split[6], split[7]
            if split[2] == "www.halowaypoint.com":
                asset = split[6]
                version = self.get_waypoint_version()
        return asset, version

    def create_category(
        self, context_col: Collection, level: ForgeLevel
    ) -> tuple[
        dict[ForgeFolder, tuple[Collection, list[tuple[ForgeFolder, Collection]]]],
        tuple[ForgeFolder, tuple[Collection, list[tuple[ForgeFolder, Collection]]]],
    ]:
        cats: dict[ForgeFolder, tuple[Collection, list[tuple[ForgeFolder, Collection]]]] = {}
        for category in level.categories:
            cats[category] = self.create_categories(category, context_col)
        rootf = [col for col in cats.items() if col[0].id == level.root_category]
        root_folder = None
        if rootf != []:
            root_folder = rootf[0]
        if not root_folder:
            root = [fol for fol in cats.items() if fol[0].id == 4294967295]
            if len(root) > 0:
                root_folder = root[0]
        if not root_folder:
            root_folder = [col for col in cats.items()][0]
        return cats, root_folder

    def execute(self, context: Context | None) -> set[str]:
        options = get_forge_map_options()
        data = get_data_folder()
        split = options.url.split("/")
        asset, version = self.get_asset_version(split)
        level = get_forge_map(asset, version, options.mvar_file)
        objects_path = Path(f"{data}/forge_objects.json")
        definition = read_json_file(objects_path, ForgeObjectDefinition)
        globals_path = Path(f"{data}/forge_materials.json")
        globals = read_json_file(globals_path, ForgeMaterial)
        if definition is None or context is None or context.scene is None or globals is None:
            return {"CANCELLED"}
        cats, root_folder = self.create_category(context.scene.collection, level)
        for object in level.objects:
            self.index = 0
            name: str = ""
            main_collection: Collection | None = None
            if options.import_folders:
                for folder, (collection, children) in cats.items():
                    for obj in folder.objects:
                        if obj.index == object.index and obj.parent == folder.id:
                            if obj.name != "":
                                name = obj.name
                            main_collection = collection
                    for child, collection in children:
                        for obj in child.objects:
                            if obj.index == object.index and obj.parent == child.id:
                                if obj.name != "":
                                    name = obj.name
                                main_collection = collection

            object_def = definition["objects"].get(str(object.global_id))
            if object_def is None:
                continue
            repres: None | ForgeObjectRepresentation = None
            non_rtgo = [m for m in object_def["representations"] if not m["is_rtgo"]]
            matching = [m for m in non_rtgo if m["name_int"] == object.variant]
            if (object.variant == 0 and len(non_rtgo) > 0) or len(non_rtgo) == 1:
                repres = non_rtgo[0]
            elif len(matching) == 0 and len(non_rtgo) > 1:
                if object.global_id in INCORRECT_RTGOS:
                    repres = non_rtgo[0]
                else:
                    repres = non_rtgo[1]
            elif len(non_rtgo) == 0 and len(object_def["representations"]) != 0:
                repres = object_def["representations"][0]
            elif len(matching) > 0:
                repres = matching[0]
            else:
                continue
            source_objects = self._get_or_create_geometry(str(repres["model"]), repres["style"])
            objects = [obj for obj in source_objects if object.variant == obj["permutation_name"]]
            if len(objects) == 0:
                objects = [obj for obj in source_objects if object.variant == obj["region_name"]]
            if len(objects) == 0:
                objects = source_objects
            for obj in objects:
                if options.remove_blockers:
                    mats = [
                        m
                        for m in obj.material_slots
                        if m.material and m.material.name in BLOCKER_MATERIAL
                    ]
                    if len(mats) > 0:
                        continue
                if obj.data is None:
                    continue
                instance_obj = bpy.data.objects.new(
                    name=f"[{object.mode.name}] {repres['name']}_instance",
                    object_data=obj.data.copy(),
                )

                if name != "":
                    instance_obj.name = name

                forward = Vector(object.rotation_forward).normalized()
                up = Vector(object.rotation_up).normalized()
                right = forward.cross(up)
                if type(up) is not Vector or type(right) is not Vector:
                    continue
                right = right.normalized()
                rot_matrix = Matrix(
                    (
                        (forward[0], -right[0], up[0], 0.0),
                        (forward[1], -right[1], up[1], 0.0),
                        (forward[2], -right[2], up[2], 0.0),
                        (0.0, 0.0, 0.0, 1.0),
                    )
                )
                quat = rot_matrix.to_quaternion()
                instance_obj.location = Vector(
                    apply_rtgo_transform(object.position, obj.location, object.scale, quat)
                )
                instance_obj.rotation_mode = "QUATERNION"
                instance_obj.rotation_quaternion = quat
                instance_obj.scale = object.scale
                if main_collection:
                    main_collection.objects.link(instance_obj)  # pyright: ignore[reportUnknownMemberType]
                elif root_folder:
                    root_folder[1][0].objects.link(instance_obj)  # pyright: ignore[reportUnknownMemberType]
                elif bpy.context.scene:
                    bpy.context.scene.collection.objects.link(instance_obj)  # pyright: ignore[reportUnknownMemberType]

                if type(instance_obj.data) is Mesh and "UV1" in instance_obj.data.uv_layers:
                    instance_obj.data.uv_layers["UV1"].active_render = True
                    instance_obj.data.uv_layers["UV1"].active = True
        master_collection = bpy.data.collections.get("Master Geometries")
        if master_collection:
            master_collection.hide_viewport = True
            master_collection.hide_render = True

        return {"FINISHED"}
