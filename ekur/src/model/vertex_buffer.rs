/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::io::Write;

use anyhow::Result;
use byteorder::{LE, WriteBytesExt};

use crate::definitions::render_model::{
    MeshResourceGroupBlock, RasterizerVertexBuffer, SectionLods, VertexBufferUsage,
};

use super::{serialize::VertexBuffers, utils::get_resource_data};

fn write_buffer(vertex_buffer: &RasterizerVertexBuffer, resource: &[u8]) -> Result<Vec<u8>> {
    let stride = vertex_buffer.stride.0 as usize;
    let mut buffer = Vec::with_capacity(vertex_buffer.count.0 as usize * stride);
    buffer.write_u8(vertex_buffer.stride.0)?;
    buffer.write_i32::<LE>(vertex_buffer.count.0)?;
    for i in 0..vertex_buffer.count.0 {
        buffer.write_all(&resource[i as usize * stride..i as usize * stride + stride])?;
    }
    Ok(buffer)
}

pub(super) fn get_vertex_buffer(
    api_resource: Option<&MeshResourceGroupBlock>,
    lod_data: &SectionLods,
    buffers: &[Vec<u8>],
    vertex_buffers: &mut VertexBuffers,
) -> Result<()> {
    if let Some(api_resource) = api_resource {
        for index in lod_data.vertex_buffer_indices.elements.iter() {
            if index.vertex_buffer_index.0 == -1 {
                continue;
            }
            let vertex_buffer = &api_resource.resource.data.vertex_buffers.elements
                [index.vertex_buffer_index.0 as usize];
            let resource_buffer = get_resource_data(
                vertex_buffer.offset.0 as usize,
                vertex_buffer.count.0 as usize * vertex_buffer.stride.0 as usize,
                buffers,
            );

            match vertex_buffer.vertex_buffer_usage.0 {
                VertexBufferUsage::Position => {
                    vertex_buffers.position = Some(write_buffer(vertex_buffer, &resource_buffer)?);
                }
                VertexBufferUsage::UV0 => {
                    vertex_buffers.uv0 = Some(write_buffer(vertex_buffer, &resource_buffer)?);
                }
                VertexBufferUsage::UV1 => {
                    vertex_buffers.uv1 = Some(write_buffer(vertex_buffer, &resource_buffer)?);
                }
                VertexBufferUsage::UV2 => {
                    vertex_buffers.uv2 = Some(write_buffer(vertex_buffer, &resource_buffer)?);
                }
                VertexBufferUsage::Normal => {
                    vertex_buffers.normal = Some(write_buffer(vertex_buffer, &resource_buffer)?);
                }
                VertexBufferUsage::Color => {
                    vertex_buffers.color = Some(write_buffer(vertex_buffer, &resource_buffer)?);
                }
                VertexBufferUsage::BlendIndices0 => {
                    vertex_buffers.blend_indices =
                        Some(write_buffer(vertex_buffer, &resource_buffer)?);
                }

                VertexBufferUsage::BlendWeights0 => {
                    vertex_buffers.blend_weights =
                        Some(write_buffer(vertex_buffer, &resource_buffer)?);
                }
                VertexBufferUsage::BlendWeights1 => {
                    vertex_buffers.blend_weights_extra =
                        Some(write_buffer(vertex_buffer, &resource_buffer)?);
                }
                _ => {}
            }
        }
    }
    Ok(())
}
