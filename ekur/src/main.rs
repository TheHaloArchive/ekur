/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::loader::module::get_tags;
use std::{
    collections::HashMap,
    fs::{create_dir_all, File},
    io::{BufRead, BufReader},
};

use crate::loader::module::load_modules;
use anyhow::Result;
use bitmap::extract::extract_all_bitmaps;
use clap::Parser;
use definitions::{
    coating_globals::CoatingGlobalsTag, coating_swatch::CoatingSwatchPODTag, material::MaterialTag,
    material_palette::MaterialPaletteTag, material_styles::MaterialStylesTag,
    material_swatch::MaterialSwatchTag, render_model::RenderModel,
    runtime_style::RuntimeCoatingStyle, runtime_styles::RuntimeCoatingStyles,
    visor::MaterialVisorSwatchTag,
};
use serialize::{
    common_coating::process_coating_global, common_styles::process_styles,
    material::process_materials, material_coating::process_material_coatings,
    model::process_models, runtime_coating::process_runtime_coatings, visor::process_visor,
};

mod bitmap;
mod definitions;
mod loader;
mod serialize;

#[derive(Debug, Parser)]
struct EkurArgs {
    #[clap(short, long)]
    module_path: String,
    #[clap(short, long)]
    save_path: String,
    #[clap(short, long)]
    strings_path: String,
}

fn main() -> Result<()> {
    let args = EkurArgs::parse();
    let mut modules = load_modules(args.module_path)?;
    let mut coating_swatches = HashMap::new();
    let mut materials = HashMap::new();
    let mut material_palette = HashMap::new();
    let mut material_styles = HashMap::new();
    let mut material_swatch = HashMap::new();
    let mut runtime_style = HashMap::new();
    let mut runtime_styles = HashMap::new();
    let mut cogl = CoatingGlobalsTag::default();
    let mut visor = MaterialVisorSwatchTag::default();
    let mut render_models = HashMap::new();
    create_dir_all(format!("{}/styles/", args.save_path))?;
    create_dir_all(format!("{}/stylelists/", args.save_path))?;
    create_dir_all(format!("{}/materials/", args.save_path))?;
    create_dir_all(format!("{}/bitmaps/", args.save_path))?;
    create_dir_all(format!("{}/models/", args.save_path))?;

    let string_file = File::open(args.strings_path)?;
    let strings = BufReader::new(string_file);
    let mut string_mappings = HashMap::new();
    for line in strings.lines().map_while(Result::ok) {
        let (id, string) = line.split_once(":").unwrap();
        string_mappings.insert(id.parse::<i32>()?, string.to_string());
    }

    for module in &mut modules {
        let m = module.read_tag_from_id(680672300)?;
        if let Some(m) = m {
            m.read_metadata(&mut cogl)?;
        }
        let m = module.read_tag_from_id(-1260457915)?;
        if let Some(m) = m {
            m.read_metadata(&mut visor)?;
        }
        materials.extend(get_tags::<MaterialTag>("mat ", module)?);
        coating_swatches.extend(get_tags::<CoatingSwatchPODTag>("cmsw", module)?);
        material_palette.extend(get_tags::<MaterialPaletteTag>("mwpl", module)?);
        material_styles.extend(get_tags::<MaterialStylesTag>("mwsy", module)?);
        material_swatch.extend(get_tags::<MaterialSwatchTag>("mwsw", module)?);
        runtime_style.extend(get_tags::<RuntimeCoatingStyle>("rucy", module)?);
        runtime_styles.extend(get_tags::<RuntimeCoatingStyles>("rucs", module)?);
        render_models.extend(get_tags::<RenderModel>("mode", module)?);
    }

    let textures = process_materials(&materials, &args.save_path)?;
    process_styles(&runtime_styles, &args.save_path, &string_mappings)?;
    process_runtime_coatings(&runtime_style, &coating_swatches, &args.save_path)?;
    process_coating_global(&cogl, &coating_swatches, &args.save_path)?;
    process_material_coatings(
        &material_styles,
        &material_palette,
        &material_swatch,
        &args.save_path,
        &string_mappings,
    )?;
    process_visor(&visor, &material_swatch, &args.save_path)?;
    extract_all_bitmaps(
        &mut modules,
        textures,
        &coating_swatches,
        &material_swatch,
        &args.save_path,
    )?;

    process_models(&render_models, &args.save_path)?;
    Ok(())
}
