/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{AnyTag, FieldBlock, FieldReference, FieldStringId},
};

#[derive(Default, Debug, TagStructure)]
#[data(size(56))]
pub struct ThemeConfiguration {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub variant_name: FieldStringId,
    #[data(offset(0x08))]
    pub theme_configs: FieldReference,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(80))]
pub struct ObjectTheme {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub model: FieldReference,
    #[data(offset(32))]
    pub object_reference: FieldReference,
    #[data(offset(60))]
    pub theme_configurations: FieldBlock<ThemeConfiguration>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x1A0))]
pub struct CustomizationGlobals {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub themes: FieldBlock<ObjectTheme>,
}
