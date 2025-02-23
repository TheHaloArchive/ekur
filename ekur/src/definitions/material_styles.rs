/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::TagStructure;
use infinite_rs::tag::types::common_types::{
    AnyTag, FieldBlock, FieldInt64Integer, FieldReal, FieldReference, FieldStringId,
};

#[derive(Debug, Default, TagStructure)]
#[data(size(0x04))]
pub struct IntentionConversionElement {
    #[data(offset(0x00))]
    pub intention_name: FieldStringId,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x18))]
pub struct MaterialRegion {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub intention_conversion_list: FieldBlock<IntentionConversionElement>,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x48))]
pub struct MaterialLayer {
    #[data(offset(0x00))]
    pub element_id: FieldInt64Integer,
    #[data(offset(0x08))]
    pub name: FieldStringId,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x28))]
pub struct MaterialStyleRegion {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x08))]
    pub layers: FieldBlock<MaterialLayer>,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x5C))]
pub struct MaterialStyle {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub palette: FieldReference,
    #[data(offset(0x20))]
    pub global_damage: FieldStringId,
    #[data(offset(0x24))]
    pub hero_damage: FieldStringId,
    #[data(offset(0x28))]
    pub global_emissive: FieldStringId,
    #[data(offset(0x2C))]
    pub emissive_amount: FieldReal,
    #[data(offset(0x30))]
    pub scratch_amount: FieldReal,
    #[data(offset(0x34))]
    pub grime_type: FieldStringId,
    #[data(offset(0x38))]
    pub grime_amount: FieldReal,
    #[data(offset(0x3C))]
    pub regions: FieldBlock<MaterialStyleRegion>,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0xB0))]
pub struct MaterialStylesTag {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub regions: FieldBlock<MaterialRegion>,
    #[data(offset(0x50))]
    pub styles: FieldBlock<MaterialStyle>,
    #[data(offset(0x74))]
    pub visor_swatch: FieldReference,
}
