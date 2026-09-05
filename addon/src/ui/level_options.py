# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import cast

import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty
from bpy.types import PropertyGroup, UILayout


class LevelOptions(PropertyGroup):
    level_path: StringProperty(
        default="",
        name="Level Path",
        description="Path to .json level file to import.",
        subtype="FILE_PATH",
    )
    import_vista: BoolProperty(
        default=True,
        name="Import Vistas",
        description="Import the level's vista BSPs.",
    )
    only_active_bsps: BoolProperty(
        default=False,
        name="Default Zone Set Only",
        description="Import only the structure BSPs the level's default zone set activates instead of every BSP the level names",
    )
    import_terrain: BoolProperty(
        default=True,
        name="Import Terrain",
        description="Rebuild the level's terrain from its heightfield, if it has one",
    )
    terrain_step: IntProperty(
        default=4,
        min=1,
        max=64,
        name="Terrain Step",
        description="Decimation of the terrain sample grid. The source is 0.1 world units per sample",
    )
    batch_size: IntProperty(
        default=250,
        min=1,
        max=10000,
        name="Batch Size",
        description="Instances placed per update. Smaller batches keep Blender more responsive",
    )


class LevelOptionsType:
    level_path: str = ""
    import_vista: bool = True
    only_active_bsps: bool = False
    import_terrain: bool = True
    terrain_step: int = 4
    batch_size: int = 250


def get_level_options() -> LevelOptionsType:
    if bpy.context.scene is None:
        return LevelOptionsType()
    props: LevelOptionsType = bpy.context.scene.level_properties  # ty: ignore[unresolved-attribute]
    if props:
        return cast(LevelOptionsType, props)
    return LevelOptionsType()


def draw_level_options(layout: UILayout, props: LevelOptionsType) -> None:
    level_header, level_body = layout.panel("VIEW3D_PT_import_level", default_closed=True)
    level_header.label(icon="MESH_GRID", text="Import Level")
    if level_body:
        level_opts = level_body.box()
        level_opts.prop(props, "level_path")
        level_opts.prop(props, "import_vista")
        level_opts.prop(props, "only_active_bsps")
        level_opts.prop(props, "batch_size")
        terrain_opts = level_body.box()
        terrain_opts.prop(props, "import_terrain")
        terrain_row = terrain_opts.row()
        terrain_row.enabled = props.import_terrain
        terrain_row.prop(props, "terrain_step")
        _ = level_body.operator("ekur.importlevel")
