# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
# pyright: reportUninitializedInstanceVariable=false, reportUnknownVariableType=false, reportUnknownMemberType=false
import bpy

from pathlib import Path
from typing import cast
from bpy.props import BoolProperty, EnumProperty, FloatProperty
from bpy.types import Context, PropertyGroup, UILayout

from ..json_definitions import ForgeMaterial, ForgeObjectCategory, ForgeObjectDefinition
from ..utils import get_data_folder, natural_sort_key, read_json_file


root_category_cache: list[tuple[str, str, str]] | None = None
sub_category_cache: dict[str, list[tuple[str, str, str]]] | None = None
object_cache: dict[str, list[tuple[str, str, str]]] | None = None
object_repr_cache: dict[str, list[tuple[str, str, str]]] | None = None
object_definition: ForgeObjectDefinition | None = None
material_cache: list[tuple[str, str, str]] | None = None


class ForgeObjectLogic:
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
        objects = ForgeObjectLogic().get_object_definition(context)
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
        properties = get_forge_object_options()
        if context is None:
            return categories
        objects = ForgeObjectLogic().get_object_definition(context)
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
        properties = get_forge_object_options()
        if context is None:
            return subcategories

        root_category = properties.root_category
        if sub_category_cache and root_category in sub_category_cache:
            return sub_category_cache[root_category]
        category = ForgeObjectLogic().get_category(context, root_category)
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
        properties = get_forge_object_options()
        if context is None:
            return subcategories

        root_category = properties.root_category
        subcategory = properties.subcategory
        category = ForgeObjectLogic().get_category(context, root_category)
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
        properties = get_forge_object_options()
        if context is None:
            return subcategories

        root_category = properties.root_category
        subcategory = properties.subcategory
        object_name = properties.objects
        category = ForgeObjectLogic().get_category(context, root_category, subcategory)
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


class ForgeObjectOptions(PropertyGroup):
    root_category: EnumProperty(
        name="Root Category", description="", items=ForgeObjectLogic.root_categories
    )
    subcategory: EnumProperty(name="Subcategory", items=ForgeObjectLogic.subcategories)
    objects: EnumProperty(name="Object", items=ForgeObjectLogic.objects)
    object_representation: EnumProperty(
        name="Object Representation", items=ForgeObjectLogic.object_representations
    )
    sort_objects: BoolProperty(name="Sort Objects By Name", default=True)
    override_materials: BoolProperty(name="Override Materials", default=False)
    layer1: EnumProperty(name="Layer 1", items=ForgeObjectLogic.forge_materials)
    layer2: EnumProperty(name="Layer 2", items=ForgeObjectLogic.forge_materials)
    layer3: EnumProperty(name="Layer 3", items=ForgeObjectLogic.forge_materials)
    grime: EnumProperty(name="Grime", items=ForgeObjectLogic.forge_materials)
    grime_amount: FloatProperty(name="Grime Amount")
    scratch_amount: FloatProperty(name="Scratch Amount")


class ForgeObjectOptionsType:
    root_category: str = ""
    subcategory: str = ""
    objects: str = ""
    object_representation: str = ""
    sort_objects: bool = True
    override_materials: bool = False
    layer1: str = ""
    layer2: str = ""
    layer3: str = ""
    grime: str = ""
    grime_amount: float = 0.0
    scratch_amount: float = 0.0


def get_forge_object_options() -> ForgeObjectOptionsType:
    if bpy.context.scene is None:
        return ForgeObjectOptionsType()
    props: ForgeObjectOptionsType = bpy.context.scene.forge_object_properties  # pyright: ignore[reportAttributeAccessIssue]
    if props:
        return cast(ForgeObjectOptionsType, props)
    return ForgeObjectOptionsType()


def draw_forge_object_options(layout: UILayout, props: ForgeObjectOptionsType) -> None:
    forge_header, forge_body = layout.panel("VIEW3D_PT_import_forge", default_closed=True)
    forge_header.label(icon="TOOL_SETTINGS", text="Import Forge Object")
    if forge_body:
        forge_opts = forge_body.box()
        forge_opts.prop(props, "sort_objects")
        forge_opts.prop(props, "root_category")
        category = props.root_category
        cat = ForgeObjectLogic().get_category(bpy.context, category)
        if cat and cat["sub_categories"]:
            forge_opts.prop(props, "subcategory")
            forge_opts.prop(props, "objects")
            forge_opts.prop(props, "object_representation")
        _ = forge_body.operator("ekur.importforge")
        forge_opts.prop(props, "override_materials")
        if props.override_materials:
            forge_opts.prop(props, "layer1")
            forge_opts.prop(props, "layer2")
            forge_opts.prop(props, "layer3")
            forge_opts.prop(props, "grime")
            forge_opts.prop(props, "grime_amount")
            forge_opts.prop(props, "scratch_amount")
