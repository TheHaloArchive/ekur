# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia

# pyright: reportUnknownMemberType=false, reportUninitializedInstanceVariable=false
import logging
import re
import random
from pathlib import Path
from typing import cast, final

from bpy.props import BoolProperty, EnumProperty, StringProperty  # pyright: ignore[reportUnknownVariableType]
from bpy.types import Context, Panel, PropertyGroup, UILayout, Operator

from ..json_definitions import CommonMaterial, CommonStyleList, CommonLayer
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
    if context.object is not None and context.object.active_material_index is not None:
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
        if context:
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
        box: UILayout = layout.box()
        box.label(icon="MATERIAL", text="Import Material")
        options = box.box()
        import_properties = context.scene.import_properties  # pyright: ignore[reportAttributeAccessIssue, reportUnknownVariableType]
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
        _ = box.operator("ekur.importmaterial")

        model_box = layout.box()
        model_box.label(icon="MESH_CUBE", text="Import Model")
        model_opts = model_box.box()
        model_opts.prop(import_properties, "model_path")
        model_opts.prop(import_properties, "import_markers")
        model_opts.prop(import_properties, "import_bones")
        model_opts.prop(import_properties, "import_materials")
        model_opts.prop(import_properties, "import_collections")
        _ = model_box.operator("ekur.importmodel")

        ocgd_box = layout.box()
        ocgd_box.label(icon="ARMATURE_DATA", text="Import Spartan")
        _ = ocgd_box.operator("ekur.importspartan")
