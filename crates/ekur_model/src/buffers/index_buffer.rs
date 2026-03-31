/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::utils::get_resource_data;
use ekur_definitions::render_model::{MeshResourceGroupBlock, SectionLods};

use anyhow::Result;
use byteorder::{LE, WriteBytesExt};
use std::io::Write;

pub(crate) fn write_index_buffer<R: Write>(
    writer: &mut R,
    api_resource: Option<&MeshResourceGroupBlock>,
    lod_data: &SectionLods,
    buffers: &[Vec<u8>],
) -> Result<()> {
    if let Some(api_resource) = api_resource {
        let index_buffer = &api_resource.resource.data.index_buffers.elements
            [lod_data.index_buffer_index.0 as usize];
        writer.write_u8(index_buffer.declaration_type.0.to_int())?;
        writer.write_i8(index_buffer.stride.0)?;
        writer.write_i32::<LE>(index_buffer.count.0)?;
        let data = get_resource_data(
            index_buffer.offset.0 as usize,
            index_buffer.stride.0 as usize * index_buffer.count.0 as usize,
            buffers,
        );
        writer.write_all(&data)?;
    }
    Ok(())
}
