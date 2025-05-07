# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy

from pathlib import Path
from typing import final
from bpy.types import Context, Operator, Object
from mathutils import Matrix

from ..ui.level_options import get_level_options
from ..json_definitions import Level
from ..model.importer.model_importer import ModelImporter
from ..utils import get_data_folder, read_json_file

__all__ = ["ImportLevelOperator"]


@final
class ImportLevelOperator(Operator):
    bl_idname = "ekur.importlevel"
    bl_label = "Import"
    bl_options = {"REGISTER", "UNDO"}

    def __init__(self, *args, **kwargs) -> None:  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        super().__init__(*args, **kwargs)
        self.index: int = 0
        self._geometry_cache = {}

    def _get_or_create_geometry(
        self,
        global_id: str,
        data_folder: str,
        materials: list[int],
    ) -> list[Object]:
        if global_id in self._geometry_cache or bpy.context.scene is None:
            return self._geometry_cache[global_id]

        path = f"{data_folder}/runtime_geo/{global_id}.ekur"
        geo_importer = ModelImporter()
        imported_objects = geo_importer.start_import(path, materials=materials, bones=False)

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

    def execute(self, context: Context | None) -> set[str]:
        self._geometry_cache: dict[str, list[Object]] = {}
        if context is None or context.collection is None:
            return {"CANCELLED"}
        options = get_level_options()

        level_path = Path(options.level_path)
        level = read_json_file(level_path, Level)
        if level is None:
            return {"CANCELLED"}
        data = get_data_folder()

        for instance in level["instances"]:
            source_objects = self._get_or_create_geometry(
                str(instance["global_id"]), data, instance["material"]
            )
            for source_object in source_objects:
                instance_obj = bpy.data.objects.new(
                    name=f"{source_object.name}_instance", object_data=source_object.data
                )
                rotmat = Matrix(
                    (
                        (instance["forward"][0], instance["left"][0], instance["up"][0], 0.0),
                        (instance["forward"][1], instance["left"][1], instance["up"][1], 0.0),
                        (instance["forward"][2], instance["left"][2], instance["up"][2], 0.0),
                        (0.0, 0.0, 0.0, 1.0),
                    )
                )
                instance_obj.matrix_world = Matrix.LocRotScale(
                    instance["position"], rotmat.to_quaternion(), instance["scale"]
                )

                context.collection.objects.link(instance_obj)  # pyright: ignore[reportUnknownMemberType]

        self._geometry_cache = {}
        return {"FINISHED"}
