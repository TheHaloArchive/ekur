/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::{Color, Pattern, VisorGlobals};
use ekur_definitions::{material_swatch::MaterialSwatchTag, visor::MaterialVisorSwatchTag};

use anyhow::Result;
use std::collections::HashMap;

pub fn process_visor(
    visor: &MaterialVisorSwatchTag,
    swatches: &HashMap<i32, MaterialSwatchTag>,
) -> Result<VisorGlobals> {
    let mut globals = VisorGlobals::default();
    for pattern in &visor.pattern_variants.elements {
        let swatch = swatches.get(&pattern.reference.global_id).unwrap();
        let pat = Pattern {
            color_and_roughness_transform: (
                swatch.color_and_roughness_texture_transform.x,
                swatch.color_and_roughness_texture_transform.y,
            ),
            normal_texture_transform: (
                swatch.normal_texture_transform.x,
                swatch.normal_texture_transform.y,
            ),
            color_gradient_map: swatch.color_gradient_map.global_id,
            roughness_white: swatch.roughness_white.0,
            roughness_black: swatch.roughness_black.0,
            normal_detail_map: swatch.normal_detail_map.global_id,
            metallic: swatch.metallic.0,
            scratch_color: (
                swatch.scratch_color.r,
                swatch.scratch_color.g,
                swatch.scratch_color.b,
            ),
            scratch_roughness: swatch.scratch_roughness.0,
            scratch_metallic: swatch.scratch_metallic.0,
        };
        globals.patterns.insert(pattern.name.0, pat);
    }
    for color in &visor.color_variants.elements {
        let col = Color {
            top_color: (color.top_color.r, color.top_color.g, color.top_color.b),
            mid_color: (color.mid_color.r, color.mid_color.g, color.mid_color.b),
            bot_color: (color.bot_color.r, color.bot_color.g, color.bot_color.b),
        };
        globals.colors.insert(color.name.0, col);
    }
    Ok(globals)
}
