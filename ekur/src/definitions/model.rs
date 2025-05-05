/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{FieldBlock, FieldReference, FieldStringId},
};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x438))]
pub struct ModelDefinition {
    #[data(offset(0x10))]
    pub render_model: FieldReference,
    #[data(offset(0xF4))]
    pub variants: FieldBlock<ModelVariant>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x16C))]
pub struct ModelVariant {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub style: FieldStringId,
}
