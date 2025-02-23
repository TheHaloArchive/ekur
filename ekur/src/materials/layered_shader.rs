/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use anyhow::Result;

use crate::definitions::material::MaterialStyleShaderSupportedLayers;
use crate::definitions::material::MaterialStyleShaderSupportsDamageEnum;
use crate::materials::serde_definitions::ShaderType;
use crate::materials::serde_definitions::TextureType;
use crate::{definitions::material::MaterialTag, materials::serde_definitions::Material};

use super::serde_definitions::StyleInfo;

const NORMAL_MAP: i32 = 2142563353;
const MASK0_TEXTURE: i32 = -1869712910;
const MASK1_TEXTURE: i32 = -1677269129;
const ASG_TEXTURE: i32 = -447337164;
const TEXEL_DENSITY: i32 = 523899303;
const DECAL_CONTROL_MAP: i32 = -699244700;
const DECAL_NORMAL_MAP: i32 = 723636081;

pub(super) fn collect_textures(
    mut style_info: Option<&mut StyleInfo>,
    material: &mut Material,
    mat: &MaterialTag,
) -> Result<()> {
    for param in &mat.material_parameters.elements {
        let id = param.bitmap.global_id;
        match param.parameter_name.0 {
            NORMAL_MAP => {
                material.textures.insert(TextureType::Normal, id);
            }
            MASK0_TEXTURE => {
                material.textures.insert(TextureType::Mask0, id);
            }
            MASK1_TEXTURE => {
                material.textures.insert(TextureType::Mask1, id);
            }
            ASG_TEXTURE => {
                material.textures.insert(TextureType::Asg, id);
            }
            TEXEL_DENSITY => {
                if let Some(ref mut style_info) = style_info {
                    style_info.texel_density = (param.real.0, param.vector.x);
                    style_info.material_offset = (param.vector.y, param.vector.z);
                }
            }
            DECAL_CONTROL_MAP => {
                material.textures.insert(TextureType::Control, id);
            }
            DECAL_NORMAL_MAP => {
                material.textures.insert(TextureType::Normal, id);
            }
            _ => {}
        };
    }
    Ok(())
}

pub(super) fn add_style_info(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    let style = &mat.style_info.elements.first();
    let mut style_info = StyleInfo::default();
    if let Some(style) = style {
        collect_textures(Some(&mut style_info), material, mat)?;
        style_info.base_intention = style.base_intention.0;
        style_info.mask0_red_intention = style.mask0_red_channel_intention.0;
        style_info.mask0_green_intention = style.mask0_green_channel_intention.0;
        style_info.mask0_blue_intention = style.mask0_blue_channel_intention.0;

        style_info.mask1_red_intention = style.mask1_red_channel_intention.0;
        style_info.mask1_green_intention = style.mask1_green_channel_intention.0;
        style_info.mask1_blue_intention = style.mask1_blue_channel_intention.0;

        style_info.region_name = style.region_name.0;
        style_info.stylelist = style.material_style.global_id;
        style_info.enable_damage =
            style.requires_damage.0 == MaterialStyleShaderSupportsDamageEnum::Yes;
        style_info.supported_layers = match style.supported_layers.0 {
            MaterialStyleShaderSupportedLayers::Supports1Layer => 1,
            MaterialStyleShaderSupportedLayers::Supports4Layers => 4,
            MaterialStyleShaderSupportedLayers::Supports7Layers => 7,
            MaterialStyleShaderSupportedLayers::LayerShaderDisabled => 0,
        };
        material.style_info = Some(style_info.clone());
        material.shader_type = ShaderType::Layered;
    }
    Ok(())
}
