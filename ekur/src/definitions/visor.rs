/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{
    tag::types::common_types::{
        AnyTag, FieldBlock, FieldRealRGBColor, FieldReference, FieldStringId,
    },
    TagStructure,
};

#[derive(Debug, Default, TagStructure)]
#[data(size(0x20))]
pub struct MaterialVisorPatternReference {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub reference: FieldReference,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x30))]
pub struct MaterialColorVariants {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub top_color: FieldRealRGBColor,
    #[data(offset(0x10))]
    pub mid_color: FieldRealRGBColor,
    #[data(offset(0x1C))]
    pub bot_color: FieldRealRGBColor,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x38))]
pub struct MaterialVisorSwatchTag {
    #[data(offset(0x00))]
    any_tag: AnyTag,
    #[data(offset(0x10))]
    pub pattern_variants: FieldBlock<MaterialVisorPatternReference>,
    #[data(offset(0x24))]
    pub color_variants: FieldBlock<MaterialColorVariants>,
}
