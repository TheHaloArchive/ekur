# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from pathlib import Path
from typing import final

import bpy
from bpy.types import Context, Mesh, Operator

from .material_operator import import_materials
from ..json_definitions import ForgeObjectDefinition
from ..utils import get_data_folder, get_import_properties, read_json_file
from ..model.importer.model_importer import ModelImporter

__all__ = ["ForgeOperator"]


@final
class ForgeOperator(Operator):
    bl_idname = "ekur.importforge"
    bl_label = "Import"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}
        properties = get_import_properties()
        selected_model = properties.objects

        represnt = properties.object_representation
        data = get_data_folder()

        objects_path = Path(f"{data}/forge_objects.json")
        definition = read_json_file(objects_path, ForgeObjectDefinition)
        if definition is None:
            return {"CANCELLED"}
        if context.scene is None:
            return {"CANCELLED"}

        for category in definition["root_categories"]:
            if category["sub_categories"] is None:
                continue
            for subcategory in category["sub_categories"]:
                if subcategory["objects"] is None:
                    continue
                for obj in subcategory["objects"]:
                    if not obj["name"] == selected_model:
                        continue
                    for representation in obj["representations"]:
                        if not representation["name"] == represnt:
                            continue
                        model_path = Path(f"{data}/models/{representation['model']}.ekur")
                        objects = ModelImporter().start_import(str(model_path), bones=False)
                        collection = bpy.data.collections.new(obj["name"])
                        count = 0
                        for bl_obj in objects:
                            if type(bl_obj.data) is Mesh and "UV1" in bl_obj.data.uv_layers:
                                bl_obj.data.uv_layers["UV1"].active_render = True
                                bl_obj.data.uv_layers["UV1"].active = True
                            if str(representation["name_int"]) == str(
                                bl_obj["permutation_name"]  # pyright: ignore[reportAny]
                            ):
                                count += 1
                                collection.objects.link(bl_obj)  # pyright: ignore[reportUnknownMemberType]
                        if count == 0:
                            for bl_obj in objects:
                                if bl_obj["permutation_name"] == 528041935:
                                    count += 1
                                    collection.objects.link(bl_obj)  # pyright: ignore[reportUnknownMemberType]
                        if count == 0:
                            for bl_obj in objects:
                                collection.objects.link(bl_obj)  # pyright: ignore[reportUnknownMemberType]
                        context.scene.collection.children.link(collection)  # pyright: ignore[reportUnknownMemberType]
                        for object in collection.objects:
                            object.select_set(True)  # pyright: ignore[reportUnknownMemberType]
                            if context.view_layer:
                                context.view_layer.objects.active = object
                            properties.use_default = False
                            properties.coat_id = str(obj["id"])
                            import_materials()
                        break

        return {"FINISHED"}
