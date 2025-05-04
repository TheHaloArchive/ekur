/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;
use serde::Serialize;

use crate::definitions::{
    forge_globals::ForgeGlobals, material_palette::MaterialPaletteTag,
    material_swatch::MaterialSwatchTag,
};

use super::common_coating::CommonLayer;

#[derive(Debug, Default, Serialize)]
pub struct ForgeLayer {
    name: i32,
    layer: CommonLayer,
}

#[derive(Debug, Default, Serialize)]
pub struct ForgeMaterials {
    layers: HashMap<String, ForgeLayer>,
    colors: Vec<(f32, f32, f32)>,
}

pub fn process_forge_materials(
    palette: &MaterialPaletteTag,
    swatches: &HashMap<i32, MaterialSwatchTag>,
    strings: &HashMap<i32, String>,
    globals: &ForgeGlobals,
    save_path: &str,
) -> Result<()> {
    let mut materials = ForgeMaterials::default();
    for pal in &palette.swatches.elements {
        let swatch = swatches.get(&pal.swatch.global_id);
        let Some(swatch) = swatch else { continue };
        let layer = CommonLayer::from_material(swatch, pal, 0);
        let forge_layer = ForgeLayer {
            name: pal.name.0,
            layer,
        };
        let name = strings
            .get(&pal.notes.0)
            .unwrap_or(&pal.notes.0.to_string())
            .clone();
        materials.layers.insert(name, forge_layer);
    }
    for color in &globals.colors.elements {
        materials
            .colors
            .push((color.color.r, color.color.g, color.color.b));
    }
    let path = PathBuf::from(format!("{save_path}/forge_materials.json"));
    let file = File::create(path)?;
    let writer = BufWriter::new(file);
    serde_json::to_writer(writer, &materials)?;
    Ok(())
}
