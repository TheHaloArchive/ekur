/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use anyhow::Result;
use ekur_definitions::material::MaterialPostProcessing;

use crate::{
    utils::{bool_from_const, f32_from_const, get_post_texture, i32_from_const},
    {ForerunnerLayered, Material, ShaderType, TextureType},
};

pub(crate) fn handle_forerunner_layered(
    post: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut params = ForerunnerLayered::default();

    get_post_texture(post, material, 0, TextureType::Normal)?; // layer1 normal
    get_post_texture(post, material, 32, TextureType::MacroMaskMap)?;
    get_post_texture(post, material, 84, TextureType::MacroConemap)?;
    get_post_texture(post, material, 132, TextureType::MacroCohmap)?;
    get_post_texture(post, material, 160, TextureType::AORoughnessTransmission)?; // ROHG
    get_post_texture(post, material, 240, TextureType::Color)?; // macro graphic
    get_post_texture(post, material, 308, TextureType::Mask0)?; // submask
    get_post_texture(post, material, 516, TextureType::Mask1)?; // staining ROHG
    get_post_texture(post, material, 712, TextureType::Layer2DetailNormal)?;
    get_post_texture(post, material, 736, TextureType::Layer2Control)?;
    get_post_texture(post, material, 896, TextureType::Layer3DetailNormal)?;
    get_post_texture(post, material, 928, TextureType::Layer3Control)?;
    get_post_texture(post, material, 1124, TextureType::Layer4Control)?;
    get_post_texture(post, material, 1152, TextureType::Cubemap)?;

    params.layer1_normal_texture_transform = [
        f32_from_const(material, 16)?,
        f32_from_const(material, 20)?,
        f32_from_const(material, 24)?,
        f32_from_const(material, 28)?,
    ];

    params.macro_mask_map_texture_transform = [
        f32_from_const(material, 48)?,
        f32_from_const(material, 52)?,
        f32_from_const(material, 56)?,
        f32_from_const(material, 60)?,
    ];

    params.layer1_enable_normal_mirror_bitmap_transform = bool_from_const(material, 64)?;
    params.layer1_enable_normal_mirror_y_bitmap_transform = bool_from_const(material, 68)?;

    params.layer1_bitmap_transform_scale =
        [f32_from_const(material, 72)?, f32_from_const(material, 76)?];

    params.layer1_normal_intensity = f32_from_const(material, 80)?;

    params.layer1_cone_texture_texture_transform = [
        f32_from_const(material, 96)?,
        f32_from_const(material, 100)?,
        f32_from_const(material, 104)?,
        f32_from_const(material, 108)?,
    ];

    params.cone_offset = f32_from_const(material, 112)?;
    params.layer1_cone_depth = f32_from_const(material, 116)?;
    params.layer1_cone_quality = f32_from_const(material, 120)?;
    params.layer1_conestep_fade_start = f32_from_const(material, 124)?;
    params.layer1_conestep_fade_end = f32_from_const(material, 128)?;

    params.layer1_coh_texture_texture_transform = [
        f32_from_const(material, 144)?,
        f32_from_const(material, 148)?,
        f32_from_const(material, 152)?,
        f32_from_const(material, 156)?,
    ];

    params.layer1_base_rohg_texture_texture_transform = [
        f32_from_const(material, 176)?,
        f32_from_const(material, 180)?,
        f32_from_const(material, 184)?,
        f32_from_const(material, 188)?,
    ];

    params.layer1_color = [
        f32_from_const(material, 192)?,
        f32_from_const(material, 196)?,
        f32_from_const(material, 200)?,
    ];

    params.layer1_color_b = [
        f32_from_const(material, 208)?,
        f32_from_const(material, 212)?,
        f32_from_const(material, 216)?,
    ];

    params.layer1_metallic = f32_from_const(material, 220)?;
    params.layer1_ior = f32_from_const(material, 224)?;
    params.layer1_height_scale = f32_from_const(material, 228)?;
    params.layer1_base_roughness = f32_from_const(material, 232)?;
    params.layer1_curvature_roughness_add = f32_from_const(material, 236)?;

    params.layer1_macro_graphic_texture_transform = [
        f32_from_const(material, 256)?,
        f32_from_const(material, 260)?,
        f32_from_const(material, 264)?,
        f32_from_const(material, 268)?,
    ];

    params.layer1_macro_graphic_uv = i32_from_const(material, 272)?;
    params.layer1_macro_graphic_offset = f32_from_const(material, 276)?;
    params.layer1_macro_graphic_blend_contrast = f32_from_const(material, 280)?;
    params.layer1_macro_graphic_pattern_masking = f32_from_const(material, 284)?;
    params.layer1_macro_pattern_opacity = f32_from_const(material, 288)?;

    params.layer1_macro_graphic_color = [
        f32_from_const(material, 292)?,
        f32_from_const(material, 296)?,
        f32_from_const(material, 300)?,
    ];

    params.layer1_macro_roughness = f32_from_const(material, 304)?;

    params.layer1_submask_texture_transform = [
        f32_from_const(material, 320)?,
        f32_from_const(material, 324)?,
        f32_from_const(material, 328)?,
        f32_from_const(material, 332)?,
    ];

    params.layer1_primary_graphic_offset = f32_from_const(material, 336)?;
    params.layer1_primary_graphic_blend_contrast = f32_from_const(material, 340)?;
    params.layer1_primary_graphic_opacity = f32_from_const(material, 344)?;

    params.layer1_primary_graphic_color = [
        f32_from_const(material, 352)?,
        f32_from_const(material, 356)?,
        f32_from_const(material, 360)?,
    ];

    params.layer1_primary_graphic_color_b = [
        f32_from_const(material, 368)?,
        f32_from_const(material, 372)?,
        f32_from_const(material, 376)?,
    ];

    params.layer1_primary_graphic_roughness = f32_from_const(material, 380)?;

    params.layer1_secondary_graphic_offset = f32_from_const(material, 384)?;
    params.layer1_secondary_graphic_blend_contrast = f32_from_const(material, 388)?;
    params.layer1_secondary_pattern_opacity = f32_from_const(material, 392)?;

    params.layer1_emissive_color = [
        f32_from_const(material, 400)?,
        f32_from_const(material, 404)?,
        f32_from_const(material, 408)?,
    ];

    params.emissive_enable_single_float_colors = bool_from_const(material, 412)?;

    params.layer1_secondary_graphic_color = [
        f32_from_const(material, 416)?,
        f32_from_const(material, 420)?,
        f32_from_const(material, 424)?,
    ];

    params.color_r = f32_from_const(material, 428)?;
    params.color_g = f32_from_const(material, 432)?;
    params.color_b = f32_from_const(material, 436)?;

    material.forerunner_layered = Some(params);
    material.shader_type = ShaderType::ForerunnerLayered;
    Ok(())
}
