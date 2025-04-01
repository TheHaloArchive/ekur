/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{FieldBlock, FieldReference, FieldStringId},
};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x5c))]
pub struct ForgeObjectDefinitionVariant {
    #[data(offset(0x00))]
    pub representation_name: FieldStringId,
    #[data(offset(0x04))]
    pub crate_variant: FieldStringId,
    #[data(offset(0x24))]
    pub object_definition: FieldReference,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x5c))]
pub struct ForgeAssetVariant {
    #[data(offset(0x00))]
    pub variant_name: FieldStringId,
    #[data(offset(0x04))]
    pub underlying_geo: FieldReference,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x228))]
pub struct ForgeObjectData {
    #[data(offset(0x34))]
    pub object_representations: FieldBlock<ForgeObjectDefinitionVariant>,
    #[data(offset(0x48))]
    pub forge_asset_variants: FieldBlock<ForgeAssetVariant>,
    #[data(offset(0x94))]
    pub default_representation: FieldStringId,
}
