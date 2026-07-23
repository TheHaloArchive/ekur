/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::{Attachment, Kit, Permutation, Region, SpartanGlobals, Theme};
use ekur_definitions::{
    customization_globals::CustomizationGlobals,
    model::ModelDefinition,
    object_attachment::AttachmentConfiguration,
    object_theme::{ObjectTheme, RegionBlock},
};

use anyhow::Result;
use std::collections::{HashMap, HashSet};

const NAMES: [(&str, i32); 9] = [
    ("Mark VII", 2059096660),
    ("Mark V [B]", 734978415),
    ("Yoroi", -877464205),
    ("Eaglestrike", 1599196406),
    ("Rakshasa", 1200330315),
    ("Chimera", -1600125127),
    ("Mirage IIC", -1062089054),
    ("HAZMAT", -1199279334),
    ("Mark IV", -1472719967),
];

fn get_attachment(
    attachment: i32,
    attachments: &HashMap<i32, AttachmentConfiguration>,
    models: &HashMap<i32, ModelDefinition>,
    model_ids: &HashMap<i32, String>,
) -> Option<Attachment> {
    let attachment = attachments.get(&attachment);
    if let Some(attachment) = attachment {
        let marker = attachment.model_attachments.elements.first();
        if let Some(marker) = marker {
            let model_definition = models.get(&marker.model.global_id);
            if let Some(model_definition) = model_definition {
                let marker_name = marker.markers.elements.first();
                if let Some(marker_name) = marker_name {
                    return Some(Attachment {
                        tag_id: attachment.any_tag.internal_struct.tag_id,
                        marker_name: marker_name.marker_name.0,
                        model: model_ids
                            .get(&model_definition.render_model.global_id)
                            .unwrap_or(&model_definition.render_model.global_id.to_string())
                            .clone(),
                    });
                }
            }
        }
    }
    None
}

fn add_region(
    region: &RegionBlock,
    attachments: &HashMap<i32, AttachmentConfiguration>,
    models: &HashMap<i32, ModelDefinition>,
    strings: &HashMap<i32, String>,
    model_ids: &HashMap<i32, String>,
) -> Region {
    let mut reg = Region {
        name: strings
            .get(&region.region_name.0)
            .unwrap_or(&region.region_name.0.to_string())
            .to_string(),
        name_int: region.region_name.0,
        ..Default::default()
    };
    for permutation in &region.permutation_regions.elements {
        reg.permutation_regions.push(permutation.name.0)
    }
    for permutation in &region.permutation_settings.elements {
        let perm = get_attachment(
            permutation.attachment.global_id,
            attachments,
            models,
            model_ids,
        );
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
    attachments: &HashMap<i32, AttachmentConfiguration>,
    model_ids: &HashMap<i32, String>,
    models: &HashMap<i32, ModelDefinition>,
    strings: &HashMap<i32, String>,
) -> Result<SpartanGlobals> {
    let mut spartan_globals = SpartanGlobals::default();
    let first_theme = globals.themes.elements.first();
    let mut theme_names = HashSet::new();
    if let Some(first_theme) = first_theme {
        spartan_globals.model = model_ids
            .get(&first_theme.model.global_id)
            .unwrap_or(&first_theme.model.global_id.to_string())
            .clone();
        for configs in &first_theme.theme_configurations.elements {
            let theme_config = themes.get(&configs.theme_configs.global_id);
            if !theme_names.insert(configs.theme_configs.global_id) {
                continue;
            }
            let theme_name = configs.name.0;
            let theme_entry = NAMES.iter().find(|&x| x.1 == theme_name);
            let config_name = match theme_entry {
                Some(theme_entry) => theme_entry.0.to_string(),
                None => theme_name.to_string(),
            };

            let mut theme = Theme {
                name: config_name,
                variant_name: configs.variant_name.0,
                ..Default::default()
            };
            if let Some(theme_config) = theme_config {
                for attachment in &theme_config.attachments.elements {
                    let attach = get_attachment(
                        attachment.attachment.global_id,
                        attachments,
                        models,
                        model_ids,
                    );
                    if let Some(attach) = attach {
                        theme.attachments.push(attach);
                    }
                }
                for region in &theme_config.regions.elements {
                    let reg = add_region(region, attachments, models, strings, model_ids);
                    theme.regions.push(reg);
                }
                for region in &theme_config.body_types.elements {
                    let reg = add_region(region, attachments, models, strings, model_ids);
                    theme.body_types.push(reg);
                }
                for region in &theme_config.prosthetics.elements {
                    let reg = add_region(region, attachments, models, strings, model_ids);
                    theme.prosthetics.push(reg);
                }
            }

            for kit in &configs.kit_configs.elements {
                let mut kit_config = Kit {
                    name: kit.name.0,
                    ..Default::default()
                };
                for region in &kit.regions.elements {
                    let reg = add_region(region, attachments, models, strings, model_ids);
                    kit_config.regions.push(reg);
                }
                theme.kits.push(kit_config);
            }
            spartan_globals.themes.push(theme);
        }
    }
    Ok(spartan_globals)
}
