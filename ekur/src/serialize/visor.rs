/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use anyhow::Result;
use serde::Serialize;
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use crate::definitions::{material_swatch::MaterialSwatchTag, visor::MaterialVisorSwatchTag};

#[derive(Debug, Default, Serialize)]
pub struct Color {
    pub top_color: (f32, f32, f32),
    pub mid_color: (f32, f32, f32),
    pub bot_color: (f32, f32, f32),
}

#[derive(Debug, Default, Serialize)]
pub struct Pattern {
    color_and_roughness_transform: (f32, f32),
    normal_texture_transform: (f32, f32),
    color_gradient_map: i32,
    roughness_white: f32,
    roughness_black: f32,
    normal_detail_map: i32,
    metallic: f32,
    scratch_color: (f32, f32, f32),
    scratch_roughness: f32,
    scratch_metallic: f32,
}

#[derive(Debug, Default, Serialize)]
pub struct VisorGlobals {
    pub patterns: HashMap<i32, Pattern>,
    pub colors: HashMap<i32, Color>,
}

pub fn process_visor(
    visor: &MaterialVisorSwatchTag,
    swatches: &HashMap<i32, MaterialSwatchTag>,
    save_path: &str,
) -> Result<()> {
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
    let path = PathBuf::from(format!("{save_path}/visor_data.json"));
    let file = File::create(path)?;
    let writer = BufWriter::new(file);
    serde_json::to_writer(writer, &globals)?;
    Ok(())
}
