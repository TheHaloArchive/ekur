/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use anyhow::Result;

use crate::definitions::material::MaterialPostProcessing;

use super::{
    common_utils::{f32_from_const, get_post_texture},
    serde_definitions::{ColorDecal, Material, ShaderType, TextureType},
};

pub(super) fn handle_color_decal(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut color_decal = ColorDecal::default();
    get_post_texture(post_process, material, 12, TextureType::Color)?;
    color_decal.opacity = f32_from_const(material, 0)?;
    color_decal.roughness = f32_from_const(material, 4)?;
    color_decal.metallic = f32_from_const(material, 8)?;
    material.color_decal = Some(color_decal);
    material.shader_type = ShaderType::ColorDecal;
    Ok(())
}

pub(super) fn handle_color_decal_forge(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut color_decal = ColorDecal::default();
    get_post_texture(post_process, material, 24, TextureType::Color)?;
    color_decal.opacity = f32_from_const(material, 12)?;
    color_decal.roughness = f32_from_const(material, 16)?;
    color_decal.metallic = f32_from_const(material, 20)?;
    material.color_decal = Some(color_decal);
    material.shader_type = ShaderType::ColorDecal;
    Ok(())
}
