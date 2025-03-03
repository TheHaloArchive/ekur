/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;
use infinite_rs::ModuleFile;
use serde::Serialize;

use crate::{
    definitions::{
        crate_block::CrateDefinition,
        equipment::Equipment,
        forge_manifest::{ForgeObjectManifest, ForgeObjectManifestEntry},
        forge_object_definition::ForgeObjectData,
        model::ModelDefinition,
        vehicle::Vehicle,
        weapon::Weapon,
    },
    loader::module::get_tags,
};

const BLACKLISTED_CATEGORIES: [u32; 3] = [2645216826, 4210236789, 114233605];

#[derive(Default, Debug, Serialize)]
struct ForgeObjectRepresentation {
    name: String,
    name_int: i32,
    model: i32,
    variant: i32,
}

#[derive(Default, Debug, Serialize)]
struct ForgeObject {
    id: i32,
    name: String,
    representations: Vec<ForgeObjectRepresentation>,
}

#[derive(Default, Debug, Serialize)]
struct ForgeObjectCategory {
    name: String,
    sub_categories: Option<Vec<ForgeObjectCategory>>,
    objects: Option<Vec<ForgeObject>>,
}

#[derive(Default, Debug, Serialize)]
struct ForgeObjectDefinition {
    root_categories: Vec<ForgeObjectCategory>,
    objects: HashMap<i32, ForgeObject>,
}

#[allow(clippy::too_many_arguments)]
fn get_object_info(
    forge_data: &HashMap<i32, ForgeObjectData>,
    objects: &[&ForgeObjectManifestEntry],
    crates: &HashMap<i32, CrateDefinition>,
    models: &HashMap<i32, ModelDefinition>,
    weapons: &HashMap<i32, Weapon>,
    vehicles: &HashMap<i32, Vehicle>,
    equipment: &HashMap<i32, Equipment>,
    strings: &HashMap<i32, String>,
) -> Option<Vec<ForgeObject>> {
    if objects.is_empty() {
        return None;
    }
    let mut object_definitions = Vec::new();
    for object in objects {
        let name = strings
            .get(&object.name.0)
            .unwrap_or(&object.name.0.to_string())
            .to_string();

        let mut forge_object = ForgeObject {
            id: object.forge_object.global_id,
            name,
            ..Default::default()
        };
        let data = forge_data.get(&object.forge_object.global_id);
        let Some(data) = data else {
            continue;
        };
        for representation in &data.object_representations.elements {
            let mut represent = ForgeObjectRepresentation {
                name: strings
                    .get(&representation.representation_name.0)
                    .unwrap_or(&representation.representation_name.0.to_string())
                    .to_string(),
                name_int: representation.representation_name.0,
                model: 0,
                variant: representation.crate_variant.0,
            };

            if let Some(model) = match representation.object_definition.group.as_str() {
                "bloc" => {
                    let crate_def = crates.get(&representation.object_definition.global_id);
                    crate_def.map(|crate_def| crate_def.model.global_id)
                }
                "weap" => {
                    let weapon_def = weapons.get(&representation.object_definition.global_id);
                    weapon_def.map(|weapon_def| weapon_def.model.global_id)
                }
                "vehi" => {
                    let vehicle_def = vehicles.get(&representation.object_definition.global_id);
                    vehicle_def.map(|vehi_def| vehi_def.model.global_id)
                }
                "eqip" => {
                    let equip_def = equipment.get(&representation.object_definition.global_id);
                    equip_def.map(|equip_def| equip_def.model.global_id)
                }
                _ => None,
            } {
                let model = models.get(&model);
                let Some(model) = model else {
                    continue;
                };
                represent.model = model.render_model.global_id;
                forge_object.representations.push(represent);
            };
        }

        object_definitions.push(forge_object);
    }
    Some(object_definitions)
}

#[allow(clippy::too_many_arguments)]
fn process_category_recursively(
    title: i32,
    category_id: u32,
    manifest: &ForgeObjectManifest,
    crates: &HashMap<i32, CrateDefinition>,
    models: &HashMap<i32, ModelDefinition>,
    weapons: &HashMap<i32, Weapon>,
    object_defs: &HashMap<i32, ForgeObjectData>,
    vehicles: &HashMap<i32, Vehicle>,
    equipment: &HashMap<i32, Equipment>,
    strings: &HashMap<i32, String>,
) -> ForgeObjectCategory {
    let child_categories: Vec<_> = manifest
        .categories
        .elements
        .iter()
        .filter(|x| x.parent_category_id.0 as u32 == category_id)
        .collect();

    let sub_categories: Vec<ForgeObjectCategory> = child_categories
        .iter()
        .map(|child| {
            process_category_recursively(
                child.title.0,
                child.category_id.0 as u32,
                manifest,
                crates,
                models,
                weapons,
                object_defs,
                vehicles,
                equipment,
                strings,
            )
        })
        .collect();

    let objects = manifest
        .entries
        .elements
        .iter()
        .filter(|x| x.object_metadata.elements.first().unwrap().keyword.0 as u32 == category_id)
        .collect::<Vec<_>>();
    let objects = get_object_info(
        object_defs,
        &objects,
        crates,
        models,
        weapons,
        vehicles,
        equipment,
        strings,
    );

    let name = strings
        .get(&title)
        .cloned()
        .unwrap_or_else(|| category_id.to_string());
    ForgeObjectCategory {
        name,
        sub_categories: if sub_categories.is_empty() {
            None
        } else {
            Some(sub_categories)
        },
        objects,
    }
}

pub fn process_forge_objects(
    modules: &mut [ModuleFile],
    manifest: &ForgeObjectManifest,
    models: &HashMap<i32, ModelDefinition>,
    strings: &HashMap<i32, String>,
    save: &str,
) -> Result<()> {
    let objects = get_tags::<ForgeObjectData>("food", modules)?;
    let crates = get_tags::<CrateDefinition>("bloc", modules)?;
    let weapons = get_tags::<Weapon>("weap", modules)?;
    let vehicles = get_tags::<Vehicle>("vehi", modules)?;
    let equipments = get_tags::<Equipment>("eqip", modules)?;

    let mut forge_object_definition = ForgeObjectDefinition::default();
    let root_categories = manifest
        .categories
        .elements
        .iter()
        .filter(|x| x.parent_category_id.0 as u32 == 3112307346)
        .collect::<Vec<_>>();

    forge_object_definition.root_categories = root_categories
        .iter()
        .filter(|x| !BLACKLISTED_CATEGORIES.contains(&(x.category_id.0 as u32)))
        .map(|category| {
            process_category_recursively(
                category.title.0,
                category.category_id.0 as u32,
                manifest,
                &crates,
                models,
                &weapons,
                &objects,
                &vehicles,
                &equipments,
                strings,
            )
        })
        .collect();
    for thing in objects {
        let mut definition = ForgeObject {
            id: thing.0,
            name: strings
                .get(&thing.0)
                .unwrap_or(&thing.0.to_string())
                .to_string(),
            ..Default::default()
        };
        for representation in &thing.1.object_representations.elements {
            let crate_def = crates.get(&representation.object_definition.global_id);
            let Some(crate_def) = crate_def else {
                continue;
            };
            let model = models.get(&crate_def.model.global_id);
            let Some(model) = model else {
                continue;
            };
            let forge_object = ForgeObjectRepresentation {
                name: strings
                    .get(&representation.representation_name.0)
                    .unwrap_or(&representation.representation_name.0.to_string())
                    .to_string(),
                name_int: representation.representation_name.0,
                model: model.render_model.global_id,
                variant: representation.crate_variant.0,
            };
            definition.representations.push(forge_object);
        }
        forge_object_definition.objects.insert(thing.0, definition);
    }
    let path = PathBuf::from(format!("{save}/forge_objects.json"));
    let file = File::create(path)?;
    let writer = BufWriter::new(file);
    serde_json::to_writer(writer, &forge_object_definition)?;
    Ok(())
}
