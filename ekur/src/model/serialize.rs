/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::{
    collections::HashMap,
    fs::File,
    io::{BufWriter, Write},
    path::PathBuf,
};

use anyhow::Result;
use byteorder::{WriteBytesExt, LE};
use infinite_rs::{module::file::TagStructure, ModuleFile};

use crate::definitions::{
    render_model::{LodFlags, RenderModel, VertexBufferUsage as VU},
    runtime_geo::RuntimeGeo,
};

use super::{
    index_buffer::write_index_buffer,
    metadata::{
        write_bones, write_bounding_boxes, write_header, write_header_rtgo, write_markers,
        write_markers_rtgo, write_materials, write_regions, write_submeshes, write_submeshes_rtgo,
    },
    vertex_buffer::{data_exists, get_vertex_buffer},
};

fn get_buffers<T: TagStructure>(
    model: (&(usize, usize, i32), &T),
    modules: &mut [ModuleFile],
) -> Result<Vec<Vec<u8>>> {
    let module = &mut modules[model.0 .0];
    let tag = &module.files[model.0 .1];
    let mut buffers = Vec::with_capacity(tag.resource_count as usize);
    let resources = module.resource_indices
        [tag.resource_index as usize..tag.resource_index as usize + tag.resource_count as usize]
        .to_vec();
    for resource in resources {
        let tag_thing = module.read_tag(resource)?;
        if let Some(tag_thing) = tag_thing {
            buffers.push(tag_thing.get_raw_data(true)?);
        }
    }
    Ok(buffers)
}

fn get_region_permutation(model: &RenderModel, section_index: usize) -> Result<(i32, i32)> {
    let mut region_name = 0;
    let mut permutation_name = 0;
    let region = model.regions.elements.iter().find(|x| {
        x.permutations
            .elements
            .iter()
            .any(|y| y.section_index.0 as usize == section_index)
    });
    if let Some(region) = region {
        region_name = region.name.0;
        let permutation = region
            .permutations
            .elements
            .iter()
            .find(|x| x.section_index.0 as usize == section_index);
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

pub fn process_models(
    models: &HashMap<(usize, usize, i32), RenderModel>,
    runtime_geo: &HashMap<(usize, usize, i32), RuntimeGeo>,
    save_path: &str,
    modules: &mut [ModuleFile],
) -> Result<()> {
    for model in models {
        let mut path = PathBuf::from(format!("{save_path}/models/"));
        path.push(model.0 .2.to_string());
        path.set_extension("ekur");
        let file = File::create(path)?;
        let mut writer = BufWriter::new(file);

        write_header(&mut writer, model.1)?;
        write_regions(&mut writer, model.1)?;
        write_bones(&mut writer, model.1)?;
        write_markers(&mut writer, model.1)?;
        write_bounding_boxes(&mut writer, &model.1.bounding_boxes)?;
        write_materials(&mut writer, model.1)?;

        let buffers = get_buffers(model, modules)?;
        let api_resource = model.1.resources.elements.first();
        for (section_index, section) in model.1.sections.elements.iter().enumerate() {
            let (region_name, permutation_name) = get_region_permutation(model.1, section_index)?;
            let lod_data = &section.section_lods.elements[0];
            if lod_data.lod_has_shadow_proxies.0 == 1 {
                continue;
            }
            if !lod_data.lod_flags.0.contains(LodFlags::LOD0) {
                continue;
            }

            writer.write_i32::<LE>(region_name)?;
            writer.write_i32::<LE>(permutation_name)?;
            writer.write_u32::<LE>(lod_data.submeshes.size)?;
            writer.write_u8(section.node_index.0)?;
            writer.write_u8(section.vertex_type.0.clone().into())?;
            writer.write_i8(section.use_dual_quat.0)?;
            write_submeshes(&mut writer, lod_data)?;
            write_index_buffer(&mut writer, api_resource, lod_data, &buffers)?;

            data_exists(lod_data, api_resource, &mut writer, VU::Position)?;
            data_exists(lod_data, api_resource, &mut writer, VU::UV0)?;
            data_exists(lod_data, api_resource, &mut writer, VU::UV1)?;
            data_exists(lod_data, api_resource, &mut writer, VU::UV2)?;
            data_exists(lod_data, api_resource, &mut writer, VU::Normal)?;
            data_exists(lod_data, api_resource, &mut writer, VU::Color)?;
            data_exists(lod_data, api_resource, &mut writer, VU::BlendIndices0)?;
            data_exists(lod_data, api_resource, &mut writer, VU::BlendWeights0)?;
            data_exists(lod_data, api_resource, &mut writer, VU::BlendWeights1)?;

            let mut model = VertexBuffers::default();
            get_vertex_buffer(api_resource, lod_data, &buffers, &mut model)?;

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
                writer.write_all(color.as_slice())?;
            }
            if let Some(ref blend0) = model.blend_indices {
                writer.write_all(blend0.as_slice())?;
            }
            if let Some(ref blend0w) = model.blend_weights {
                writer.write_all(blend0w.as_slice())?;
            }
            if let Some(ref blend1w) = model.blend_weights_extra {
                writer.write_all(blend1w.as_slice())?;
            }
        }
    }

    for model in runtime_geo {
        let mut path = PathBuf::from(format!("{save_path}/runtime_geo/"));
        path.push(model.0 .2.to_string());
        path.set_extension("ekur");
        let file = File::create(path)?;
        let mut writer = BufWriter::new(file);

        write_header_rtgo(&mut writer, model.1)?;
        write_markers_rtgo(&mut writer, model.1)?;
        write_bounding_boxes(&mut writer, &model.1.bounding_boxes)?;

        let buffers = get_buffers(model, modules)?;
        let api_resource = model.1.mesh_resource_groups.elements.first();
        for section in model.1.sections.elements.iter() {
            let lod_data = &section.section_lods.elements[0];
            if lod_data.lod_has_shadow_proxies.0 == 1 {
                continue;
            }
            if !lod_data.lod_flags.0.contains(LodFlags::LOD0) {
                continue;
            }

            writer.write_i32::<LE>(0)?;
            writer.write_i32::<LE>(0)?;
            writer.write_u32::<LE>(lod_data.submeshes.size)?;
            writer.write_u8(section.node_index.0)?;
            writer.write_u8(section.vertex_type.0.clone().into())?;
            writer.write_i8(section.use_dual_quat.0)?;
            write_submeshes_rtgo(&mut writer, lod_data)?;
            write_index_buffer(&mut writer, api_resource, lod_data, &buffers)?;

            data_exists(lod_data, api_resource, &mut writer, VU::Position)?;
            data_exists(lod_data, api_resource, &mut writer, VU::UV0)?;
            data_exists(lod_data, api_resource, &mut writer, VU::UV1)?;
            data_exists(lod_data, api_resource, &mut writer, VU::UV2)?;
            data_exists(lod_data, api_resource, &mut writer, VU::Normal)?;
            data_exists(lod_data, api_resource, &mut writer, VU::Color)?;
            data_exists(lod_data, api_resource, &mut writer, VU::BlendIndices0)?;
            data_exists(lod_data, api_resource, &mut writer, VU::BlendWeights0)?;
            data_exists(lod_data, api_resource, &mut writer, VU::BlendWeights1)?;

            let mut model = VertexBuffers::default();
            get_vertex_buffer(api_resource, lod_data, &buffers, &mut model)?;

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
                writer.write_all(color.as_slice())?;
            }
        }
    }

    Ok(())
}
