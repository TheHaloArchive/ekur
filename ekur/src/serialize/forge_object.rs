/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;
use serde::Serialize;

use crate::definitions::{
    crate_block::CrateDefinition,
    forge_manifest::{ForgeObjectManifest, ForgeObjectManifestEntry},
    forge_object_definition::ForgeObjectData,
    model::ModelDefinition,
};

const BLACKLISTED_CATEGORIES: [u32; 3] = [2645216826, 4210236789, 114233605];

#[derive(Debug, Serialize)]
struct ForgeObject {
    name: String,
    model: i32,
    variant: i32,
}

#[derive(Debug, Serialize)]
struct ForgeObjectCategory {
    name: String,
    sub_categories: Option<Vec<ForgeObjectCategory>>,
    objects: Option<Vec<ForgeObject>>,
}

#[derive(Default, Debug, Serialize)]
struct ForgeObjectDefinition {
    root_categories: Vec<ForgeObjectCategory>,
}

fn get_object_info(
    forge_data: &HashMap<i32, ForgeObjectData>,
    objects: &[&ForgeObjectManifestEntry],
    crates: &HashMap<i32, CrateDefinition>,
    models: &HashMap<i32, ModelDefinition>,
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
        let data = forge_data.get(&object.forge_object.global_id);
        // holy shit this is a lot
        let Some(data) = data else {
            continue;
        };
        let representation = data.object_representations.elements.first();
        let Some(representation) = representation else {
            continue;
        };
        let crate_def = crates.get(&representation.object_definition.global_id);
        let Some(crate_def) = crate_def else {
            continue;
        };
        let model = models.get(&crate_def.model.global_id);
        let Some(model) = model else {
            continue;
        };
        let forge_object = ForgeObject {
            name,
            model: model.render_model.global_id,
            variant: representation.crate_variant.0,
        };
        object_definitions.push(forge_object);
    }
    Some(object_definitions)
}

fn process_category_recursively(
    title: i32,
    category_id: u32,
    manifest: &ForgeObjectManifest,
    crates: &HashMap<i32, CrateDefinition>,
    models: &HashMap<i32, ModelDefinition>,
    object_defs: &HashMap<i32, ForgeObjectData>,
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
                object_defs,
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
    let objects = get_object_info(object_defs, &objects, crates, models, strings);

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
    objects: &HashMap<i32, ForgeObjectData>,
    manifest: &ForgeObjectManifest,
    crates: &HashMap<i32, CrateDefinition>,
    models: &HashMap<i32, ModelDefinition>,
    strings: &HashMap<i32, String>,
    save: &str,
) -> Result<()> {
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
                crates,
                models,
                objects,
                strings,
            )
        })
        .collect();
    let path = PathBuf::from(format!("{save}/forge_objects.json"));
    let file = File::create(path)?;
    let writer = BufWriter::new(file);
    serde_json::to_writer(writer, &forge_object_definition)?;
    Ok(())
}
