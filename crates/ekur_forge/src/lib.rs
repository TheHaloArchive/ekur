/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use ekur_coating::CommonLayer;

use serde::Serialize;
use std::collections::HashMap;

pub mod forge_material;
pub mod forge_object;
pub mod stringlist;

#[derive(Default, Debug, Serialize)]
pub struct ForgeObjectRepresentation {
    pub name: String,
    pub name_int: i32,
    pub model: i32,
    pub variant: i32,
    pub style: i32,
    pub is_rtgo: bool,
}

#[derive(Default, Debug, Serialize)]
pub struct ForgeObject {
    pub id: i32,
    pub name: String,
    pub default_variant: i32,
    pub representations: Vec<ForgeObjectRepresentation>,
}

#[derive(Default, Debug, Serialize)]
pub struct ForgeObjectCategory {
    pub name: String,
    pub sub_categories: Option<Vec<ForgeObjectCategory>>,
    pub objects: Option<Vec<ForgeObject>>,
}

#[derive(Default, Debug, Serialize)]
pub struct ForgeObjectDefinition {
    pub root_categories: Vec<ForgeObjectCategory>,
    pub objects: HashMap<i32, ForgeObject>,
}

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
