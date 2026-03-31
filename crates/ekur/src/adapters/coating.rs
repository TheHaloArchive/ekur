/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::utils::{get_tag, get_tags};
use ekur_coating::{
    common::{common_coating::process_coating_global, common_styles::process_styles},
    material::{
        material_coating::process_material_coatings, runtime_coating::process_runtime_coatings,
    },
};
use ekur_definitions::{
    coating_globals::CoatingGlobalsTag, coating_swatch::CoatingSwatchPODTag,
    material_palette::MaterialPaletteTag, material_styles::MaterialStylesTag,
    material_swatch::MaterialSwatchTag, runtime_style::RuntimeCoatingStyle,
    runtime_styles::RuntimeCoatingStyles,
};

use anyhow::Result;
use infinite_rs::ModuleFile;
use std::{
    collections::HashMap,
    fs::{File, create_dir_all},
    io::BufWriter,
    path::PathBuf,
};

const GLOBALS_ID: i32 = 680672300;

const RUNTIME_STYLES_GROUP: &str = "rucs";
const RUNTIME_STYLE_GROUP: &str = "rucy";
const MATERIAL_STYLE_GROUP: &str = "mwsy";

pub(crate) fn extract_coating_globals(
    modules: &mut [ModuleFile],
    swatches: &HashMap<i32, CoatingSwatchPODTag>,
    save_path: &str,
) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    let coat_global = get_tag::<CoatingGlobalsTag>(GLOBALS_ID, modules)?;
    if let Some(coat_global) = coat_global {
        let entries = process_coating_global(&coat_global, swatches)?;
        save_path.push("globals.json");
        let file = File::create(save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &entries)?;
    }
    Ok(())
}

pub(crate) fn extract_styles(
    modules: &mut [ModuleFile],
    strings: &HashMap<i32, String>,
    save_path: &str,
) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    save_path.push("stylelists/");
    create_dir_all(&save_path)?;
    let style_tags = get_tags::<RuntimeCoatingStyles>(RUNTIME_STYLES_GROUP, modules)?;
    let style_lists = process_styles(&style_tags, strings)?;
    for (id, list) in style_lists {
        save_path.push(id.to_string());
        save_path.add_extension("json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &list)?;
        save_path.pop();
    }
    Ok(())
}

pub(crate) fn extract_runtime_coatings(
    modules: &mut [ModuleFile],
    swatches: &HashMap<i32, CoatingSwatchPODTag>,
    save_path: &str,
) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    save_path.push("styles/");
    create_dir_all(&save_path)?;
    let style_tags = get_tags::<RuntimeCoatingStyle>(RUNTIME_STYLE_GROUP, modules)?;
    let styles = process_runtime_coatings(&style_tags, swatches)?;
    for (id, style) in styles {
        save_path.push(id.to_string());
        save_path.add_extension("json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &style)?;
        save_path.pop();
    }
    Ok(())
}

pub(crate) fn extract_material_coatings(
    modules: &mut [ModuleFile],
    palettes: &HashMap<i32, MaterialPaletteTag>,
    swatches: &HashMap<i32, MaterialSwatchTag>,
    strings: &HashMap<i32, String>,
    save_path: &str,
) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    save_path.push("stylelists/");
    let style_tags = get_tags::<MaterialStylesTag>(MATERIAL_STYLE_GROUP, modules)?;
    let styles = process_material_coatings(&style_tags, palettes, swatches, strings)?;
    for (id, style) in styles.0 {
        save_path.push(id.to_string());
        save_path.add_extension("json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &style)?;
        save_path.pop();
    }
    save_path.pop();
    save_path.push("styles/");
    for (id, style) in styles.1 {
        save_path.push(&id);
        save_path.add_extension("json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &style)?;
        save_path.pop();
    }
    Ok(())
}
