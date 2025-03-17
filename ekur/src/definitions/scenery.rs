/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{TagStructure, tag::types::common_types::FieldReference};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x6D8))]
pub struct Scenery {
    #[data(offset(0x78))]
    pub model: FieldReference,
}
