# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
import bpy

from pathlib import Path
from typing import final
from bpy.types import Collection, Context, Object, Operator
from ..ui.spartan_options import get_spartan_options
from ..operators.spartan_online_operator import import_attachments
from ..model.importer.model_importer import ModelImporter
from ..json_definitions import (
    CustomizationGlobals,
    CustomizationRegion,
    CustomizationTheme,
    NameRegion,
)
from ..utils import (
    get_data_folder,
    get_package_name,
    import_custom_rig,
    read_json_file,
)

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
        options = get_spartan_options()

        customization_path = Path(f"{data_folder}/customization_globals.json")
        if not customization_path.exists():
            logging.warning(f"Customization globals path does not exist!: {customization_path}")
            return {"CANCELLED"}

        customization_globals = read_json_file(customization_path, CustomizationGlobals)
        if customization_globals is None:
            return {"CANCELLED"}
        model_path = Path(f"{data_folder}/models/{customization_globals['model']}.ekur")
        if not model_path.exists():
            logging.warning(f"Model path does not exist!: {model_path}")
            return {"CANCELLED"}
        importer = ModelImporter()
        rig = import_custom_rig()
        objects = importer.start_import(str(model_path), custom_rig=rig)
        global_collection = bpy.data.collections.new("Spartans")
        themes = customization_globals["themes"]
        if options.import_specific_core:
            themes = [theme for theme in themes if theme["name"] == options.core]

        extension_path = bpy.utils.extension_path_user(get_package_name(), create=True)
        names_path = Path(f"{extension_path}/regions_and_permutations.json")
        names = read_json_file(names_path, dict[str, NameRegion])
        if names is None:
            return {"CANCELLED"}

        for theme in themes:
            self.import_theme(theme, global_collection, objects, importer, names, rig)
        if context.scene:
            context.scene.collection.children.link(global_collection)  # pyright: ignore[reportUnknownMemberType]
            if rig and rig.name not in context.scene.collection.objects:
                context.scene.collection.objects.link(rig)  # pyright: ignore[reportUnknownMemberType]
        return {"FINISHED"}

    def import_theme(
        self,
        theme: CustomizationTheme,
        global_collection: Collection,
        objects: list[Object],
        importer: ModelImporter,
        names: dict[str, NameRegion],
        rig: Object | None,
    ) -> None:
        data_folder = get_data_folder()
        theme_col = bpy.data.collections.new(theme["name"])
        global_collection.children.link(theme_col)  # pyright: ignore[reportUnknownMemberType]
        for region in theme["regions"]:
            self.import_region(region, theme, objects, importer, theme_col, "REGION", names, rig)
        for region in theme["prosthetics"]:
            self.import_region(region, theme, objects, importer, theme_col, "PROSTH", names, rig)
        for region in theme["body_types"]:
            self.import_region(region, theme, objects, importer, theme_col, "BT", names, rig)

        kits_collections = bpy.data.collections.new(f"[KITS] {theme['name']}")
        for kit in theme["kits"]:
            kit_col = bpy.data.collections.new(f"[KIT] {kit['name']}")
            for region in kit["regions"]:
                self.import_region(
                    region, theme, objects, importer, kit_col, "KIT", names, rig, kit["name"]
                )
            kits_collections.children.link(kit_col)  # pyright: ignore[reportUnknownMemberType]
        if kits_collections.name not in theme_col.children:
            theme_col.children.link(kits_collections)  # pyright: ignore[reportUnknownMemberType]

        attachment_collection = bpy.data.collections.new(f"[ATTACHMENTS] {theme['name']}")
        theme_col.children.link(attachment_collection)  # pyright: ignore[reportUnknownMemberType]
        for attachment in theme["attachments"]:
            model_path = f"{data_folder}/models/{attachment['model']}.ekur"
            attachments = ModelImporter().start_import(model_path, False)
            alt_name = f"{attachment['marker_name']}"
            attach_name = names.get(str(attachment["tag_id"]))
            for attach in attachments:
                if attach_name:
                    attach.name = attach_name["name"]
                markers = [marker for marker in importer.markers if alt_name in marker.name]
                import_attachments("", alt_name, markers[-1], attach, rig)
                if attach.name not in attachment_collection.objects:
                    attachment_collection.objects.link(attach)  # pyright: ignore[reportUnknownMemberType]

    def import_region(
        self,
        region: CustomizationRegion,
        theme: CustomizationTheme,
        objects: list[Object],
        importer: ModelImporter,
        theme_collection: Collection,
        id: str,
        names: dict[str, NameRegion],
        rig: Object | None,
        kit_name: int = 0,
    ) -> None:
        data_folder = get_data_folder()
        options = get_spartan_options()
        if len(region["permutations"]) > 0 and id == "KIT":
            region["permutations"] = [region["permutations"][0]]
        for perm in region["permutation_regions"]:
            name = f"[{id}] {theme['name']}_{region['name']}"
            if kit_name != 0:
                name += f"_{kit_name}"
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
                for mode in model:
                    if options.import_names:
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
                    attach_name = names.get(str(perm_region["attachment"]["tag_id"]))
                    model_path = f"{data_folder}/models/{perm_region['attachment']['model']}.ekur"
                    attachments = ModelImporter().start_import(model_path, False)
                    for attachment in attachments:
                        if attach_name:
                            attachment.name = f"{region['name']}_{attach_name['name']}"
                        name = f"{perm_region['attachment']['marker_name']}_{perm}_{perm_region['name']}"
                        alt_name = f"{perm_region['attachment']['marker_name']}_{perm}"
                        markers = [
                            marker
                            for marker in importer.markers
                            if marker.name == name or alt_name in marker.name
                        ]
                        import_attachments(name, alt_name, markers[-1], attachment, rig)
                        if attachment.name not in region_collection.objects:
                            region_collection.objects.link(attachment)  # pyright: ignore[reportUnknownMemberType]

            if len(region_collection.objects) == 0:
                theme_collection.children.unlink(region_collection)  # pyright: ignore[reportUnknownMemberType]
