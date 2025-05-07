# pyright: reportUninitializedInstanceVariable=false, reportUnknownVariableType=false, reportUnknownMemberType=false
import bpy

from typing import cast
from bpy.props import BoolProperty, StringProperty
from bpy.types import PropertyGroup, UILayout


class ForgeMapOptions(PropertyGroup):
    url: StringProperty(name="URL", default="")
    use_file: BoolProperty(name="Use MVAR File", default=False)
    import_folders: BoolProperty(name="Import Folders", default=True)
    remove_blockers: BoolProperty(name="Remove Blockers", default=True)
    mvar_file: StringProperty(
        name="MVAR File",
        description="Path to .mvar file to import.",
        subtype="FILE_PATH",
    )


class ForgeMapOptionsType:
    url: str = ""
    use_file: bool = False
    import_folders: bool = True
    remove_blockers: bool = True
    mvar_file: str = ""


def get_forge_map_options() -> ForgeMapOptionsType:
    if bpy.context.scene is None:
        return ForgeMapOptionsType()
    props: ForgeMapOptionsType = bpy.context.scene.forge_map_properties  # pyright: ignore[reportAttributeAccessIssue]
    if props:
        return cast(ForgeMapOptionsType, props)
    return ForgeMapOptionsType()


def draw_forge_map_options(layout: UILayout, props: ForgeMapOptionsType) -> None:
    forge_header, forge_body = layout.panel("VIEW3D_PT_import_forge_map", default_closed=True)
    forge_header.label(icon="MAT_SPHERE_SKY", text="Import Forge Map")
    if forge_body:
        forge_opts = forge_body.box()
        forge_opts.prop(props, "url")
        forge_opts.prop(props, "import_folders")
        forge_opts.prop(props, "remove_blockers")
        op = forge_opts.operator("wm.url_open", text="Browse Maps (Cylix)", icon="URL")
        op.url = "https://cylix.guide/discovery/"  # pyright: ignore[reportAttributeAccessIssue]
        op = forge_opts.operator("wm.url_open", text="Browse Maps (Waypoint)", icon="URL")
        op.url = "https://www.halowaypoint.com/halo-infinite/ugc/browse"  # pyright: ignore[reportAttributeAccessIssue]
        forge_opts.prop(props, "use_file")
        if props.use_file:
            forge_opts.prop(props, "mvar_file")
        _ = forge_body.operator("ekur.importforgemap")
