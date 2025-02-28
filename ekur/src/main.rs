/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::loader::module::get_tags;
use crate::loader::module::load_modules;
use anyhow::Result;
use bitmap::extract::extract_all_bitmaps;
use clap::Parser;
use definitions::customization_globals::CustomizationGlobals;
use definitions::forge_manifest::ForgeObjectManifest;
use definitions::model::ModelDefinition;
use definitions::object_attachment::AttachmentConfiguration;
use definitions::object_theme::ObjectTheme;
use definitions::particle_model::ParticleModel;
use definitions::runtime_geo::RuntimeGeo;
use definitions::scenario::ScenarioStructureBsp;
use definitions::stringlist::UnicodeStringListGroup;
use definitions::{
    coating_globals::CoatingGlobalsTag, coating_swatch::CoatingSwatchPODTag, material::MaterialTag,
    material_palette::MaterialPaletteTag, material_styles::MaterialStylesTag,
    material_swatch::MaterialSwatchTag, render_model::RenderModel,
    runtime_style::RuntimeCoatingStyle, runtime_styles::RuntimeCoatingStyles,
    visor::MaterialVisorSwatchTag,
};
use infinite_rs::ModuleFile;
use loader::module::get_models;
use materials::process_material::process_materials;
use materials::serde_definitions::TextureType;
use model::serialize::process_models;
use serialize::customization_globals::process_object_globals;
use serialize::forge_object::process_forge_objects;
use serialize::scenario_bsp::process_scenarios;
use serialize::stringlist::process_stringlists;
use serialize::{
    common_coating::process_coating_global, common_styles::process_styles,
    material_coating::process_material_coatings, runtime_coating::process_runtime_coatings,
    visor::process_visor,
};
use std::{
    collections::HashMap,
    fs::File,
    io::{BufRead, BufReader},
};

mod bitmap;
pub mod definitions;
mod loader;
mod materials;
pub mod model;
pub mod serialize;

#[derive(Debug, Parser)]
struct EkurArgs {
    #[clap(short, long)]
    module_path: String,
    #[clap(long)]
    save_path: String,
    #[clap(long)]
    strings_path: String,
}

fn extract_models(
    modules: &mut [ModuleFile],
    save: &str,
    strings: &HashMap<i32, String>,
) -> Result<()> {
    std::fs::create_dir_all(format!("{}/models/", save))?;
    std::fs::create_dir_all(format!("{}/runtime_geo/", save))?;
    std::fs::create_dir_all(format!("{}/particle_models/", save))?;

    let mut models = HashMap::new();
    let mut part_models = HashMap::new();
    let mut runtime_geo = HashMap::new();

    for (idx, module) in modules.iter_mut().enumerate() {
        models.extend(get_models::<RenderModel>("mode", module, idx)?);
        part_models.extend(get_models::<ParticleModel>("pmdf", module, idx)?);
        runtime_geo.extend(get_models::<RuntimeGeo>("rtgo", module, idx)?);
    }
    process_models(&models, &runtime_geo, &part_models, save, modules, strings)?;
    Ok(())
}

fn extract_materials(modules: &mut [ModuleFile], save: &str) -> Result<Vec<(TextureType, i32)>> {
    std::fs::create_dir_all(format!("{}/materials/", save))?;
    let materials = get_tags::<MaterialTag>("mat ", modules)?;
    let textures = process_materials(&materials, save)?;
    Ok(textures)
}

fn extract_scenarios(modules: &mut [ModuleFile], save: &str) -> Result<()> {
    std::fs::create_dir_all(format!("{}/levels/", save))?;
    let scenarios = get_tags::<ScenarioStructureBsp>("sbsp", modules)?;
    process_scenarios(&scenarios, save)?;
    Ok(())
}

fn extract_visor_data(
    modules: &mut [ModuleFile],
    swatches: &HashMap<i32, MaterialSwatchTag>,
    save: &str,
) -> Result<()> {
    for module in modules.iter_mut() {
        let m = module.read_tag_from_id(-1260457915)?;
        if let Some(m) = m {
            let mut visor = MaterialVisorSwatchTag::default();
            m.read_metadata(&mut visor)?;
            process_visor(&visor, swatches, save)?;
        }
    }
    Ok(())
}

fn extract_object_customization(
    modules: &mut [ModuleFile],
    themes: &HashMap<i32, ObjectTheme>,
    attachments: &HashMap<i32, AttachmentConfiguration>,
    models: &HashMap<i32, ModelDefinition>,
    save: &str,
    strings: &HashMap<i32, String>,
) -> Result<()> {
    for module in modules.iter_mut() {
        let m = module.read_tag_from_id(1672913609)?;
        if let Some(m) = m {
            let mut globals = CustomizationGlobals::default();
            m.read_metadata(&mut globals)?;
            process_object_globals(&globals, themes, save, attachments, models, strings)?;
        }
    }
    Ok(())
}

fn extract_coating_globals(
    modules: &mut [ModuleFile],
    swatches: &HashMap<i32, CoatingSwatchPODTag>,
    save: &str,
) -> Result<()> {
    for module in modules.iter_mut() {
        let m = module.read_tag_from_id(680672300)?;
        if let Some(m) = m {
            let mut globals = CoatingGlobalsTag::default();
            m.read_metadata(&mut globals)?;
            process_coating_global(&globals, swatches, save)?;
        }
    }
    Ok(())
}

fn extract_styles(
    modules: &mut [ModuleFile],
    save: &str,
    strings: &HashMap<i32, String>,
) -> Result<()> {
    std::fs::create_dir_all(format!("{}/stylelists/", save))?;
    let styles = get_tags::<RuntimeCoatingStyles>("rucs", modules)?;
    process_styles(&styles, save, strings)?;
    Ok(())
}

fn extract_runtime_coatings(
    modules: &mut [ModuleFile],
    swatches: &HashMap<i32, CoatingSwatchPODTag>,
    save: &str,
) -> Result<()> {
    std::fs::create_dir_all(format!("{}/styles/", save))?;
    let runtime_styles = get_tags::<RuntimeCoatingStyle>("rucy", modules)?;
    process_runtime_coatings(&runtime_styles, swatches, save)?;
    Ok(())
}

fn extract_material_coatings(
    modules: &mut [ModuleFile],
    swatches: &HashMap<i32, MaterialSwatchTag>,
    save: &str,
    strings: &HashMap<i32, String>,
) -> Result<()> {
    std::fs::create_dir_all(format!("{}/material_coatings/", save))?;
    let material_styles = get_tags::<MaterialStylesTag>("mwsy", modules)?;
    let material_palette = get_tags::<MaterialPaletteTag>("mwpl", modules)?;
    process_material_coatings(&material_styles, &material_palette, swatches, save, strings)?;
    Ok(())
}

fn extract_forge_objects(
    modules: &mut [ModuleFile],
    models: &HashMap<i32, ModelDefinition>,
    save: &str,
) -> Result<()> {
    let mut manifest = ForgeObjectManifest::default();
    let mut stringlists = HashMap::new();
    for (idx, module) in modules.iter_mut().enumerate() {
        let m = module.read_tag_from_id(-117678174)?;
        if let Some(m) = m {
            m.read_metadata(&mut manifest)?;
        }
        stringlists.extend(get_models::<UnicodeStringListGroup>("uslg", module, idx)?);
    }
    let strings = process_stringlists(&stringlists, modules)?;
    process_forge_objects(modules, &manifest, models, &strings, save)?;
    Ok(())
}

fn main() -> Result<()> {
    let args = EkurArgs::parse();
    let mut modules = load_modules(args.module_path)?;

    let string_file = File::open(args.strings_path)?;
    let strings = BufReader::new(string_file);
    let mut string_mappings = HashMap::new();
    for line in strings.lines().map_while(Result::ok) {
        let (id, string) = line.split_once(":").unwrap();
        string_mappings.insert(id.parse::<i32>()?, string.to_string());
    }

    let save = &args.save_path;
    let textures = extract_materials(&mut modules, save)?;
    let material_swatches = get_tags::<MaterialSwatchTag>("mwsw", &mut modules)?;
    let attachments = get_tags::<AttachmentConfiguration>("ocad", &mut modules)?;
    let models = get_tags::<ModelDefinition>("hlmt", &mut modules)?;
    let themes = get_tags::<ObjectTheme>("ocur", &mut modules)?;
    let coat_swatch = get_tags::<CoatingSwatchPODTag>("cmsw", &mut modules)?;

    extract_forge_objects(&mut modules, &models, save)?;
    extract_scenarios(&mut modules, save)?;
    extract_visor_data(&mut modules, &material_swatches, save)?;
    extract_models(&mut modules, save, &string_mappings)?;
    extract_object_customization(
        &mut modules,
        &themes,
        &attachments,
        &models,
        save,
        &string_mappings,
    )?;
    extract_coating_globals(&mut modules, &coat_swatch, save)?;
    extract_styles(&mut modules, save, &string_mappings)?;
    extract_runtime_coatings(&mut modules, &coat_swatch, save)?;
    extract_material_coatings(&mut modules, &material_swatches, save, &string_mappings)?;
    extract_all_bitmaps(
        &mut modules,
        textures,
        &coat_swatch,
        &material_swatches,
        &args.save_path,
    )?;
    Ok(())
}
