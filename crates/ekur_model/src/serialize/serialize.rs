/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use ekur_definitions::render_model::{
    LodFlags, MeshFlags, MeshResourceGroupBlock, NodeMapBlock, RenderModel, SectionBlock,
    VertexBufferUsage as VU,
};
use ekur_definitions::{particle_model::ParticleModel, runtime_geo::RuntimeGeo};

use anyhow::Result;
use byteorder::{LE, WriteBytesExt};
use infinite_rs::ModuleFile;
use std::io::Write;
use std::{collections::HashMap, io::BufWriter};

use crate::{
    serialize::metadata::{
        write_blendshape_boxes, write_bones, write_bounding_boxes, write_header,
        write_header_particle, write_header_rtgo, write_markers, write_markers_rtgo,
        write_materials, write_regions,
    },
    utils::get_buffers,
};

use crate::{
    buffers::{index_buffer::write_index_buffer, vertex_buffer::get_vertex_buffer},
    utils::data_exists,
};

use super::metadata::write_submeshes;

pub(crate) fn get_region_permutation(
    model: &RenderModel,
    section_index: usize,
) -> Result<(i32, i32)> {
    let mut region_name = 0;
    let mut permutation_name = 0;
    let region = model.regions.elements.iter().find(|x| {
        x.permutations.elements.iter().any(|y| {
            let start = y.section_index.0 as usize;
            let end = start + y.section_count.0 as usize;
            section_index >= start && section_index < end
        })
    });
    if let Some(region) = region {
        region_name = region.name.0;
        let permutation = region.permutations.elements.iter().find(|x| {
            let start = x.section_index.0 as usize;
            let end = start + x.section_count.0 as usize;
            section_index >= start && section_index < end
        });
        if let Some(permutation) = permutation {
            permutation_name = permutation.name.0;
        }
    }
    Ok((region_name, permutation_name))
}

#[derive(Default, Debug)]
pub(crate) struct VertexBuffers {
    pub(crate) position: Option<Vec<u8>>,
    pub(crate) uv0: Option<Vec<u8>>,
    pub(crate) uv1: Option<Vec<u8>>,
    pub(crate) uv2: Option<Vec<u8>>,
    pub(crate) normal: Option<Vec<u8>>,
    pub(crate) color: Option<Vec<u8>>,
    pub(crate) blend_indices: Option<Vec<u8>>,
    pub(crate) blend_weights: Option<Vec<u8>>,
    pub(crate) blend_weights_extra: Option<Vec<u8>>,
    pub(crate) blendshape_index: Option<Vec<u8>>,
    pub(crate) blendshape_position: Option<Vec<u8>>,
}

pub(crate) fn write_section<R: Write>(
    section: &SectionBlock,
    api_resource: Option<&MeshResourceGroupBlock>,
    writer: &mut R,
    buffers: &[Vec<u8>],
    region_name: Option<i32>,
    permutation_name: Option<i32>,
    node_maps: Option<&NodeMapBlock>,
) -> Result<()> {
    let lod_data = &section.section_lods.elements[0];
    if lod_data.lod_has_shadow_proxies.0 == 1 {
        return Ok(());
    }
    if !lod_data.lod_flags.0.contains(LodFlags::LOD0) {
        return Ok(());
    }

    if let Some(region_name) = region_name {
        writer.write_i32::<LE>(region_name)?;
    } else {
        writer.write_i32::<LE>(0)?;
    }
    if let Some(permutation_name) = permutation_name {
        writer.write_i32::<LE>(permutation_name)?;
    } else {
        writer.write_i32::<LE>(0)?;
    }
    writer.write_u32::<LE>(lod_data.submeshes.size)?;
    writer.write_u8(section.node_index.0)?;
    writer.write_u8(section.vertex_type.0.clone().into())?;
    writer.write_i8(section.use_dual_quat.0)?;
    write_submeshes(writer, lod_data)?;
    if section.mesh_flags.0.contains(MeshFlags::MESH_IS_UNINDEXED) {
        writer.write_u8(section.index_buffer_type.0.to_int())?;
        writer.write_i8(4)?;
        let vertex_count = api_resource
            .unwrap()
            .resource
            .data
            .vertex_buffers
            .elements
            .iter()
            .find(|x| x.vertex_buffer_usage.0 == VU::Position)
            .unwrap()
            .count
            .0;
        writer.write_i32::<LE>(vertex_count)?;
        for i in 0..vertex_count {
            writer.write_i32::<LE>(i)?;
        }
    } else {
        write_index_buffer(writer, api_resource, lod_data, buffers)?;
    }

    data_exists(lod_data, api_resource, writer, VU::Position)?;
    data_exists(lod_data, api_resource, writer, VU::UV0)?;
    data_exists(lod_data, api_resource, writer, VU::UV1)?;
    data_exists(lod_data, api_resource, writer, VU::UV2)?;
    data_exists(lod_data, api_resource, writer, VU::Normal)?;
    let uses_vertex_color = section.mesh_flags.0.contains(MeshFlags::USES_VERTEX_COLOR);
    if uses_vertex_color {
        data_exists(lod_data, api_resource, writer, VU::Color)?;
    } else {
        writer.write_u8(0)?;
    }
    data_exists(lod_data, api_resource, writer, VU::BlendIndices0)?;
    data_exists(lod_data, api_resource, writer, VU::BlendWeights0)?;
    data_exists(lod_data, api_resource, writer, VU::BlendWeights1)?;
    data_exists(lod_data, api_resource, writer, VU::BlendshapeIndex)?;
    data_exists(lod_data, api_resource, writer, VU::BlendshapePosition)?;

    let mut model = VertexBuffers::default();
    get_vertex_buffer(api_resource, lod_data, buffers, &mut model)?;

    if let Some(ref position) = model.position {
        writer.write_all(position.as_slice())?;
    }
    if let Some(ref uv0) = model.uv0 {
        writer.write_all(uv0.as_slice())?;
    }
    if let Some(ref uv1) = model.uv1 {
        writer.write_all(uv1.as_slice())?;
    }
    if let Some(ref uv2) = model.uv2 {
        writer.write_all(uv2.as_slice())?;
    }
    if let Some(ref normal) = model.normal {
        writer.write_all(normal.as_slice())?;
    }
    if let Some(ref color) = model.color
        && uses_vertex_color
    {
        writer.write_all(color.as_slice())?;
    }
    if let Some(ref blend0) = model.blend_indices {
        if let Some(node_maps) = node_maps {
            let mut new_blend = vec![0; 5];
            new_blend[0] = 8u8;
            new_blend[1] = blend0[1];
            new_blend[2] = blend0[2];
            new_blend[3] = blend0[3];
            new_blend[4] = blend0[4];
            for m in &blend0[5..] {
                let s = &node_maps.indices.elements[*m as usize];
                new_blend.write_u16::<LE>(s.index.0)?;
            }
            writer.write_all(new_blend.as_slice())?;
        } else {
            writer.write_all(blend0.as_slice())?;
        }
    }
    if let Some(ref blend0w) = model.blend_weights {
        writer.write_all(blend0w.as_slice())?;
    }
    if let Some(ref blend1w) = model.blend_weights_extra {
        writer.write_all(blend1w.as_slice())?;
    }
    if let Some(blend) = model.blendshape_index {
        writer.write_all(blend.as_slice())?;
    }
    if let Some(blend) = model.blendshape_position {
        writer.write_all(blend.as_slice())?;
    }
    Ok(())
}

pub fn process_model(
    model: RenderModel,
    indices: (usize, usize),
    modules: &mut [ModuleFile],
    string_mappings: &HashMap<i32, String>,
) -> Result<Vec<u8>> {
    let buffer = Vec::new();
    let mut writer = BufWriter::new(buffer);
    write_header(&mut writer, &model)?;
    write_regions(&mut writer, &model)?;
    write_bones(&mut writer, &model, string_mappings)?;
    write_markers(&mut writer, &model, string_mappings)?;
    write_bounding_boxes(&mut writer, &model.bounding_boxes)?;
    write_materials(&mut writer, &model)?;
    write_blendshape_boxes(&mut writer, &model.blend_shape_compression)?;

    let buffers = get_buffers(indices, modules, &Vec::new())?;
    let api_resource = model.resources.elements.first();

    for (section_index, section) in model.sections.elements.iter().enumerate() {
        let (region_name, permutation_name) = get_region_permutation(&model, section_index)?;
        write_section(
            section,
            api_resource,
            &mut writer,
            &buffers,
            Some(region_name),
            Some(permutation_name),
            model.node_maps.elements.get(section_index),
        )?;
    }
    Ok(writer.into_inner()?)
}

pub fn process_rtgo(
    model: RuntimeGeo,
    indices: (usize, usize),
    modules: &mut [ModuleFile],
    string_mappings: &HashMap<i32, String>,
) -> Result<Vec<u8>> {
    let buffer = Vec::new();
    let mut writer = BufWriter::new(buffer);

    write_header_rtgo(&mut writer, &model)?;
    write_markers_rtgo(&mut writer, &model, string_mappings)?;
    write_bounding_boxes(&mut writer, &model.bounding_boxes)?;

    for per_mesh in &model.per_mesh_data.elements {
        writer.write_i32::<LE>(per_mesh.name.0)?;
        writer.write_i16::<LE>(per_mesh.mesh_index.0)?;
        writer.write_all(&per_mesh.position.x.to_le_bytes())?;
        writer.write_all(&per_mesh.position.y.to_le_bytes())?;
        writer.write_all(&per_mesh.position.z.to_le_bytes())?;
    }

    let buffers = get_buffers(indices, modules, &Vec::new())?;
    let api_resource = model.mesh_resource_groups.elements.first();

    for (section_index, section) in model.sections.elements.iter().enumerate() {
        write_section(
            section,
            api_resource,
            &mut writer,
            &buffers,
            None,
            None,
            model.node_maps.elements.get(section_index),
        )?;
    }
    Ok(writer.into_inner()?)
}

pub fn process_particle(
    model: ParticleModel,
    indices: (usize, usize),
    modules: &mut [ModuleFile],
) -> Result<Vec<u8>> {
    let buffer = Vec::new();
    let mut writer = BufWriter::new(buffer);

    write_header_particle(&mut writer, &model)?;
    write_bounding_boxes(&mut writer, &model.bounding_boxes)?;

    let mut buffers = Vec::new();
    let api_resource = model.resources.elements.first();
    if let Some(api_resource) = api_resource {
        let elements = &api_resource.resource.data.vertex_buffers.elements;
        buffers = get_buffers(indices, modules, elements)?;
    }
    for section in model.sections.elements.iter() {
        write_section(
            section,
            api_resource,
            &mut writer,
            &buffers,
            None,
            None,
            None,
        )?;
    }
    Ok(writer.into_inner()?)
}
