/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{
        AnyTag, FieldBlock, FieldReal, FieldRealQuaternion, FieldRealVector3D, FieldShortEnum,
        FieldShortInteger, FieldStringId,
    },
};
use num_enum::TryFromPrimitive;

use super::render_model::{BoundingBoxBlock, MeshResourceGroupBlock, NodeMapBlock, SectionBlock};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x04))]
pub struct LODTransitionDistanceBlock {
    #[data(offset(0x00))]
    pub distance: FieldReal,
}

#[derive(Default, Debug, TryFromPrimitive)]
#[repr(u16)]
pub enum ResourcePackingPolicyU16 {
    #[default]
    SingleResource,
    ResourcePerMeshPermutation,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x90))]
pub struct RuntimeGeoPerMeshData {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub mesh_index: FieldShortInteger,
    #[data(offset(0x08))]
    pub scale: FieldRealVector3D,
    #[data(offset(0x14))]
    pub forward: FieldRealVector3D,
    #[data(offset(0x20))]
    pub left: FieldRealVector3D,
    #[data(offset(0x2C))]
    pub right: FieldRealVector3D,
    #[data(offset(0x38))]
    pub position: FieldRealVector3D,
    #[data(offset(0x6C))]
    pub lod_levels: FieldBlock<LODTransitionDistanceBlock>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(24))]
pub struct StaticMarkerGroupBlock {
    #[data(offset(0x00))]
    pub translation: FieldRealVector3D,
    #[data(offset(12))]
    pub rotation: FieldRealQuaternion,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(24))]
pub struct StaticMarkerBlock {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub markers: FieldBlock<StaticMarkerGroupBlock>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x198))]
pub struct RuntimeGeo {
    #[data(offset(0x0))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub per_mesh_data: FieldBlock<RuntimeGeoPerMeshData>,
    #[data(offset(64))]
    pub sections: FieldBlock<SectionBlock>,
    #[data(offset(104))]
    pub bounding_boxes: FieldBlock<BoundingBoxBlock>,
    #[data(offset(124))]
    pub node_maps: FieldBlock<NodeMapBlock>,
    #[data(offset(186))]
    pub resource_packing_policy: FieldShortEnum<ResourcePackingPolicyU16>,
    #[data(offset(188))]
    pub total_index_buffer_count: FieldShortInteger,
    #[data(offset(190))]
    pub total_vertex_buffer_count: FieldShortInteger,
    #[data(offset(196))]
    pub mesh_resource_groups: FieldBlock<MeshResourceGroupBlock>,
    #[data(offset(376))]
    pub markers: FieldBlock<StaticMarkerBlock>,
}
