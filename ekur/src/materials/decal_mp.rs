/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use anyhow::Result;

use crate::definitions::material::MaterialTag;

use super::{
    common_utils::{f32_from_const, f32_from_params},
    serde_definitions::{DecalSlot, Material, ShaderType},
};

pub(super) fn handle_mp_decal(mat: &MaterialTag, material: &mut Material) -> Result<()> {
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

    let roughness_white = f32_from_params(mat, -918784873)?;
    let roughness_black = f32_from_params(mat, -1982683011)?;
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
