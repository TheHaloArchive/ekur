# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
# pyright: reportUninitializedInstanceVariable=false, reportUnknownVariableType=false, reportUnknownMemberType=false
import bpy

from typing import cast
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty
from bpy.types import PropertyGroup, UILayout


class BakeOptions(PropertyGroup):
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


class BakeOptionsType:
    output_path: str = ""
    output_workflow: str = ""
    width: int = 0
    height: int = 0
    bit_depth: str = ""
    bake_detail_normals: bool = False
    merge_textures: bool = False
    merge_objects: bool = False
    bake_ao: bool = False
    bake_layer_map: bool = False
    advanced_bake: bool = False
    selected_layer: str = ""
    selected_objects: str = ""
    pixel_padding: int = 0
    uv_to_bake_to: str = ""
    align_bakes: bool = False
    save_normals: bool = False


def get_bake_options() -> BakeOptionsType:
    if bpy.context.scene is None:
        return BakeOptionsType()
    props: BakeOptionsType = bpy.context.scene.bake_properties  # pyright: ignore[reportAttributeAccessIssue]
    if props:
        return cast(BakeOptionsType, props)
    return BakeOptionsType()


def draw_bake_menu_options(layout: UILayout, props: BakeOptionsType) -> None:
    bake_header, bake_body = layout.panel("VIEW3D_PT_bake_menu", default_closed=True)
    bake_header.label(icon="SHADING_TEXTURE", text="Bake Textures")
    if bake_body:
        bake_opts = bake_body.box()
        bake_opts.prop(props, "output_path")
        bake_opts.prop(props, "output_workflow")
        bake_opts.prop(props, "align_bakes")
        if not props.align_bakes:
            bake_opts.prop(props, "width")
            bake_opts.prop(props, "height")
            _ = bake_opts.operator("ekur.alignbake")
        bake_opts.prop(props, "pixel_padding")
        bake_opts.prop(props, "bit_depth")
        bake_opts.prop(props, "save_normals")
        bake_opts.prop(props, "merge_textures")
        bake_opts.prop(props, "merge_objects")
        bake_opts.prop(props, "bake_detail_normals")
        bake_opts.prop(props, "bake_ao")
        bake_opts.prop(props, "bake_layer_map")
        bake_opts.prop(props, "uv_to_bake_to")
        bake_opts.prop(props, "advanced_bake")
        if props.advanced_bake:
            advanced_opts = bake_opts.box()
            advanced_opts.prop(props, "selected_layer")
            advanced_opts.prop(props, "selected_objects")
            _ = advanced_opts.operator("ekur.toggleadvancedbake")
        _ = bake_body.operator("ekur.baketextures")
