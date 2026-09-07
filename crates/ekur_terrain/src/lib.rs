/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
pub mod tiles;

use crate::tiles::TileStore;
use ekur_definitions::runtime_terrain::RuntimeTerrain;

use anyhow::Result;
use image::{ImageBuffer, ImageFormat, Rgba};
use infinite_rs::ModuleFile;
use serde::Serialize;
use std::{
    collections::{BTreeMap, HashSet},
    path::Path,
};

const SURFACE_BORDER: usize = 2;

#[derive(Default, Debug, Serialize)]
pub struct MaterialLayerTexture {
    pub bitmap: i32,
    pub uv_scale: [f32; 2],
}

#[derive(Default, Debug, Serialize)]
pub struct MaterialLayerSurface {
    pub detail_scale: f32,
    pub height_blend_width: f32,
    pub roughness_scale: f32,
    pub roughness_bias: f32,
    pub metallic_scale: f32,
    pub metallic_bias: f32,
    pub color_blend_mode: u32,
    pub normal_blend_mode: u32,
    pub nonmetal_f0: f32,
    pub normal_intensity: f32,
    pub top_color: [f32; 3],
    pub middle_color: [f32; 3],
    pub bottom_or_tint_color: [f32; 3],
    pub control_uv_transform: [f32; 4],
    pub color_uv_transform: [f32; 4],
    pub normal_uv_transform: [f32; 4],
    pub surface_parameters: [f32; 4],
    pub anti_tiling_offset: f32,
    pub anti_tiling_power: f32,
    pub anti_tiling_flags: u32,
}

#[derive(Default, Debug, Serialize)]
pub struct MaterialLayer {
    pub id: i32,
    pub color: Option<MaterialLayerTexture>,
    pub normal: Option<MaterialLayerTexture>,
    pub control: Option<MaterialLayerTexture>,
    pub surface: Option<MaterialLayerSurface>,
}

#[derive(Default, Debug, Serialize)]
pub struct Terrain {
    pub global_id: i32,
    pub name: String,
    pub heightfield: String,
    pub position: [f32; 3],
    pub size: [f32; 3],
    pub grid: [usize; 2],
    pub level_count: u16,
    pub leaf_node_edge_count: usize,
    pub active_leaf_indices: Vec<usize>,
    pub surfaces: Vec<String>,
    pub render_material: i32,
    pub masks_composite_material: i32,
    pub material_layers: Vec<MaterialLayer>,
}

fn place(
    heights: &mut [u16],
    tile: &[u16],
    leaf: usize,
    leaf_side: usize,
    edge: usize,
    width: usize,
) {
    let step = edge - 1;
    let (leaf_row, leaf_column) = (leaf / leaf_side, leaf % leaf_side);
    for row in 0..edge {
        for column in 0..edge {
            heights[(leaf_row * step + row) * width + leaf_column * step + column] =
                tile[(edge - 1 - row) * edge + column];
        }
    }
}

fn flat_height_tile(min: f32, max: f32, edge: usize) -> Option<Vec<u16>> {
    if !(max > 0.0 && max >= min) {
        return None;
    }
    let value = ((min + max) * 0.5 * 65535.0).round().clamp(0.0, 65535.0) as u16;
    Some(vec![value; edge * edge])
}

fn place_surface(
    canvas: &mut [u8],
    tile: &[u8],
    tile_edge: usize,
    leaf: usize,
    leaf_side: usize,
    inner: usize,
) {
    let canvas_width = leaf_side * inner;
    let (leaf_row, leaf_column) = (leaf / leaf_side, leaf % leaf_side);
    for row in 0..inner {
        for column in 0..inner {
            let src =
                ((SURFACE_BORDER + inner - 1 - row) * tile_edge + SURFACE_BORDER + column) * 4;
            let dst = ((leaf_row * inner + row) * canvas_width + leaf_column * inner + column) * 4;
            canvas[dst..dst + 4].copy_from_slice(&tile[src..src + 4]);
        }
    }
}

fn surface_key(output_id: Option<i32>, fallback: &str) -> String {
    match output_id {
        Some(1) => "macro_normal".into(),
        Some(2) => "macro_color".into(),
        Some(3) => "wetness".into(),
        Some(n) if n >= 4 => format!("mask_{}", n - 4),
        _ => fallback.into(),
    }
}

const MATERIAL_LAYER_DATA_STRIDE: usize = 208;

fn read_f32(data: &[u8], offset: usize) -> f32 {
    data.get(offset..offset + 4)
        .map_or(0.0, |b| f32::from_le_bytes(b.try_into().unwrap()))
}

fn read_f32_array<const N: usize>(data: &[u8], offset: usize) -> [f32; N] {
    std::array::from_fn(|i| read_f32(data, offset + i * 4))
}

fn read_u32(data: &[u8], offset: usize) -> u32 {
    data.get(offset..offset + 4)
        .map_or(0, |b| u32::from_le_bytes(b.try_into().unwrap()))
}

fn material_layer_surface(data: &[u8], index: usize) -> Option<MaterialLayerSurface> {
    let record = data.get(index * MATERIAL_LAYER_DATA_STRIDE..)?;
    let record = record.get(..MATERIAL_LAYER_DATA_STRIDE)?;
    Some(MaterialLayerSurface {
        detail_scale: read_f32(record, 12),
        height_blend_width: read_f32(record, 72),
        roughness_scale: read_f32(record, 56),
        roughness_bias: read_f32(record, 60),
        metallic_scale: read_f32(record, 48),
        metallic_bias: read_f32(record, 52),
        color_blend_mode: read_u32(record, 80),
        normal_blend_mode: read_u32(record, 88),
        nonmetal_f0: read_f32(record, 172),
        normal_intensity: read_f32(record, 76),
        top_color: read_f32_array(record, 96),
        middle_color: read_f32_array(record, 112),
        bottom_or_tint_color: read_f32_array(record, 160),
        control_uv_transform: read_f32_array(record, 32),
        color_uv_transform: read_f32_array(record, 128),
        normal_uv_transform: read_f32_array(record, 144),
        surface_parameters: read_f32_array(record, 176),
        anti_tiling_offset: read_f32(record, 192),
        anti_tiling_power: read_f32(record, 196),
        anti_tiling_flags: read_u32(record, 204),
    })
}

fn material_layers(terrain: &RuntimeTerrain) -> Vec<MaterialLayer> {
    let bitmap_refs = &terrain.material_layer_bitmap_references.elements;
    terrain
        .material_layer_ids
        .elements
        .iter()
        .enumerate()
        .map(|(index, layer)| {
            let mut slots = layer.output_bitmap_references.elements.iter().map(|r| {
                let index = usize::try_from(r.bitmap_reference_index.0).ok()?;
                let bitmap = bitmap_refs.get(index)?.bitmap_reference.global_id;
                (bitmap != -1).then_some(MaterialLayerTexture {
                    bitmap,
                    uv_scale: [r.uv_scale.x, r.uv_scale.y],
                })
            });
            MaterialLayer {
                id: layer.id.0,
                color: slots.next().flatten(),
                normal: slots.next().flatten(),
                control: slots.next().flatten(),
                surface: material_layer_surface(&terrain.material_layer_data.data, index),
            }
        })
        .collect()
}

pub fn process_terrain(
    terrain: &RuntimeTerrain,
    modules: &mut [ModuleFile],
    name: &str,
    save_path: &Path,
) -> Result<Option<(Terrain, Vec<u16>)>> {
    let Some(mut store) = TileStore::open(terrain.bitmap.global_id, modules)? else {
        return Ok(None);
    };
    let Some(edge) = store.height_edge() else {
        return Ok(None);
    };

    let nodes = terrain.quad_tree_nodes.elements.len();
    let leaves = (3 * nodes + 1) / 4;
    let leaf_side = (leaves as f64).sqrt() as usize;
    let first_leaf = nodes - leaves;
    if leaf_side == 0 {
        return Ok(None);
    }

    let node_tile: Vec<Option<u32>> = terrain
        .quad_tree_nodes
        .elements
        .iter()
        .map(|node| {
            node.input_bitmap_indices
                .elements
                .iter()
                .map(|tile| tile.index.0)
                .find(|&id| store.is_height(id))
        })
        .collect();

    let step = edge - 1;
    let width = leaf_side * step + 1;
    let mut heights = vec![0u16; width * width];
    let mut active_leaf_indices = Vec::new();
    let mut surfaces: BTreeMap<String, (usize, Vec<u8>)> = BTreeMap::new();

    for leaf in 0..leaf_side * leaf_side {
        let node = first_leaf + leaf;
        let Some(quad_node) = terrain.quad_tree_nodes.elements.get(node) else {
            continue;
        };
        let tile = match node_tile[node] {
            Some(id) => store.height_tile(id, modules)?,
            None => None,
        };
        let tile =
            tile.or_else(|| flat_height_tile(quad_node.min_height.0, quad_node.max_height.0, edge));
        let Some(tile) = tile else {
            continue;
        };
        place(&mut heights, &tile, leaf, leaf_side, edge, width);
        active_leaf_indices.push(leaf);

        if quad_node.input_bitmap_indices.elements.is_empty() {
            continue;
        }
        let mut seen_keys = HashSet::new();
        for bitmap in &quad_node.input_bitmap_indices.elements {
            let id = bitmap.index.0;
            if node_tile[node] == Some(id) {
                continue;
            }
            let Some((pixels, tile_width, tile_height, slug)) = store.surface_tile(id, modules)?
            else {
                continue;
            };
            let tile_edge = tile_width as usize;
            if tile_width != tile_height || tile_edge <= SURFACE_BORDER * 2 {
                continue;
            }

            let id_signed = i32::try_from(id).unwrap_or(-1);
            let output_id = quad_node
                .input_texture_data
                .elements
                .iter()
                .rev()
                .find(|entry| entry.bitmap_index.0 == id_signed)
                .map(|entry| entry.output_id.0);
            let key = surface_key(output_id, &slug);
            if !seen_keys.insert(key.clone()) {
                continue;
            }

            let inner = tile_edge - SURFACE_BORDER * 2;
            let canvas_width = leaf_side * inner;
            let (stored_edge, canvas) = surfaces
                .entry(key)
                .or_insert_with(|| (tile_edge, vec![0u8; canvas_width * canvas_width * 4]));
            if *stored_edge != tile_edge {
                continue;
            }
            place_surface(canvas, &pixels, tile_edge, leaf, leaf_side, inner);
        }
    }

    let mut surface_names = Vec::new();
    for (key, (tile_edge, canvas)) in surfaces {
        let canvas_width = (leaf_side * (tile_edge - SURFACE_BORDER * 2)) as u32;
        let Some(image) = ImageBuffer::<Rgba<u8>, _>::from_raw(canvas_width, canvas_width, canvas)
        else {
            continue;
        };
        let file_name = format!("{name}_{key}.png");
        image.save_with_format(save_path.join(&file_name), ImageFormat::Png)?;
        surface_names.push(file_name);
    }

    let record = Terrain {
        global_id: terrain.any_tag.internal_struct.tag_id,
        name: name.to_string(),
        heightfield: format!("{name}.r16"),
        position: [
            terrain.quad_tree_position.x,
            terrain.quad_tree_position.y,
            terrain.quad_tree_position.z,
        ],
        size: [
            terrain.quad_tree_size.x,
            terrain.quad_tree_size.y,
            terrain.quad_tree_size.z,
        ],
        grid: [width, width],
        level_count: terrain.quad_tree_level_count.0,
        leaf_node_edge_count: leaf_side,
        active_leaf_indices,
        surfaces: surface_names,
        render_material: terrain.render_material.global_id,
        masks_composite_material: terrain.masks_composite_material.global_id,
        material_layers: material_layers(terrain),
    };
    Ok(Some((record, heights)))
}
