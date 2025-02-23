/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{
        FieldBlock, FieldRealBounds, FieldRealPoint3D, FieldRealVector3D, FieldReference,
        FieldShortInteger, FieldWordFlags,
    },
};

use super::render_model::{MaterialBlock, MeshFlags};

#[derive(Default, Debug, TagStructure)]
#[data(size(100))]
pub struct ClusterBlock {
    #[data(offset(0x0))]
    pub x_bounds: FieldRealBounds,
    #[data(offset(0x8))]
    pub y_bounds: FieldRealBounds,
    #[data(offset(16))]
    pub z_bounds: FieldRealBounds,
    #[data(offset(44))]
    pub section_index: FieldShortInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(320))]
pub struct BspGeometryInstanceBlock {
    #[data(offset(0x00))]
    pub transform_scale: FieldRealVector3D,
    #[data(offset(0x0c))]
    pub forward: FieldRealVector3D,
    #[data(offset(0x18))]
    pub left: FieldRealVector3D,
    #[data(offset(0x24))]
    pub up: FieldRealVector3D,
    #[data(offset(0x30))]
    pub position: FieldRealPoint3D,
    #[data(offset(60))]
    pub runtime_geo: FieldReference,
    #[data(offset(116))]
    pub mesh_index: FieldShortInteger,
    #[data(offset(118))]
    pub bounds_index: FieldShortInteger,
    #[data(offset(240))]
    pub material: FieldBlock<MaterialBlock>,
    #[data(offset(272))]
    pub flags_override: FieldWordFlags<MeshFlags>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x2518))]
pub struct ScenarioStructureBsp {
    #[data(offset(0x12c))]
    pub cluster_blocks: FieldBlock<ClusterBlock>,
    #[data(offset(420))]
    pub bsp_geometry_instances: FieldBlock<BspGeometryInstanceBlock>,
}
