/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{AnyTag, FieldBlock, FieldShortEnum, FieldWordInteger},
};

use super::{
    render_model::{BoundingBoxBlock, MeshResourceGroupBlock, SectionBlock},
    runtime_geo::ResourcePackingPolicyU16,
};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x178))]
pub struct ParticleModel {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(40))]
    pub sections: FieldBlock<SectionBlock>,
    #[data(offset(80))]
    pub bounding_boxes: FieldBlock<BoundingBoxBlock>,
    #[data(offset(162))]
    pub mesh_resource_packing_policy: FieldShortEnum<ResourcePackingPolicyU16>,
    #[data(offset(164))]
    pub total_index_buffer_count: FieldWordInteger,
    #[data(offset(166))]
    pub total_vertex_buffer_count: FieldWordInteger,
    #[data(offset(172))]
    pub resources: FieldBlock<MeshResourceGroupBlock>,
}
