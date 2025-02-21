/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::materials::serde_definitions::ShaderType;
use anyhow::Result;

use crate::definitions::material::MaterialTag;

use super::{
    common_utils::{f32_from_const, get_post_texture},
    serde_definitions::{ConemappedLevel, Material, TextureType},
};

pub(super) fn handle_banished_metal(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    let mut conemapped_level = ConemappedLevel::default();
    let Some(post) = mat.post_process_definition.elements.first() else {
        return Ok(());
    };
    get_post_texture(post, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post, material, 32, TextureType::MacroNormal)?;
    get_post_texture(post, material, 68, TextureType::MacroCohmap)?;
    get_post_texture(post, material, 100, TextureType::MacroConemap)?;
    get_post_texture(post, material, 144, TextureType::NoiseTexture)?;
    get_post_texture(post, material, 228, TextureType::Normal)?;
    get_post_texture(post, material, 256, TextureType::Control)?;
    get_post_texture(post, material, 384, TextureType::SharedControl)?;
    get_post_texture(post, material, 416, TextureType::BurntGradient)?;

    conemapped_level.macro_mask_transform =
        [f32_from_const(material, 16)?, f32_from_const(material, 20)?];

    conemapped_level.macro_normal_transform =
        [f32_from_const(material, 48)?, f32_from_const(material, 52)?];

    conemapped_level.macro_normal_intensity = f32_from_const(material, 64)?;
    conemapped_level.macro_cohmap_transform =
        [f32_from_const(material, 80)?, f32_from_const(material, 84)?];
    conemapped_level.macro_height_scale = f32_from_const(material, 96)?;
    conemapped_level.macro_conemap_transform = [
        f32_from_const(material, 112)?,
        f32_from_const(material, 116)?,
    ];

    conemapped_level.macro_cone_depth = f32_from_const(material, 128)?;
    conemapped_level.macro_cone_offset = f32_from_const(material, 132)?;
    conemapped_level.macro_cone_quality = f32_from_const(material, 136)?;
    conemapped_level.macro_noise_transform = [
        f32_from_const(material, 160)?,
        f32_from_const(material, 164)?,
    ];
    conemapped_level.macro_noise_color = [
        f32_from_const(material, 176)?,
        f32_from_const(material, 180)?,
        f32_from_const(material, 184)?,
    ];
    conemapped_level.macro_noise_roughness = f32_from_const(material, 188)?;
    conemapped_level.macro_noise_remap_white = f32_from_const(material, 200)?;
    conemapped_level.macro_noise_remap_black = f32_from_const(material, 204)?;
    conemapped_level.macro_noise_detail_remap_white = f32_from_const(material, 208)?;
    conemapped_level.macro_noise_detail_remap_black = f32_from_const(material, 212)?;
    conemapped_level.macro_noise_opacity = f32_from_const(material, 216)?;
    conemapped_level.base_normal_intensity = f32_from_const(material, 224)?;
    conemapped_level.base_normal_transform = [
        f32_from_const(material, 240)?,
        f32_from_const(material, 244)?,
    ];
    conemapped_level.base_control_transform = [
        f32_from_const(material, 272)?,
        f32_from_const(material, 276)?,
    ];
    conemapped_level.base_height_scale = f32_from_const(material, 288)?;
    conemapped_level.base_top_color = [
        f32_from_const(material, 292)?,
        f32_from_const(material, 296)?,
        f32_from_const(material, 300)?,
    ];
    conemapped_level.base_mid_color = [
        f32_from_const(material, 304)?,
        f32_from_const(material, 308)?,
        f32_from_const(material, 312)?,
    ];
    conemapped_level.base_bottom_color = [
        f32_from_const(material, 320)?,
        f32_from_const(material, 324)?,
        f32_from_const(material, 328)?,
    ];
    conemapped_level.base_roughness_white = f32_from_const(material, 332)?;
    conemapped_level.base_roughness_black = f32_from_const(material, 336)?;
    conemapped_level.base_metallic = f32_from_const(material, 340)?;
    conemapped_level.base_curvature_height_influence = f32_from_const(material, 344)?;

    conemapped_level.base_edge_wear_offset = f32_from_const(material, 348)?;
    conemapped_level.base_edge_wear_contrast = f32_from_const(material, 352)?;
    conemapped_level.base_edge_wear_offset = f32_from_const(material, 356)?;
    conemapped_level.base_edge_wear_color = [
        f32_from_const(material, 368)?,
        f32_from_const(material, 372)?,
        f32_from_const(material, 376)?,
    ];
    conemapped_level.base_edge_wear_roughness = f32_from_const(material, 380)?;

    conemapped_level.shared_control_transform = [
        f32_from_const(material, 400)?,
        f32_from_const(material, 404)?,
    ];
    conemapped_level.burnt_gradient_transform = [
        f32_from_const(material, 432)?,
        f32_from_const(material, 436)?,
    ];
    conemapped_level.layer2_height_scale = f32_from_const(material, 448)?;
    conemapped_level.char_height_scale = f32_from_const(material, 452)?;
    conemapped_level.char_height_offset = f32_from_const(material, 456)?;
    conemapped_level.char_height_offset = f32_from_const(material, 460)?;
    conemapped_level.char_top_color = [
        f32_from_const(material, 464)?,
        f32_from_const(material, 468)?,
        f32_from_const(material, 472)?,
    ];
    conemapped_level.char_mid_color = [
        f32_from_const(material, 480)?,
        f32_from_const(material, 484)?,
        f32_from_const(material, 488)?,
    ];
    conemapped_level.char_bot_color = [
        f32_from_const(material, 496)?,
        f32_from_const(material, 500)?,
        f32_from_const(material, 504)?,
    ];
    conemapped_level.char_roughness_white = f32_from_const(material, 508)?;
    conemapped_level.char_roughness_black = f32_from_const(material, 512)?;

    conemapped_level.rust_height_scale = f32_from_const(material, 516)?;
    conemapped_level.rust_height_offset = f32_from_const(material, 520)?;
    conemapped_level.rust_staining_offset = f32_from_const(material, 524)?;
    conemapped_level.rust_falloff_color = [
        f32_from_const(material, 528)?,
        f32_from_const(material, 532)?,
        f32_from_const(material, 536)?,
    ];
    conemapped_level.rust_heavy_rust_offset = f32_from_const(material, 540)?;
    conemapped_level.rust_heavy_rust_falloff_paint_opacity = f32_from_const(material, 544)?;
    conemapped_level.rust_secondary_top_color = [
        f32_from_const(material, 548)?,
        f32_from_const(material, 552)?,
        f32_from_const(material, 556)?,
    ];
    conemapped_level.rust_secondary_mid_color = [
        f32_from_const(material, 560)?,
        f32_from_const(material, 564)?,
        f32_from_const(material, 568)?,
    ];
    conemapped_level.rust_secondary_bottom_color = [
        f32_from_const(material, 576)?,
        f32_from_const(material, 580)?,
        f32_from_const(material, 584)?,
    ];
    conemapped_level.rust_secondary_color_start = f32_from_const(material, 588)?;
    conemapped_level.rust_secondary_color_end = f32_from_const(material, 592)?;
    conemapped_level.rust_top_color = [
        f32_from_const(material, 596)?,
        f32_from_const(material, 600)?,
        f32_from_const(material, 604)?,
    ];
    conemapped_level.rust_mid_color = [
        f32_from_const(material, 608)?,
        f32_from_const(material, 612)?,
        f32_from_const(material, 616)?,
    ];
    conemapped_level.rust_bottom_color = [
        f32_from_const(material, 624)?,
        f32_from_const(material, 628)?,
        f32_from_const(material, 632)?,
    ];
    conemapped_level.rust_normal_intensity_new = f32_from_const(material, 636)?;
    conemapped_level.rust_heavy_rust_edge_start = f32_from_const(material, 640)?;
    conemapped_level.rust_heavy_rust_edge_end = f32_from_const(material, 644)?;
    conemapped_level.rust_roughness_white = f32_from_const(material, 648)?;
    conemapped_level.rust_roughness_black = f32_from_const(material, 652)?;
    conemapped_level.rust_metallic = f32_from_const(material, 656)?;
    conemapped_level.burnt_height_offset = f32_from_const(material, 660)?;
    conemapped_level.burnt_opacity = f32_from_const(material, 664)?;
    material.shader_type = ShaderType::ConesteppedLevel;
    material.conemapped_level = Some(conemapped_level);
    Ok(())
}
