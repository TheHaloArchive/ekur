# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
import re
from pathlib import Path

from bpy.types import Context

from ..json_definitions import (
    CommonMaterial,
    CommonStyleList,
    CommonLayer,
    CustomizationGlobals,
    ForgeObjectCategory,
    ForgeObjectDefinition,
)

from ..utils import get_data_folder, get_import_properties, read_json_file

_nsre = re.compile("([0-9]+)")

__all__ = ["GrabStrings"]


def natural_sort_key(s: str) -> list[int | str]:
    """Natural sort order implementation.

    Args:
        s: String to sort

    Returns:
        Sorted list of strings and integers
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s[1])]


def get_styles(context: Context) -> CommonStyleList | None:
    """Get the styles for the current material slot selected.

    Args:
        context: Blender context used to access preferences.

    Returns:
        Return a list of styles for the current material slot selected if it exists.
    """
    data = get_data_folder()
    if (
        context.object is not None
        and context.object.active_material_index is not None
        and context.object.active_material_index < len(context.object.material_slots)
    ):
        bl_material = context.object.material_slots[context.object.active_material_index]
        definition_path = Path(f"{data}/materials/{bl_material.name}.json")
        if not definition_path.exists():
            logging.warning(f"Material path does not exist!: {definition_path}")
            return
        material = read_json_file(definition_path, CommonMaterial)
        if material["style_info"]:
            styles_path = Path(f"{data}/stylelists/{material['style_info']['stylelist']}.json")
            if not styles_path.exists():
                logging.warning(f"Styles path does not exist!: {styles_path}")
                return
            styles = read_json_file(styles_path, CommonStyleList)
            return styles

    return None


class GrabStrings:
    def common_styles(self, context: Context | None) -> list[tuple[str, str, str]]:
        all_styles: list[tuple[str, str, str]] = []
        import_properties = get_import_properties()
        if context:
            styles = get_styles(context)
            if styles:
                for style, entry in styles["styles"].items():
                    all_styles.append((style, entry["name"], ""))
                if import_properties.sort_by_name:
                    all_styles.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
        return all_styles

    def visors(self, _context: Context | None) -> list[tuple[str, str, str]]:
        all_visors: list[tuple[str, str, str]] = []
        data = get_data_folder()
        properties = get_import_properties()

        visors_path = Path(f"{data}/all_visors.json")
        if not visors_path.exists():
            return all_visors
        visors = read_json_file(visors_path, dict[str, CommonLayer])
        for name, _ in visors.items():
            all_visors.append((name, name, ""))
        if properties.sort_by_name:
            all_visors.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
        return all_visors

    def cores(self, _context: Context | None) -> list[tuple[str, str, str]]:
        all_cores: list[tuple[str, str, str]] = []
        data = get_data_folder()
        globals_path = Path(f"{data}/customization_globals.json")
        if not globals_path.exists():
            return all_cores
        globals = read_json_file(globals_path, CustomizationGlobals)
        for entry in globals["themes"]:
            all_cores.append((str(entry["name"]), str(entry["name"]), ""))
        return all_cores

    def get_object_definition(self, _context: Context) -> ForgeObjectDefinition:
        data = get_data_folder()
        objects_path = Path(f"{data}/forge_objects.json")
        objects = read_json_file(objects_path, ForgeObjectDefinition)
        return objects

    def get_category(self, context: Context, category: str) -> ForgeObjectCategory | None:
        objects = GrabStrings().get_object_definition(context)
        for entry in objects["root_categories"]:
            if entry["name"] == category:
                return entry
        return None

    def root_categories(self, context: Context | None) -> list[tuple[str, str, str]]:
        categories: list[tuple[str, str, str]] = []
        properties = get_import_properties()
        if context is None:
            return categories
        objects = GrabStrings().get_object_definition(context)
        for entry in objects["root_categories"]:
            categories.append((entry["name"], entry["name"], ""))
        if properties.sort_objects:
            categories.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]

        return categories

    def subcategories(self, context: Context | None) -> list[tuple[str, str, str]]:
        subcategories: list[tuple[str, str, str]] = []
        properties = get_import_properties()
        if context is None:
            return subcategories

        root_category = properties.root_category
        category = GrabStrings().get_category(context, root_category)
        if category and category["sub_categories"]:
            for subcat in category["sub_categories"]:
                subcategories.append((subcat["name"], subcat["name"], ""))
        if properties.sort_objects:
            subcategories.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]

        return subcategories

    def objects(self, context: Context | None) -> list[tuple[str, str, str]]:
        subcategories: list[tuple[str, str, str]] = []
        properties = get_import_properties()
        if context is None:
            return subcategories

        root_category = properties.root_category
        subcategory = properties.subcategory
        category = GrabStrings().get_category(context, root_category)
        if category and subcategory and category["sub_categories"]:
            for subcat in category["sub_categories"]:
                if subcat["name"] == subcategory and subcat["objects"]:
                    for obj in subcat["objects"]:
                        subcategories.append((obj["name"], obj["name"], ""))
        if properties.sort_objects:
            subcategories.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]

        return subcategories
