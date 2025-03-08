/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::definitions::render_model::{
    MeshResourceGroupBlock, NodeMapBlock, SectionBlock, VertexBufferUsage,
};
use crate::{
    definitions::{particle_model::ParticleModel, render_model::MeshFlags},
    model::utils::{data_exists, get_buffers},
};
use std::{
    collections::HashMap,
    fs::File,
    io::{BufWriter, Write},
    path::PathBuf,
};

use anyhow::Result;
use byteorder::{LE, WriteBytesExt};
use infinite_rs::ModuleFile;

use crate::definitions::{
    render_model::{LodFlags, RenderModel, VertexBufferUsage as VU},
    runtime_geo::RuntimeGeo,
};

use super::{
    index_buffer::write_index_buffer,
    metadata::{
        write_bones, write_bounding_boxes, write_header, write_header_particle, write_header_rtgo,
        write_markers, write_markers_rtgo, write_materials, write_regions, write_submeshes,
    },
    vertex_buffer::get_vertex_buffer,
};

fn get_region_permutation(model: &RenderModel, section_index: usize) -> Result<(i32, i32)> {
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
pub(super) struct VertexBuffers {
    pub(super) position: Option<Vec<u8>>,
    pub(super) uv0: Option<Vec<u8>>,
    pub(super) uv1: Option<Vec<u8>>,
    pub(super) uv2: Option<Vec<u8>>,
    pub(super) normal: Option<Vec<u8>>,
    pub(super) color: Option<Vec<u8>>,
    pub(super) blend_indices: Option<Vec<u8>>,
    pub(super) blend_weights: Option<Vec<u8>>,
    pub(super) blend_weights_extra: Option<Vec<u8>>,
}

fn write_section(
    section: &SectionBlock,
    api_resource: Option<&MeshResourceGroupBlock>,
    writer: &mut BufWriter<File>,
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
            .find(|x| x.vertex_buffer_usage.0 == VertexBufferUsage::Position)
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
    if let Some(ref color) = model.color {
        if uses_vertex_color {
            writer.write_all(color.as_slice())?;
        }
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
    Ok(())
}

pub fn process_models(
    models: &HashMap<(usize, usize, i32), RenderModel>,
    runtime_geo: &HashMap<(usize, usize, i32), RuntimeGeo>,
    particle_models: &HashMap<(usize, usize, i32), ParticleModel>,
    save_path: &str,
    modules: &mut [ModuleFile],
    string_mappings: &HashMap<i32, String>,
) -> Result<()> {
    for model in models {
        let mut path = PathBuf::from(format!("{save_path}/models/"));
        path.push(model.0.2.to_string());
        path.set_extension("ekur");
        let file = File::create(path)?;
        let mut writer = BufWriter::new(file);

        write_header(&mut writer, model.1)?;
        write_regions(&mut writer, model.1)?;
        write_bones(&mut writer, model.1, string_mappings)?;
        write_markers(&mut writer, model.1, string_mappings)?;
        write_bounding_boxes(&mut writer, &model.1.bounding_boxes)?;
        write_materials(&mut writer, model.1)?;

        let buffers = get_buffers(model, modules, &Vec::new())?;
        let api_resource = model.1.resources.elements.first();
        for (section_index, section) in model.1.sections.elements.iter().enumerate() {
            let (region_name, permutation_name) = get_region_permutation(model.1, section_index)?;
            write_section(
                section,
                api_resource,
                &mut writer,
                &buffers,
                Some(region_name),
                Some(permutation_name),
                model.1.node_maps.elements.get(section_index),
            )?;
        }
    }

    for model in runtime_geo {
        let mut path = PathBuf::from(format!("{save_path}/runtime_geo/"));
        path.push(model.0.2.to_string());
        path.set_extension("ekur");
        let file = File::create(path)?;
        let mut writer = BufWriter::new(file);

        write_header_rtgo(&mut writer, model.1)?;
        write_markers_rtgo(&mut writer, model.1, string_mappings)?;
        write_bounding_boxes(&mut writer, &model.1.bounding_boxes)?;

        let buffers = get_buffers(model, modules, &Vec::new())?;
        let api_resource = model.1.mesh_resource_groups.elements.first();
        for (section_index, section) in model.1.sections.elements.iter().enumerate() {
            write_section(
                section,
                api_resource,
                &mut writer,
                &buffers,
                None,
                None,
                model.1.node_maps.elements.get(section_index),
            )?;
        }
    }

    for model in particle_models {
        let mut path = PathBuf::from(format!("{save_path}/particle_models/"));
        path.push(model.0.2.to_string());
        path.set_extension("ekur");
        let file = File::create(path)?;
        let mut writer = BufWriter::new(file);

        write_header_particle(&mut writer, model.1)?;
        write_bounding_boxes(&mut writer, &model.1.bounding_boxes)?;
        let mut buffers = Vec::new();
        let api_resource = model.1.resources.elements.first();
        if let Some(api_resource) = api_resource {
            let elements = &api_resource.resource.data.vertex_buffers.elements;
            buffers = get_buffers(model, modules, elements)?;
        }
        for section in model.1.sections.elements.iter() {
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
    }
    Ok(())
}
