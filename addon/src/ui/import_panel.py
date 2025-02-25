# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia

# pyright: reportUnknownMemberType=false, reportUninitializedInstanceVariable=false
import logging
import re
import random
from pathlib import Path
from typing import cast, final

from bpy.props import BoolProperty, EnumProperty, StringProperty  # pyright: ignore[reportUnknownVariableType]
from bpy.types import Context, Panel, PropertyGroup, Operator

from ..json_definitions import (
    CommonMaterial,
    CommonStyleList,
    CommonLayer,
    CustomizationGlobals,
    ForgeObjectCategory,
    ForgeObjectDefinition,
)
from ..utils import read_json_file

_nsre = re.compile("([0-9]+)")


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
    data = cast(str, context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder)  # pyright: ignore[reportAttributeAccessIssue]
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
    """Some helper functions for the coating import panel."""

    def common_styles(self, context: Context | None) -> list[tuple[str, str, str]]:
        """Returns a list of all styles available on the selected material.

        Args:
            context: Blender context used to access preferences.

        Returns:
            List of all styles available on the selected material to be used on the import panel.
        """
        all_styles: list[tuple[str, str, str]] = []
        if context:
            styles = get_styles(context)
            if styles:
                for style, entry in styles["styles"].items():
                    all_styles.append((style, entry["name"], ""))
                if context.scene.import_properties.sort_by_name:  # pyright: ignore[reportAttributeAccessIssue]
                    all_styles.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
        return all_styles

    def visors(self, context: Context | None) -> list[tuple[str, str, str]]:
        """Returns a list of all visors available.

        Args:
            context: Blender context used to access preferences.

        Returns:
            List of all visors available to be used on the import panel.
        """
        all_visors: list[tuple[str, str, str]] = []
        if context is None:
            return all_visors
        data = cast(
            str,
            context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder,  # pyright: ignore[reportAttributeAccessIssue]
        )
        visors_path = Path(f"{data}/all_visors.json")
        if not visors_path.exists():
            return all_visors
        visors = read_json_file(visors_path, dict[str, CommonLayer])
        for name, _ in visors.items():
            all_visors.append((name, name, ""))
        if context.scene.import_properties.sort_by_name:  # pyright: ignore[reportAttributeAccessIssue]
            all_visors.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
        return all_visors

    def cores(self, context: Context | None) -> list[tuple[str, str, str]]:
        all_cores: list[tuple[str, str, str]] = []
        if context is None:
            return all_cores
        data = cast(
            str,
            context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder,  # pyright: ignore[reportAttributeAccessIssue]
        )
        globals_path = Path(f"{data}/customization_globals.json")
        if not globals_path.exists():
            return all_cores
        globals = read_json_file(globals_path, CustomizationGlobals)
        for entry in globals["themes"]:
            all_cores.append((str(entry["name"]), str(entry["name"]), ""))
        return all_cores

    def get_object_definition(self, context: Context) -> ForgeObjectDefinition:
        data = cast(
            str,
            context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder,  # pyright: ignore[reportAttributeAccessIssue]
        )
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
        if context is None:
            return categories
        objects = GrabStrings().get_object_definition(context)
        for entry in objects["root_categories"]:
            categories.append((entry["name"], entry["name"], ""))
        return categories

    def subcategories(self, context: Context | None) -> list[tuple[str, str, str]]:
        subcategories: list[tuple[str, str, str]] = []
        if context is None:
            return subcategories

        root_category = cast(str, context.scene.import_properties.root_category)  # pyright: ignore[reportAttributeAccessIssue]
        category = GrabStrings().get_category(context, root_category)
        if category and category["sub_categories"]:
            for subcat in category["sub_categories"]:
                subcategories.append((subcat["name"], subcat["name"], ""))
        return subcategories

    def objects(self, context: Context | None) -> list[tuple[str, str, str]]:
        subcategories: list[tuple[str, str, str]] = []
        if context is None:
            return subcategories

        root_category = cast(str, context.scene.import_properties.root_category)  # pyright: ignore[reportAttributeAccessIssue]
        subcategory = cast(str, context.scene.import_properties.subcategory)  # pyright: ignore[reportAttributeAccessIssue]
        category = GrabStrings().get_category(context, root_category)
        if category and subcategory and category["sub_categories"]:
            for subcat in category["sub_categories"]:
                if subcat["name"] == subcategory and subcat["objects"]:
                    for obj in subcat["objects"]:
                        subcategories.append((obj["name"], obj["name"], ""))
        return subcategories


@final
class RandomizeCoatingOperator(Operator):
    """Operator to randomize the coating style on the selected material."""

    bl_idname = "ekur.randomize"
    bl_label = "Surprise Me"

    def execute(self, context: Context) -> set[str]:
        """Select a random style from the available styles.

        Args:
            context: Blender context used to access import properties
        """
        styles = get_styles(context)
        if styles:
            props = cast(ImportProperties, context.scene.import_properties)  # pyright: ignore[reportAttributeAccessIssue]
            props.coat_id = random.choice(list(styles["styles"].keys()))

        return {"FINISHED"}


class ImportProperties(PropertyGroup):
    use_default: BoolProperty(name="Use Default Coating", default=True)
    coat_id: StringProperty(name="Coating ID Override", default="")
    toggle_damage: BoolProperty(name="Disable Damage", default=False)
    selected_only: BoolProperty(name="Selected Only", default=True)
    sort_by_name: BoolProperty(name="Sort by Name", default=True)
    coatings: EnumProperty(name="Coating", items=GrabStrings.common_styles)
    toggle_visors: BoolProperty(name="Override Visor", default=False)
    visors: EnumProperty(name="Visor", items=GrabStrings.visors)
    model_path: StringProperty(
        name="Model Path",
        subtype="FILE_PATH",
    )
    import_materials: BoolProperty(name="Import Materials", default=True)
    import_markers: BoolProperty(name="Import Markers", default=True)
    import_bones: BoolProperty(name="Import Bones", default=True)
    import_collections: BoolProperty(name="Import Collections", default=True)
    import_vertex_color: BoolProperty(name="Import Vertex Color (SLOW)", default=False)
    level_path: StringProperty(
        name="Level Path",
        subtype="FILE_PATH",
    )
    import_specific_core: BoolProperty(name="Import Specific Core", default=False)
    core: EnumProperty(name="Core", items=GrabStrings.cores)
    root_category: EnumProperty(name="Root Category", items=GrabStrings.root_categories)
    subcategory: EnumProperty(name="Subcategory", items=GrabStrings.subcategories)
    objects: EnumProperty(name="Object", items=GrabStrings.objects)


@final
class CoatingImportPanel(Panel):
    bl_idname = "VIEW3D_PT_coating_import"
    bl_label = "Ekur"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ekur"

    def draw(self, context: Context | None) -> None:
        if context is None:
            return
        layout = self.layout
        import_properties = cast(ImportProperties, context.scene.import_properties)  # pyright: ignore[reportAttributeAccessIssue]

        material_header, material_body = layout.panel("VIEW3D_PT_import_material")
        material_header.label(icon="MATERIAL", text="Import Material")

        if material_body:
            options = material_body.box()
            import_properties = cast(ImportProperties, context.scene.import_properties)  # pyright: ignore[reportAttributeAccessIssue]
            options.prop(import_properties, "use_default")
            if not import_properties.use_default:
                box2 = options.box()
                box2.prop(import_properties, "coatings")
                box2.prop(import_properties, "coat_id")
                box2.prop(import_properties, "sort_by_name")
                _ = box2.operator("ekur.randomize")
            options.prop(import_properties, "toggle_damage")
            options.prop(import_properties, "selected_only")
            options.prop(import_properties, "toggle_visors")
            if import_properties.toggle_visors:
                options.prop(import_properties, "visors")
            _ = material_body.operator("ekur.importmaterial")

        model_header, model_body = layout.panel("VIEW3D_PT_import_model")
        model_header.label(icon="MESH_CUBE", text="Import Model")
        if model_body:
            model_opts = model_body.box()
            model_opts.prop(import_properties, "model_path")
            model_opts.prop(import_properties, "import_markers")
            model_opts.prop(import_properties, "import_bones")
            model_opts.prop(import_properties, "import_materials")
            model_opts.prop(import_properties, "import_collections")
            model_opts.prop(import_properties, "import_vertex_color")
            _ = model_body.operator("ekur.importmodel")

        ocgd_header, ocgd_body = layout.panel("VIEW3D_PT_import_ocgd")
        ocgd_header.label(icon="ARMATURE_DATA", text="Import Spartan")
        if ocgd_body:
            ocgd_opts = ocgd_body.box()
            ocgd_opts.prop(import_properties, "import_specific_core")
            if import_properties.import_specific_core:
                ocgd_opts.prop(import_properties, "core")
            _ = ocgd_body.operator("ekur.importspartan")

        level_header, level_body = layout.panel("VIEW3D_PT_import_level")
        level_header.label(icon="MESH_GRID", text="Import Level")
        if level_body:
            level_opts = level_body.box()
            level_opts.prop(import_properties, "level_path")
            _ = level_body.operator("ekur.importlevel")

        forge_header, forge_body = layout.panel("VIEW3D_PT_import_forge")
        forge_header.label(icon="TOOL_SETTINGS", text="Import Forge")
        if forge_body:
            forge_opts = forge_body.box()
            forge_opts.prop(import_properties, "root_category")
            category = cast(str, import_properties.root_category)
            cat = GrabStrings().get_category(context, category)
            if cat and cat["sub_categories"]:
                forge_opts.prop(import_properties, "subcategory")
                forge_opts.prop(import_properties, "objects")
            _ = forge_body.operator("ekur.importforge")
