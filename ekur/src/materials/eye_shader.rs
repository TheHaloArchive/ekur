use anyhow::Result;

use crate::definitions::material::MaterialPostProcessing;

use super::{
    common_utils::{f32_from_const, get_post_texture},
    serde_definitions::{EyeShader, Material, ShaderType, TextureType},
};

pub(super) fn handle_eye_shader(
    post: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut eye_shader = EyeShader::default();
    get_post_texture(post, material, 8, TextureType::Sclera)?;
    get_post_texture(post, material, 20, TextureType::ScleraNormal)?;
    get_post_texture(post, material, 40, TextureType::Iris)?;
    get_post_texture(post, material, 56, TextureType::IrisNormal)?;
    eye_shader.sclera_brightness = f32_from_const(material, 16)?;
    eye_shader.sclera_normal_intensity = f32_from_const(material, 28)?;
    eye_shader.sclera_roughness = f32_from_const(material, 32)?;
    eye_shader.sclera_ior = f32_from_const(material, 36)?;
    eye_shader.iris_radius = f32_from_const(material, 48)?;
    eye_shader.iris_brightness = f32_from_const(material, 52)?;
    eye_shader.iris_normal_intensity = f32_from_const(material, 64)?;
    eye_shader.cornea_roughness = f32_from_const(material, 68)?;
    eye_shader.cornea_ior = f32_from_const(material, 72)?;
    eye_shader.pupil_scale = f32_from_const(material, 76)?;
    eye_shader.limbus_width = f32_from_const(material, 80)?;
    eye_shader.limbus_darkening_scale = f32_from_const(material, 84)?;
    eye_shader.limbus_power = f32_from_const(material, 88)?;
    eye_shader.eye_ior = f32_from_const(material, 92)?;
    eye_shader.cornea_height_scale = f32_from_const(material, 96)?;
    eye_shader.overall_scale = f32_from_const(material, 108)?;
    material.eye = Some(eye_shader);
    material.shader_type = ShaderType::EyeShader;
    Ok(())
}
