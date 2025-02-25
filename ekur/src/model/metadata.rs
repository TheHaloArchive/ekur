/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::{
    definitions::{
        particle_model::ParticleModel,
        render_model::{BoundingBoxBlock, LodFlags, SectionLods},
        runtime_geo::RuntimeGeo,
    },
    model::bone::create_node,
};
use std::{
    collections::HashMap,
    fs::File,
    io::{BufWriter, Write},
};

use anyhow::Result;
use byteorder::{LE, WriteBytesExt};
use infinite_rs::tag::types::common_types::FieldBlock;

use crate::definitions::render_model::RenderModel;

const MAGIC: &str = "SURA";

pub(super) fn write_header(reader: &mut BufWriter<File>, model: &RenderModel) -> Result<()> {
    reader.write_all(MAGIC.as_bytes())?;
    reader.write_i32::<LE>(model.any_tag.internal_struct.tag_id)?;
    reader.write_u32::<LE>(model.regions.size)?;
    reader.write_u32::<LE>(model.nodes.size)?;
    reader.write_u32::<LE>(model.marker_groups.size)?;
    reader.write_u32::<LE>(model.materials.size)?;
    let section_size = model
        .sections
        .elements
        .iter()
        .filter(|x| {
            x.section_lods.elements[0]
                .lod_flags
                .0
                .contains(LodFlags::LOD0)
                && x.section_lods.elements[0].lod_has_shadow_proxies.0 != 1
        })
        .count();
    reader.write_u32::<LE>(section_size as u32)?;
    reader.write_u32::<LE>(model.bounding_boxes.size)?;
    Ok(())
}

pub(super) fn write_header_rtgo(reader: &mut BufWriter<File>, model: &RuntimeGeo) -> Result<()> {
    reader.write_all(MAGIC.as_bytes())?;
    reader.write_i32::<LE>(model.any_tag.internal_struct.tag_id)?;
    reader.write_u32::<LE>(0)?;
    reader.write_u32::<LE>(0)?;
    reader.write_u32::<LE>(model.markers.size)?;
    reader.write_u32::<LE>(0)?;
    let section_size = model
        .sections
        .elements
        .iter()
        .filter(|x| {
            x.section_lods.elements[0]
                .lod_flags
                .0
                .contains(LodFlags::LOD0)
                && x.section_lods.elements[0].lod_has_shadow_proxies.0 != 1
        })
        .count();
    reader.write_u32::<LE>(section_size as u32)?;
    reader.write_u32::<LE>(model.bounding_boxes.size)?;
    Ok(())
}

pub(super) fn write_header_particle(
    reader: &mut BufWriter<File>,
    model: &ParticleModel,
) -> Result<()> {
    reader.write_all(MAGIC.as_bytes())?;
    reader.write_i32::<LE>(model.any_tag.internal_struct.tag_id)?;
    reader.write_u32::<LE>(0)?;
    reader.write_u32::<LE>(0)?;
    reader.write_u32::<LE>(0)?;
    reader.write_u32::<LE>(0)?;
    let section_size = model
        .sections
        .elements
        .iter()
        .filter(|x| {
            x.section_lods.elements[0]
                .lod_flags
                .0
                .contains(LodFlags::LOD0)
                && x.section_lods.elements[0].lod_has_shadow_proxies.0 != 1
        })
        .count();
    reader.write_u32::<LE>(section_size as u32)?;
    reader.write_u32::<LE>(model.bounding_boxes.size)?;
    Ok(())
}

pub(super) fn write_regions(writer: &mut BufWriter<File>, model: &RenderModel) -> Result<()> {
    for region in &model.regions.elements {
        writer.write_i32::<LE>(region.name.0)?;
        writer.write_u32::<LE>(region.permutations.size)?;
        for permutation in &region.permutations.elements {
            writer.write_i32::<LE>(permutation.name.0)?;
            writer.write_u16::<LE>(permutation.section_count.0)?;
            writer.write_i16::<LE>(permutation.section_index.0)?;
        }
    }
    Ok(())
}

pub(super) fn write_bones(
    writer: &mut BufWriter<File>,
    model: &RenderModel,
    string_mappings: &HashMap<i32, String>,
) -> Result<()> {
    for node in &model.nodes.elements {
        let bone = create_node(node);
        let name = if string_mappings.contains_key(&bone.name) {
            string_mappings.get(&bone.name).unwrap().clone()
        } else {
            bone.name.to_string()
        };
        writer.write_u8(name.len() as u8)?;
        writer.write_all(name.as_bytes())?;
        writer.write_i32::<LE>(bone.parent_index)?;
        for row in &bone.rotation_matrix {
            for val in row {
                writer.write_f32::<LE>(*val)?;
            }
        }
        for row in &bone.transformation_matrix {
            for val in row {
                writer.write_f32::<LE>(*val)?;
            }
        }
        for row in &bone.world_transform {
            for val in row {
                writer.write_f32::<LE>(*val)?;
            }
        }
    }
    Ok(())
}

pub(super) fn write_markers(writer: &mut BufWriter<File>, model: &RenderModel) -> Result<()> {
    for marker in &model.marker_groups.elements {
        writer.write_i32::<LE>(marker.name.0)?;
        writer.write_u32::<LE>(marker.markers.size)?;
        for mark in &marker.markers.elements {
            writer.write_f32::<LE>(mark.translation.x)?;
            writer.write_f32::<LE>(mark.translation.y)?;
            writer.write_f32::<LE>(mark.translation.z)?;
            writer.write_f32::<LE>(mark.rotation.x)?;
            writer.write_f32::<LE>(mark.rotation.y)?;
            writer.write_f32::<LE>(mark.rotation.z)?;
            writer.write_f32::<LE>(mark.rotation.w)?;
            writer.write_i8(mark.region_index.0)?;
            writer.write_i32::<LE>(mark.permutation_index.0)?;
            writer.write_u8(mark.node_index.0)?;
        }
    }

    Ok(())
}

pub(super) fn write_markers_rtgo(writer: &mut BufWriter<File>, model: &RuntimeGeo) -> Result<()> {
    for marker in &model.markers.elements {
        writer.write_i32::<LE>(marker.name.0)?;
        writer.write_u32::<LE>(marker.markers.size)?;
        for mark in &marker.markers.elements {
            writer.write_f32::<LE>(mark.translation.x)?;
            writer.write_f32::<LE>(mark.translation.y)?;
            writer.write_f32::<LE>(mark.translation.z)?;
            writer.write_f32::<LE>(mark.rotation.x)?;
            writer.write_f32::<LE>(mark.rotation.y)?;
            writer.write_f32::<LE>(mark.rotation.z)?;
            writer.write_f32::<LE>(mark.rotation.w)?;
            writer.write_u8(0)?;
            writer.write_i32::<LE>(0)?;
            writer.write_u8(0)?;
        }
    }

    Ok(())
}

pub(super) fn write_bounding_boxes(
    writer: &mut BufWriter<File>,
    bounding_boxes: &FieldBlock<BoundingBoxBlock>,
) -> Result<()> {
    for bounding_box in &bounding_boxes.elements {
        writer.write_f32::<LE>(bounding_box.x_bounds.min)?;
        writer.write_f32::<LE>(bounding_box.x_bounds.max)?;
        writer.write_f32::<LE>(bounding_box.y_bounds.min)?;
        writer.write_f32::<LE>(bounding_box.y_bounds.max)?;
        writer.write_f32::<LE>(bounding_box.z_bounds.min)?;
        writer.write_f32::<LE>(bounding_box.z_bounds.max)?;
        writer.write_f32::<LE>(bounding_box.u_bounds.min)?;
        writer.write_f32::<LE>(bounding_box.u_bounds.max)?;
        writer.write_f32::<LE>(bounding_box.v_bounds.min)?;
        writer.write_f32::<LE>(bounding_box.v_bounds.max)?;
        writer.write_f32::<LE>(bounding_box.u_bounds_1.min)?;
        writer.write_f32::<LE>(bounding_box.u_bounds_1.max)?;
        writer.write_f32::<LE>(bounding_box.v_bounds_1.min)?;
        writer.write_f32::<LE>(bounding_box.v_bounds_1.max)?;
        writer.write_f32::<LE>(bounding_box.u_bounds_2.min)?;
        writer.write_f32::<LE>(bounding_box.u_bounds_2.max)?;
        writer.write_f32::<LE>(bounding_box.v_bounds_2.min)?;
        writer.write_f32::<LE>(bounding_box.v_bounds_2.max)?;
    }
    Ok(())
}

pub(super) fn write_materials(writer: &mut BufWriter<File>, model: &RenderModel) -> Result<()> {
    for m in &model.materials.elements {
        writer.write_i32::<LE>(m.material.global_id)?
    }
    Ok(())
}

pub(super) fn write_submeshes(writer: &mut BufWriter<File>, lod_data: &SectionLods) -> Result<()> {
    for submesh in lod_data.submeshes.elements.iter() {
        writer.write_i32::<LE>(submesh.index_start.0)?;
        writer.write_i32::<LE>(submesh.index_count.0)?;
        writer.write_u16::<LE>(submesh.vertex_count.0)?;
        writer.write_u16::<LE>(submesh.subset_count.0)?;
        writer.write_i16::<LE>(submesh.subset_index.0)?;
        writer.write_i16::<LE>(submesh.shader_index.0)?;
    }
    Ok(())
}
