/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use anyhow::Result;
use ekur_definitions::material::MaterialPostProcessing;

use crate::utils::{f32_from_const, get_post_texture};

use crate::{ColorTintDecal, Material, ShaderType, TextureType};

pub(crate) fn handle_color_tint_decal(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut color_decal = ColorTintDecal::default();
    get_post_texture(post_process, material, 60, TextureType::Color)?;
    get_post_texture(post_process, material, 16, TextureType::Normal)?;
    color_decal.opacity = f32_from_const(material, 12)?;
    color_decal.roughness = f32_from_const(material, 52)?;
    color_decal.metallic = f32_from_const(material, 56)?;
    color_decal.normal_intensity = f32_from_const(material, 48)?;
    color_decal.tint_color = (
        f32_from_const(material, 0)?,
        f32_from_const(material, 4)?,
        f32_from_const(material, 8)?,
    );
    material.color_tint_decal = Some(color_decal);
    material.shader_type = ShaderType::ColorTintDecal;
    Ok(())
}

pub(crate) fn handle_color_notint_decal(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut color_decal = ColorTintDecal::default();
    get_post_texture(post_process, material, 44, TextureType::Color)?;
    get_post_texture(post_process, material, 4, TextureType::Normal)?;
    color_decal.opacity = f32_from_const(material, 0)?;
    color_decal.roughness = f32_from_const(material, 36)?;
    color_decal.metallic = f32_from_const(material, 40)?;
    color_decal.normal_intensity = f32_from_const(material, 32)?;
    color_decal.tint_color = (1.0, 1.0, 1.0);
    material.color_tint_decal = Some(color_decal);
    material.shader_type = ShaderType::ColorTintDecal;
    Ok(())
}
