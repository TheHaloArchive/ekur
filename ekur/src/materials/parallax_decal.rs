/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use anyhow::Result;

use crate::definitions::material::MaterialTag;

use super::{
    common_utils::{f32_from_const, get_post_texture},
    serde_definitions::{DecalSlot, Material, ShaderType, TextureType},
};

pub(super) fn handle_parallax_decal(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    let post_process = mat.post_process_definition.elements.first();
    if let Some(post_process) = post_process {
        get_post_texture(post_process, material, 48, TextureType::Control)?;
        get_post_texture(post_process, material, 56, TextureType::Normal)?;
        let top_color = (
            f32_from_const(material, 64)?,
            f32_from_const(material, 68)?,
            f32_from_const(material, 72)?,
        );
        let mid_color = (
            f32_from_const(material, 80)?,
            f32_from_const(material, 84)?,
            f32_from_const(material, 88)?,
        );
        let bot_color = (
            f32_from_const(material, 96)?,
            f32_from_const(material, 100)?,
            f32_from_const(material, 104)?,
        );
        let roughness_white = f32_from_const(material, 108)?;
        let roughness_black = f32_from_const(material, 112)?;
        let metallic = f32_from_const(material, 116)?;
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
    };
    Ok(())
}
