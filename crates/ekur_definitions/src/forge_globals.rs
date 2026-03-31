/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{FieldBlock, FieldRealRGBColor},
};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x5D8))]
pub struct ForgeGlobals {
    #[data(offset(0x10))]
    pub colors: FieldBlock<ForgeColor>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x10))]
pub struct ForgeColor {
    #[data(offset(0x04))]
    pub color: FieldRealRGBColor,
}
