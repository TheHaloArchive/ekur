# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import cast

import bpy
from bpy.props import BoolProperty, FloatProperty, StringProperty
from bpy.types import PropertyGroup, UILayout


class AnimationOptions(PropertyGroup):
    animation_path: StringProperty(
        default="",
        name="Animation Path",
        description="Path to .ekuranimation file to import.",
        subtype="FILE_PATH",
    )
    bulk_import: BoolProperty(
        default=False,
        name="Bulk Import",
        description="Import multiple animations from a directory.",
    )
    bulk_directory: StringProperty(
        default="",
        name="Bulk Directory",
        description="Directory containing .ekuranimation files to import.",
        subtype="DIR_PATH",
    )


class AnimationOptionsType:
    animation_path: str = ""
    bulk_import: bool = False
    bulk_directory: str = ""


def get_animation_options() -> AnimationOptionsType:
    if bpy.context.scene is None:
        return AnimationOptionsType()
    props: AnimationOptions = bpy.context.scene.animation_properties  # ty: ignore[unresolved-attribute]
    if props:
        return cast(AnimationOptionsType, props)
    return AnimationOptionsType()


def draw_animation_options(layout: UILayout, props: AnimationOptionsType) -> None:
    animation_header, animation_body = layout.panel(
        "VIEW3D_PT_import_animation", default_closed=True
    )
    animation_header.label(icon="ANIM_DATA", text="Import Animation")
    if animation_body:
        animation_opts = animation_body.box()
        animation_opts.prop(props, "animation_path")
        animation_opts.prop(props, "bulk_import")
        if props.bulk_import:
            animation_opts.prop(props, "bulk_directory")
        animation_opts.operator("ekur.importanimation")
