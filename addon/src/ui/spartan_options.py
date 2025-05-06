# pyright: reportUninitializedInstanceVariable=false, reportUnknownVariableType=false, reportUnknownMemberType=false

from pathlib import Path
from typing import cast
import bpy
from bpy.props import BoolProperty, EnumProperty, StringProperty
from bpy.types import Context, PropertyGroup, UILayout

from ..json_definitions import CustomizationGlobals
from ..utils import get_data_folder, read_json_file

BODY_TYPES = [
    ("Body Type 1", "Body Type 1", ""),
    ("Body Type 2", "Body Type 2", ""),
    ("Body Type 3", "Body Type 3", ""),
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
    core: EnumProperty(
        name="Core",
        description="Specific armor core you want to import.",
        items=CoreLogic.cores,
    )


class SpartanOptionsType:
    import_specific_core: bool = False
    import_names: bool = True
    use_purp_rig: bool = True
    gamertag: str = ""
    body_type: str = ""
    left_arm: str = ""
    right_arm: str = ""
    left_leg: str = ""
    right_leg: str = ""
    core: str = ""


def get_spartan_options() -> SpartanOptionsType:
    if bpy.context.scene is None:
        return SpartanOptionsType()
    props: SpartanOptions = bpy.context.scene.spartan_properties  # pyright: ignore[reportAttributeAccessIssue]
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
        vanity_opts = ocgd_body.box()
        vanity_opts.prop(props, "body_type")
        vanity_opts.prop(props, "left_arm")
        vanity_opts.prop(props, "right_arm")
        vanity_opts.prop(props, "left_leg")
        vanity_opts.prop(props, "right_leg")
        vanity_opts.prop(props, "gamertag")
        _ = vanity_opts.operator("ekur.importvanity")
