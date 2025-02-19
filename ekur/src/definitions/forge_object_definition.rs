use infinite_rs::{
    tag::types::common_types::{FieldBlock, FieldReference, FieldStringId},
    TagStructure,
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
#[data(size(0x228))]
pub struct ForgeObjectData {
    #[data(offset(0x34))]
    pub object_representations: FieldBlock<ForgeObjectDefinitionVariant>,
}
