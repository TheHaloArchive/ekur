# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia

# pyright: reportUnknownMemberType=false, reportUninitializedInstanceVariable=false
from typing import final

from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty  # pyright: ignore[reportUnknownVariableType]
from bpy.types import Context, Panel, PropertyGroup

from .spartan_options import draw_spartan_options, get_spartan_options
from .model_options import draw_model_options, get_model_options
from .material_options import draw_material_options, get_material_options
from .import_utils import GrabStrings
from ..utils import ImportPropertiesType, get_addon_preferences, get_import_properties

__all__ = ["ImportProperties", "CoatingImportPanel"]


class ImportProperties(PropertyGroup):
    level_path: StringProperty(
        default="",
        name="Level Path",
        description="Path to .json level file to import.",
        subtype="FILE_PATH",
    )
    root_category: EnumProperty(
        name="Root Category", description="", items=GrabStrings.root_categories
    )
    subcategory: EnumProperty(name="Subcategory", items=GrabStrings.subcategories)
    objects: EnumProperty(name="Object", items=GrabStrings.objects)
    object_representation: EnumProperty(
        name="Object Representation", items=GrabStrings.object_representations
    )
    sort_objects: BoolProperty(name="Sort Objects By Name", default=True)
    override_materials: BoolProperty(name="Override Materials", default=False)
    layer1: EnumProperty(name="Layer 1", items=GrabStrings.forge_materials)
    layer2: EnumProperty(name="Layer 2", items=GrabStrings.forge_materials)
    layer3: EnumProperty(name="Layer 3", items=GrabStrings.forge_materials)
    grime: EnumProperty(name="Grime", items=GrabStrings.forge_materials)
    grime_amount: FloatProperty(name="Grime Amount")
    scratch_amount: FloatProperty(name="Scratch Amount")

    url: StringProperty(name="URL", default="")
    use_file: BoolProperty(name="Use MVAR File", default=False)
    import_folders: BoolProperty(name="Import Folders", default=True)
    remove_blockers: BoolProperty(name="Remove Blockers", default=True)
    mvar_file: StringProperty(
        name="MVAR File",
        description="Path to .mvar file to import.",
        subtype="FILE_PATH",
    )
    output_path: StringProperty(name="Output Path", default="", subtype="DIR_PATH")
    output_workflow: EnumProperty(
        name="Output Workflow",
        description="Workflow to use for baking textures.",
        items=[
            ("PBR MetRough", "PBR MetRough", ""),
            ("PBR SpecGloss", "PBR SpecGloss", ""),
            ("PBR MetRoughSpecColor", "PBR MetRoughSpecColor", ""),
            ("PBR ORM", "PBR ORM", ""),
            ("Unity Smoothness/Mask", "Unity Smoothness/Mask", ""),
            ("Color", "Color", ""),
            ("Metallic", "Metallic", ""),
            ("Roughness", "Roughness", ""),
            ("Emission", "Emission", ""),
            ("Specular", "Specular", ""),
            ("SpecColor", "SpecColor", ""),
            ("AO", "AO", ""),
            ("Normal", "Normal", ""),
            ("Unity Mask Map", "Unity Mask Map", ""),
            ("Smoothness", "Smoothness", ""),
            ("ID Mask", "ID Mask", ""),
            ("ORM", "ORM", ""),
        ],
    )
    width: IntProperty(name="Width", default=1024)
    height: IntProperty(name="Height", default=1024)
    bit_depth: EnumProperty(name="Bit Depth", items=[("8", "8", ""), ("16", "16", "")])
    bake_detail_normals: BoolProperty(name="Bake Detail Normals", default=False)
    merge_textures: BoolProperty(name="Merge Textures Into Single Bake", default=False)
    merge_objects: BoolProperty(name="Merge Objects Into Single Bake", default=False)
    bake_ao: BoolProperty(name="Bake Ambient Occlusion", default=False)
    bake_layer_map: BoolProperty(name="Bake Layer Map", default=False)
    advanced_bake: BoolProperty(name="Toggle Advanced Bake Options", default=False)
    selected_layer: EnumProperty(
        name="Selected Layer",
        description="Layer to bake for objects.",
        items=[
            ("None", "None", ""),
            ("Color", "Color", ""),
            ("Metallic", "Metallic", ""),
            ("Roughness", "Roughness", ""),
            ("Emission", "Emission", ""),
            ("Specular", "Specular", ""),
            ("SpecColor", "SpecColor", ""),
            ("AO", "AO", ""),
            ("Normal", "Normal", ""),
            ("Unity Mask Map", "Unity Mask Map", ""),
            ("Smoothness", "Smoothness", ""),
            ("ID Mask", "ID Mask", ""),
            ("ORM", "ORM", ""),
        ],
    )
    selected_objects: EnumProperty(
        name="Objects to Bake",
        description="Objects to bake for.",
        items=[("Selected", "Selected", ""), ("All", "All", "")],
    )
    pixel_padding: IntProperty(name="Pixel Padding", default=16)
    uv_to_bake_to: EnumProperty(
        name="UV Map to Bake To", items=[("UV0", "UV0", ""), ("UV1", "UV1", ""), ("UV2", "UV2", "")]
    )
    align_bakes: BoolProperty(
        name="Align All Bakes Automatically",
        description="Bakes materials by their texture dimensions.",
        default=False,
    )
    save_normals: BoolProperty(
        name="Save Normals",
        description="Save the base normals from the game.",
        default=False,
    )


@final
class CoatingImportPanel(Panel):
    bl_idname = "VIEW3D_PT_coating_import"
    bl_label = "Ekur"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ekur"

    def draw(self, context: Context | None) -> None:
        layout = self.layout
        if layout is None or context is None:
            return
        import_properties = get_import_properties()
        prefs = get_addon_preferences()
        draw_material_options(layout, get_material_options())
        draw_model_options(layout, get_model_options())
        if not prefs.is_campaign:
            draw_spartan_options(layout, get_spartan_options())
        self.draw_level(import_properties)
        if not prefs.is_campaign:
            self.draw_forge(context, import_properties)
        self.draw_forge_map(import_properties)
        self.draw_bake_menu(import_properties)

    def draw_level(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        level_header, level_body = layout.panel("VIEW3D_PT_import_level", default_closed=True)
        level_header.label(icon="MESH_GRID", text="Import Level")
        if level_body:
            level_opts = level_body.box()
            level_opts.prop(import_properties, "level_path")
            _ = level_body.operator("ekur.importlevel")

    def draw_forge(self, context: Context | None, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None or context is None:
            return
        forge_header, forge_body = layout.panel("VIEW3D_PT_import_forge", default_closed=True)
        forge_header.label(icon="TOOL_SETTINGS", text="Import Forge Object")
        if forge_body:
            forge_opts = forge_body.box()
            forge_opts.prop(import_properties, "sort_objects")
            forge_opts.prop(import_properties, "root_category")
            category = import_properties.root_category
            cat = GrabStrings().get_category(context, category)
            if cat and cat["sub_categories"]:
                forge_opts.prop(import_properties, "subcategory")
                forge_opts.prop(import_properties, "objects")
                forge_opts.prop(import_properties, "object_representation")
            _ = forge_body.operator("ekur.importforge")
            forge_opts.prop(import_properties, "override_materials")
            if import_properties.override_materials:
                forge_opts.prop(import_properties, "layer1")
                forge_opts.prop(import_properties, "layer2")
                forge_opts.prop(import_properties, "layer3")
                forge_opts.prop(import_properties, "grime")
                forge_opts.prop(import_properties, "grime_amount")
                forge_opts.prop(import_properties, "scratch_amount")

    def draw_forge_map(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        forge_header, forge_body = layout.panel("VIEW3D_PT_import_forge_map", default_closed=True)
        forge_header.label(icon="MAT_SPHERE_SKY", text="Import Forge Map")
        if forge_body:
            forge_opts = forge_body.box()
            forge_opts.prop(import_properties, "url")
            forge_opts.prop(import_properties, "import_folders")
            forge_opts.prop(import_properties, "remove_blockers")
            op = forge_opts.operator("wm.url_open", text="Browse Maps (Cylix)", icon="URL")
            op.url = "https://cylix.guide/discovery/"  # pyright: ignore[reportAttributeAccessIssue]
            op = forge_opts.operator("wm.url_open", text="Browse Maps (Waypoint)", icon="URL")
            op.url = "https://www.halowaypoint.com/halo-infinite/ugc/browse"  # pyright: ignore[reportAttributeAccessIssue]
            forge_opts.prop(import_properties, "use_file")
            if import_properties.use_file:
                forge_opts.prop(import_properties, "mvar_file")
            _ = forge_body.operator("ekur.importforgemap")

    def draw_bake_menu(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        bake_header, bake_body = layout.panel("VIEW3D_PT_bake_menu", default_closed=True)
        bake_header.label(icon="SHADING_TEXTURE", text="Bake Textures")
        if bake_body:
            bake_opts = bake_body.box()
            bake_opts.prop(import_properties, "output_path")
            bake_opts.prop(import_properties, "output_workflow")
            bake_opts.prop(import_properties, "align_bakes")
            if not import_properties.align_bakes:
                bake_opts.prop(import_properties, "width")
                bake_opts.prop(import_properties, "height")
                _ = bake_opts.operator("ekur.alignbake")
            bake_opts.prop(import_properties, "pixel_padding")
            bake_opts.prop(import_properties, "bit_depth")
            bake_opts.prop(import_properties, "save_normals")
            bake_opts.prop(import_properties, "merge_textures")
            bake_opts.prop(import_properties, "merge_objects")
            bake_opts.prop(import_properties, "bake_detail_normals")
            bake_opts.prop(import_properties, "bake_ao")
            bake_opts.prop(import_properties, "bake_layer_map")
            bake_opts.prop(import_properties, "uv_to_bake_to")
            bake_opts.prop(import_properties, "advanced_bake")
            if import_properties.advanced_bake:
                advanced_opts = bake_opts.box()
                advanced_opts.prop(import_properties, "selected_layer")
                advanced_opts.prop(import_properties, "selected_objects")
                _ = advanced_opts.operator("ekur.toggleadvancedbake")
            _ = bake_body.operator("ekur.baketextures")
