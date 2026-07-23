/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::utils::get_tags;
use ekur_definitions::scenario::ScenarioStructureBsp;
use ekur_scenario::scenario_bsp::process_scenarios;

use anyhow::Result;
use infinite_rs::ModuleFile;
use std::{
    collections::HashMap,
    fs::{File, create_dir_all},
    io::BufWriter,
    path::PathBuf,
};

const SCENARIO_BSP_GROUP: &str = "sbsp";

pub(crate) fn extract_scenario(
    modules: &mut [ModuleFile],
    save_path: &str,
    map_ids: &HashMap<i32, String>,
) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    save_path.push("levels/");
    create_dir_all(&save_path)?;

    let scenarios = get_tags::<ScenarioStructureBsp>(SCENARIO_BSP_GROUP, modules)?;
    let levels = process_scenarios(&scenarios)?;
    for level in levels {
        let temp_level_id = level.0.to_string();
        let map_name = map_ids.get(&level.0).unwrap_or(&temp_level_id);
        save_path.push(map_name);
        save_path.add_extension("json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &level.1)?;
        save_path.pop();
    }
    Ok(())
}
