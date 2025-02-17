use infinite_rs::{tag::types::common_types::FieldReference, TagStructure};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x438))]
pub struct ModelDefinition {
    #[data(offset(0x10))]
    pub render_model: FieldReference,
}
