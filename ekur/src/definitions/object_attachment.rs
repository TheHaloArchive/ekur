/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{AnyTag, FieldBlock, FieldReference, FieldStringId},
};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x28))]
pub struct ObjectMarker {
    #[data(offset(0x00))]
    pub marker_name: FieldStringId,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x38))]
pub struct ModelAttachment {
    #[data(offset(0x00))]
    pub model: FieldReference,
    #[data(offset(0x1C))]
    pub variant_name: FieldStringId,
    #[data(offset(0x20))]
    pub markers: FieldBlock<ObjectMarker>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x28))]
pub struct AttachmentConfiguration {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub model_attachments: FieldBlock<ModelAttachment>,
}
