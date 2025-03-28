# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
import re
from pathlib import Path

import bpy
from bpy.types import Context

from ..json_definitions import (
    CommonMaterial,
    CommonStyleList,
    CommonLayer,
    CustomizationGlobals,
    ForgeObjectCategory,
    ForgeObjectDefinition,
)

from ..utils import get_data_folder, get_import_properties, get_package_name, read_json_file

_nsre = re.compile("([0-9]+)")

__all__ = ["GrabStrings"]

root_category_cache: list[tuple[str, str, str]] | None = None
sub_category_cache: dict[str, list[tuple[str, str, str]]] | None = None
object_cache: dict[str, list[tuple[str, str, str]]] | None = None
object_repr_cache: dict[str, list[tuple[str, str, str]]] | None = None
visor_cache: list[tuple[str, str, str]] | None = None
styles_cache: dict[str, CommonStyleList] | None = None
style_cache: dict[str, list[tuple[str, str, str]]] | None = None
object_definition: ForgeObjectDefinition | None = None


def natural_sort_key(s: str) -> list[int | str]:
    """Natural sort order implementation.

    Args:
        s: String to sort

    Returns:
        Sorted list of strings and integers
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s[1])]


def get_styles(context: Context) -> tuple[str, CommonStyleList] | None:
    """Get the styles for the current material slot selected.

    Args:
        context: Blender context used to access preferences.

    Returns:
        Return a list of styles for the current material slot selected if it exists.
    """
    global styles_cache
    data = get_data_folder()
    if (
        context.object is not None
        and context.object.active_material_index is not None
        and context.object.active_material_index < len(context.object.material_slots)
    ):
        bl_material = context.object.material_slots[context.object.active_material_index]
        if styles_cache and bl_material.name in styles_cache:
            return (bl_material.name, styles_cache[bl_material.name])

        definition_path = Path(f"{data}/materials/{bl_material.name.split('.')[0]}.json")
        if not definition_path.exists():
            logging.warning(f"Material path does not exist!: {definition_path}")
            return
        material = read_json_file(definition_path, CommonMaterial)
        if material is None:
            return
        if material["style_info"]:
            styles_path = Path(f"{data}/stylelists/{material['style_info']['stylelist']}.json")
            styles = read_json_file(styles_path, CommonStyleList)
            if styles is None:
                return
            styles_cache = {bl_material.name: styles}
            return (bl_material.name, styles)

    return


class GrabStrings:
    def common_styles(self, context: Context | None) -> list[tuple[str, str, str]]:
        global style_cache
        all_styles: list[tuple[str, str, str]] = []
        import_properties = get_import_properties()
        if context:
            styles = get_styles(context)
            if styles:
                if style_cache and styles[0] in style_cache:
                    return style_cache[styles[0]]
                for style, entry in styles[1]["styles"].items():
                    all_styles.append((style, entry["name"], ""))
                if import_properties.sort_by_name:
                    all_styles.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
                style_cache = {styles[0]: all_styles}
        return all_styles

    def visors(self, _context: Context | None) -> list[tuple[str, str, str]]:
        global visor_cache
        if visor_cache:
            return visor_cache
        all_visors: list[tuple[str, str, str]] = []
        extension_path = bpy.utils.extension_path_user(get_package_name(), create=True)
        properties = get_import_properties()

        visors_path = Path(f"{extension_path}/all_visors.json")
        if not visors_path.exists():
            return all_visors
        visors = read_json_file(visors_path, dict[str, CommonLayer])
        if visors is None:
            return all_visors
        for name, _ in visors.items():
            all_visors.append((name, name, ""))
        if properties.sort_by_name:
            all_visors.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
        visor_cache = all_visors
        return all_visors

    def cores(self, _context: Context | None) -> list[tuple[str, str, str]]:
        all_cores: list[tuple[str, str, str]] = []
        data = get_data_folder()
        globals_path = Path(f"{data}/customization_globals.json")
        if not globals_path.exists():
            return all_cores
        globals = read_json_file(globals_path, CustomizationGlobals)
        if globals is None:
            return all_cores
        for entry in globals["themes"]:
            all_cores.append((str(entry["name"]), str(entry["name"]), ""))
        return all_cores

    def get_object_definition(self, _context: Context) -> ForgeObjectDefinition | None:
        global object_definition
        data = get_data_folder()
        objects_path = Path(f"{data}/forge_objects.json")
        if object_definition:
            return object_definition
        else:
            object_definition = read_json_file(objects_path, ForgeObjectDefinition)
        if object_definition is None:
            return
        return object_definition

    def get_category(
        self, context: Context, category: str, subcat: str | None = None
    ) -> ForgeObjectCategory | None:
        objects = GrabStrings().get_object_definition(context)
        if objects is None:
            return
        for entry in objects["root_categories"]:
            if entry["name"] == category and not subcat:
                return entry
            if subcat and entry["sub_categories"] and entry["name"] == category:
                for subcategory in entry["sub_categories"]:
                    if subcategory["name"] == subcat:
                        return subcategory
        return

    def root_categories(self, context: Context | None) -> list[tuple[str, str, str]]:
        global root_category_cache
        if root_category_cache:
            return root_category_cache
        categories: list[tuple[str, str, str]] = []
        properties = get_import_properties()
        if context is None:
            return categories
        objects = GrabStrings().get_object_definition(context)
        if objects is None:
            return categories

        for entry in objects["root_categories"]:
            categories.append((entry["name"], entry["name"], ""))
        if properties.sort_objects:
            categories.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
        root_category_cache = categories
        return categories

    def subcategories(self, context: Context | None) -> list[tuple[str, str, str]]:
        global sub_category_cache
        subcategories: list[tuple[str, str, str]] = []
        properties = get_import_properties()
        if context is None:
            return subcategories

        root_category = properties.root_category
        if sub_category_cache and root_category in sub_category_cache:
            return sub_category_cache[root_category]
        category = GrabStrings().get_category(context, root_category)
        if category and category["sub_categories"]:
            for subcat in category["sub_categories"]:
                subcategories.append((subcat["name"], subcat["name"], ""))
        if properties.sort_objects:
            subcategories.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
        sub_category_cache = {root_category: subcategories}
        return subcategories

    def objects(self, context: Context | None) -> list[tuple[str, str, str]]:
        global object_cache
        subcategories: list[tuple[str, str, str]] = []
        properties = get_import_properties()
        if context is None:
            return subcategories

        root_category = properties.root_category
        subcategory = properties.subcategory
        category = GrabStrings().get_category(context, root_category)
        if object_cache and subcategory in object_cache:
            return object_cache[subcategory]
        if category and subcategory and category["sub_categories"]:
            for subcat in category["sub_categories"]:
                if subcat["name"] == subcategory and subcat["objects"]:
                    for obj in subcat["objects"]:
                        subcategories.append((obj["name"], obj["name"], ""))
        if properties.sort_objects:
            subcategories.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]

        object_cache = {subcategory: subcategories}
        return subcategories

    def object_representations(self, context: Context | None) -> list[tuple[str, str, str]]:
        global object_repr_cache
        subcategories: list[tuple[str, str, str]] = []
        properties = get_import_properties()
        if context is None:
            return subcategories

        root_category = properties.root_category
        subcategory = properties.subcategory
        object_name = properties.objects
        category = GrabStrings().get_category(context, root_category, subcategory)
        if object_repr_cache and object_name in object_repr_cache:
            return object_repr_cache[object_name]
        if category and category["objects"]:
            for object in category["objects"]:
                if object["name"] == str(object_name):
                    for obj in object["representations"]:
                        subcategories.append((obj["name"], obj["name"], ""))
        if properties.sort_objects:
            subcategories.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]

        object_repr_cache = {object_name: subcategories}
        return subcategories
