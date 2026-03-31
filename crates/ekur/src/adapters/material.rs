/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::utils::get_tags;
use ekur_definitions::material::{MaterialTag, MaterialTagCampaign};
use ekur_materials::{
    TextureType,
    process::{process_material, process_material_campaign},
};

use anyhow::Result;
use infinite_rs::ModuleFile;
use std::{
    collections::HashMap,
    fs::{File, create_dir_all},
    io::BufWriter,
    path::PathBuf,
};

const MATERIAL_GROUP: &str = "mat ";

pub(crate) fn extract_materials(
    modules: &mut [ModuleFile],
    save_path: &str,
    is_campaign: bool,
) -> Result<HashMap<i32, TextureType>> {
    let mut save_path = PathBuf::from(save_path);
    save_path.push("materials/");
    create_dir_all(&save_path)?;

    let mut materials = HashMap::new();
    let mut textures = HashMap::new();

    if is_campaign {
        let material_tags = get_tags::<MaterialTagCampaign>(MATERIAL_GROUP, modules)?;
        for mat in material_tags {
            materials.insert(mat.0, process_material_campaign(&mat.1)?);
        }
    } else {
        let material_tags = get_tags::<MaterialTag>(MATERIAL_GROUP, modules)?;
        for mat in material_tags {
            materials.insert(mat.0, process_material(&mat.1)?);
        }
    }

    for (id, mat) in materials {
        save_path.push(id.to_string());
        save_path.add_extension("json");
        let file = File::create(&save_path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &mat)?;
        for (tex_type, tex_id) in mat.textures {
            textures.insert(tex_id, tex_type);
        }
        save_path.pop();
    }
    Ok(textures)
}
