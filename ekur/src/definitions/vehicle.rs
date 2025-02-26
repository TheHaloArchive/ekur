use infinite_rs::{TagStructure, tag::types::common_types::FieldReference};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x1130))]
pub struct Vehicle {
    #[data(offset(0x78))]
    pub model: FieldReference,
}
