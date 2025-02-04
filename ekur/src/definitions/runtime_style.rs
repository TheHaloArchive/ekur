/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::tag::types::common_types::{
    AnyTag, FieldBlock, FieldCharEnum, FieldInt64Integer, FieldReal, FieldRealRGBColor,
    FieldReference, FieldShortEnum, FieldStringId,
};
use infinite_rs::TagStructure;
use num_enum::TryFromPrimitive;

#[derive(Default, Debug, TryFromPrimitive)]
#[repr(u8)]
pub enum OverrideColorsEnum {
    #[default]
    OverrideColors,
    UseDefaultColors,
}

#[derive(Default, Debug, TryFromPrimitive)]
#[repr(u8)]
pub enum MaterialState {
    #[default]
    Disabled,
    Enabled,
}

#[derive(Default, Debug, TryFromPrimitive)]
#[repr(u16)]
pub enum UseSSSEnum {
    #[default]
    DoNotUseSubsurface,
    UseSubsurface,
    Gummy,
    Alien,
    Brute,
    HumanPost,
    HumanPre,
    Inquisitor,
    Marble,
    Plastic,
    Preintegrated,
    Snow,
    Flood,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x80))]
pub struct CoatingPaletteInfo {
    #[data(offset(0x00))]
    pub element_id: FieldInt64Integer,
    #[data(offset(0x08))]
    pub description: FieldStringId,
    #[data(offset(0x0C))]
    pub swatch: FieldReference,
    #[data(offset(0x28))]
    pub gradient_color_flag: FieldCharEnum<OverrideColorsEnum>,
    #[data(offset(0x2C))]
    pub gradient_top_color: FieldRealRGBColor,
    #[data(offset(0x38))]
    pub gradient_mid_color: FieldRealRGBColor,
    #[data(offset(0x44))]
    pub gradient_bot_color: FieldRealRGBColor,
    #[data(offset(0x50))]
    pub roughness_offset: FieldReal,
    #[data(offset(0x54))]
    pub scratch_color_flag: FieldCharEnum<OverrideColorsEnum>,
    #[data(offset(0x58))]
    pub scratch_color: FieldRealRGBColor,
    #[data(offset(0x64))]
    pub scratch_roughness_offset: FieldReal,
    #[data(offset(0x68))]
    pub use_emissive: FieldCharEnum<MaterialState>,
    #[data(offset(0x76))]
    pub subsurface_usage: FieldShortEnum<UseSSSEnum>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x218))]
pub struct RuntimeCoatingStyleInfo {
    #[data(offset(0x00))]
    pub global_damage_swatch: CoatingPaletteInfo,
    #[data(offset(0x80))]
    pub hero_damage_swatch: CoatingPaletteInfo,
    #[data(offset(0x100))]
    pub global_emissive_swatch: CoatingPaletteInfo,
    #[data(offset(0x180))]
    pub emissive_amount: FieldReal,
    #[data(offset(0x184))]
    pub emissive_intensity: FieldReal,
    #[data(offset(0x188))]
    pub scratch_amount: FieldReal,
    #[data(offset(0x190))]
    pub grime_swatch: CoatingPaletteInfo,
    #[data(offset(0x210))]
    pub grime_amount: FieldReal,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x88))]
pub struct RuntimeCoatingIntention {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x08))]
    pub info: CoatingPaletteInfo,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x34))]
pub struct RuntimeCoatingRegion {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub coating_material_override: FieldReference,
    #[data(offset(0x20))]
    pub intentions: FieldBlock<RuntimeCoatingIntention>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x240))]
pub struct RuntimeCoatingStyle {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub info: RuntimeCoatingStyleInfo,
    #[data(offset(0x228))]
    pub regions: FieldBlock<RuntimeCoatingRegion>,
}
