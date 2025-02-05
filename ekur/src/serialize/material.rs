/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use serde_with::base64::Base64;
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;
use serde::Serialize;
use serde_with::serde_as;

use crate::definitions::material::{
    MaterialStyleShaderSupportedLayers, MaterialStyleShaderSupportsDamageEnum, MaterialTag,
};

const NORMAL_MAP: i32 = 2142563353;
const MASK0_TEXTURE: i32 = -1869712910;
const MASK1_TEXTURE: i32 = -1677269129;
const ASG_TEXTURE: i32 = -447337164;
const TEXEL_DENSITY: i32 = 523899303;

#[derive(Default, Debug, Serialize)]
pub enum ShaderType {
    #[default]
    LayeredShader,
    DiffuseShader,
}

#[derive(Default, Debug, Serialize, PartialEq, Eq, Hash)]
pub enum TextureType {
    #[default]
    Normal,
    AsgTexture,
    Mask0Texture,
    Mask1Texture,
    ColorTexture,
    ControlTexture,
    Unknown,
}

#[derive(Default, Debug, Serialize)]
pub struct Texture(i32);

#[derive(Default, Debug, Serialize)]
pub struct StyleInfo {
    texel_density: (f32, f32),
    material_offset: (f32, f32),
    stylelist: i32,
    region_name: i32,
    base_intention: i32,
    mask0_red_intention: i32,
    mask0_green_intention: i32,
    mask0_blue_intention: i32,
    mask1_red_intention: i32,
    mask1_green_intention: i32,
    mask1_blue_intention: i32,
    supported_layers: u8,
    enable_damage: bool,
}

#[derive(Default, Debug, Serialize)]
pub struct DiffuseInfo {
    metallic_white: f32,
    metallic_black: f32,
    roughness_white: f32,
    roughness_black: f32,
}

#[serde_as]
#[derive(Default, Debug, Serialize)]
pub struct Material {
    textures: HashMap<TextureType, Texture>,
    shader_type: ShaderType,
    style_info: Option<StyleInfo>,
    diffuse_info: Option<DiffuseInfo>,
    #[serde_as(as = "Base64")]
    material_constants: Vec<u8>,
}

impl Material {
    pub fn from_mat(mat: &MaterialTag) -> Result<Self> {
        let mut material = Material::default();
        let mut style_info = StyleInfo::default();
        for param in &mat.material_parameters.elements {
            match param.parameter_name.0 {
                NORMAL_MAP => {
                    material
                        .textures
                        .insert(TextureType::Normal, Texture(param.bitmap.global_id));
                }
                MASK0_TEXTURE => {
                    material
                        .textures
                        .insert(TextureType::Mask0Texture, Texture(param.bitmap.global_id));
                }
                MASK1_TEXTURE => {
                    material
                        .textures
                        .insert(TextureType::Mask1Texture, Texture(param.bitmap.global_id));
                }
                ASG_TEXTURE => {
                    material
                        .textures
                        .insert(TextureType::AsgTexture, Texture(param.bitmap.global_id));
                }
                TEXEL_DENSITY => {
                    style_info.texel_density = (param.real.0, param.vector.x);
                    style_info.material_offset = (param.vector.y, param.vector.z);
                }
                _ => {
                    material
                        .textures
                        .insert(TextureType::Unknown, Texture(param.bitmap.global_id));
                }
            };
        }
        if let Some(post) = &mat.post_process_definition.elements.first() {
            material.material_constants = post
                .material_constants
                .elements
                .iter()
                .flat_map(|c| {
                    [
                        c.register.x.to_ne_bytes(),
                        c.register.y.to_ne_bytes(),
                        c.register.z.to_ne_bytes(),
                        c.register.w.to_ne_bytes(),
                    ]
                    .concat()
                })
                .collect();
        }
        let style = &mat.style_info.elements.first();
        if let Some(style) = style {
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
            material.style_info = Some(style_info);
            material.shader_type = ShaderType::LayeredShader;
        }

        if mat.material_shader.global_id == 1102829229 {
            let post_process = mat.post_process_definition.elements.first();
            let mut diffuse_info = DiffuseInfo::default();
            if let Some(post_process) = post_process {
                material.shader_type = ShaderType::DiffuseShader;
                let color_map = post_process
                    .textures
                    .elements
                    .iter()
                    .find(|t| t.parameter_index.0 == 0)
                    .unwrap()
                    .bitmap_reference
                    .global_id;
                material
                    .textures
                    .insert(TextureType::ColorTexture, Texture(color_map));
                let control_map = post_process
                    .textures
                    .elements
                    .iter()
                    .find(|t| t.parameter_index.0 == 60)
                    .unwrap()
                    .bitmap_reference
                    .global_id;
                material
                    .textures
                    .insert(TextureType::ControlTexture, Texture(control_map));

                diffuse_info.metallic_white =
                    f32::from_ne_bytes(material.material_constants[96..100].try_into()?);
                diffuse_info.metallic_black =
                    f32::from_ne_bytes(material.material_constants[100..104].try_into()?);
                diffuse_info.roughness_white =
                    f32::from_ne_bytes(material.material_constants[104..108].try_into()?);
                diffuse_info.roughness_black =
                    f32::from_ne_bytes(material.material_constants[108..112].try_into()?);
                material.diffuse_info = Some(diffuse_info);
            }
        }
        Ok(material)
    }
}

pub fn process_materials(materials: &HashMap<i32, MaterialTag>, save_path: &str) -> Result<()> {
    for (id, mat) in materials.iter() {
        let material = Material::from_mat(mat)?;
        let mut path = PathBuf::from(format!("{save_path}/materials"));
        path.push(id.to_string());
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &material)?;
    }
    Ok(())
}
