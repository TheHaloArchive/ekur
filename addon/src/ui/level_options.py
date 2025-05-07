# pyright: reportUnknownMemberType=false, reportUninitializedInstanceVariable=false, reportUnknownVariableType=false
from typing import cast
import bpy
from bpy.props import StringProperty
from bpy.types import PropertyGroup, UILayout


class LevelOptions(PropertyGroup):
    level_path: StringProperty(
        default="",
        name="Level Path",
        description="Path to .json level file to import.",
        subtype="FILE_PATH",
    )


class LevelOptionsType:
    level_path: str = ""


def get_level_options() -> LevelOptionsType:
    if bpy.context.scene is None:
        return LevelOptionsType()
    props: LevelOptionsType = bpy.context.scene.level_properties  # pyright: ignore[reportAttributeAccessIssue]
    if props:
        return cast(LevelOptionsType, props)
    return LevelOptionsType()


def draw_level_options(layout: UILayout, props: LevelOptionsType) -> None:
    level_header, level_body = layout.panel("VIEW3D_PT_import_level", default_closed=True)
    level_header.label(icon="MESH_GRID", text="Import Level")
    if level_body:
        level_opts = level_body.box()
        level_opts.prop(props, "level_path")
        _ = level_body.operator("ekur.importlevel")
