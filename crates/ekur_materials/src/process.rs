/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::{
    Material,
    basic::{
        color_decal::{handle_color_decal, handle_color_decal_forge},
        color_tint_decal::{handle_color_notint_decal, handle_color_tint_decal},
        const_decal::handle_const_decal,
        decal_mp::handle_mp_decal,
        diffuse_shader::{
            handle_diffuse_billboard_shader, handle_diffuse_decal_notint_shader,
            handle_diffuse_decal_shader, handle_diffuse_emissive_shader, handle_diffuse_shader,
            handle_diffuse_si_shader, handle_diffuse_si_shader_norough,
        },
        eye_shader::handle_eye_shader,
        hair::handle_hair_shader,
        meter_shader::handle_meter_shader,
        parallax_decal::handle_parallax_decal,
        self_illum::{handle_illum, handle_illum_full},
        skin_shader::handle_skin,
    },
    layered::{
        layered_level::{
            handle_rohg_rohg_alpha_alt, handle_rohg_rohg_rohg_rohg_mm, handle_rohg_rohg_rohg_rohm,
            handle_rohg_rohg_rohg_rohm_mm, handle_rohg_rohg_rohm_nnhg_mm,
            handle_rohg_rohg_rohm_rohg, handle_rohg_rohm_rohg_rohm_mm, handle_rohg_rohm_rohm_cone,
            handle_rohg_rohm_rohm_mm_color, handle_rohg_rohm_rohm_nnhg_mm, handle_rohm_alpha,
            handle_rohm_cone, handle_rohm_nnhg_cone, handle_rohm_rohg_cone, handle_rohm_rohg_nnhg,
            handle_rohm_rohg_rohg_rohg_mm, handle_rohm_rohg_rohg_rohg_mm_alt,
            handle_rohm_rohg_rohg_rohm, handle_rohm_rohg_rohg_rohm_mm,
            handle_rohm_rohg_rohg_rohm_mm_alt, handle_rohm_rohg_rohm_mm_alpha,
            handle_rohm_rohg_rohm_rohm_mm_cone, handle_rohm_rohm_nnhg_nnhg,
            handle_rohm_rohm_nnhg_nnhg_mm, handle_rohm_rohm_nnhg_nnhg_mm_color,
            handle_rohm_rohm_rohg_nnhg, handle_rohm_rohm_rohg_rohg_mm, handle_rohm_rohm_rohm_mm,
            handle_rohm_rohm_rohm_nnhg, handle_rohm_rohm_rohm_nnhg_mm_color,
            handle_rohm_rohm_rohm_rohg_mm,
        },
        layered_shader::{add_style_info, add_style_info_campaign, collect_textures},
    },
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
        317783742 => handle_color_decal(post_process, &mut material)?,
        2055304184 => handle_diffuse_billboard_shader(post_process, &mut material)?,
        1014564527 => handle_diffuse_emissive_shader(post_process, &mut material)?,
        -1648222720 | 1656409392 | -1492085200 | -1458013003 | 2085772820 => {
            handle_diffuse_decal_shader(post_process, &mut material)?
        }
        -947343524 => handle_rohg_rohg_rohg_rohm_mm(post_process, &mut material)?,
        2008195483 => handle_rohm_rohm_nnhg_nnhg_mm(post_process, &mut material)?,
        438536334 => handle_rohm_rohg_rohm_rohm_mm_cone(post_process, &mut material)?,
        -1185995257 => handle_diffuse_decal_notint_shader(post_process, &mut material)?,
        1081175655 | 991432226 => handle_color_decal_forge(post_process, &mut material)?,
        2006960401 => handle_illum_full(&mut material)?,
        -648442023 => handle_meter_shader(post_process, &mut material)?,
        -1825366364 | 1644211276 | -989555086 | -95283743 | -1663998616 | -1380774585 => {
            handle_skin(post_process, &mut material)?
        }
        -661688748 => handle_rohg_rohg_rohg_rohg_mm(post_process, &mut material, false)?,
        281877372 => handle_rohg_rohg_rohm_rohg(post_process, &mut material)?,
        1689556590 => handle_rohg_rohg_rohg_rohm(post_process, &mut material)?,
        -739576559 => handle_rohm_rohg_nnhg(post_process, &mut material)?,
        43664280 => handle_rohm_rohg_rohg_rohm(post_process, &mut material)?,
        -613067308 => handle_rohm_rohm_rohm_nnhg(post_process, &mut material)?,
        -521185921 => handle_rohm_rohm_rohm_mm(post_process, &mut material)?,
        1111433296 => handle_rohm_rohg_rohg_rohm_mm_alt(post_process, &mut material)?,
        2138702411 => handle_rohg_rohg_rohm_nnhg_mm(post_process, &mut material)?,
        -593060668 => handle_rohg_rohm_rohm_nnhg_mm(post_process, &mut material)?,
        -1420447106 => handle_rohm_rohm_rohg_nnhg(post_process, &mut material)?,
        877439063 => handle_rohm_rohm_rohg_rohg_mm(post_process, &mut material)?,
        -483456698 => handle_eye_shader(post_process, &mut material)?,
        -1187376535 => handle_hair_shader(post_process, &mut material)?,
        1855121939 => handle_diffuse_si_shader_norough(post_process, &mut material)?,
        -338864971 => handle_rohg_rohm_rohm_mm_color(post_process, &mut material)?,
        -1674484151 => handle_rohm_rohg_cone(post_process, &mut material, true)?,
        -1300928187 => handle_rohm_rohg_cone(post_process, &mut material, false)?,
        -1322925105 => handle_rohm_cone(post_process, &mut material, true)?,
        337507735 | -2067383589 => handle_rohm_rohg_rohg_rohm_mm(post_process, &mut material)?,
        121237379 => handle_rohm_cone(post_process, &mut material, false)?,
        915229326 => handle_rohg_rohm_rohm_cone(post_process, &mut material)?,
        -1061664150 => handle_color_tint_decal(post_process, &mut material)?,
        1513831273 => handle_rohm_nnhg_cone(post_process, &mut material)?,
        -1525938898 => handle_color_notint_decal(post_process, &mut material)?,
        -1054410158 => handle_rohm_rohm_nnhg_nnhg(post_process, &mut material)?,
        1242808444 | 1892746775 => handle_rohm_alpha(post_process, &mut material)?,
        513702545 => handle_rohg_rohg_alpha_alt(post_process, &mut material)?,
        1941810293 => handle_rohm_rohm_nnhg_nnhg_mm_color(post_process, &mut material)?,
        1072858306 => handle_rohm_rohg_rohg_rohg_mm(post_process, &mut material)?,
        -420180489 => handle_rohm_rohm_rohm_rohg_mm(post_process, &mut material)?,
        -899153114 => handle_rohm_rohg_rohm_mm_alpha(post_process, &mut material)?,
        1425254988 => handle_rohm_rohg_rohg_rohg_mm_alt(post_process, &mut material)?,
        540729820 => handle_rohm_rohm_rohm_nnhg_mm_color(post_process, &mut material)?,
        1678208609 => handle_rohg_rohg_rohg_rohg_mm(post_process, &mut material, true)?,
        304925447 => handle_rohg_rohm_rohg_rohm_mm(post_process, &mut material)?,
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
