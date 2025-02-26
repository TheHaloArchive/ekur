use infinite_rs::{TagStructure, tag::types::common_types::FieldReference};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x1198))]
pub struct Weapon {
    #[data(offset(0x78))]
    pub model: FieldReference,
}
