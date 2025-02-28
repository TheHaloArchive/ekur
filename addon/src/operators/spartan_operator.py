# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
from pathlib import Path
from typing import final

import bpy
from bpy.types import Collection, Context, Object, Operator

from ..model.importer.model_importer import ModelImporter

from ..json_definitions import (
    CustomizationGlobals,
    CustomizationRegion,
    CustomizationTheme,
    NameRegion,
)
from ..utils import get_data_folder, get_import_properties, read_json_file

__all__ = ["ImportSpartanOperator"]


@final
class ImportSpartanOperator(Operator):
    bl_idname = "ekur.importspartan"
    bl_label = "Import Spartan"
    bl_options = {"REGISTER", "UNDO"}

    def __init__(self, *args, **kwargs) -> None:  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        super().__init__(*args, **kwargs)
        self.region_cache: dict[str, Collection] = {}

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
            themes = [theme for theme in themes if theme["name"] == properties.core]

        names_path = Path(f"{data_folder}/regions_and_permutations.json")
        names = read_json_file(names_path, dict[str, NameRegion])
        if not names_path.exists():
            logging.warning(f"Names path does not exist!: {names_path}")
            return {"CANCELLED"}

        for theme in themes:
            theme_col = bpy.data.collections.new(theme["name"])
            global_collection.children.link(theme_col)  # pyright: ignore[reportUnknownMemberType]
            for region in theme["regions"]:
                self.import_region(region, theme, objects, importer, theme_col, "REGION", names)
            for region in theme["prosthetics"]:
                self.import_region(
                    region, theme, objects, importer, theme_col, "PROSTHETICS", names
                )
            for region in theme["body_types"]:
                self.import_region(region, theme, objects, importer, theme_col, "BODY TYPE", names)

            kits_collections = bpy.data.collections.new(f"[KITS] {theme['name']}")
            for kit in theme["kits"]:
                kit_collection = bpy.data.collections.new(f"[KIT] {kit['name']}")
                for region in kit["regions"]:
                    self.import_region(
                        region, theme, objects, importer, kit_collection, "KIT", names
                    )
                kits_collections.children.link(kit_collection)  # pyright: ignore[reportUnknownMemberType]
            if kits_collections.name not in theme_col.children:
                theme_col.children.link(kits_collections)  # pyright: ignore[reportUnknownMemberType]

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
        names: dict[str, NameRegion],
    ) -> None:
        data_folder = get_data_folder()
        if len(region["permutations"]) > 0 and id == "KIT":
            region["permutations"] = [region["permutations"][0]]
        for perm in region["permutation_regions"]:
            name = f"[{id}] {theme['name']}_{region['name']}"
            region_collection = self.region_cache.get(name)
            if region_collection is None:
                region_collection = bpy.data.collections.new(name)
                self.region_cache[name] = region_collection

            if region_collection.name not in theme_collection.children:
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
                        region_name = names.get(str(mode["region_name"]))  # pyright: ignore[reportAny]
                        if region_name:
                            perm_name = region_name["permutations"].get(
                                str(mode["permutation_name"])  # pyright: ignore[reportAny]
                            )
                            if perm_name:
                                mode.name = f"{region['name']}_{perm_name['name']}"
                        if mode.name not in region_collection.objects:
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
