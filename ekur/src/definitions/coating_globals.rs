use crate::definitions::runtime_style::CoatingPaletteInfo;
use infinite_rs::{
    tag::types::common_types::{AnyTag, FieldBlock, FieldStringId},
    TagStructure,
};

#[derive(Debug, Default, TagStructure)]
#[data(size(0x88))]
pub struct CoatingIntentionDefinition {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub fallback_intention: FieldStringId,
    #[data(offset(0x08))]
    pub intention: CoatingPaletteInfo,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x38))]
pub struct CoatingGlobalsTag {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x24))]
    pub global_shader_lookup: FieldBlock<CoatingIntentionDefinition>,
}
