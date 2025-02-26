use infinite_rs::{TagStructure, tag::types::common_types::FieldReference};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x9F8))]
pub struct Equipment {
    #[data(offset(0x78))]
    pub model: FieldReference,
}
