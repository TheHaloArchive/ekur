# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import final

import bpy
from bpy.types import Collection, Context, Operator

from ..utils import get_import_properties

from ..model.importer.model_importer import ModelImporter

__all__ = ["ImportModelOperator"]


@final
class ImportModelOperator(Operator):
    bl_idname = "ekur.importmodel"
    bl_label = "Import"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: Context | None) -> set[str]:
        if context is None or context.scene is None:
            return {"CANCELLED"}
        properties = get_import_properties()
        model_path = properties.model_path
        model_name = model_path.split("/")[-1].split(".")[0]
        if model_name == model_path:
            model_name = model_path.split("\\")[-1].split(".")[0]
        objects = ModelImporter().start_import(model_path)
        collections: dict[int, Collection] = {}
        model_collection = bpy.data.collections.new(model_name)
        context.scene.collection.children.link(model_collection)  # pyright: ignore[reportUnknownMemberType]

        if properties.import_collections:
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
