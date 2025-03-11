/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use anyhow::Result;

use crate::definitions::material::MaterialPostProcessing;

use super::{
    common_utils::{f32_from_const, get_post_texture},
    serde_definitions::{Hair, Material, ShaderType, TextureType},
};

pub(super) fn handle_hair_shader(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut hair_shader = Hair::default();
    get_post_texture(post_process, material, 48, TextureType::Color)?;
    get_post_texture(post_process, material, 92, TextureType::Control)?;
    get_post_texture(post_process, material, 144, TextureType::Normal)?;
    get_post_texture(post_process, material, 224, TextureType::AO)?;
    hair_shader.tint_color = (
        f32_from_const(material, 80)?,
        f32_from_const(material, 84)?,
        f32_from_const(material, 88)?,
    );
    hair_shader.roughness_white = f32_from_const(material, 128)?;
    hair_shader.roughness_black = f32_from_const(material, 132)?;
    hair_shader.ior = f32_from_const(material, 136)?;
    material.hair = Some(hair_shader);
    material.shader_type = ShaderType::Hair;
    Ok(())
}
