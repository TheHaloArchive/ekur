/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{
    tag::types::common_types::{AnyTag, FieldBlock, FieldReference, FieldStringId},
    TagStructure,
};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x04))]
pub struct PermutationName {
    #[data(offset(0x00))]
    pub name: FieldStringId,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(60))]
pub struct PermutationSetting {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub style: FieldReference,
    #[data(offset(32))]
    pub attachment: FieldReference,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(44))]
pub struct RegionBlock {
    #[data(offset(0x00))]
    pub region_name: FieldStringId,
    #[data(offset(0x04))]
    pub permutation_regions: FieldBlock<PermutationName>,
    #[data(offset(24))]
    pub permutation_settings: FieldBlock<PermutationSetting>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(28))]
pub struct Attachment {
    #[data(offset(0x00))]
    pub attachment: FieldReference,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x90))]
pub struct ObjectTheme {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub regions: FieldBlock<RegionBlock>,
    #[data(offset(0x20))]
    pub attachments: FieldBlock<Attachment>,
    #[data(offset(56))]
    pub prosthetics: FieldBlock<RegionBlock>,
    #[data(offset(76))]
    pub body_types: FieldBlock<RegionBlock>,
}
