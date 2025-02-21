/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{TagStructure, tag::types::common_types::FieldReference};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x438))]
pub struct ModelDefinition {
    #[data(offset(0x10))]
    pub render_model: FieldReference,
}
