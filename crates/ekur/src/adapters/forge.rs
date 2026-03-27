/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::utils::{get_tag, get_tags, get_tags_w_index};
use ekur_definitions::{
    crate_block::CrateDefinition, equipment::Equipment, forge_globals::ForgeGlobals,
    forge_manifest::ForgeObjectManifest, forge_object_definition::ForgeObjectData,
    material_palette::MaterialPaletteTag, material_swatch::MaterialSwatchTag,
    model::ModelDefinition, scenery::Scenery, stringlist::UnicodeStringListGroup, vehicle::Vehicle,
    weapon::Weapon,
};
use ekur_forge::{
    forge_material::process_forge_materials, forge_object::process_forge_objects,
    stringlist::process_stringlists,
};

use anyhow::Result;
use infinite_rs::ModuleFile;
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

const OBJECT_MANIFEST: i32 = -117678174;
const FORGE_GLOBALS: i32 = 81;
const FORGE_PALETTE: i32 = 1339504468;

const STRINGLIST: &str = "uslg";
const FORGE_OBJECT: &str = "food";
const CRATE: &str = "bloc";
const WEAPON: &str = "weap";
const VEHICLE: &str = "vehi";
const EQUIPMENT: &str = "eqip";
const SCENERY: &str = "scen";

pub(crate) fn extract_forge(
    modules: &mut [ModuleFile],
    models: &HashMap<i32, ModelDefinition>,
    palettes: &HashMap<i32, MaterialPaletteTag>,
    swatches: &HashMap<i32, MaterialSwatchTag>,
    save_path: &str,
) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    let manifest = get_tag::<ForgeObjectManifest>(OBJECT_MANIFEST, modules)?;
    let globals = get_tag::<ForgeGlobals>(FORGE_GLOBALS, modules)?;

    let objects = get_tags::<ForgeObjectData>(&FORGE_OBJECT, modules)?;
    let crates = get_tags::<CrateDefinition>(&CRATE, modules)?;
    let weapons = get_tags::<Weapon>(&WEAPON, modules)?;
    let vehicles = get_tags::<Vehicle>(&VEHICLE, modules)?;
    let equipments = get_tags::<Equipment>(&EQUIPMENT, modules)?;
    let scenery = get_tags::<Scenery>(&SCENERY, modules)?;

    let mut stringlists = HashMap::new();

    for (idx, module) in modules.iter_mut().enumerate() {
        let uslg_tags = get_tags_w_index::<UnicodeStringListGroup>(STRINGLIST, module, idx)?;
        stringlists.extend(uslg_tags);
    }

    let strings = process_stringlists(&stringlists, modules)?;
    if let Some(manifest) = manifest {
        let objects = process_forge_objects(
            &manifest,
            models,
            &objects,
            &crates,
            &weapons,
            &vehicles,
            &equipments,
            &scenery,
            &strings,
        )?;
        save_path.push("forge_objects.json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &objects)?;
        save_path.pop();
    }

    let palette = palettes.get(&FORGE_PALETTE);
    if let Some(palette) = palette
        && let Some(globals) = globals
    {
        let materials = process_forge_materials(palette, swatches, &strings, &globals)?;
        save_path.push("forge_materials.json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &materials)?;
    }
    Ok(())
}
