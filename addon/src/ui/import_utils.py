# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import re
from pathlib import Path

from bpy.types import Context

from ..json_definitions import (
    ForgeMaterial,
    ForgeObjectCategory,
    ForgeObjectDefinition,
)

from ..utils import get_data_folder, get_import_properties, natural_sort_key, read_json_file

_nsre = re.compile("([0-9]+)")

__all__ = ["GrabStrings"]

root_category_cache: list[tuple[str, str, str]] | None = None
sub_category_cache: dict[str, list[tuple[str, str, str]]] | None = None
object_cache: dict[str, list[tuple[str, str, str]]] | None = None
object_repr_cache: dict[str, list[tuple[str, str, str]]] | None = None
object_definition: ForgeObjectDefinition | None = None
material_cache: list[tuple[str, str, str]] | None = None


class GrabStrings:
    def forge_materials(self, _context: Context | None) -> list[tuple[str, str, str]]:
        global material_cache
        if material_cache:
            return material_cache
        all_materials: list[tuple[str, str, str]] = []
        data = get_data_folder()
        globals_path = Path(f"{data}/forge_materials.json")
        if not globals_path.exists():
            return all_materials
        globals = read_json_file(globals_path, ForgeMaterial)
        if globals is None:
            return all_materials
        for entry in globals["layers"].items():
            all_materials.append((str(entry[0]), str(entry[0]), ""))
        material_cache = all_materials
        material_cache.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
        return all_materials

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
