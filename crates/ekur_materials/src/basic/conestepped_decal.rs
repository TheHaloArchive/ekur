/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use anyhow::Result;
use ekur_definitions::material::MaterialPostProcessing;

use crate::utils::{f32_from_const, get_post_texture};

use crate::{ConesteppedDecal, Material, ShaderType, TextureType};

pub(crate) fn handle_conestepped_decal(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut conestepped_decal = ConesteppedDecal::default();
    get_post_texture(post_process, material, 20, TextureType::MacroConemap)?;
    get_post_texture(post_process, material, 48, TextureType::Control)?;
    get_post_texture(post_process, material, 80, TextureType::Normal)?;
    conestepped_decal.normal_intensity = f32_from_const(material, 112)?;
    conestepped_decal.parallax_depth = f32_from_const(material, 0)?;
    conestepped_decal.parallax_height_offset = f32_from_const(material, 4)?;
    material.conestepped_decal = Some(conestepped_decal);
    material.shader_type = ShaderType::ConesteppedDecal;
    Ok(())
}
