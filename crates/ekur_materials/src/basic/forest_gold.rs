/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use anyhow::Result;
use ekur_definitions::material::MaterialPostProcessing;

use crate::{
    utils::{bool_from_const, f32_from_const, get_post_texture},
    {ForestGold, Material, ShaderType, TextureType},
};

pub(crate) fn handle_forest_gold(
    post: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut params = ForestGold::default();

    get_post_texture(post, material, 12, TextureType::DetailNormal)?; // layer2 normal
    get_post_texture(post, material, 48, TextureType::Control)?; // layer2 control

    get_post_texture(post, material, 272, TextureType::MacroMaskMap)?;
    get_post_texture(post, material, 304, TextureType::MacroNormal)?;
    get_post_texture(post, material, 336, TextureType::MacroCohmap)?;

    get_post_texture(post, material, 376, TextureType::Color)?; // layer1 color
    get_post_texture(post, material, 400, TextureType::Normal)?; // layer1 normal
    get_post_texture(post, material, 432, TextureType::AORoughnessTransmission)?;
    get_post_texture(post, material, 464, TextureType::Emissive)?;

    get_post_texture(post, material, 672, TextureType::Cubemap)?; // reflection

    params.layer2_enable_color_overlay = bool_from_const(material, 0)?;
    params.layer2_enable_specular = bool_from_const(material, 4)?;
    params.layer2_uvmode_uv3 = bool_from_const(material, 8)?;

    params.layer2_normal_map_texture_transform = [
        f32_from_const(material, 32)?,
        f32_from_const(material, 36)?,
        f32_from_const(material, 40)?,
        f32_from_const(material, 44)?,
    ];

    params.layer2_control_map_texture_transform = [
        f32_from_const(material, 64)?,
        f32_from_const(material, 68)?,
        f32_from_const(material, 72)?,
        f32_from_const(material, 76)?,
    ];

    params.layer2_height_offset = f32_from_const(material, 80)?;
    params.layer2_height_scale = f32_from_const(material, 84)?;
    params.layer2_previous_height_influence = f32_from_const(material, 88)?;
    params.layer2_curvature_height_influence = f32_from_const(material, 92)?;
    params.layer2_occlusion_height_influence = f32_from_const(material, 96)?;
    params.layer2_height_blend_range = f32_from_const(material, 100)?;
    params.layer2_opacity = f32_from_const(material, 104)?;

    params.layer2_top_color = [
        f32_from_const(material, 112)?,
        f32_from_const(material, 116)?,
        f32_from_const(material, 120)?,
    ];
    params.layer2_mid_color = [
        f32_from_const(material, 128)?,
        f32_from_const(material, 132)?,
        f32_from_const(material, 136)?,
    ];
    params.layer2_bottom_color = [
        f32_from_const(material, 144)?,
        f32_from_const(material, 148)?,
        f32_from_const(material, 152)?,
    ];

    params.layer2_enable_secondary_color = bool_from_const(material, 156)?;
    params.layer2_secondary_color_start = f32_from_const(material, 160)?;
    params.layer2_secondary_color_end = f32_from_const(material, 164)?;

    params.layer2_secondary_top_color = [
        f32_from_const(material, 176)?,
        f32_from_const(material, 180)?,
        f32_from_const(material, 184)?,
    ];
    params.layer2_secondary_mid_color = [
        f32_from_const(material, 192)?,
        f32_from_const(material, 196)?,
        f32_from_const(material, 200)?,
    ];
    params.layer2_secondary_bottom_color = [
        f32_from_const(material, 208)?,
        f32_from_const(material, 212)?,
        f32_from_const(material, 216)?,
    ];

    params.layer2_enable_fresnel = bool_from_const(material, 220)?;
    params.layer2_fresnel_color_tint = [
        f32_from_const(material, 224)?,
        f32_from_const(material, 228)?,
        f32_from_const(material, 232)?,
    ];
    params.layer2_fresnel_intensity = f32_from_const(material, 236)?;
    params.layer2_fresnel_exponent = f32_from_const(material, 240)?;
    params.layer2_fresnel_opacity = f32_from_const(material, 244)?;

    params.layer2_roughness_white = f32_from_const(material, 248)?;
    params.layer2_roughness_black = f32_from_const(material, 252)?;
    params.layer2_ior = f32_from_const(material, 256)?;
    params.layer2_metallic = f32_from_const(material, 260)?;

    params.layer1_uvmode_uv3 = bool_from_const(material, 264)?;
    params.macro_uvmode_uv3 = bool_from_const(material, 268)?;

    params.macro_mask_map_texture_transform = [
        f32_from_const(material, 288)?,
        f32_from_const(material, 292)?,
        f32_from_const(material, 296)?,
        f32_from_const(material, 300)?,
    ];

    params.macro_normal_texture_transform = [
        f32_from_const(material, 320)?,
        f32_from_const(material, 324)?,
        f32_from_const(material, 328)?,
        f32_from_const(material, 332)?,
    ];

    params.macro_coh_texture_transform = [
        f32_from_const(material, 352)?,
        f32_from_const(material, 356)?,
        f32_from_const(material, 360)?,
        f32_from_const(material, 364)?,
    ];

    params.macro_normal_intensity = f32_from_const(material, 368)?;
    params.macro_height_scale = f32_from_const(material, 372)?;

    material.forest_gold = Some(params);
    material.shader_type = ShaderType::ForestGold;
    Ok(())
}
