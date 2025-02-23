/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;
use serde::Serialize;

use crate::definitions::{render_model::MeshFlags, scenario::ScenarioStructureBsp};

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

pub fn process_scenarios(
    scenarios: &HashMap<i32, ScenarioStructureBsp>,
    save_path: &str,
) -> Result<()> {
    for levl in scenarios {
        let scenario = levl.1;
        let mut level = Level::default();
        for instance in &scenario.bsp_geometry_instances.elements {
            let mut inst = Instance::default();
            if instance.runtime_geo.global_id == -1 {
                continue;
            }
            if instance
                .flags_override
                .0
                .contains(MeshFlags::MESH_IS_CUSTOM_SHADOW_CASTER)
            {
                continue;
            }
            inst.bounding_box_index = instance.bounds_index.0 as i32;
            inst.global_id = instance.runtime_geo.global_id;

            inst.position = [
                instance.position.x,
                instance.position.y,
                instance.position.z,
            ];
            inst.scale = [
                instance.transform_scale.x,
                instance.transform_scale.y,
                instance.transform_scale.z,
            ];
            inst.forward = [instance.forward.x, instance.forward.y, instance.forward.z];
            inst.left = [instance.left.x, instance.left.y, instance.left.z];
            inst.up = [instance.up.x, instance.up.y, instance.up.z];

            inst.material = instance
                .material
                .elements
                .iter()
                .map(|x| x.material.global_id)
                .collect();
            level.instances.push(inst);
        }
        let mut path = PathBuf::from(format!("{save_path}/levels/"));
        path.push(levl.0.to_string());
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &level)?;
    }
    Ok(())
}
