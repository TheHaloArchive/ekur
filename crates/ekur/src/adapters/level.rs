/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::utils::get_tags;
use ekur_definitions::{
    level::LevelTag, runtime_terrain::RuntimeTerrain, scenario::ScenarioStructureBsp,
};
use ekur_scenario::level::process_level;
use ekur_terrain::process_terrain;

use anyhow::Result;
use infinite_rs::ModuleFile;
use std::{
    collections::HashMap,
    fs::{File, create_dir_all},
    io::{BufWriter, Write},
    path::PathBuf,
};

const LEVEL_GROUP: &str = "levl";
const SCENARIO_BSP_GROUP: &str = "sbsp";
const RUNTIME_TERRAIN_GROUP: &str = "rtrn";

/// The `rtrn` a level renders its terrain from, if it has one.
fn runtime_terrain(level: &LevelTag) -> Option<i32> {
    level
        .terrains
        .elements
        .iter()
        .map(|terrain| &terrain.runtime_terrain)
        .find(|reference| reference.group == "rtrn" && reference.global_id != -1)
        .map(|reference| reference.global_id)
}

pub(crate) fn extract_levels(
    modules: &mut [ModuleFile],
    save_path: &str,
    map_ids: &HashMap<i32, String>,
) -> Result<()> {
    let mut level_path = PathBuf::from(save_path);
    level_path.push("levels/");
    create_dir_all(&level_path)?;
    let mut terrain_path = PathBuf::from(save_path);
    terrain_path.push("terrain/");
    create_dir_all(&terrain_path)?;

    let levels = get_tags::<LevelTag>(LEVEL_GROUP, modules)?;
    let scenarios = get_tags::<ScenarioStructureBsp>(SCENARIO_BSP_GROUP, modules)?;
    let terrains = get_tags::<RuntimeTerrain>(RUNTIME_TERRAIN_GROUP, modules)?;

    let mut level_ids: Vec<&i32> = levels.keys().collect();
    level_ids.sort_unstable();

    let mut processed = Vec::new();
    let mut name_counts: HashMap<String, usize> = HashMap::new();
    for id in level_ids {
        let level_tag = &levels[id];
        let level = process_level(level_tag, &scenarios, map_ids);
        if level.bsps.is_empty() {
            continue;
        }
        *name_counts.entry(level.name.clone()).or_default() += 1;
        processed.push((level_tag, level));
    }

    let mut written_terrain: HashMap<i32, String> = HashMap::new();

    for (level_tag, mut level) in processed {
        if name_counts.get(&level.name).is_some_and(|count| *count > 1) {
            level.name = format!("{}_{}", level.name, level.global_id);
        }

        if let Some(terrain_id) = runtime_terrain(level_tag) {
            if let Some(existing) = written_terrain.get(&terrain_id) {
                level.terrain = Some(format!("{existing}.json"));
            } else if let Some(terrain) = terrains.get(&terrain_id)
                && let Some((record, heights)) = process_terrain(terrain, modules, &level.name)?
            {
                terrain_path.push(&level.name);
                terrain_path.add_extension("r16");
                let mut raw = BufWriter::new(File::create(&terrain_path)?);
                for height in &heights {
                    raw.write_all(&height.to_le_bytes())?;
                }
                raw.flush()?;
                terrain_path.pop();

                terrain_path.push(&level.name);
                terrain_path.add_extension("json");
                serde_json::to_writer(BufWriter::new(File::create(&terrain_path)?), &record)?;
                terrain_path.pop();

                written_terrain.insert(terrain_id, level.name.clone());
                level.terrain = Some(format!("{}.json", level.name));
            }
        }

        level_path.push(&level.name);
        level_path.add_extension("json");
        serde_json::to_writer(BufWriter::new(File::create(&level_path)?), &level)?;
        level_path.pop();
    }
    Ok(())
}
