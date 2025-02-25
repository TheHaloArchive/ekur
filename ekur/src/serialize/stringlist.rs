/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::collections::HashMap;

use anyhow::Result;
use infinite_rs::ModuleFile;

use crate::definitions::stringlist::{UnicodeStringListGroup, UnicodeStringListResource};

pub fn process_stringlists(
    stringlists: &HashMap<(usize, usize, i32), UnicodeStringListGroup>,
    modules: &mut [ModuleFile],
) -> Result<HashMap<i32, String>> {
    let mut strings = HashMap::new();
    for stringlist in stringlists {
        let tag = &modules[stringlist.0.0].files[stringlist.0.1];
        let resource = modules[stringlist.0.0].resource_indices[tag.resource_index as usize];
        let res = modules[stringlist.0.0].read_tag(resource)?;
        if let Some(res) = res {
            let mut resource = UnicodeStringListResource::default();
            res.read_metadata(&mut resource)?;
            for string in &resource.string_lookup_info.elements {
                if string.offset.0 == -1 {
                    continue;
                }
                let string_data = String::from_utf8_lossy(
                    resource.string_data_utf8.data[string.offset.0 as usize..]
                        .split(|x| *x == 0)
                        .next()
                        .unwrap(),
                );
                strings.insert(string.string_id.0, string_data.to_string());
            }
        }
    }
    Ok(strings)
}
