/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::tag::types::common_types::{
    AnyTag, FieldReal, FieldRealRGBColor, FieldRealVector2D, FieldReference,
};
use infinite_rs::TagStructure;

#[derive(Debug, Default, TagStructure)]
#[data(size(0xD8))]
pub struct CoatingSwatchPODTag {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x2C))]
    pub color_and_roughness_texture_transform: FieldRealVector2D,
    #[data(offset(0x34))]
    pub normal_texture_transform: FieldRealVector2D,
    #[data(offset(0x3C))]
    pub color_gradient_map: FieldReference,
    #[data(offset(0x58))]
    pub gradient_top_color: FieldRealRGBColor,
    #[data(offset(0x64))]
    pub gradient_mid_color: FieldRealRGBColor,
    #[data(offset(0x70))]
    pub gradient_bot_color: FieldRealRGBColor,
    #[data(offset(0x7C))]
    pub roughness_white: FieldReal,
    #[data(offset(0x80))]
    pub roughness_black: FieldReal,
    #[data(offset(0x84))]
    pub normal_detail_map: FieldReference,
    #[data(offset(0xA0))]
    pub metallic: FieldReal,
    #[data(offset(0xAC))]
    pub scratch_color: FieldRealRGBColor,
    #[data(offset(0xBC))]
    pub scratch_roughness: FieldReal,
    #[data(offset(0xC0))]
    pub scratch_metallic: FieldReal,
    #[data(offset(0xCC))]
    pub sss_intensity: FieldReal,
    #[data(offset(0xD0))]
    pub emissive_intensity: FieldReal,
    #[data(offset(0xD4))]
    pub emissive_amount: FieldReal,
}
