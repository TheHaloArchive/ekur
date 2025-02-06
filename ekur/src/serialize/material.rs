/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use serde_with::base64::Base64;
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;
use serde::Serialize;
use serde_with::serde_as;

use crate::definitions::material::{
    MaterialPostProcessing, MaterialStyleShaderSupportedLayers,
    MaterialStyleShaderSupportsDamageEnum, MaterialTag,
};

const NORMAL_MAP: i32 = 2142563353;
const MASK0_TEXTURE: i32 = -1869712910;
const MASK1_TEXTURE: i32 = -1677269129;
const ASG_TEXTURE: i32 = -447337164;
const TEXEL_DENSITY: i32 = 523899303;
const DECAL_CONTROL_MAP: i32 = -699244700;
const DECAL_NORMAL_MAP: i32 = 723636081;

const DIFFUSE_SHADER: i32 = 1102829229;
const DIFFUSE_SI_SHADERS: &[i32; 2] = &[-1051699871, -1659664443];
const KNOWN_DECALS: &[i32; 6] = &[
    -51713036,
    -131335022,
    690034699,
    2003821059,
    1996403871,
    -2003821059,
];
const DECAL_MP: i32 = -131335022;
const PARALLAX_DECAL: i32 = -93074746;
const SELF_ILLUM: i32 = -79437929;

#[derive(Default, Debug, Serialize)]
pub enum ShaderType {
    #[default]
    Unknown,
    Layered,
    Diffuse,
    Decal,
    SelfIllum,
}

#[derive(Default, Debug, Serialize, PartialEq, Eq, Hash)]
pub enum TextureType {
    #[default]
    Normal,
    Asg,
    Mask0,
    Mask1,
    Color,
    Control,
    AlphaMap,
    Unknown,
}

#[derive(Default, Debug, Serialize)]
pub struct Texture(i32);

#[derive(Default, Debug, Serialize, Clone)]
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
    si_color_tint: (f32, f32, f32),
    si_intensity: f32,
    si_amount: f32,
    color_tint: (f32, f32, f32),
}

#[derive(Default, Debug, Serialize)]
pub struct DecalSlot {
    top_color: (f32, f32, f32),
    mid_color: (f32, f32, f32),
    bot_color: (f32, f32, f32),
    roughness_white: f32,
    roughness_black: f32,
    metallic: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct SelfIllum {
    color: (f32, f32, f32),
    intensity: f32,
    opacity: f32,
}

#[serde_as]
#[derive(Default, Debug, Serialize)]
pub struct Material {
    textures: HashMap<TextureType, Texture>,
    shader_type: ShaderType,
    style_info: Option<StyleInfo>,
    diffuse_info: Option<DiffuseInfo>,
    illum_info: Option<SelfIllum>,
    decal_slots: Option<DecalSlot>,
    #[serde_as(as = "Base64")]
    material_constants: Vec<u8>,
}

fn collect_textures(
    material: &mut Material,
    mat: &MaterialTag,
    style_info: &mut StyleInfo,
) -> Result<()> {
    for param in &mat.material_parameters.elements {
        let id = param.bitmap.global_id;
        match param.parameter_name.0 {
            NORMAL_MAP => {
                material.textures.insert(TextureType::Normal, Texture(id));
            }
            MASK0_TEXTURE => {
                material.textures.insert(TextureType::Mask0, Texture(id));
            }
            MASK1_TEXTURE => {
                material.textures.insert(TextureType::Mask1, Texture(id));
            }
            ASG_TEXTURE => {
                material.textures.insert(TextureType::Asg, Texture(id));
            }
            TEXEL_DENSITY => {
                style_info.texel_density = (param.real.0, param.vector.x);
                style_info.material_offset = (param.vector.y, param.vector.z);
            }
            DECAL_CONTROL_MAP => {
                material.textures.insert(TextureType::Control, Texture(id));
            }
            DECAL_NORMAL_MAP => {
                material.textures.insert(TextureType::Normal, Texture(id));
            }
            _ => {
                material.textures.insert(TextureType::Unknown, Texture(id));
            }
        };
    }
    Ok(())
}

fn collect_constants(mat: &MaterialTag, material: &mut Material) -> Result<()> {
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
    Ok(())
}

fn add_style_info(
    style_info: &mut StyleInfo,
    mat: &MaterialTag,
    material: &mut Material,
) -> Result<()> {
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
        material.style_info = Some(style_info.clone());
        material.shader_type = ShaderType::Layered;
    }
    Ok(())
}

fn get_post_texture(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
    index: u16,
    texture_type: TextureType,
) -> Result<()> {
    let tex = post_process
        .textures
        .elements
        .iter()
        .find(|t| t.parameter_index.0 == index);
    if let Some(tex) = tex {
        material
            .textures
            .insert(texture_type, Texture(tex.bitmap_reference.global_id));
    };
    Ok(())
}

fn handle_diffuse_shader(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    if mat.material_shader.global_id == DIFFUSE_SHADER {
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
    }

    if DIFFUSE_SI_SHADERS.contains(&mat.material_shader.global_id) {
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
    }
    Ok(())
}

fn f32_from_const(material: &mut Material, start_index: usize) -> Result<f32> {
    let val =
        f32::from_ne_bytes(material.material_constants[start_index..start_index + 4].try_into()?);
    Ok(val)
}

fn f32_from_params(mat: &MaterialTag, name: i32) -> Result<f32> {
    let val = mat
        .material_parameters
        .elements
        .iter()
        .find(|m| m.parameter_name.0 == name);
    if let Some(val) = val {
        Ok(val.real.0)
    } else {
        Ok(0.0)
    }
}

fn handle_const_decal(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    if KNOWN_DECALS.contains(&mat.material_shader.global_id) {
        let post_process = mat.post_process_definition.elements.first();
        if let Some(post_process) = post_process {
            get_post_texture(post_process, material, 0, TextureType::Control)?;
            get_post_texture(post_process, material, 8, TextureType::Normal)?;
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
            let roughness_white = f32_from_const(material, 60)?;
            let roughness_black = f32_from_const(material, 64)?;
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
        };
    }
    Ok(())
}

fn handle_parallax_decal(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    if mat.material_shader.global_id == PARALLAX_DECAL {
        let post_process = mat.post_process_definition.elements.first();
        if let Some(post_process) = post_process {
            get_post_texture(post_process, material, 48, TextureType::Control)?;
            get_post_texture(post_process, material, 56, TextureType::Normal)?;
            let top_color = (
                f32_from_const(material, 64)?,
                f32_from_const(material, 68)?,
                f32_from_const(material, 72)?,
            );
            let mid_color = (
                f32_from_const(material, 80)?,
                f32_from_const(material, 84)?,
                f32_from_const(material, 88)?,
            );
            let bot_color = (
                f32_from_const(material, 96)?,
                f32_from_const(material, 100)?,
                f32_from_const(material, 104)?,
            );
            let roughness_white = f32_from_const(material, 108)?;
            let roughness_black = f32_from_const(material, 112)?;
            let metallic = f32_from_const(material, 116)?;
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
        };
    }
    Ok(())
}

fn handle_mp_decal(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    if mat.material_shader.global_id == DECAL_MP {
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
    }
    Ok(())
}

fn handle_illum(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    if mat.material_shader.global_id == SELF_ILLUM {
        if let Some(post) = mat.post_process_definition.elements.first() {
            material.shader_type = ShaderType::SelfIllum;
            get_post_texture(post, material, 0, TextureType::Color)?;
            get_post_texture(post, material, 48, TextureType::AlphaMap)?;
            let color = (
                f32_from_const(material, 32)?,
                f32_from_const(material, 36)?,
                f32_from_const(material, 40)?,
            );
            let intensity = f32_from_const(material, 44)?;
            let opacity = f32_from_const(material, 64)?;
            let illum = SelfIllum {
                color,
                intensity,
                opacity,
            };
            material.illum_info = Some(illum);
        }
    };
    Ok(())
}

impl Material {
    pub fn from_mat(mat: &MaterialTag) -> Result<Self> {
        let mut material = Material::default();
        let mut style_info = StyleInfo::default();
        collect_textures(&mut material, mat, &mut style_info)?;
        collect_constants(mat, &mut material)?;
        add_style_info(&mut style_info, mat, &mut material)?;
        handle_diffuse_shader(mat, &mut material)?;
        handle_const_decal(mat, &mut material)?;
        handle_mp_decal(mat, &mut material)?;
        handle_parallax_decal(mat, &mut material)?;
        handle_illum(mat, &mut material)?;
        Ok(material)
    }
}
pub fn process_materials(
    materials: &HashMap<i32, MaterialTag>,
    save_path: &str,
) -> Result<Vec<i32>> {
    let mut all_textures = Vec::new();
    for (id, mat) in materials.iter() {
        let material = Material::from_mat(mat)?;
        all_textures.extend(material.textures.values().map(|x| x.0));
        let mut path = PathBuf::from(format!("{save_path}/materials"));
        path.push(id.to_string());
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &material)?;
    }
    Ok(all_textures)
}
