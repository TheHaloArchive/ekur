/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use anyhow::Result;

use crate::definitions::material::MaterialTag;

use super::{
    common_utils::{f32_from_const, get_post_texture},
    serde_definitions::{DiffuseInfo, Material, ShaderType, TextureType},
};

pub(super) fn handle_diffuse_shader(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    let post_process = mat.post_process_definition.elements.first();
    let mut diffuse_info = DiffuseInfo::default();
    if let Some(post_process) = post_process {
        material.shader_type = ShaderType::Diffuse;
        get_post_texture(post_process, material, 0, TextureType::Color)?;
        get_post_texture(post_process, material, 60, TextureType::Control)?;
        get_post_texture(post_process, material, 116, TextureType::Normal)?;
        diffuse_info.metallic_white = f32_from_const(material, 96)?;
        diffuse_info.metallic_black = f32_from_const(material, 100)?;
        diffuse_info.roughness_white = f32_from_const(material, 104)?;
        diffuse_info.roughness_black = f32_from_const(material, 108)?;
        material.diffuse_info = Some(diffuse_info);
    }
    material.shader_type = ShaderType::Diffuse;

    Ok(())
}

pub(super) fn handle_diffuse_si_shader(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    let post_process = mat.post_process_definition.elements.first();
    let mut diffuse_info = DiffuseInfo::default();
    if let Some(post_process) = post_process {
        material.shader_type = ShaderType::Diffuse;
        get_post_texture(post_process, material, 20, TextureType::Color)?;
        get_post_texture(post_process, material, 76, TextureType::Control)?;
        get_post_texture(post_process, material, 132, TextureType::Normal)?;
        diffuse_info.metallic_white = f32_from_const(material, 112)?;
        diffuse_info.metallic_black = f32_from_const(material, 116)?;
        diffuse_info.roughness_white = f32_from_const(material, 120)?;
        diffuse_info.roughness_black = f32_from_const(material, 124)?;
        diffuse_info.si_color_tint = (
            f32_from_const(material, 0)?,
            f32_from_const(material, 4)?,
            f32_from_const(material, 8)?,
        );
        diffuse_info.si_intensity = f32_from_const(material, 12)?;
        diffuse_info.si_amount = f32_from_const(material, 16)?;
        diffuse_info.color_tint = (
            f32_from_const(material, 48)?,
            f32_from_const(material, 52)?,
            f32_from_const(material, 56)?,
        );
        material.diffuse_info = Some(diffuse_info);
    }
    material.shader_type = ShaderType::Diffuse;
    Ok(())
}
