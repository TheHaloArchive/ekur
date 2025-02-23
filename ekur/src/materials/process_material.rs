/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;

use crate::definitions::material::MaterialTag;

use super::{
    banished_metal::handle_banished_metal,
    color_decal::handle_color_decal,
    common_utils::collect_constants,
    conestepped_decal::handle_conestepped_decal,
    const_decal::handle_const_decal,
    decal_mp::handle_mp_decal,
    diffuse_shader::{handle_diffuse_shader, handle_diffuse_si_shader},
    layered_shader::{add_style_info, collect_textures},
    parallax_decal::handle_parallax_decal,
    self_illum::handle_illum,
    serde_definitions::{Material, TextureType},
};

pub fn process_materials(
    materials: &HashMap<i32, MaterialTag>,
    save_path: &str,
) -> Result<Vec<(TextureType, i32)>> {
    let mut all_textures = Vec::new();
    for (id, mat) in materials.iter() {
        let mut material = Material::default();
        collect_constants(mat, &mut material)?;
        add_style_info(mat, &mut material)?;
        collect_textures(None, &mut material, mat)?;
        match mat.material_shader.global_id {
            1102829229 | 52809748 => handle_diffuse_shader(mat, &mut material)?,
            -1051699871 | -1659664443 => handle_diffuse_si_shader(mat, &mut material)?,
            -51713036 | 690034699 | 2003821059 | -2003821059 => {
                handle_const_decal(mat, &mut material)?
            }
            -131335022 => handle_mp_decal(mat, &mut material)?,
            -93074746 => handle_parallax_decal(mat, &mut material)?,
            -79437929 => handle_illum(mat, &mut material)?,
            -232573636 => handle_banished_metal(mat, &mut material)?,
            317783742 => handle_color_decal(mat, &mut material)?,
            -557915351 => handle_conestepped_decal(mat, &mut material)?,
            _ => {}
        };

        let mut path = PathBuf::from(format!("{save_path}/materials"));
        path.push(id.to_string());
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &material)?;
        all_textures.extend(material.textures);
    }
    Ok(all_textures)
}
