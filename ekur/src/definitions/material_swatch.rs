use infinite_rs::tag::types::common_types::{
    AnyTag, FieldBlock, FieldReal, FieldRealRGBColor, FieldRealVector2D, FieldReference,
    FieldStringId,
};
use infinite_rs::TagStructure;

#[derive(Debug, Default, TagStructure)]
#[data(size(0x30))]
pub struct MaterialColorVariant {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub gradient_top_color: FieldRealRGBColor,
    #[data(offset(0x10))]
    pub gradient_mid_color: FieldRealRGBColor,
    #[data(offset(0x1C))]
    pub gradient_bot_color: FieldRealRGBColor,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0xA8))]
pub struct MaterialSwatchTag {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub color_and_roughness_texture_transform: FieldRealVector2D,
    #[data(offset(0x18))]
    pub normal_texture_transform: FieldRealVector2D,
    #[data(offset(0x20))]
    pub color_gradient_map: FieldReference,
    #[data(offset(0x3c))]
    pub roughness_white: FieldReal,
    #[data(offset(0x40))]
    pub roughness_black: FieldReal,
    #[data(offset(0x44))]
    pub normal_detail_map: FieldReference,
    #[data(offset(0x60))]
    pub metallic: FieldReal,
    #[data(offset(0x6c))]
    pub sss_strength: FieldReal,
    #[data(offset(0x70))]
    pub scratch_color: FieldRealRGBColor,
    #[data(offset(0x80))]
    pub scratch_roughness: FieldReal,
    #[data(offset(0x84))]
    pub scratch_metallic: FieldReal,
    #[data(offset(0x90))]
    pub sss_intensity: FieldReal,
    #[data(offset(0x94))]
    pub color_variants: FieldBlock<MaterialColorVariant>,
}
