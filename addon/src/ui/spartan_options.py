# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive

from pathlib import Path
from typing import cast

import bpy
from bpy.props import BoolProperty, EnumProperty
from bpy.types import Context, PropertyGroup, UILayout

from ..json_definitions import CustomizationGlobals
from ..utils import get_data_folder, read_json_file


class CoreLogic:
    def cores(self, _context: Context | None) -> list[tuple[str, str, str]]:
        all_cores: list[tuple[str, str, str]] = []
        data = get_data_folder()
        globals_path = Path(f"{data}/customization_globals.json")
        if not globals_path.exists():
            return all_cores
        globals = read_json_file(globals_path, CustomizationGlobals)
        if globals is None:
            return all_cores
        for entry in globals["themes"]:
            all_cores.append((str(entry["name"]), str(entry["name"]), ""))
        return all_cores


class SpartanOptions(PropertyGroup):
    import_specific_core: BoolProperty(
        name="Import Specific Core",
        description="Whether to filter out a specific armor core for spartans.",
        default=False,
    )
    import_names: BoolProperty(
        name="Import Names of Armor Pieces",
        description="Whether to replace object name hashes with their proper in-game names",
        default=True,
    )
    use_purp_rig: BoolProperty(
        default=True,
        description="Whether to use Purplmunkii's IK/FK Control rig for spartans.",
        name="Use Purp's IK Rig",
    )
    core: EnumProperty(
        name="Core",
        description="Specific armor core you want to import.",
        items=CoreLogic.cores,
    )


class SpartanOptionsType:
    import_specific_core: bool = False
    import_names: bool = True
    use_purp_rig: bool = True
    core: str = ""


def get_spartan_options() -> SpartanOptionsType:
    if bpy.context.scene is None:
        return SpartanOptionsType()
    props: SpartanOptions = bpy.context.scene.spartan_properties  # ty: ignore[unresolved-attribute]
    if props:
        return cast(SpartanOptionsType, props)
    return SpartanOptionsType()


def draw_spartan_options(layout: UILayout, props: SpartanOptionsType) -> None:
    ocgd_header, ocgd_body = layout.panel("VIEW3D_PT_import_ocgd", default_closed=True)
    ocgd_header.label(icon="ARMATURE_DATA", text="Import Spartan")
    if ocgd_body:
        ocgd_body.prop(props, "use_purp_rig")
        ocgd_opts = ocgd_body.box()
        ocgd_opts.prop(props, "import_specific_core")
        if props.import_specific_core:
            ocgd_opts.prop(props, "core")
        ocgd_opts.prop(props, "import_names")
        _ = ocgd_opts.operator("ekur.importspartan")
