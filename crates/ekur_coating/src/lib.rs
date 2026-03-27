/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use serde::Serialize;
use std::collections::HashMap;

pub mod common;
pub mod material;

#[derive(Debug, Default, Serialize)]
pub struct CommonLayer {
    pub index: i32,
    pub disabled: bool,
    pub gradient_transform: (f32, f32),
    pub normal_transform: (f32, f32),
    pub gradient_bitmap: i32,
    pub normal_bitmap: i32,
    pub roughness: f32,
    pub roughness_white: f32,
    pub roughness_black: f32,
    pub metallic: f32,
    pub emissive_amount: f32,
    pub top_color: (f32, f32, f32),
    pub mid_color: (f32, f32, f32),
    pub bot_color: (f32, f32, f32),
    pub scratch_roughness: f32,
    pub scratch_metallic: f32,
    pub scratch_color: (f32, f32, f32),
}

#[derive(Debug, Default, Serialize)]
pub struct CommonRegion {
    pub layers: HashMap<i32, CommonLayer>,
}

#[derive(Debug, Default, Serialize)]
pub struct CommonCoating {
    pub grime_amount: f32,
    pub scratch_amount: f32,
    pub grime_swatch: CommonLayer,
    pub regions: HashMap<i32, CommonRegion>,
}

#[derive(Debug, Default, Serialize)]
pub struct CoatingGlobalEntry {
    pub fallback: i32,
    pub layer: CommonLayer,
}

#[derive(Debug, Default, Serialize)]
pub struct CoatingGlobalEntries {
    pub entries: HashMap<i32, CoatingGlobalEntry>,
}

#[derive(Debug, Default, Serialize)]
pub struct CommonStyleListEntry {
    pub reference: String,
    pub name: String,
}

#[derive(Debug, Default, Serialize)]
pub struct CommonStyleList {
    pub default_style: CommonStyleListEntry,
    pub styles: HashMap<i32, CommonStyleListEntry>,
}
