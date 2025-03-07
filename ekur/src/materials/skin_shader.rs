use anyhow::Result;

use crate::definitions::material::MaterialPostProcessing;

use super::{
    common_utils::{f32_from_const, get_post_texture},
    serde_definitions::{Material, ShaderType, SkinShader, TextureType},
};

pub(super) fn handle_skin(post: &MaterialPostProcessing, material: &mut Material) -> Result<()> {
    material.shader_type = ShaderType::SkinShader;
    let mut skin_shader = SkinShader::default();
    get_post_texture(post, material, 28, TextureType::Color)?;
    get_post_texture(post, material, 64, TextureType::Normal)?;
    get_post_texture(post, material, 96, TextureType::AORoughnessTransmission)?;
    get_post_texture(post, material, 128, TextureType::SpecScatterPore)?;
    get_post_texture(post, material, 160, TextureType::PoreNormal)?;
    get_post_texture(post, material, 196, TextureType::DetailNormal)?;
    skin_shader.sss_strength = f32_from_const(material, 0)?;
    skin_shader.specular_white = f32_from_const(material, 12)?;
    skin_shader.specular_black = f32_from_const(material, 16)?;
    skin_shader.specular_intensity = f32_from_const(material, 8)?;
    skin_shader.pore_normal_intensity = f32_from_const(material, 192)?;
    skin_shader.micro_normal_intensity = f32_from_const(material, 224)?;
    skin_shader.micro_normal_scale = [
        f32_from_const(material, 208)?,
        f32_from_const(material, 212)?,
    ];
    material.skin = Some(skin_shader);
    Ok(())
}
