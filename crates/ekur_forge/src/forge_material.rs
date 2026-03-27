/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::{ForgeLayer, ForgeMaterials};
use ekur_coating::CommonLayer;
use ekur_definitions::{
    forge_globals::ForgeGlobals, material_palette::MaterialPaletteTag,
    material_swatch::MaterialSwatchTag,
};

use anyhow::Result;
use std::collections::HashMap;

pub fn process_forge_materials(
    palette: &MaterialPaletteTag,
    swatches: &HashMap<i32, MaterialSwatchTag>,
    strings: &HashMap<i32, String>,
    globals: &ForgeGlobals,
) -> Result<ForgeMaterials> {
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
    Ok(materials)
}
