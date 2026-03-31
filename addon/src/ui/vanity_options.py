# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive

from typing import cast

import bpy
from bpy.props import BoolProperty, EnumProperty, StringProperty
from bpy.types import PropertyGroup, UILayout

BODY_TYPES = [
    ("Body Type 0", "Body Type 0", ""),
    ("Body Type 1", "Body Type 1", ""),
    ("Body Type 2", "Body Type 2", ""),
]

ARM = [
    ("None", "None", ""),
    ("Transhumeral", "Transhumeral", ""),
    ("Transradial", "Transradial", ""),
    ("Hand", "Hand", ""),
]

LEG = [
    ("None", "None", ""),
    ("Transfemoral", "Transfemoral", ""),
]


class VanityOptions(PropertyGroup):
    use_purp_rig: BoolProperty(
        default=True,
        description="Whether to use Purplmunkii's IK/FK Control rig for spartans.",
        name="Use Purp's IK Rig",
    )
    gamertag: StringProperty(
        name="Gamertag", description="Gamertag of the spartan you want to import.", default=""
    )
    body_type: EnumProperty(
        name="Body Type",
        description="Body type of the spartan you want to import.",
        items=BODY_TYPES,
    )
    left_arm: EnumProperty(
        name="Left Arm",
        description="Prosthesis for the left arm.",
        items=ARM,
    )
    right_arm: EnumProperty(
        name="Right Arm", description="Prosthesis for the right arm.", items=ARM
    )
    left_leg: EnumProperty(name="Left Leg", description="Prosthesis for the left leg.", items=LEG)
    right_leg: EnumProperty(
        name="Right Leg", description="Prosthesis for the right leg.", items=LEG
    )


class VanityOptionsType:
    use_purp_rig: bool = True
    gamertag: str = ""
    body_type: str = ""
    left_arm: str = ""
    right_arm: str = ""
    left_leg: str = ""
    right_leg: str = ""


def get_vanity_options() -> VanityOptionsType:
    if bpy.context.scene is None:
        return VanityOptionsType()
    props: VanityOptions = bpy.context.scene.vanity_properties  # ty: ignore[unresolved-attribute]
    if props:
        return cast(VanityOptionsType, props)
    return VanityOptionsType()


def draw_vanity_options(layout: UILayout, props: VanityOptionsType) -> None:
    ocgd_header, ocgd_body = layout.panel("VIEW3D_PT_import_vanity", default_closed=True)
    ocgd_header.label(icon="ARMATURE_DATA", text="Import Vanity")
    if ocgd_body:
        vanity_opts = ocgd_body.box()
        vanity_opts.prop(props, "use_purp_rig")
        vanity_opts.prop(props, "body_type")
        vanity_opts.prop(props, "left_arm")
        vanity_opts.prop(props, "right_arm")
        vanity_opts.prop(props, "left_leg")
        vanity_opts.prop(props, "right_leg")
        vanity_opts.prop(props, "gamertag")
        _ = ocgd_body.operator("ekur.importvanity")
