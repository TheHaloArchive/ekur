/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use anyhow::Result;
use ekur_definitions::material::MaterialPostProcessing;

use crate::utils::{f32_from_const, get_post_texture};

use crate::{Material, SelfIllum, ShaderType, TextureType};

pub(crate) fn handle_illum(post: &MaterialPostProcessing, material: &mut Material) -> Result<()> {
    material.shader_type = ShaderType::SelfIllum;
    get_post_texture(post, material, 0, TextureType::Color)?;
    get_post_texture(post, material, 48, TextureType::AlphaMap)?;
    let color = (
        f32_from_const(material, 32)?,
        f32_from_const(material, 36)?,
        f32_from_const(material, 40)?,
    );
    let intensity = f32_from_const(material, 44)?;
    let opacity = f32_from_const(material, 64)?;
    let illum = SelfIllum {
        color,
        intensity,
        opacity,
    };
    material.illum_info = Some(illum);
    Ok(())
}

pub(crate) fn handle_illum_full(material: &mut Material) -> Result<()> {
    material.shader_type = ShaderType::SelfIllum;
    let color = (
        f32_from_const(material, 0)?,
        f32_from_const(material, 4)?,
        f32_from_const(material, 8)?,
    );
    let intensity = f32_from_const(material, 12)?;
    let opacity = 1.0;
    let illum = SelfIllum {
        color,
        intensity,
        opacity,
    };
    material.illum_info = Some(illum);
    Ok(())
}
