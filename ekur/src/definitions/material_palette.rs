/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::TagStructure;
use infinite_rs::tag::types::common_types::{
    AnyTag, FieldBlock, FieldCharEnum, FieldReal, FieldReference, FieldStringId,
};
use num_enum::TryFromPrimitive;

#[derive(Default, Debug, TryFromPrimitive)]
#[repr(u8)]
pub enum MaterialRoughnessOverride {
    #[default]
    Neg100,
    Neg75,
    Neg50,
    Neg25,
    None,
    Pos25,
    Pos50,
    Pos75,
    Pos100,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x38))]
pub struct MaterialSwatchEntry {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub swatch: FieldReference,
    #[data(offset(0x20))]
    pub color: FieldStringId,
    #[data(offset(0x24))]
    pub roughness_override: FieldCharEnum<MaterialRoughnessOverride>,
    #[data(offset(0x28))]
    pub emissive_intensity: FieldReal,
    #[data(offset(0x2C))]
    pub emissive_amount: FieldReal,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x28))]
pub struct MaterialPaletteTag {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub swatches: FieldBlock<MaterialSwatchEntry>,
}
