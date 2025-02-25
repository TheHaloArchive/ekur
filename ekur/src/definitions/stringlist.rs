/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */

use infinite_rs::{
    TagStructure,
    tag::types::common_types::{
        AnyTag, FieldBlock, FieldData, FieldLongEnum, FieldLongInteger, FieldStringId,
        FieldTagResource,
    },
};
use num_enum::TryFromPrimitive;

#[derive(Debug, Default, TagStructure)]
#[data(size(0x08))]
pub struct UnicodeStringListLookupInfo {
    #[data(offset(0x00))]
    pub string_id: FieldStringId,
    #[data(offset(0x04))]
    pub offset: FieldLongInteger,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x0C))]
pub struct UnicodeSubstitutionPair {
    #[data(offset(0x00))]
    pub first_string_id: FieldStringId,
    #[data(offset(0x04))]
    pub second_string_id: FieldStringId,
    #[data(offset(0x08))]
    pub associated_value: FieldLongInteger,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x40))]
pub struct UnicodeStringListResource {
    #[data(offset(0x00))]
    pub string_lookup_info: FieldBlock<UnicodeStringListLookupInfo>,
    #[data(offset(0x14))]
    pub substitution_pairs: FieldBlock<UnicodeSubstitutionPair>,
    #[data(offset(0x28))]
    pub string_data_utf8: FieldData,
}

#[derive(Debug, Default, TryFromPrimitive)]
#[repr(u32)]
pub enum Language {
    #[default]
    English,
    Japanese,
    German,
    French,
    Spanish,
    MexicanSpanish,
    Italian,
    Korean,
    ChineseTraditional,
    ChineseSimplified,
    Portuguese,
    Polish,
    Russian,
    Danish,
    Finnish,
    Dutch,
    Norwegian,
    BrazilianPortuguese,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x14))]
pub struct LanguageReference {
    #[data(offset(0x00))]
    pub language_id: FieldLongEnum<Language>,
    #[data(offset(0x04))]
    pub string_list_resource: FieldTagResource<UnicodeStringListResource>,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x28))]
pub struct UnicodeStringListGroup {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub language_references: FieldBlock<LanguageReference>,
}
