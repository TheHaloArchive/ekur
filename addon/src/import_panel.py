# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
import re
import random
from pathlib import Path

import bpy
from bpy.props import BoolProperty, EnumProperty, StringProperty
from bpy.types import Context, Panel, PropertyGroup, UILayout, Operator

from .json_definitions import CommonMaterial, CommonStyleList, CommonLayer
from .utils import read_json_file

_nsre = re.compile("([0-9]+)")


def natural_sort_key(s: str) -> list[int | str]:
    """Natural sort order implementation.

    Args:
        s: String to sort

    Returns:
        Sorted list of strings and integers
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s[1])]


def get_styles(context: Context | None) -> CommonStyleList | None:
    """Get the styles for the current material slot selected.

    Args:
        context: Blender context used to access preferences.

    Returns:
        Return a list of styles for the current material slot selected if it exists.
    """
    data = context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder  # pyright: ignore[reportAttributeAccessIssue]
    if context.object is not None and context.object.active_material_index is not None:
        bl_material = context.object.material_slots[context.object.active_material_index]
        definition_path = Path(f"{data}/materials/{bl_material.name}.json")
        if not definition_path.exists():
            logging.warning(f"Material path does not exist!: {definition_path}")
            return
        material: CommonMaterial = read_json_file(definition_path)
        if material["style_info"]:
            styles_path = Path(f"{data}/stylelists/{material['style_info']['stylelist']}.json")
            if not styles_path.exists():
                logging.warning(f"Styles path does not exist!: {styles_path}")
                return
            styles: CommonStyleList = read_json_file(styles_path)
            return styles


class GrabStrings:
    """Some helper functions for the coating import panel."""

    def common_styles(self, context: Context | None) -> list[tuple[str, str, str]]:
        """Returns a list of all styles available on the selected material.

        Args:
            context: Blender context used to access preferences.

        Returns:
            List of all styles available on the selected material to be used on the import panel.
        """
        all_styles = []
        styles = get_styles(context)
        if styles:
            for style, entry in styles["styles"].items():
                all_styles.append((style, entry["name"], ""))
            if context.scene.import_properties.sort_by_name:  # pyright: ignore[reportAttributeAccessIssue]
                all_styles.sort(key=natural_sort_key)
        return all_styles

    def visors(self, context: Context | None) -> list[tuple[str, str, str]]:
        """Returns a list of all visors available.

        Args:
            context: Blender context used to access preferences.

        Returns:
            List of all visors available to be used on the import panel.
        """
        data = context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder  # pyright: ignore[reportAttributeAccessIssue]
        visors_path = Path(f"{data}/all_visors.json")
        all_visors = []
        if not visors_path.exists():
            return all_visors
        visors: dict[str, CommonLayer] = read_json_file(visors_path)
        for name, _ in visors.items():
            all_visors.append((name, name, ""))
        if context.scene.import_properties.sort_by_name:  # pyright: ignore[reportAttributeAccessIssue]
            all_visors.sort(key=natural_sort_key)
        return all_visors


class RandomizeCoatingOperator(Operator):
    """Operator to randomize the coating style on the selected material."""

    bl_idname = "ekur.randomize"
    bl_label = "Surprise Me"

    def execute(self, context: Context | None) -> set[str]:
        """Select a random style from the available styles.

        Args:
            context: Blender context used to access import properties
        """
        styles = get_styles(context)
        if styles:
            props = context.scene.import_properties  # pyright: ignore[reportAttributeAccessIssue]
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


class CoatingImportPanel(Panel):
    bl_idname = "VIEW3D_PT_coating_import"
    bl_label = "Ekur"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ekur"

    def draw(self, context: Context | None) -> None:
        layout = self.layout
        box: UILayout = layout.box()
        box.label(icon="MATERIAL", text="Import Material")
        options = box.box()
        options.prop(context.scene.import_properties, "use_default")  # pyright: ignore[reportAttributeAccessIssue]
        if not context.scene.import_properties.use_default:  # pyright: ignore[reportAttributeAccessIssue]
            box2 = options.box()
            box2.prop(context.scene.import_properties, "coatings")  # pyright: ignore[reportAttributeAccessIssue]
            box2.prop(context.scene.import_properties, "coat_id")  # pyright: ignore[reportAttributeAccessIssue]
            box2.prop(context.scene.import_properties, "sort_by_name")  # pyright: ignore[reportAttributeAccessIssue]
            _ = box2.operator("ekur.randomize")
        options.prop(context.scene.import_properties, "toggle_damage")  # pyright: ignore[reportAttributeAccessIssue]
        options.prop(context.scene.import_properties, "selected_only")  # pyright: ignore[reportAttributeAccessIssue]
        options.prop(context.scene.import_properties, "toggle_visors")  # pyright: ignore[reportAttributeAccessIssue]
        if context.scene.import_properties.toggle_visors:  # pyright: ignore[reportAttributeAccessIssue]
            options.prop(context.scene.import_properties, "visors")  # pyright: ignore[reportAttributeAccessIssue]
        _ = box.operator("ekur.importmaterial")

        model_box: UILayout = layout.box()
        model_box.label(icon="FILE", text="Import Model")
        model_box.prop(context.scene.import_properties, "model_path")  # pyright: ignore[reportAttributeAccessIssue]
        model_box.prop(context.scene.import_properties, "import_markers")  # pyright: ignore[reportAttributeAccessIssue]
        model_box.prop(context.scene.import_properties, "import_bones")  # pyright: ignore[reportAttributeAccessIssue]
        model_box.prop(context.scene.import_properties, "import_materials")  # pyright: ignore[reportAttributeAccessIssue]
        _ = model_box.operator("ekur.importmodel")

    @classmethod
    def poll(cls, context: Context | None) -> bool:
        return context.object is not None
