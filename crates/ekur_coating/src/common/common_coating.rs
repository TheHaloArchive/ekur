/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::{CoatingGlobalEntries, CoatingGlobalEntry, CommonLayer};
use ekur_definitions::{
    coating_globals::CoatingGlobalsTag,
    coating_swatch::CoatingSwatchPODTag,
    material_palette::{MaterialRoughnessOverride, MaterialSwatchEntry},
    material_swatch::{MaterialColorVariant, MaterialSwatchTag},
    runtime_style::{CoatingPaletteInfo, OverrideColorsEnum},
};

use anyhow::Result;
use std::collections::HashMap;

const DEFAULT_NORMAL: i32 = 10070;
const DEFAULT_GRADIENT: i32 = 15173;

pub fn get_color(
    flag: &OverrideColorsEnum,
    swatch: &CoatingSwatchPODTag,
    info: &CoatingPaletteInfo,
) -> [(f32, f32, f32); 3] {
    match flag {
        OverrideColorsEnum::UseDefaultColors => [
            (
                swatch.gradient_top_color.r,
                swatch.gradient_top_color.g,
                swatch.gradient_top_color.b,
            ),
            (
                swatch.gradient_mid_color.r,
                swatch.gradient_mid_color.g,
                swatch.gradient_mid_color.b,
            ),
            (
                swatch.gradient_bot_color.r,
                swatch.gradient_bot_color.g,
                swatch.gradient_bot_color.b,
            ),
        ],
        OverrideColorsEnum::OverrideColors => [
            (
                info.gradient_top_color.r,
                info.gradient_top_color.g,
                info.gradient_top_color.b,
            ),
            (
                info.gradient_mid_color.r,
                info.gradient_mid_color.g,
                info.gradient_mid_color.b,
            ),
            (
                info.gradient_bot_color.r,
                info.gradient_bot_color.g,
                info.gradient_bot_color.b,
            ),
        ],
    }
}

impl CommonLayer {
    pub fn from_material(
        swatch: &MaterialSwatchTag,
        palette_swatch: &MaterialSwatchEntry,
        index: i32,
    ) -> Self {
        let mut disabled = false;
        let mut color = &MaterialColorVariant::default();
        let color_thing = swatch
            .color_variants
            .elements
            .iter()
            .find(|x| x.name.0 == palette_swatch.color.0);
        if let Some(color_thing) = color_thing {
            color = color_thing
        } else {
            disabled = true;
        }
        if (swatch.normal_detail_map.global_id == DEFAULT_NORMAL)
            && (swatch.color_gradient_map.global_id == DEFAULT_GRADIENT)
        {
            disabled = true
        }

        Self {
            index,
            disabled,
            gradient_transform: (
                swatch.color_and_roughness_texture_transform.x,
                swatch.color_and_roughness_texture_transform.y,
            ),
            normal_transform: (
                swatch.normal_texture_transform.x,
                swatch.normal_texture_transform.y,
            ),
            gradient_bitmap: swatch.color_gradient_map.global_id,
            normal_bitmap: swatch.normal_detail_map.global_id,
            roughness: match palette_swatch.roughness_override.0 {
                MaterialRoughnessOverride::Neg100 => 0.0,
                MaterialRoughnessOverride::Neg75 => 1.0,
                MaterialRoughnessOverride::Neg50 => 2.0,
                MaterialRoughnessOverride::Neg25 => 3.0,
                MaterialRoughnessOverride::None => 4.0,
                MaterialRoughnessOverride::Pos25 => 5.0,
                MaterialRoughnessOverride::Pos50 => 6.0,
                MaterialRoughnessOverride::Pos75 => 7.0,
                MaterialRoughnessOverride::Pos100 => 8.0,
            },
            roughness_black: swatch.roughness_black.0,
            roughness_white: swatch.roughness_white.0,
            metallic: swatch.metallic.0,
            emissive_amount: (palette_swatch.emissive_amount.0
                + palette_swatch.emissive_intensity.0),
            top_color: (
                color.gradient_top_color.r,
                color.gradient_top_color.g,
                color.gradient_top_color.b,
            ),
            mid_color: (
                color.gradient_mid_color.r,
                color.gradient_mid_color.g,
                color.gradient_mid_color.b,
            ),
            bot_color: (
                color.gradient_bot_color.r,
                color.gradient_bot_color.g,
                color.gradient_bot_color.b,
            ),
            scratch_roughness: swatch.scratch_roughness.0,
            scratch_metallic: swatch.scratch_metallic.0,
            scratch_color: (
                swatch.scratch_color.r,
                swatch.scratch_color.g,
                swatch.scratch_color.b,
            ),
        }
    }

    pub fn from_runtime(
        info: &CoatingPaletteInfo,
        coating_swatches: &HashMap<i32, CoatingSwatchPODTag>,
        index: i32,
    ) -> Self {
        if info.swatch.global_id == -1 {
            return Self {
                disabled: true,
                ..Default::default()
            };
        }

        let swatch = coating_swatches
            .get(&info.swatch.global_id)
            .expect("Invalid swatch ID");
        let color = get_color(&info.gradient_color_flag.0, swatch, info);
        let mut disabled = false;
        if (swatch.normal_detail_map.global_id == DEFAULT_NORMAL)
            && (swatch.color_gradient_map.global_id == DEFAULT_GRADIENT)
        {
            disabled = true
        }

        Self {
            index,
            disabled,
            gradient_transform: (
                swatch.color_and_roughness_texture_transform.x,
                swatch.color_and_roughness_texture_transform.y,
            ),
            normal_transform: (
                swatch.normal_texture_transform.x,
                swatch.normal_texture_transform.y,
            ),
            gradient_bitmap: swatch.color_gradient_map.global_id,
            normal_bitmap: swatch.normal_detail_map.global_id,
            roughness: 4.0 + (4.0 * info.roughness_offset.0),
            roughness_black: swatch.roughness_black.0,
            roughness_white: swatch.roughness_white.0,
            metallic: swatch.metallic.0,
            emissive_amount: info.emissive_amount.0 + info.emissive_intensity.0 * 0.5,
            top_color: color[0],
            mid_color: color[1],
            bot_color: color[2],
            scratch_roughness: swatch.scratch_roughness.0 * (1.0 + info.scratch_roughness_offset.0),
            scratch_metallic: swatch.scratch_metallic.0,
            scratch_color: match info.scratch_color_flag.0 {
                OverrideColorsEnum::UseDefaultColors => (
                    swatch.scratch_color.r,
                    swatch.scratch_color.g,
                    swatch.scratch_color.b,
                ),
                OverrideColorsEnum::OverrideColors => (
                    info.scratch_color.r,
                    info.scratch_color.g,
                    info.scratch_color.b,
                ),
            },
        }
    }
}

pub fn process_coating_global(
    coating_globals: &CoatingGlobalsTag,
    coating_swatches: &HashMap<i32, CoatingSwatchPODTag>,
) -> Result<CoatingGlobalEntries> {
    let mut entries = CoatingGlobalEntries::default();
    for (idx, thing) in coating_globals
        .global_shader_lookup
        .elements
        .iter()
        .enumerate()
    {
        let entry = CoatingGlobalEntry {
            fallback: thing.fallback_intention.0,
            layer: CommonLayer::from_runtime(&thing.intention, coating_swatches, idx as i32),
        };
        entries.entries.insert(thing.name.0, entry);
    }
    Ok(entries)
}
