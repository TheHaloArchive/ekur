/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::scenario_bsp::process_scenario;
use crate::{Level, LevelBsp};
use ekur_definitions::{
    level::{LevelTag, StructureBspFlags},
    scenario::ScenarioStructureBsp,
};

use std::collections::HashMap;

fn default_zone_set_bsps(level: &LevelTag) -> Vec<usize> {
    let count = level.structure_bsps.elements.len();
    let Some(zone_set) = level.zone_sets.elements.first() else {
        return Vec::new();
    };
    let mut active = Vec::new();
    for (word_index, word) in zone_set.bsp_zone_flags.elements.iter().enumerate() {
        for bit in 0..32 {
            let index = word_index * 32 + bit;
            if index < count && word.flags.0 & (1 << bit) != 0 {
                active.push(index);
            }
        }
    }
    active
}

fn level_name(level: &LevelTag, map_ids: &HashMap<i32, String>) -> String {
    level
        .structure_bsps
        .elements
        .iter()
        .filter(|bsp| !bsp.flags.0.contains(StructureBspFlags::VISTA_BSP))
        .find_map(|bsp| map_ids.get(&bsp.structure_bsp.global_id).cloned())
        .unwrap_or_else(|| level.any_tag.internal_struct.tag_id.to_string())
}

pub fn process_level(
    level: &LevelTag,
    scenarios: &HashMap<i32, ScenarioStructureBsp>,
    map_ids: &HashMap<i32, String>,
) -> Level {
    let active = default_zone_set_bsps(level);
    let mut bsps = Vec::new();
    for (index, entry) in level.structure_bsps.elements.iter().enumerate() {
        let global_id = entry.structure_bsp.global_id;
        let Some(scenario) = scenarios.get(&global_id) else {
            continue;
        };
        bsps.push(LevelBsp {
            global_id,
            name: map_ids
                .get(&global_id)
                .cloned()
                .unwrap_or_else(|| global_id.to_string()),
            is_vista: entry.flags.0.contains(StructureBspFlags::VISTA_BSP),
            is_active: active.contains(&index),
            instances: process_scenario(scenario),
        });
    }
    Level {
        global_id: level.any_tag.internal_struct.tag_id,
        name: level_name(level, map_ids),
        terrain: None,
        bsps,
    }
}
