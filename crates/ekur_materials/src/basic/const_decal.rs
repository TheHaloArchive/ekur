/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use anyhow::Result;

use crate::utils::{f32_from_const, get_post_texture};
use crate::{DecalSlot, Material, ShaderType, TextureType};
use ekur_definitions::material::MaterialPostProcessing;

pub(crate) fn handle_const_decal(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    get_post_texture(post_process, material, 0, TextureType::Control)?;
    get_post_texture(post_process, material, 8, TextureType::Normal)?;
    let top_color = (
        f32_from_const(material, 16)?,
        f32_from_const(material, 20)?,
        f32_from_const(material, 24)?,
    );
    let mid_color = (
        f32_from_const(material, 32)?,
        f32_from_const(material, 36)?,
        f32_from_const(material, 40)?,
    );
    let bot_color = (
        f32_from_const(material, 48)?,
        f32_from_const(material, 52)?,
        f32_from_const(material, 56)?,
    );
    let roughness_white = f32_from_const(material, 60)?;
    let roughness_black = f32_from_const(material, 64)?;
    let metallic = f32_from_const(material, 68)?;
    let decal_slot = DecalSlot {
        top_color,
        mid_color,
        bot_color,
        roughness_white,
        roughness_black,
        metallic,
    };
    material.decal_slots = Some(decal_slot);
    material.shader_type = ShaderType::Decal;
    Ok(())
}
