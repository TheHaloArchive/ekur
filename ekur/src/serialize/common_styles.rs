/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::definitions::runtime_styles::RuntimeCoatingStyles;
use anyhow::Result;
use indexmap::IndexMap;
use serde::Serialize;
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

#[derive(Debug, Default, Serialize)]
pub struct CommonStyleListEntry {
    pub reference: String,
    pub name: String,
}

#[derive(Debug, Default, Serialize)]
pub struct CommonStyleList {
    default_style: CommonStyleListEntry,
    pub styles: IndexMap<i32, CommonStyleListEntry>,
}

pub fn process_styles(
    styles: &HashMap<i32, RuntimeCoatingStyles>,
    save_path: &str,
    strings: &HashMap<i32, String>,
) -> Result<()> {
    let mut list = CommonStyleList::default();
    for (id, style) in styles {
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
        let default_style = style
            .styles
            .elements
            .get(style.default_style_index.0 as usize)
            .unwrap();
        list.default_style = CommonStyleListEntry {
            reference: default_style.style_ref.global_id.to_string(),
            name: strings
                .get(&default_style.name.0)
                .cloned()
                .unwrap_or(default_style.name.0.to_string()),
        };
        let mut path = PathBuf::from(format!("{save_path}/stylelists/"));
        path.push(id.to_string());
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer_pretty(writer, &list)?;
    }
    Ok(())
}
