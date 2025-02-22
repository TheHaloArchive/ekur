use anyhow::Result;

use crate::definitions::material::MaterialTag;

use super::{
    common_utils::{f32_from_const, get_post_texture},
    serde_definitions::{ColorDecal, Material, ShaderType, TextureType},
};

pub(super) fn handle_color_decal(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    let post_process = mat.post_process_definition.elements.first();
    let mut color_decal = ColorDecal::default();
    if let Some(post_process) = post_process {
        get_post_texture(post_process, material, 12, TextureType::Color)?;
        color_decal.opacity = f32_from_const(material, 0)?;
        color_decal.roughness = f32_from_const(material, 4)?;
        color_decal.metallic = f32_from_const(material, 8)?;
        material.color_decal = Some(color_decal);
        material.shader_type = ShaderType::ColorDecal;
    }
    Ok(())
}
