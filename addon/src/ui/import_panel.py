# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia

# pyright: reportUnknownMemberType=false, reportUninitializedInstanceVariable=false
import random
from typing import final

from bpy.props import BoolProperty, EnumProperty, StringProperty  # pyright: ignore[reportUnknownVariableType]
from bpy.types import Context, Panel, PropertyGroup, Operator

from ..utils import get_import_properties
from .import_utils import GrabStrings, get_styles

__all__ = ["RandomizeCoatingOperator", "ImportProperties", "CoatingImportPanel"]


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
            props = get_import_properties()
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
        default="",
        name="Model Path",
        subtype="FILE_PATH",
    )
    import_materials: BoolProperty(name="Import Materials", default=True)
    import_markers: BoolProperty(name="Import Markers", default=True)
    import_bones: BoolProperty(name="Import Bones", default=True)
    import_collections: BoolProperty(name="Import Collections", default=True)
    import_vertex_color: BoolProperty(name="Import Vertex Color (SLOW)", default=False)
    level_path: StringProperty(
        default="",
        name="Level Path",
        subtype="FILE_PATH",
    )
    import_specific_core: BoolProperty(name="Import Specific Core", default=False)
    core: EnumProperty(name="Core", items=GrabStrings.cores)
    root_category: EnumProperty(name="Root Category", items=GrabStrings.root_categories)
    subcategory: EnumProperty(name="Subcategory", items=GrabStrings.subcategories)
    objects: EnumProperty(name="Object", items=GrabStrings.objects)
    sort_objects: BoolProperty(name="Sort Objects By Name", default=True)


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
        import_properties = get_import_properties()

        material_header, material_body = layout.panel("VIEW3D_PT_import_material")
        material_header.label(icon="MATERIAL", text="Import Material")

        if material_body:
            options = material_body.box()
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
            forge_opts.prop(import_properties, "sort_objects")
            forge_opts.prop(import_properties, "root_category")
            category = import_properties.root_category
            cat = GrabStrings().get_category(context, category)
            if cat and cat["sub_categories"]:
                forge_opts.prop(import_properties, "subcategory")
                forge_opts.prop(import_properties, "objects")
            _ = forge_body.operator("ekur.importforge")
