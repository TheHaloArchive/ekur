/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::definitions::{
    customization_globals::CustomizationGlobals,
    model::ModelDefinition,
    object_attachment::AttachmentConfiguration,
    object_theme::{ObjectTheme, RegionBlock},
};
use anyhow::Result;
use serde::Serialize;
use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::BufWriter,
    path::PathBuf,
};

#[derive(Debug, Default, Serialize)]
pub struct Attachment {
    pub marker_name: i32,
    pub model: i32,
}

#[derive(Debug, Default, Serialize)]
pub struct Permutation {
    pub name: i32,
    pub attachment: Option<Attachment>,
}

#[derive(Debug, Default, Serialize)]
pub struct Region {
    pub name: i32,
    pub permutations: Vec<Permutation>,
    pub permutation_regions: Vec<i32>,
}

#[derive(Debug, Default, Serialize)]
pub struct Theme {
    pub name: i32,
    pub variant_name: i32,
    pub attachments: Vec<Attachment>,
    pub regions: Vec<Region>,
    pub prosthetics: Vec<Region>,
    pub body_types: Vec<Region>,
}

#[derive(Debug, Default, Serialize)]
pub struct SpartanGlobals {
    pub model: i32,
    pub themes: Vec<Theme>,
}

fn get_attachment(
    attachment: i32,
    attachments: &HashMap<i32, AttachmentConfiguration>,
    models: &HashMap<i32, ModelDefinition>,
) -> Option<Attachment> {
    let attachment = attachments.get(&attachment);
    if let Some(attachment) = attachment {
        let marker = attachment.model_attachments.elements.first();
        if let Some(marker) = marker {
            let model_definition = models.get(&marker.model.global_id);
            if let Some(model_definition) = model_definition {
                return Some(Attachment {
                    marker_name: marker.markers.elements.first().unwrap().marker_name.0,
                    model: model_definition.render_model.global_id,
                });
            }
        }
    }
    None
}

fn add_region(
    region: &RegionBlock,
    attachments: &HashMap<i32, AttachmentConfiguration>,
    models: &HashMap<i32, ModelDefinition>,
) -> Region {
    let mut reg = Region {
        name: region.region_name.0,
        ..Default::default()
    };
    for permutation in &region.permutation_regions.elements {
        reg.permutation_regions.push(permutation.name.0)
    }
    for permutation in &region.permutation_settings.elements {
        let perm = get_attachment(permutation.attachment.global_id, attachments, models);
        reg.permutations.push(Permutation {
            name: permutation.name.0,
            attachment: perm,
        });
    }
    reg
}

pub fn process_object_globals(
    globals: &CustomizationGlobals,
    themes: &HashMap<i32, ObjectTheme>,
    save_path: &str,
    attachments: &HashMap<i32, AttachmentConfiguration>,
    models: &HashMap<i32, ModelDefinition>,
) -> Result<()> {
    let mut spartan_globals = SpartanGlobals::default();
    let first_theme = globals.themes.elements.first();
    let mut theme_names = HashSet::new();
    if let Some(first_theme) = first_theme {
        spartan_globals.model = first_theme.model.global_id;
        for configs in &first_theme.theme_configurations.elements {
            let theme_config = themes.get(&configs.theme_configs.global_id);
            if !theme_names.insert(configs.theme_configs.global_id) {
                continue;
            }
            let mut theme = Theme {
                name: configs.name.0,
                variant_name: configs.variant_name.0,
                ..Default::default()
            };
            if let Some(theme_config) = theme_config {
                for attachment in &theme_config.attachments.elements {
                    let attach =
                        get_attachment(attachment.attachment.global_id, attachments, models);
                    if let Some(attach) = attach {
                        theme.attachments.push(attach);
                    }
                }
                for region in &theme_config.regions.elements {
                    let reg = add_region(region, attachments, models);
                    theme.regions.push(reg);
                }
                for region in &theme_config.body_types.elements {
                    let reg = add_region(region, attachments, models);
                    theme.regions.push(reg);
                }
                for region in &theme_config.prosthetics.elements {
                    let reg = add_region(region, attachments, models);
                    theme.regions.push(reg);
                }
            }
            spartan_globals.themes.push(theme);
        }
    }
    let path = PathBuf::from(format!("{save_path}/customization_globals.json"));
    let file = File::create(path)?;
    let writer = BufWriter::new(file);
    serde_json::to_writer(writer, &spartan_globals)?;
    Ok(())
}
