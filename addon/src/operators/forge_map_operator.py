# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
from pathlib import Path
import re
from typing import final
import urllib.error
import urllib.request


import bpy
from bpy.types import Collection, Context, Object, Operator
from mathutils import Matrix, Vector

from ..model.importer.model_importer import ModelImporter

from ..json_definitions import ForgeObjectDefinition

from ..madeleine.forge_level_reader import ForgeFolder, get_forge_map
from ..utils import get_data_folder, get_import_properties, read_json_file


@final
class ForgeMapOperator(Operator):
    bl_idname = "ekur.importforgemap"
    bl_label = "Import"
    bl_options = {"REGISTER", "UNDO"}

    _geometry_cache: dict[str, list[Object]] = {}

    def _get_or_create_geometry(self, global_id: str) -> list[Object]:
        if global_id in self._geometry_cache or bpy.context.scene is None:
            return self._geometry_cache[global_id]

        data = get_data_folder()
        path = f"{data}/models/{global_id}.ekur"
        if not Path(path).exists():
            path = f"{data}/runtime_geo/{global_id}.ekur"
        geo_importer = ModelImporter()
        imported_objects = geo_importer.start_import(path, bones=False)

        master_collection = bpy.data.collections.get("Master Geometries")
        if not master_collection:
            master_collection = bpy.data.collections.new("Master Geometries")
            bpy.context.scene.collection.children.link(master_collection)  # pyright: ignore[reportUnknownMemberType]

        master_collection.hide_viewport = True
        master_collection.hide_render = True

        source_objects = imported_objects
        for source_object in source_objects:
            if source_object.name in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.unlink(source_object)  # pyright: ignore[reportUnknownMemberType]
            master_collection.objects.link(source_object)  # pyright: ignore[reportUnknownMemberType]

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
        props = get_import_properties()
        try:
            with (
                urllib.request.urlopen(props.url) as response,  # pyright: ignore[reportAny]
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

    def execute(self, context: Context | None) -> set[str]:
        props = get_import_properties()
        data = get_data_folder()
        split = props.url.split("/")
        asset, version = "", ""
        if not props.use_file:
            if split[2] == "cylix.guide":
                asset, version = split[6], split[7]
            if split[2] == "www.halowaypoint.com":
                asset = split[6]
                version = self.get_waypoint_version()
        objects, categories, root = get_forge_map(asset, version, props.mvar_file)
        objects_path = Path(f"{data}/forge_objects.json")
        definition = read_json_file(objects_path, ForgeObjectDefinition)
        if definition is None or context is None or context.scene is None:
            return {"CANCELLED"}
        cats: dict[ForgeFolder, tuple[Collection, list[tuple[ForgeFolder, Collection]]]] = {}
        for category in categories:
            cats[category] = self.create_categories(category, context.scene.collection)
        root_folder = [col for col in cats.items() if col[0].id == root][0]
        for object in objects:
            name: str = ""
            main_collection: Collection | None = None
            if props.import_folders:
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
            representation = [
                m
                for m in object_def["representations"]
                if m["name_int"] == object.variant
                if not m["is_rtgo"]
            ]
            if len(representation) == 0:
                representation = [
                    m
                    for m in object_def["representations"]
                    if m["variant"] == object.variant
                    if not m["is_rtgo"]
                ]
            if len(representation) == 0:
                representation = [
                    m for m in object_def["representations"] if m["name_int"] == object.variant
                ]
            if len(representation) == 0:
                continue
            source_objects = self._get_or_create_geometry(str(representation[0]["model"]))
            objects = [obj for obj in source_objects if object.variant == obj["permutation_name"]]
            if len(objects) == 0:
                objects = [obj for obj in source_objects if object.variant == obj["region_name"]]
            if len(objects) == 0:
                objects = source_objects
            for obj in objects:
                instance_obj = bpy.data.objects.new(
                    name=f"{representation[0]['name']}_instance", object_data=obj.data
                )
                instance_obj["permutation_name"] = obj["permutation_name"]
                instance_obj["region_name"] = obj["region_name"]
                if name != "":
                    instance_obj.name = name

                instance_obj.location = object.position
                forward = Vector(object.rotation_forward).normalized()
                up = Vector(object.rotation_up).normalized()
                right = forward.cross(up)
                if type(up) is Vector and type(right) is Vector:
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
                    instance_obj.rotation_mode = "QUATERNION"
                    instance_obj.rotation_quaternion = quat
                    instance_obj.scale = object.scale
                    if main_collection:
                        main_collection.objects.link(instance_obj)  # pyright: ignore[reportUnknownMemberType]
                    else:
                        root_folder[1][0].objects.link(instance_obj)  # pyright: ignore[reportUnknownMemberType]
        self._geometry_cache = {}
        return {"FINISHED"}
