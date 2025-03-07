/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;

use crate::definitions::material::{MaterialTag, MaterialTagCampaign};

use super::{
    banished_metal::handle_banished_metal,
    color_decal::{handle_color_decal, handle_color_decal_forge},
    common_utils::collect_constants,
    conestepped_decal::handle_conestepped_decal,
    const_decal::handle_const_decal,
    decal_mp::handle_mp_decal,
    diffuse_shader::{
        handle_diffuse_billboard_shader, handle_diffuse_decal_notint_shader,
        handle_diffuse_decal_shader, handle_diffuse_emissive_shader, handle_diffuse_shader,
        handle_diffuse_si_shader,
    },
    eye_shader::handle_eye_shader,
    layered_shader::{add_style_info, add_style_info_campaign, collect_textures},
    meter_shader::handle_meter_shader,
    parallax_decal::handle_parallax_decal,
    self_illum::{handle_illum, handle_illum_full},
    serde_definitions::{Material, TextureType},
    skin_shader::handle_skin,
};

pub fn process_materials(
    materials: &HashMap<i32, MaterialTag>,
    save_path: &str,
) -> Result<Vec<(TextureType, i32)>> {
    let mut all_textures = Vec::new();
    for (id, mat) in materials.iter() {
        let mut material = Material::default();
        let post_process = mat.post_process_definition.elements.first();
        let post_process = if let Some(post) = post_process {
            post
        } else {
            continue;
        };
        collect_constants(post_process, &mut material)?;
        add_style_info(mat, &mut material)?;
        collect_textures(None, &mut material, &mat.material_parameters.elements)?;

        match mat.material_shader.global_id {
            1102829229 | 52809748 | 340368681 | 1514907409 => {
                handle_diffuse_shader(post_process, &mut material)?
            }
            -1051699871 | -1659664443 => handle_diffuse_si_shader(post_process, &mut material)?,
            -51713036 | 690034699 | 2003821059 | -2003821059 | 1996403871 => {
                handle_const_decal(post_process, &mut material)?
            }
            -131335022 => handle_mp_decal(
                post_process,
                &mut material,
                &mat.material_parameters.elements,
            )?,
            -93074746 => handle_parallax_decal(post_process, &mut material)?,
            -79437929 => handle_illum(post_process, &mut material)?,
            -232573636 => handle_banished_metal(post_process, &mut material)?,
            317783742 => handle_color_decal(post_process, &mut material)?,
            -557915351 => handle_conestepped_decal(post_process, &mut material)?,
            2055304184 => handle_diffuse_billboard_shader(post_process, &mut material)?,
            1014564527 => handle_diffuse_emissive_shader(post_process, &mut material)?,
            -1648222720 | 1656409392 | -1492085200 => {
                handle_diffuse_decal_shader(post_process, &mut material)?
            }
            -1185995257 => handle_diffuse_decal_notint_shader(post_process, &mut material)?,
            1081175655 => handle_color_decal_forge(post_process, &mut material)?,
            2006960401 => handle_illum_full(&mut material)?,
            -648442023 => handle_meter_shader(post_process, &mut material)?,
            -1825366364 | 1644211276 | -989555086 => handle_skin(post_process, &mut material)?,
            -483456698 => handle_eye_shader(post_process, &mut material)?,
            _ => {}
        };
        material.shader = mat.material_shader.global_id;
        material.alpha_blend_mode = format!("{:?}", mat.alpha_blend_mode.0);
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

pub fn process_materials_campaign(
    materials: &HashMap<i32, MaterialTagCampaign>,
    save_path: &str,
) -> Result<Vec<(TextureType, i32)>> {
    let mut all_textures = Vec::new();
    for (id, mat) in materials.iter() {
        let mut material = Material::default();
        let post_process = mat.post_process_definition.elements.first();
        let post_process = if let Some(post) = post_process {
            post
        } else {
            continue;
        };

        collect_constants(post_process, &mut material)?;
        add_style_info_campaign(mat, &mut material)?;
        collect_textures(None, &mut material, &mat.material_parameters.elements)?;
        material.shader = mat.material_shader.global_id;
        material.alpha_blend_mode = format!("{:?}", mat.alpha_blend_mode.0);
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
