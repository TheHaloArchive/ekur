/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::utils::{f32_from_const, f32_from_params, get_post_texture};
use crate::{DecalSlot, Material, ShaderType, TextureType};
use anyhow::Result;
use ekur_definitions::material::{MaterialParameter, MaterialPostProcessing};

pub(crate) fn handle_mp_decal(
    post: &MaterialPostProcessing,
    material: &mut Material,
    parameters: &[MaterialParameter],
) -> Result<()> {
    get_post_texture(post, material, 0, TextureType::Control)?;
    get_post_texture(post, material, 8, TextureType::Normal)?;
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

    let mut roughness_white = f32_from_params(parameters, -918784873)?;
    if roughness_white == 0.0 {
        roughness_white = f32_from_const(material, 60)?;
    }
    let mut roughness_black = f32_from_params(parameters, -1982683011)?;
    if roughness_black == 0.0 {
        roughness_black = f32_from_const(material, 64)?;
    }
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
