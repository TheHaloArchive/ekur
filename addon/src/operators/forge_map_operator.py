# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from pathlib import Path
from typing import final

import bpy
from bpy.types import Context, Object, Operator
from mathutils import Matrix, Vector

from ..model.importer.model_importer import ModelImporter

from ..json_definitions import ForgeObjectDefinition

from ..madeleine.forge_level_reader import get_forge_map
from ..utils import get_data_folder, get_import_properties, read_json_file


@final
class ForgeMapOperator(Operator):
    bl_idname = "ekur.importforgemap"
    bl_label = "Import"
    bl_options = {"REGISTER", "UNDO"}

    _geometry_cache: dict[str, list[Object]] = {}

    def _get_or_create_geometry(self, global_id: str) -> list[Object]:
        if (
            global_id in self._geometry_cache
            or bpy.context.collection is None
            or bpy.context.scene is None
        ):
            return self._geometry_cache[global_id]

        data = get_data_folder()
        path = f"{data}/models/{global_id}.ekur"
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
            if source_object.name in bpy.context.collection.objects:
                bpy.context.collection.objects.unlink(source_object)  # pyright: ignore[reportUnknownMemberType]
            master_collection.objects.link(source_object)  # pyright: ignore[reportUnknownMemberType]

        self._geometry_cache[global_id] = source_objects
        return source_objects

    def execute(self, context: Context | None) -> set[str]:
        props = get_import_properties()
        data = get_data_folder()
        objects = get_forge_map(props.asset_id, props.version_id)
        objects_path = Path(f"{data}/forge_objects.json")
        definition = read_json_file(objects_path, ForgeObjectDefinition)
        if definition is None:
            return {"CANCELLED"}
        for object in objects:
            object_def = [
                obj[1] for obj in definition["objects"].items() if str(object.global_id) == obj[0]
            ]
            representation = [
                representation
                for representation in object_def[0]["representations"]
                if representation["name_int"] == object.variant
                or representation["variant"] == object.variant
                or representation["variant"] == 0
            ]
            if len(representation) >= 1:
                source_objects = self._get_or_create_geometry(str(representation[0]["model"]))
                for obj in source_objects:
                    instance_obj = bpy.data.objects.new(
                        name=f"{obj.name}_instance", object_data=obj.data
                    )

                    if len(object.position) != 3:
                        i = len(object.position)
                        while i != 3:
                            object.position.append(0)
                            i += 1
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
                    if len(object.scale) == 3:
                        instance_obj.scale = object.scale
                    if (
                        bpy.context.scene
                        and instance_obj.name not in bpy.context.scene.collection.objects
                    ):
                        bpy.context.scene.collection.objects.link(instance_obj)  # pyright: ignore[reportUnknownMemberType]

        self._geometry_cache = {}
        return {"FINISHED"}
