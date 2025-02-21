/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::TagStructure;
use infinite_rs::tag::types::common_types::{
    AnyTag, FieldBlock, FieldLongInteger, FieldReference, FieldStringId,
};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x24))]
pub struct RuntimeCoatingStyleRef {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub variant_name: FieldStringId,
    #[data(offset(0x08))]
    pub style_ref: FieldReference,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x48))]
pub struct RuntimeCoatingStyles {
    #[data(offset(0x00))]
    any_tag: AnyTag,
    #[data(offset(0x10))]
    pub styles: FieldBlock<RuntimeCoatingStyleRef>,
    #[data(offset(0x24))]
    pub visor_swatch: FieldReference,
    #[data(offset(0x40))]
    pub default_style_index: FieldLongInteger,
}
