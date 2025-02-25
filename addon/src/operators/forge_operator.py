# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from pathlib import Path
from typing import cast, final

import bpy
from bpy.types import Context, Mesh, Operator

from ..json_definitions import ForgeObjectDefinition
from ..utils import read_json_file
from ..model.importer.model_importer import ModelImporter

__all__ = ["ForgeOperator"]


@final
class ForgeOperator(Operator):
    bl_idname = "ekur.importforge"
    bl_label = "Import"

    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}
        properties = context.scene.import_properties  # pyright: ignore[reportAttributeAccessIssue, reportUnknownVariableType, reportUnknownMemberType]
        selected_model = cast(str, properties.objects)
        data = cast(
            str,
            context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder,  # pyright: ignore[reportAttributeAccessIssue]
        )
        objects_path = Path(f"{data}/forge_objects.json")
        definition = read_json_file(objects_path, ForgeObjectDefinition)
        for category in definition["root_categories"]:
            if category["sub_categories"] is None:
                continue
            for subcategory in category["sub_categories"]:
                if subcategory["objects"] is None:
                    continue
                for obj in subcategory["objects"]:
                    if obj["name"] == selected_model:
                        model_path = Path(f"{data}/models/{obj['model']}.ekur")
                        objects = ModelImporter().start_import(context, str(model_path), bones=False)
                        collection = bpy.data.collections.new(obj["name"])
                        count = 0
                        for bl_obj in objects:
                            if type(bl_obj.data) is Mesh and "UV1" in bl_obj.data.uv_layers:
                                bl_obj.data.uv_layers["UV1"].active_render = True
                                bl_obj.data.uv_layers["UV1"].active = True
                            if obj["variant"] == bl_obj["permutation_name"]:
                                count += 1
                                collection.objects.link(bl_obj) # pyright: ignore[reportUnknownMemberType]
                        if count == 0:
                            for bl_obj in objects:
                                collection.objects.link(bl_obj) # pyright: ignore[reportUnknownMemberType]
                        context.scene.collection.children.link(collection) # pyright: ignore[reportUnknownMemberType]
                        break

        return {"FINISHED"}
