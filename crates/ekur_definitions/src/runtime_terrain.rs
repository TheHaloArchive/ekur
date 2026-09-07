/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{
        AnyTag, FieldArray, FieldBlock, FieldDwordInteger, FieldLongInteger, FieldReal,
        FieldRealVector2D, FieldRealVector3D, FieldReference, FieldStringId, FieldWordInteger,
    },
};

#[derive(Default, Debug, TagStructure)]
#[data(size(4))]
pub struct InputBitmapIndexBlock {
    #[data(offset(0x00))]
    pub index: FieldDwordInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(24))]
pub struct InputTextureDataBlock {
    #[data(offset(0x00))]
    pub output_id: FieldLongInteger,
    #[data(offset(0x04))]
    pub bitmap_index: FieldLongInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(112))]
pub struct QuadTreeNodeBlock {
    #[data(offset(0x3C))]
    pub input_bitmap_indices: FieldBlock<InputBitmapIndexBlock>,
    #[data(offset(0x50))]
    pub min_height: FieldReal,
    #[data(offset(0x54))]
    pub max_height: FieldReal,
    #[data(offset(0x58))]
    pub input_texture_data: FieldBlock<InputTextureDataBlock>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(12))]
pub struct OutputBitmapReferenceBlock {
    #[data(offset(0x00))]
    pub bitmap_reference_index: FieldLongInteger,
    #[data(offset(0x04))]
    pub uv_scale: FieldRealVector2D,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(40))]
pub struct MaterialLayerIdBlock {
    #[data(offset(0x00))]
    pub id: FieldStringId,
    #[data(offset(0x04), count(3))]
    pub output_bitmap_references: FieldArray<OutputBitmapReferenceBlock>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(32))]
pub struct MaterialLayerBitmapReferenceBlock {
    #[data(offset(0x04))]
    pub bitmap_reference: FieldReference,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x208))]
pub struct RuntimeTerrain {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub bitmap: FieldReference,
    #[data(offset(0x40))]
    pub render_material: FieldReference,
    #[data(offset(0x5C))]
    pub masks_composite_material: FieldReference,
    #[data(offset(0x7C))]
    pub quad_tree_level_count: FieldWordInteger,
    #[data(offset(0x80))]
    pub quad_tree_position: FieldRealVector3D,
    #[data(offset(0x8C))]
    pub quad_tree_size: FieldRealVector3D,
    #[data(offset(0x98))]
    pub quad_tree_nodes: FieldBlock<QuadTreeNodeBlock>,
    #[data(offset(0xAC))]
    pub material_layer_ids: FieldBlock<MaterialLayerIdBlock>,
    #[data(offset(0xC8))]
    pub material_layer_bitmap_references: FieldBlock<MaterialLayerBitmapReferenceBlock>,
}
