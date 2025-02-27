# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
from pathlib import Path
from typing import final

import bpy
from bpy.types import Collection, Context, Object, Operator

from ..model.importer.model_importer import ModelImporter

from ..json_definitions import CustomizationGlobals, CustomizationRegion, CustomizationTheme
from ..utils import get_data_folder, get_import_properties, read_json_file

__all__ = ["ImportSpartanOperator"]


@final
class ImportSpartanOperator(Operator):
    bl_idname = "ekur.importspartan"
    bl_label = "Import Spartan"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}

        data_folder = get_data_folder()
        properties = get_import_properties()

        customization_path = Path(f"{data_folder}/customization_globals.json")
        if not customization_path.exists():
            logging.warning(f"Customization globals path does not exist!: {customization_path}")
            return {"CANCELLED"}

        customization_globals = read_json_file(customization_path, CustomizationGlobals)
        model_path = Path(f"{data_folder}/models/{customization_globals['model']}.ekur")
        if not model_path.exists():
            logging.warning(f"Model path does not exist!: {model_path}")
            return {"CANCELLED"}
        importer = ModelImporter()
        objects = importer.start_import(str(model_path))
        global_collection = bpy.data.collections.new("Spartans")
        themes = customization_globals["themes"]
        if properties.import_specific_core:
            themes = [theme for theme in themes if str(theme["name"]) == properties.core]

        for theme in themes:
            theme_col = bpy.data.collections.new(str(theme["name"]))
            global_collection.children.link(theme_col)  # pyright: ignore[reportUnknownMemberType]
            for region in theme["regions"]:
                self.import_region(region, theme, objects, importer, theme_col, "REGION")
            for region in theme["prosthetics"]:
                self.import_region(region, theme, objects, importer, theme_col, "PROSTHETICS")
            for region in theme["body_types"]:
                self.import_region(region, theme, objects, importer, theme_col, "BODY TYPE")

            attachment_collection = bpy.data.collections.new(f"[ATTACHMENTS] {theme['name']}")
            theme_col.children.link(attachment_collection)  # pyright: ignore[reportUnknownMemberType]
            for attachment in theme["attachments"]:
                model_path = f"{data_folder}/models/{attachment['model']}.ekur"
                attachments = ModelImporter().start_import(model_path, False)
                alt_name = f"{attachment['marker_name']}"
                for attach in attachments:
                    for marker in importer.markers:
                        self.import_attachments("", alt_name, marker, attach)
                        if attach.name not in attachment_collection.objects:
                            attachment_collection.objects.link(attach)  # pyright: ignore[reportUnknownMemberType]

        if context.scene:
            context.scene.collection.children.link(global_collection)  # pyright: ignore[reportUnknownMemberType]
        return {"FINISHED"}

    def import_attachments(
        self,
        name: str,
        alt_name: str,
        marker: Object,
        attachment: Object,
    ) -> None:
        if marker.name == name or alt_name in marker.name:
            empty_global_transform = marker.matrix_world
            mesh_global_transform = attachment.matrix_world
            offset = (
                -(mesh_global_transform.translation - empty_global_transform.translation) * 3.048
            )
            attachment.location = offset
            attachment.rotation_euler = (0.0, 0.0, 0.0)

    def import_region(
        self,
        region: CustomizationRegion,
        theme: CustomizationTheme,
        objects: list[Object],
        importer: ModelImporter,
        theme_collection: Collection,
        id: str,
    ) -> None:
        data_folder = get_data_folder()
        for perm in region["permutation_regions"]:
            region_collection = bpy.data.collections.new(f"[{id}] {theme['name']}_{region['name']}")
            theme_collection.children.link(region_collection)  # pyright: ignore[reportUnknownMemberType]
            for perm_region in region["permutations"]:
                model = [
                    object
                    for object in objects
                    if object["permutation_name"] == perm_region["name"]
                    and object["region_name"] == perm
                ]
                if len(model) >= 1:
                    for mode in model:
                        region_collection.objects.link(mode)  # pyright: ignore[reportUnknownMemberType]
                if perm_region["attachment"]:
                    model_path = f"{data_folder}/models/{perm_region['attachment']['model']}.ekur"
                    attachments = ModelImporter().start_import(model_path, False)
                    for attachment in attachments:
                        for marker in importer.markers:
                            name = f"{perm_region['attachment']['marker_name']}_{perm}_{perm_region['name']}"
                            alt_name = f"{perm_region['attachment']['marker_name']}_{perm}"
                            self.import_attachments(name, alt_name, marker, attachment)
                            if attachment.name not in region_collection.objects:
                                region_collection.objects.link(attachment)  # pyright: ignore[reportUnknownMemberType]

            if len(region_collection.objects) == 0:
                theme_collection.children.unlink(region_collection)  # pyright: ignore[reportUnknownMemberType]
