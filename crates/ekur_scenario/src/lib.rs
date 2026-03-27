/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
pub mod scenario_bsp;

use serde::Serialize;

#[derive(Default, Debug, Serialize)]
pub struct Instance {
    pub global_id: i32,
    pub position: [f32; 3],
    pub scale: [f32; 3],
    pub forward: [f32; 3],
    pub left: [f32; 3],
    pub up: [f32; 3],
    pub material: Vec<i32>,
    pub bounding_box_index: i32,
}

#[derive(Default, Debug, Serialize)]
pub struct Level {
    pub instances: Vec<Instance>,
}
