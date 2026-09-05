/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::Instance;
use ekur_definitions::{render_model::MeshFlags, scenario::ScenarioStructureBsp};

pub fn process_scenario(scenario: &ScenarioStructureBsp) -> Vec<Instance> {
    let mut instances = Vec::new();
    for instance in &scenario.bsp_geometry_instances.elements {
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
        instances.push(Instance {
            global_id: instance.runtime_geo.global_id,
            position: [
                instance.position.x,
                instance.position.y,
                instance.position.z,
            ],
            scale: [
                instance.transform_scale.x,
                instance.transform_scale.y,
                instance.transform_scale.z,
            ],
            forward: [instance.forward.x, instance.forward.y, instance.forward.z],
            left: [instance.left.x, instance.left.y, instance.left.z],
            up: [instance.up.x, instance.up.y, instance.up.z],
            material: instance
                .material
                .elements
                .iter()
                .map(|x| x.material.global_id)
                .collect(),
            bounding_box_index: instance.bounds_index.0 as i32,
        });
    }
    instances
}
