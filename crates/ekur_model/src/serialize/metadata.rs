/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::buffers::bone::create_node;
use ekur_definitions::{
    particle_model::ParticleModel,
    render_model::{BlendShapeCompression, BoundingBoxBlock, LodFlags, RenderModel, SectionLods},
    runtime_geo::RuntimeGeo,
};

use anyhow::Result;
use byteorder::{LE, WriteBytesExt};
use infinite_rs::tag::types::common_types::FieldBlock;
use std::{collections::HashMap, io::Write};

const MAGIC: &str = "SURA";

pub(crate) fn write_header<R: Write>(writer: &mut R, model: &RenderModel) -> Result<()> {
    writer.write_all(MAGIC.as_bytes())?;
    writer.write_i32::<LE>(model.any_tag.internal_struct.tag_id)?;
    writer.write_u8(0)?;
    writer.write_u32::<LE>(model.regions.size)?;
    writer.write_u32::<LE>(model.nodes.size)?;
    writer.write_u32::<LE>(model.marker_groups.size)?;
    writer.write_u32::<LE>(model.materials.size)?;
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
    writer.write_u32::<LE>(section_size as u32)?;
    writer.write_u32::<LE>(model.bounding_boxes.size)?;
    writer.write_u32::<LE>(model.blend_shape_compression.size)?;
    Ok(())
}

pub(crate) fn write_header_rtgo<R: Write>(writer: &mut R, model: &RuntimeGeo) -> Result<()> {
    writer.write_all(MAGIC.as_bytes())?;
    writer.write_i32::<LE>(model.any_tag.internal_struct.tag_id)?;
    writer.write_u8(1)?;
    writer.write_u32::<LE>(0)?;
    writer.write_u32::<LE>(0)?;
    writer.write_u32::<LE>(model.markers.size)?;
    writer.write_u32::<LE>(0)?;
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
    writer.write_u32::<LE>(section_size as u32)?;
    writer.write_u32::<LE>(model.bounding_boxes.size)?;
    writer.write_u32::<LE>(0)?;
    writer.write_u32::<LE>(model.per_mesh_data.size)?;
    Ok(())
}

pub(crate) fn write_header_particle<R: Write>(writer: &mut R, model: &ParticleModel) -> Result<()> {
    writer.write_all(MAGIC.as_bytes())?;
    writer.write_i32::<LE>(model.any_tag.internal_struct.tag_id)?;
    writer.write_u8(0)?;
    writer.write_u32::<LE>(0)?;
    writer.write_u32::<LE>(0)?;
    writer.write_u32::<LE>(0)?;
    writer.write_u32::<LE>(0)?;
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
    writer.write_u32::<LE>(section_size as u32)?;
    writer.write_u32::<LE>(model.bounding_boxes.size)?;
    writer.write_u32::<LE>(0)?;
    Ok(())
}

pub(crate) fn write_regions<R: Write>(writer: &mut R, model: &RenderModel) -> Result<()> {
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

pub(crate) fn write_bones<R: Write>(
    writer: &mut R,
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

pub(crate) fn write_markers<R: Write>(
    writer: &mut R,
    model: &RenderModel,
    strings: &HashMap<i32, String>,
) -> Result<()> {
    for marker in &model.marker_groups.elements {
        let name = if strings.contains_key(&marker.name.0) {
            strings.get(&marker.name.0).unwrap().clone()
        } else {
            marker.name.0.to_string()
        };
        writer.write_u8(name.len() as u8)?;
        writer.write_all(name.as_bytes())?;
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

pub(crate) fn write_markers_rtgo<R: Write>(
    writer: &mut R,
    model: &RuntimeGeo,
    strings: &HashMap<i32, String>,
) -> Result<()> {
    for marker in &model.markers.elements {
        let name = if strings.contains_key(&marker.name.0) {
            strings.get(&marker.name.0).unwrap().clone()
        } else {
            marker.name.0.to_string()
        };
        writer.write_u8(name.len() as u8)?;
        writer.write_all(name.as_bytes())?;
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

pub(crate) fn write_bounding_boxes<R: Write>(
    writer: &mut R,
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

pub(crate) fn write_blendshape_boxes<R: Write>(
    writer: &mut R,
    bounding_boxes: &FieldBlock<BlendShapeCompression>,
) -> Result<()> {
    for bounding_box in &bounding_boxes.elements {
        writer.write_f32::<LE>(bounding_box.position_scale.x)?;
        writer.write_f32::<LE>(bounding_box.position_scale.y)?;
        writer.write_f32::<LE>(bounding_box.position_scale.z)?;
        writer.write_f32::<LE>(bounding_box.position_offset.x)?;
        writer.write_f32::<LE>(bounding_box.position_offset.y)?;
        writer.write_f32::<LE>(bounding_box.position_offset.z)?;
        writer.write_f32::<LE>(bounding_box.normal_scale.x)?;
        writer.write_f32::<LE>(bounding_box.normal_scale.y)?;
        writer.write_f32::<LE>(bounding_box.normal_scale.z)?;
        writer.write_f32::<LE>(bounding_box.normal_offset.x)?;
        writer.write_f32::<LE>(bounding_box.normal_offset.y)?;
        writer.write_f32::<LE>(bounding_box.normal_offset.z)?;
    }
    Ok(())
}

pub(crate) fn write_materials<R: Write>(writer: &mut R, model: &RenderModel) -> Result<()> {
    for m in &model.materials.elements {
        writer.write_i32::<LE>(m.material.global_id)?
    }
    Ok(())
}

pub(crate) fn write_submeshes<R: Write>(writer: &mut R, lod_data: &SectionLods) -> Result<()> {
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
