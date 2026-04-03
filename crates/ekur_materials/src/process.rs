/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::{
    Material,
    basic::{
        banished_metal::handle_banished_metal,
        color_decal::{handle_color_decal, handle_color_decal_forge},
        conestepped_decal::handle_conestepped_decal,
        const_decal::handle_const_decal,
        decal_mp::handle_mp_decal,
        diffuse_shader::{
            handle_diffuse_billboard_shader, handle_diffuse_decal_notint_shader,
            handle_diffuse_decal_shader, handle_diffuse_emissive_shader, handle_diffuse_shader,
            handle_diffuse_si_shader, handle_diffuse_si_shader_norough,
        },
        eye_shader::handle_eye_shader,
        forerunner_layered::handle_forerunner_layered,
        forest_gold::handle_forest_gold,
        hair::handle_hair_shader,
        meter_shader::handle_meter_shader,
        parallax_decal::handle_parallax_decal,
        self_illum::{handle_illum, handle_illum_full},
        skin_shader::handle_skin,
        wetness_layered::handle_wetness_layered,
    },
    layered::layered_shader::{add_style_info, add_style_info_campaign, collect_textures},
    utils::collect_constants,
};
use ekur_definitions::material::MaterialTag;
use ekur_definitions::material::MaterialTagCampaign;

use anyhow::Result;

pub fn process_material(material_tag: &MaterialTag) -> Result<Material> {
    let mut material = Material::default();
    let post_process = material_tag.post_process_definition.elements.first();
    let Some(post_process) = post_process else {
        return Ok(material);
    };
    collect_constants(post_process, &mut material)?;
    add_style_info(material_tag, &mut material)?;
    collect_textures(
        None,
        &mut material,
        &material_tag.material_parameters.elements,
    )?;

    match material_tag.material_shader.global_id {
        1102829229 | 52809748 | 340368681 | 1514907409 | -1825069108 => {
            handle_diffuse_shader(post_process, &mut material)?
        }
        -1051699871 | -1659664443 => handle_diffuse_si_shader(post_process, &mut material)?,
        -51713036 | 690034699 | 2003821059 | -2003821059 | 1996403871 | -697609548 => {
            handle_const_decal(post_process, &mut material)?
        }
        -131335022 | 195584229 => handle_mp_decal(
            post_process,
            &mut material,
            &material_tag.material_parameters.elements,
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
        -1825366364 | 1644211276 | -989555086 | -95283743 | -1663998616 => {
            handle_skin(post_process, &mut material)?
        }
        -483456698 => handle_eye_shader(post_process, &mut material)?,
        -1187376535 => handle_hair_shader(post_process, &mut material)?,
        1855121939 => handle_diffuse_si_shader_norough(post_process, &mut material)?,
        1228155841 => handle_forerunner_layered(post_process, &mut material)?,
        376733134 => handle_forest_gold(post_process, &mut material)?,
        1830164087 => handle_wetness_layered(post_process, &mut material)?,
        _ => {}
    };
    material.shader = material_tag.material_shader.global_id;
    material.alpha_blend_mode = format!("{:?}", material_tag.alpha_blend_mode.0);
    Ok(material)
}

pub fn process_material_campaign(material_tag: &MaterialTagCampaign) -> Result<Material> {
    let mut material = Material::default();
    let post_process = material_tag.post_process_definition.elements.first();
    let Some(post_process) = post_process else {
        return Ok(material);
    };

    collect_constants(post_process, &mut material)?;
    add_style_info_campaign(material_tag, &mut material)?;
    collect_textures(
        None,
        &mut material,
        &material_tag.material_parameters.elements,
    )?;
    material.shader = material_tag.material_shader.global_id;
    material.alpha_blend_mode = format!("{:?}", material_tag.alpha_blend_mode.0);
    Ok(material)
}
