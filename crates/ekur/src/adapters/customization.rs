/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::utils::{get_tag, get_tags};
use ekur_customization::{customization_globals::process_object_globals, visor::process_visor};
use ekur_definitions::{
    customization_globals::CustomizationGlobals, material_swatch::MaterialSwatchTag,
    model::ModelDefinition, object_attachment::AttachmentConfiguration, object_theme::ObjectTheme,
    visor::MaterialVisorSwatchTag,
};

use anyhow::Result;
use infinite_rs::ModuleFile;
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

const OCGD_ID: i32 = 1672913609;
const VISOR_ID: i32 = -1260457915;

const OBJECT_THEME_GROUP: &str = "ocur";
const OBJECT_ATTACHMENT_GROUP: &str = "ocad";

pub(crate) fn extract_customization(
    modules: &mut [ModuleFile],
    models: &HashMap<i32, ModelDefinition>,
    strings: &HashMap<i32, String>,
    save_path: &str,
) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    let themes = get_tags::<ObjectTheme>(OBJECT_THEME_GROUP, modules)?;
    let attchs = get_tags::<AttachmentConfiguration>(OBJECT_ATTACHMENT_GROUP, modules)?;
    let global = get_tag::<CustomizationGlobals>(OCGD_ID, modules)?;

    if let Some(global) = global {
        let spartan_globals = process_object_globals(&global, &themes, &attchs, models, strings)?;
        save_path.push("customization_globals.json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &spartan_globals)?;
    }
    Ok(())
}

pub(crate) fn extract_visors(
    modules: &mut [ModuleFile],
    swatches: &HashMap<i32, MaterialSwatchTag>,
    save_path: &str,
) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    let visor_globals = get_tag::<MaterialVisorSwatchTag>(VISOR_ID, modules)?;
    if let Some(visor_globals) = visor_globals {
        let visors = process_visor(&visor_globals, swatches)?;
        save_path.push("visor_data.json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &visors)?;
    }
    Ok(())
}
