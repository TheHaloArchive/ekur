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
        get_post_texture(post_process, material, 196, TextureType::AlphaMap)?;
        diffuse_info.metallic_white = f32_from_const(material, 96)?;
        diffuse_info.metallic_black = f32_from_const(material, 100)?;
        diffuse_info.roughness_white = f32_from_const(material, 104)?;
        diffuse_info.roughness_black = f32_from_const(material, 108)?;
        material.diffuse_info = Some(diffuse_info);
    }
    material.shader_type = ShaderType::Diffuse;

    Ok(())
}

pub(super) fn handle_diffuse_decal_shader(
    mat: &MaterialTag,
    material: &mut Material,
) -> Result<()> {
    let post_process = mat.post_process_definition.elements.first();
    let mut diffuse_info = DiffuseInfo::default();
    if let Some(post_process) = post_process {
        material.shader_type = ShaderType::Diffuse;
        get_post_texture(post_process, material, 96, TextureType::Color)?;
        get_post_texture(post_process, material, 56, TextureType::Control)?;
        get_post_texture(post_process, material, 16, TextureType::Normal)?;
        diffuse_info.metallic_white = 0.5;
        diffuse_info.metallic_black = 1.0;
        diffuse_info.roughness_white = 0.5;
        diffuse_info.roughness_black = 1.0;
        diffuse_info.color_tint = (
            f32_from_const(material, 0)?,
            f32_from_const(material, 4)?,
            f32_from_const(material, 8)?,
        );
        material.diffuse_info = Some(diffuse_info);
    }
    material.shader_type = ShaderType::Diffuse;

    Ok(())
}

pub(super) fn handle_diffuse_decal_notint_shader(
    mat: &MaterialTag,
    material: &mut Material,
) -> Result<()> {
    let post_process = mat.post_process_definition.elements.first();
    let mut diffuse_info = DiffuseInfo::default();
    if let Some(post_process) = post_process {
        material.shader_type = ShaderType::Diffuse;
        get_post_texture(post_process, material, 48, TextureType::Color)?;
        get_post_texture(post_process, material, 8, TextureType::Control)?;
        diffuse_info.roughness_black = 0.25;
        diffuse_info.roughness_white = 0.20;
        diffuse_info.metallic_black = 0.25;
        diffuse_info.metallic_white = 0.20;
        material.diffuse_info = Some(diffuse_info);
    }
    material.shader_type = ShaderType::Diffuse;

    Ok(())
}

pub(super) fn handle_diffuse_billboard_shader(
    mat: &MaterialTag,
    material: &mut Material,
) -> Result<()> {
    let post_process = mat.post_process_definition.elements.first();
    let mut diffuse_info = DiffuseInfo::default();
    if let Some(post_process) = post_process {
        material.shader_type = ShaderType::Diffuse;
        get_post_texture(post_process, material, 96, TextureType::Color)?;
        get_post_texture(post_process, material, 160, TextureType::Control)?;
        get_post_texture(post_process, material, 128, TextureType::Normal)?;
        diffuse_info.metallic_white = f32_from_const(material, 76)?;
        diffuse_info.metallic_black = f32_from_const(material, 80)?;
        diffuse_info.roughness_white = f32_from_const(material, 60)?;
        diffuse_info.roughness_black = f32_from_const(material, 64)?;
        material.diffuse_info = Some(diffuse_info);
    }
    material.shader_type = ShaderType::Diffuse;

    Ok(())
}

pub(super) fn handle_diffuse_emissive_shader(
    mat: &MaterialTag,
    material: &mut Material,
) -> Result<()> {
    let post_process = mat.post_process_definition.elements.first();
    let mut diffuse_info = DiffuseInfo::default();
    if let Some(post_process) = post_process {
        material.shader_type = ShaderType::Diffuse;
        get_post_texture(post_process, material, 96, TextureType::Color)?;
        get_post_texture(post_process, material, 160, TextureType::Control)?;
        get_post_texture(post_process, material, 128, TextureType::Normal)?;
        get_post_texture(post_process, material, 244, TextureType::Emissive)?;
        diffuse_info.metallic_white = f32_from_const(material, 76)?;
        diffuse_info.metallic_black = f32_from_const(material, 80)?;
        diffuse_info.roughness_white = f32_from_const(material, 60)?;
        diffuse_info.roughness_black = f32_from_const(material, 64)?;
        diffuse_info.color_tint = (
            f32_from_const(material, 84)?,
            f32_from_const(material, 88)?,
            f32_from_const(material, 92)?,
        );
        diffuse_info.si_color_tint = (
            f32_from_const(material, 224)?,
            f32_from_const(material, 228)?,
            f32_from_const(material, 232)?,
        );
        diffuse_info.si_intensity = f32_from_const(material, 240)?;
        diffuse_info.si_amount = f32_from_const(material, 236)?;
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
