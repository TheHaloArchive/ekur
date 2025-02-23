# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import cast, final

import bpy
from bpy.types import Collection, Context, Operator

from ..model.importer.model_importer import ModelImporter

__all__ = ["ImportModelOperator"]


@final
class ImportModelOperator(Operator):
    bl_idname = "ekur.importmodel"
    bl_label = "Import"

    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}
        properties = context.scene.import_properties  # pyright: ignore[reportAttributeAccessIssue, reportUnknownVariableType, reportUnknownMemberType]
        model_path = cast(str, properties.model_path)
        model_name = model_path.split("/")[-1].split(".")[0]
        objects = ModelImporter().start_import(context, model_path)
        collections: dict[int, Collection] = {}
        model_collection = bpy.data.collections.new(model_name)
        bpy.context.scene.collection.children.link(model_collection)  # pyright: ignore[reportUnknownMemberType]

        if cast(bool, properties.import_collections):
            for object in objects:
                permutation_name: int = object["permutation_name"]
                region_name: int = object["permutation_name"]

                region_collection_name = f"{region_name}_{permutation_name}"
                if permutation_name not in collections:
                    permutation_collection = bpy.data.collections.new(str(permutation_name))
                    model_collection.children.link(permutation_collection)  # pyright: ignore[reportUnknownMemberType]
                    collections[permutation_name] = permutation_collection
                else:
                    permutation_collection = collections[permutation_name]

                if permutation_collection.children.get(region_collection_name) is None:
                    region_collection = bpy.data.collections.new(region_collection_name)
                    permutation_collection.children.link(region_collection)  # pyright: ignore[reportUnknownMemberType]
                else:
                    region_collection = permutation_collection.children.get(region_collection_name)
                if region_collection is not None:
                    region_collection.objects.link(object)  # pyright: ignore[reportUnknownMemberType]
        else:
            for object in objects:
                model_collection.objects.link(object)  # pyright: ignore[reportUnknownMemberType]
        return {"FINISHED"}
