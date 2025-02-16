/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::definitions::{customization_globals::CustomizationGlobals, object_theme::ObjectTheme};
use anyhow::Result;
use serde::Serialize;
use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::BufWriter,
    path::PathBuf,
};

#[derive(Debug, Default, Serialize)]
pub struct Permutation {
    pub name: i32,
    pub attachment: i32,
}

#[derive(Debug, Default, Serialize)]
pub struct Region {
    pub name: i32,
    pub permutations: Vec<Permutation>,
}

#[derive(Debug, Default, Serialize)]
pub struct Theme {
    pub name: i32,
    pub variant_name: i32,
    pub regions: Vec<Region>,
    pub attachments: Vec<i32>,
    pub prosthetics: Vec<Region>,
    pub body_types: Vec<Region>,
}

#[derive(Debug, Default, Serialize)]
pub struct SpartanGlobals {
    pub model: i32,
    pub themes: Vec<Theme>,
}

pub fn process_object_globals(
    globals: &CustomizationGlobals,
    themes: &HashMap<i32, ObjectTheme>,
    save_path: &str,
) -> Result<()> {
    let mut spartan_globals = SpartanGlobals::default();
    let first_theme = globals.themes.elements.first();
    let mut theme_names = HashSet::new();
    if let Some(first_theme) = first_theme {
        spartan_globals.model = first_theme.model.global_id;
        for configs in &first_theme.theme_configurations.elements {
            let theme_config = themes.get(&configs.theme_configs.global_id);
            if !theme_names.insert(configs.name.0) {
                continue;
            }
            let mut theme = Theme {
                name: configs.name.0,
                variant_name: configs.variant_name.0,
                ..Default::default()
            };
            if let Some(theme_config) = theme_config {
                for region in &theme_config.regions.elements {
                    let mut reg = Region {
                        name: region.region_name.0,
                        ..Default::default()
                    };
                    for permutation in &region.permutation_settings.elements {
                        reg.permutations.push(Permutation {
                            name: permutation.name.0,
                            attachment: permutation.attachment.global_id,
                        });
                    }
                    theme.regions.push(reg);
                }
                for attachment in &theme_config.attachments.elements {
                    theme.attachments.push(attachment.attachment.global_id);
                }
                for prosthetic in &theme_config.prosthetics.elements {
                    let mut reg = Region {
                        name: prosthetic.region_name.0,
                        ..Default::default()
                    };
                    for permutation in &prosthetic.permutation_settings.elements {
                        reg.permutations.push(Permutation {
                            name: permutation.name.0,
                            attachment: permutation.attachment.global_id,
                        });
                    }
                    theme.prosthetics.push(reg);
                }
                for body_type in &theme_config.body_types.elements {
                    let mut reg = Region {
                        name: body_type.region_name.0,
                        ..Default::default()
                    };
                    for permutation in &body_type.permutation_settings.elements {
                        reg.permutations.push(Permutation {
                            name: permutation.name.0,
                            attachment: permutation.attachment.global_id,
                        });
                    }
                    theme.body_types.push(reg);
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
