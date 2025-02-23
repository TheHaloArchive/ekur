/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use anyhow::Result;
use byteorder::WriteBytesExt;
use infinite_rs::{ModuleFile, module::file::TagStructure};
use std::{fs::File, io::BufWriter};

use crate::definitions::render_model::{MeshResourceGroupBlock, SectionLods, VertexBufferUsage};

pub(super) fn get_resource_data(
    offset: usize,
    length: usize,
    resource_buffers: &[Vec<u8>],
) -> Vec<u8> {
    let mut output = vec![0u8; length];
    let mut resource_index = 0;
    let mut resource_position = 0;
    let mut output_position = 0;

    while output_position < length && resource_index < resource_buffers.len() {
        let resource_buffer = &resource_buffers[resource_index];

        if offset >= resource_position + resource_buffer.len() {
            resource_position += resource_buffer.len();
            resource_index += 1;
            continue;
        }

        let mut offset_in_block = 0;
        if offset > resource_position {
            offset_in_block += offset - resource_position;
            resource_position += offset_in_block;
        }

        let bytes_to_copy = (length - output_position).min(resource_buffer.len() - offset_in_block);
        output[output_position..output_position + bytes_to_copy]
            .copy_from_slice(&resource_buffer[offset_in_block..offset_in_block + bytes_to_copy]);

        output_position += bytes_to_copy;
        resource_position += bytes_to_copy;
        resource_index += 1;
    }

    output
}

pub(super) fn get_buffers<T: TagStructure>(
    model: (&(usize, usize, i32), &T),
    modules: &mut [ModuleFile],
) -> Result<Vec<Vec<u8>>> {
    let module = &mut modules[model.0.0];
    let mut buffers = Vec::new();
    {
        let tag = &module.files[model.0.1];
        let resources = module.resource_indices[tag.resource_index as usize
            ..tag.resource_index as usize + tag.resource_count as usize]
            .to_vec();
        for resource in resources {
            let tag_thing = module.read_tag(resource)?;
            if let Some(tag_thing) = tag_thing {
                buffers.push(tag_thing.get_raw_data(true)?);
            }
            module.files[resource as usize].data_stream = None;
        }
    }
    Ok(buffers)
}

pub(super) fn data_exists(
    lod_data: &SectionLods,
    api_resource: Option<&MeshResourceGroupBlock>,
    writer: &mut BufWriter<File>,
    usage: VertexBufferUsage,
) -> Result<()> {
    let mut vert = false;
    if let Some(api_resource) = api_resource {
        vert = lod_data.vertex_buffer_indices.elements.iter().any(|x| {
            if x.vertex_buffer_index.0 == -1 {
                return false;
            }
            api_resource.resource.data.vertex_buffers.elements[x.vertex_buffer_index.0 as usize]
                .vertex_buffer_usage
                .0
                == usage
        });
    }
    writer.write_u8(if vert { 1 } else { 0 })?;
    Ok(())
}
