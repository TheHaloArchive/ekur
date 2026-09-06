/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
pub mod tiles;

use crate::tiles::TileStore;
use ekur_definitions::runtime_terrain::RuntimeTerrain;

use anyhow::Result;
use infinite_rs::ModuleFile;
use serde::Serialize;

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

pub fn process_terrain(
    terrain: &RuntimeTerrain,
    modules: &mut [ModuleFile],
    name: &str,
) -> Result<Option<(Terrain, Vec<u16>)>> {
    let Some(store) = TileStore::open(terrain.bitmap.global_id, modules)? else {
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

    for leaf in 0..leaf_side * leaf_side {
        let node = first_leaf + leaf;
        let Some(quad_node) = terrain.quad_tree_nodes.elements.get(node) else {
            continue;
        };
        if quad_node.input_bitmap_indices.elements.is_empty() {
            continue;
        }
        let tile = match node_tile[node] {
            Some(id) => store.height_tile(id, modules)?,
            None => None,
        };
        let Some(tile) = tile else {
            continue;
        };
        place(&mut heights, &tile, leaf, leaf_side, edge, width);
        active_leaf_indices.push(leaf);
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
    };
    Ok(Some((record, heights)))
}
