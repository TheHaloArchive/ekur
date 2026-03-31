/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use std::{
    collections::HashMap,
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
};

use anyhow::Result;
use infinite_rs::{ModuleFile, module::file::TagStructure};

pub(crate) fn load_modules<P: AsRef<Path>>(deploy_path: P) -> Result<Vec<ModuleFile>> {
    let mut modules = Vec::new();
    for entry in walkdir::WalkDir::new(deploy_path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        if entry.file_type().is_file() {
            let file_path = entry.path().to_str();
            if let Some(file_path) = file_path
                && file_path.ends_with(".module")
                && !file_path.contains("ds")
            {
                let module = ModuleFile::from_path(file_path)?;
                modules.push(module);
            }
        }
    }
    Ok(modules)
}

pub(crate) fn get_tags<T: TagStructure + Default>(
    tag_group: &str,
    modules: &mut [ModuleFile],
) -> Result<HashMap<i32, T>> {
    let mut tags = HashMap::new();
    for module in modules.iter_mut() {
        for idx in 0..module.files.len() {
            if module.files[idx].tag_group == tag_group {
                let tag = module.read_tag(idx as u32)?;
                if let Some(tag) = tag {
                    let mat = tag.read_metadata::<T>()?;
                    tags.insert(tag.tag_id, mat);
                }
            }
            module.files[idx].data_stream = None;
        }
    }
    Ok(tags)
}

pub(crate) fn get_tag<T: TagStructure + Default>(
    tag_id: i32,
    modules: &mut [ModuleFile],
) -> Result<Option<T>> {
    for module in modules.iter_mut() {
        for idx in 0..module.files.len() {
            if module.files[idx].tag_id == tag_id {
                let tag = module.read_tag(idx as u32)?;
                if let Some(tag) = tag {
                    let mat = tag.read_metadata::<T>()?;
                    return Ok(Some(mat));
                }
            }
            module.files[idx].data_stream = None;
        }
    }
    Ok(None)
}

pub(crate) fn get_tags_w_index<T: TagStructure + Default>(
    tag_group: &str,
    module: &mut ModuleFile,
    module_index: usize,
) -> Result<HashMap<(usize, usize, i32), T>> {
    let mut tags = HashMap::new();
    for idx in 0..module.files.len() {
        if module.files[idx].tag_group == tag_group {
            let tag = module.read_tag(idx as u32)?;
            if let Some(tag) = tag {
                let mat = tag.read_metadata::<T>()?;
                tags.insert((module_index, idx, tag.tag_id), mat);
            }
        }
        module.files[idx].data_stream = None;
    }
    Ok(tags)
}

pub(crate) fn get_strings(path: &str) -> Result<HashMap<i32, String>> {
    let string_file = File::open(path)?;
    let strings = BufReader::new(string_file);
    let mut string_mappings = HashMap::new();
    for line in strings.lines().map_while(Result::ok) {
        let string_id = line.split_once(":");
        if let Some((id, string)) = string_id {
            string_mappings.insert(id.parse::<i32>()?, string.to_string());
        }
    }
    Ok(string_mappings)
}
