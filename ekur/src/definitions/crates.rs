use infinite_rs::{tag::types::common_types::FieldReference, TagStructure};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x708))]
pub struct CrateDefinition {
    #[data(offset(0x78))]
    pub model: FieldReference,
}
