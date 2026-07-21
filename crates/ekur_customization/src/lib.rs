/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use serde::Serialize;
use std::collections::HashMap;

pub mod customization_globals;
pub mod visor;

#[derive(Debug, Default, Serialize)]
pub struct Attachment {
    pub tag_id: i32,
    pub marker_name: i32,
    pub model: String,
}

#[derive(Debug, Default, Serialize)]
pub struct Permutation {
    pub name: i32,
    pub attachment: Option<Attachment>,
}

#[derive(Debug, Default, Serialize)]
pub struct Region {
    pub name: String,
    pub name_int: i32,
    pub permutations: Vec<Permutation>,
    pub permutation_regions: Vec<i32>,
}

#[derive(Debug, Default, Serialize)]
pub struct Kit {
    pub name: i32,
    pub regions: Vec<Region>,
}

#[derive(Debug, Default, Serialize)]
pub struct Theme {
    pub name: String,
    pub variant_name: i32,
    pub attachments: Vec<Attachment>,
    pub regions: Vec<Region>,
    pub prosthetics: Vec<Region>,
    pub body_types: Vec<Region>,
    pub kits: Vec<Kit>,
}

#[derive(Debug, Default, Serialize)]
pub struct SpartanGlobals {
    pub model: String,
    pub themes: Vec<Theme>,
}

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
