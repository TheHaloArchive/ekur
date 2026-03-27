/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::utils::get_tags;
use ekur_definitions::scenario::ScenarioStructureBsp;
use ekur_scenario::scenario_bsp::process_scenarios;

use anyhow::Result;
use infinite_rs::ModuleFile;
use std::{
    fs::{File, create_dir_all},
    io::BufWriter,
    path::PathBuf,
};

const SCENARIO_BSP_GROUP: &str = "sbsp";

pub(crate) fn extract_scenario(modules: &mut [ModuleFile], save_path: &str) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    save_path.push("levels/");
    create_dir_all(&save_path)?;

    let scenarios = get_tags::<ScenarioStructureBsp>(&SCENARIO_BSP_GROUP, modules)?;
    let levels = process_scenarios(&scenarios)?;
    for level in levels {
        save_path.push(level.0.to_string());
        save_path.add_extension(".json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &level.1)?;
        save_path.pop();
    }
    Ok(())
}
