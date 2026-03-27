/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::{CommonStyleList, CommonStyleListEntry};
use ekur_definitions::runtime_styles::RuntimeCoatingStyles;

use anyhow::Result;
use std::collections::HashMap;

pub fn process_styles(
    styles: &HashMap<i32, RuntimeCoatingStyles>,
    strings: &HashMap<i32, String>,
) -> Result<HashMap<i32, CommonStyleList>> {
    let mut style_map = HashMap::new();
    for (id, style) in styles {
        let mut list = CommonStyleList::default();
        for reference in &style.styles.elements {
            let entry = CommonStyleListEntry {
                reference: reference.style_ref.global_id.to_string(),
                name: strings
                    .get(&reference.name.0)
                    .cloned()
                    .unwrap_or(reference.name.0.to_string()),
            };
            list.styles.insert(reference.name.0, entry);
        }
        let Some(default_style) = style
            .styles
            .elements
            .get(style.default_style_index.0 as usize)
        else {
            style_map.insert(*id, list);
            continue;
        };
        list.default_style = CommonStyleListEntry {
            reference: default_style.style_ref.global_id.to_string(),
            name: strings
                .get(&default_style.name.0)
                .cloned()
                .unwrap_or(default_style.name.0.to_string()),
        };
        style_map.insert(*id, list);
    }
    Ok(style_map)
}
