/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;
use serde::Serialize;

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

const DIFFUSE_SHADER: &[i32; 2] = &[1102829229, 52809748];
const DIFFUSE_SI_SHADERS: &[i32; 2] = &[-1051699871, -1659664443];
const KNOWN_DECALS: &[i32; 5] = &[-51713036, -131335022, 690034699, 2003821059, -2003821059];
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
    ConesteppedLevel,
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
    MacroMaskMap,
    MacroCohmap,
    MacroConemap,
    MacroNormal,
    NoiseTexture,
    SharedControl,
    BurntGradient,
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

#[derive(Default, Debug, Serialize)]
pub struct ConemappedLevel {
    macro_mask_transform: [f32; 4],
    macro_normal_transform: [f32; 4],
    macro_normal_intensity: f32,
    macro_cohmap_transform: [f32; 4],
    macro_height_scale: f32,
    macro_conemap_transform: [f32; 4],
    macro_cone_depth: f32,
    macro_cone_offset: f32,
    macro_cone_quality: f32,
    macro_noise_transform: [f32; 4],
    macro_noise_color: [f32; 3],
    macro_noise_roughness: f32,
    macro_noise_remap_white: f32,
    macro_noise_remap_black: f32,
    macro_noise_detail_remap_white: f32,
    macro_noise_detail_remap_black: f32,
    macro_noise_opacity: f32,
    base_normal_intensity: f32,
    base_normal_transform: [f32; 4],
    base_control_transform: [f32; 4],
    base_height_scale: f32,
    base_top_color: [f32; 3],
    base_mid_color: [f32; 3],
    base_bottom_color: [f32; 3],
    base_roughness_white: f32,
    base_roughness_black: f32,
    base_metallic: f32,
    base_curvature_height_influence: f32,
    base_edge_wear_offset: f32,
    base_edge_wear_contrast: f32,
    base_edge_wear_opacity: f32,
    base_edge_wear_color: [f32; 3],
    base_edge_wear_roughness: f32,
    shared_control_transform: [f32; 4],
    burnt_gradient_transform: [f32; 4],
    layer2_height_scale: f32,
    char_height_scale: f32,
    char_height_offset: f32,
    char_opacity: f32,
    char_top_color: [f32; 3],
    char_mid_color: [f32; 3],
    char_bot_color: [f32; 3],
    char_roughness_white: f32,
    char_roughness_black: f32,
    rust_height_scale: f32,
    rust_height_offset: f32,
    rust_staining_offset: f32,
    rust_falloff_color: [f32; 3],
    rust_heavy_rust_offset: f32,
    rust_heavy_rust_falloff_paint_opacity: f32,
    rust_secondary_top_color: [f32; 3],
    rust_secondary_mid_color: [f32; 3],
    rust_secondary_bottom_color: [f32; 3],
    rust_secondary_color_start: f32,
    rust_secondary_color_end: f32,
    rust_top_color: [f32; 3],
    rust_mid_color: [f32; 3],
    rust_bottom_color: [f32; 3],
    rust_normal_intensity_new: f32,
    rust_heavy_rust_edge_start: f32,
    rust_heavy_rust_edge_end: f32,
    rust_roughness_white: f32,
    rust_roughness_black: f32,
    rust_metallic: f32,
    burnt_height_offset: f32,
    burnt_opacity: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct Material {
    shader: i32,
    textures: HashMap<TextureType, Texture>,
    shader_type: ShaderType,
    style_info: Option<StyleInfo>,
    diffuse_info: Option<DiffuseInfo>,
    illum_info: Option<SelfIllum>,
    decal_slots: Option<DecalSlot>,
    conemapped_level: Option<ConemappedLevel>,
    #[serde(skip)]
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
            _ => {}
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
    if DIFFUSE_SHADER.contains(&mat.material_shader.global_id) {
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

fn handle_conestepped_level(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    if mat.material_shader.global_id == -232573636 {
        let mut conemapped_level = ConemappedLevel::default();
        let Some(post) = mat.post_process_definition.elements.first() else {
            return Ok(());
        };
        get_post_texture(post, material, 0, TextureType::MacroMaskMap)?;
        get_post_texture(post, material, 32, TextureType::MacroNormal)?;
        get_post_texture(post, material, 68, TextureType::MacroCohmap)?;
        get_post_texture(post, material, 100, TextureType::MacroConemap)?;
        get_post_texture(post, material, 144, TextureType::NoiseTexture)?;
        get_post_texture(post, material, 228, TextureType::Normal)?;
        get_post_texture(post, material, 256, TextureType::Control)?;
        get_post_texture(post, material, 384, TextureType::SharedControl)?;
        get_post_texture(post, material, 416, TextureType::BurntGradient)?;

        conemapped_level.macro_mask_transform = [
            f32_from_const(material, 16)?,
            f32_from_const(material, 20)?,
            f32_from_const(material, 24)?,
            f32_from_const(material, 28)?,
        ];

        conemapped_level.macro_normal_transform = [
            f32_from_const(material, 48)?,
            f32_from_const(material, 52)?,
            f32_from_const(material, 56)?,
            f32_from_const(material, 60)?,
        ];

        conemapped_level.macro_normal_intensity = f32_from_const(material, 64)?;
        conemapped_level.macro_cohmap_transform = [
            f32_from_const(material, 80)?,
            f32_from_const(material, 84)?,
            f32_from_const(material, 88)?,
            f32_from_const(material, 92)?,
        ];
        conemapped_level.macro_height_scale = f32_from_const(material, 96)?;
        conemapped_level.macro_conemap_transform = [
            f32_from_const(material, 112)?,
            f32_from_const(material, 116)?,
            f32_from_const(material, 120)?,
            f32_from_const(material, 124)?,
        ];

        conemapped_level.macro_cone_depth = f32_from_const(material, 128)?;
        conemapped_level.macro_cone_offset = f32_from_const(material, 132)?;
        conemapped_level.macro_cone_quality = f32_from_const(material, 136)?;
        conemapped_level.macro_noise_transform = [
            f32_from_const(material, 160)?,
            f32_from_const(material, 164)?,
            f32_from_const(material, 168)?,
            f32_from_const(material, 172)?,
        ];
        conemapped_level.macro_noise_color = [
            f32_from_const(material, 176)?,
            f32_from_const(material, 180)?,
            f32_from_const(material, 184)?,
        ];
        conemapped_level.macro_noise_roughness = f32_from_const(material, 188)?;
        conemapped_level.macro_noise_remap_white = f32_from_const(material, 200)?;
        conemapped_level.macro_noise_remap_black = f32_from_const(material, 204)?;
        conemapped_level.macro_noise_detail_remap_white = f32_from_const(material, 208)?;
        conemapped_level.macro_noise_detail_remap_black = f32_from_const(material, 212)?;
        conemapped_level.macro_noise_opacity = f32_from_const(material, 216)?;
        conemapped_level.base_normal_intensity = f32_from_const(material, 224)?;
        conemapped_level.base_normal_transform = [
            f32_from_const(material, 240)?,
            f32_from_const(material, 244)?,
            f32_from_const(material, 248)?,
            f32_from_const(material, 252)?,
        ];
        conemapped_level.base_control_transform = [
            f32_from_const(material, 272)?,
            f32_from_const(material, 276)?,
            f32_from_const(material, 280)?,
            f32_from_const(material, 284)?,
        ];
        conemapped_level.base_height_scale = f32_from_const(material, 288)?;
        conemapped_level.base_top_color = [
            f32_from_const(material, 292)?,
            f32_from_const(material, 296)?,
            f32_from_const(material, 300)?,
        ];
        conemapped_level.base_mid_color = [
            f32_from_const(material, 304)?,
            f32_from_const(material, 308)?,
            f32_from_const(material, 312)?,
        ];
        conemapped_level.base_bottom_color = [
            f32_from_const(material, 320)?,
            f32_from_const(material, 324)?,
            f32_from_const(material, 328)?,
        ];
        conemapped_level.base_roughness_white = f32_from_const(material, 332)?;
        conemapped_level.base_roughness_black = f32_from_const(material, 336)?;
        conemapped_level.base_metallic = f32_from_const(material, 340)?;
        conemapped_level.base_curvature_height_influence = f32_from_const(material, 344)?;

        conemapped_level.base_edge_wear_offset = f32_from_const(material, 348)?;
        conemapped_level.base_edge_wear_contrast = f32_from_const(material, 352)?;
        conemapped_level.base_edge_wear_offset = f32_from_const(material, 356)?;
        conemapped_level.base_edge_wear_color = [
            f32_from_const(material, 368)?,
            f32_from_const(material, 372)?,
            f32_from_const(material, 376)?,
        ];
        conemapped_level.base_edge_wear_roughness = f32_from_const(material, 380)?;

        conemapped_level.shared_control_transform = [
            f32_from_const(material, 400)?,
            f32_from_const(material, 404)?,
            f32_from_const(material, 408)?,
            f32_from_const(material, 412)?,
        ];
        conemapped_level.burnt_gradient_transform = [
            f32_from_const(material, 432)?,
            f32_from_const(material, 436)?,
            f32_from_const(material, 440)?,
            f32_from_const(material, 444)?,
        ];
        conemapped_level.layer2_height_scale = f32_from_const(material, 448)?;
        conemapped_level.char_height_scale = f32_from_const(material, 452)?;
        conemapped_level.char_height_offset = f32_from_const(material, 456)?;
        conemapped_level.char_height_offset = f32_from_const(material, 460)?;
        conemapped_level.char_top_color = [
            f32_from_const(material, 464)?,
            f32_from_const(material, 468)?,
            f32_from_const(material, 472)?,
        ];
        conemapped_level.char_mid_color = [
            f32_from_const(material, 480)?,
            f32_from_const(material, 484)?,
            f32_from_const(material, 488)?,
        ];
        conemapped_level.char_bot_color = [
            f32_from_const(material, 496)?,
            f32_from_const(material, 500)?,
            f32_from_const(material, 504)?,
        ];
        conemapped_level.char_roughness_white = f32_from_const(material, 508)?;
        conemapped_level.char_roughness_black = f32_from_const(material, 512)?;

        conemapped_level.rust_height_scale = f32_from_const(material, 516)?;
        conemapped_level.rust_height_offset = f32_from_const(material, 520)?;
        conemapped_level.rust_staining_offset = f32_from_const(material, 524)?;
        conemapped_level.rust_falloff_color = [
            f32_from_const(material, 528)?,
            f32_from_const(material, 532)?,
            f32_from_const(material, 536)?,
        ];
        conemapped_level.rust_heavy_rust_offset = f32_from_const(material, 540)?;
        conemapped_level.rust_heavy_rust_falloff_paint_opacity = f32_from_const(material, 544)?;
        conemapped_level.rust_secondary_top_color = [
            f32_from_const(material, 548)?,
            f32_from_const(material, 552)?,
            f32_from_const(material, 556)?,
        ];
        conemapped_level.rust_secondary_mid_color = [
            f32_from_const(material, 560)?,
            f32_from_const(material, 564)?,
            f32_from_const(material, 568)?,
        ];
        conemapped_level.rust_secondary_bottom_color = [
            f32_from_const(material, 576)?,
            f32_from_const(material, 580)?,
            f32_from_const(material, 584)?,
        ];
        conemapped_level.rust_secondary_color_start = f32_from_const(material, 588)?;
        conemapped_level.rust_secondary_color_end = f32_from_const(material, 592)?;
        conemapped_level.rust_top_color = [
            f32_from_const(material, 596)?,
            f32_from_const(material, 600)?,
            f32_from_const(material, 604)?,
        ];
        conemapped_level.rust_mid_color = [
            f32_from_const(material, 608)?,
            f32_from_const(material, 612)?,
            f32_from_const(material, 616)?,
        ];
        conemapped_level.rust_bottom_color = [
            f32_from_const(material, 624)?,
            f32_from_const(material, 628)?,
            f32_from_const(material, 632)?,
        ];
        conemapped_level.rust_normal_intensity_new = f32_from_const(material, 636)?;
        conemapped_level.rust_heavy_rust_edge_start = f32_from_const(material, 640)?;
        conemapped_level.rust_heavy_rust_edge_end = f32_from_const(material, 644)?;
        conemapped_level.rust_roughness_white = f32_from_const(material, 648)?;
        conemapped_level.rust_roughness_black = f32_from_const(material, 652)?;
        conemapped_level.rust_metallic = f32_from_const(material, 656)?;
        conemapped_level.burnt_height_offset = f32_from_const(material, 660)?;
        conemapped_level.burnt_opacity = f32_from_const(material, 664)?;
        material.shader_type = ShaderType::ConesteppedLevel;
        material.conemapped_level = Some(conemapped_level);
    }
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
        handle_conestepped_level(mat, &mut material)?;
        material.shader = mat.material_shader.global_id;
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
