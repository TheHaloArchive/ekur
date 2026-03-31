/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::{Instance, Level};
use ekur_definitions::{render_model::MeshFlags, scenario::ScenarioStructureBsp};

use anyhow::Result;
use std::collections::HashMap;

pub fn process_scenarios(
    scenarios: &HashMap<i32, ScenarioStructureBsp>,
) -> Result<Vec<(i32, Level)>> {
    let mut levels = Vec::new();
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
        levels.push((*levl.0, level));
    }
    Ok(levels)
}
