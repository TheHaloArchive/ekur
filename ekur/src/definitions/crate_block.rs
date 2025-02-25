/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{TagStructure, tag::types::common_types::FieldReference};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x708))]
pub struct CrateDefinition {
    #[data(offset(0x78))]
    pub model: FieldReference,
}
