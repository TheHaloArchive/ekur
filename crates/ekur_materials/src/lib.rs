/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
mod basic;
mod layered;
pub mod process;
mod utils;

use serde::Serialize;
use std::collections::HashMap;

use crate::utils::{bool_from_const, f32_from_const, i32_from_const};

#[derive(Default, Debug, Serialize)]
pub enum ShaderType {
    #[default]
    Unknown,
    Layered,
    Diffuse,
    Decal,
    SelfIllum,
    ColorDecal,
    Meter,
    SkinShader,
    EyeShader,
    Hair,
    LayeredLevel,
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
    MacroControl,
    SharedControl,
    BurntGradient,
    Emissive,
    Meter,
    AORoughnessTransmission,
    SpecScatterPore,
    PoreNormal,
    DetailNormal,
    Sclera,
    ScleraNormal,
    Iris,
    IrisNormal,
    AO,
    EyeGazeMap,
    Cubemap,
    Layer1Color,
    Layer1DetailNormal,
    Layer1Normal,
    Layer1Control,
    Layer3Packed,
    Layer1Rohm,
    Layer2DetailNormal,
    Layer2Control,
    Layer2Packed,
    Layer2Normal,
    Layer2Color,
    Layer3Color,
    Layer3Rohm,
    Layer3DetailNormal,
    Layer3Normal,
    Layer3Control,
    Layer4Control,
    Layer4Packed,
    Layer4Color,
    Layer4DetailNormal,
    Layer4Rohm,
    Layer4Normal,
    Wetness,
    WetnessPuddleNormal,
    MacroColor,
    FourLayeredMacroMask,
    AmbientOcclusion,
}

#[derive(Default, Debug, Serialize, Clone)]
pub struct StyleInfo {
    pub(crate) texel_density: (f32, f32),
    pub(crate) material_offset: (f32, f32),
    pub(crate) stylelist: i32,
    pub(crate) region_name: i32,
    pub(crate) base_intention: i32,
    pub(crate) mask0_red_intention: i32,
    pub(crate) mask0_green_intention: i32,
    pub(crate) mask0_blue_intention: i32,
    pub(crate) mask1_red_intention: i32,
    pub(crate) mask1_green_intention: i32,
    pub(crate) mask1_blue_intention: i32,
    pub(crate) supported_layers: u8,
    pub(crate) enable_damage: bool,
}

#[derive(Default, Debug, Serialize)]
pub struct DiffuseInfo {
    pub metallic_white: f32,
    pub metallic_black: f32,
    pub roughness_white: f32,
    pub roughness_black: f32,
    pub si_color_tint: (f32, f32, f32),
    pub si_intensity: f32,
    pub si_amount: f32,
    pub color_tint: (f32, f32, f32),
}

#[derive(Default, Debug, Serialize)]
pub struct DecalSlot {
    pub top_color: (f32, f32, f32),
    pub mid_color: (f32, f32, f32),
    pub bot_color: (f32, f32, f32),
    pub roughness_white: f32,
    pub roughness_black: f32,
    pub metallic: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct SelfIllum {
    pub color: (f32, f32, f32),
    pub intensity: f32,
    pub opacity: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct ColorDecal {
    pub opacity: f32,
    pub metallic: f32,
    pub roughness: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct Meter {
    pub meter_off_color: (f32, f32, f32),
    pub meter_on_color: (f32, f32, f32),
    pub meter_value: f32,
    pub meter_intensity: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct SkinShader {
    pub sss_strength: f32,
    pub specular_intensity: f32,
    pub specular_white: f32,
    pub specular_black: f32,
    pub pore_normal_intensity: f32,
    pub micro_normal_intensity: f32,
    pub micro_normal_scale: [f32; 2],
}

#[derive(Default, Debug, Serialize)]
pub struct EyeShader {
    pub sclera_brightness: f32,
    pub sclera_normal_intensity: f32,
    pub sclera_roughness: f32,
    pub sclera_ior: f32,
    pub iris_radius: f32,
    pub iris_brightness: f32,
    pub iris_normal_intensity: f32,
    pub cornea_roughness: f32,
    pub cornea_ior: f32,
    pub pupil_scale: f32,
    pub limbus_width: f32,
    pub limbus_darkening_scale: f32,
    pub limbus_power: f32,
    pub eye_ior: f32,
    pub cornea_height_scale: f32,
    pub overall_scale: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct Hair {
    pub tint_color: (f32, f32, f32),
    pub roughness_white: f32,
    pub roughness_black: f32,
    pub ior: f32,
}

#[derive(Default, Debug, Serialize, PartialEq, Eq, Hash)]
pub enum LayerType {
    #[default]
    RohgLayer,
    RohmLayer,
    NnhgLayer,
}

#[derive(Default, Debug, Serialize, PartialEq, Eq, Hash)]
pub enum LevelType {
    #[default]
    Rohg3Rohm1MM,
    Rohm2Pack2MM,
    Rohm3Rohg1MMCone,
    Rohm2Rohg2MM,
    Rohm3MM,
    Rohg2Rohm1Nnhg1MM,
    Rohg1Rohm2Nnhg1MM,
    Rohm2Rohg1Nnhg1,
    Rohm2Rohg2NoControl,
    Rohm3Nnhg1,
    Rohm1Rohg1Nnhg1,
    Rohg3Rohm1NoControl,
    Rohm1Rohg2Nnhg1NoControl,
    Rohg4MM,
}

// TODO: Macro Mask Info may not have all the info but still exist (e.g control is missing)
#[derive(Default, Debug, Serialize)]
pub struct MacroMaskInfo {
    pub macro_normal_map_transform: [f32; 4],
    pub macro_normal_intensity: f32,
    pub macro_control_map_transform: [f32; 4],
    pub macro_roughness_intensity: f32,
    pub macro_occlusion_intensity: f32,
    pub macro_metallic_intensity: f32,
    pub macro_cavity_intensity: f32,
    pub macro_cavity_exponent: f32,
}

impl MacroMaskInfo {
    pub fn read(material: &mut Material, offset: usize) -> anyhow::Result<Self> {
        Ok(Self {
            macro_normal_map_transform: [
                f32_from_const(material, offset)?,
                f32_from_const(material, offset + 4)?,
                f32_from_const(material, offset + 8)?,
                f32_from_const(material, offset + 12)?,
            ],
            macro_normal_intensity: f32_from_const(material, offset + 16)?,
            macro_control_map_transform: [
                f32_from_const(material, offset + 32)?,
                f32_from_const(material, offset + 36)?,
                f32_from_const(material, offset + 40)?,
                f32_from_const(material, offset + 44)?,
            ],
            macro_roughness_intensity: f32_from_const(material, offset + 48)?,
            macro_occlusion_intensity: f32_from_const(material, offset + 52)?,
            macro_metallic_intensity: f32_from_const(material, offset + 56)?,
            macro_cavity_intensity: f32_from_const(material, offset + 60)?,
            macro_cavity_exponent: f32_from_const(material, offset + 64)?,
        })
    }
}

#[derive(Default, Debug, Serialize)]
pub struct ExtraLayerData {
    opacity: f32,
    height_blend_range: f32,
    height_accumulation: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct NnhgLayer {
    color_blend_mode: i32,
    normal_blend_mode: i32,
    invert_height_blend: bool,
    texture_bomb_enabled: bool,
    texture_bomb_height_blend_enabled: bool,
    texture_bomb_offset_strength: f32,
    texture_bomb_mask_contrast: f32,
    texture_bomb_height_mask_range: f32,
    micro_tessellation_scale: f32,
    height_scale: f32,
    roughness_white: f32,
    roughness_black: f32,
    ior: f32,
    normal_intensity: f32,
    metallic: f32,
    top_color: [f32; 3],
    mid_color: [f32; 3],
    bottom_color: [f32; 3],
    packed_map_texture_transform: [f32; 4],
    extra_data: Option<ExtraLayerData>,
}

impl NnhgLayer {
    pub fn read(material: &mut Material, offset: usize, is_layer1: bool) -> anyhow::Result<Self> {
        let shift = if is_layer1 { 8 } else { 0 };

        let mut data = Self {
            color_blend_mode: i32_from_const(material, offset)?,
            normal_blend_mode: i32_from_const(material, offset + 4)?,
            invert_height_blend: bool_from_const(material, offset + 8)?,
            texture_bomb_enabled: bool_from_const(material, offset + 12)?,
            texture_bomb_height_blend_enabled: bool_from_const(material, offset + 16)?,
            texture_bomb_offset_strength: f32_from_const(material, offset + 20)?,
            texture_bomb_mask_contrast: f32_from_const(material, offset + 24)?,
            texture_bomb_height_mask_range: f32_from_const(material, offset + 28)?,
            micro_tessellation_scale: f32_from_const(material, offset + 32)?,
            height_scale: f32_from_const(material, offset + 36)?,

            roughness_white: f32_from_const(material, offset + 64 - shift)?,
            roughness_black: f32_from_const(material, offset + 68 - shift)?,
            ior: f32_from_const(material, offset + 72 - shift)?,
            normal_intensity: f32_from_const(material, offset + 76 - shift)?,
            metallic: f32_from_const(material, offset + 80 - shift)?,

            top_color: [
                f32_from_const(material, offset + 84 - shift)?,
                f32_from_const(material, offset + 88 - shift)?,
                f32_from_const(material, offset + 92 - shift)?,
            ],
            mid_color: [
                f32_from_const(material, offset + 96 - shift)?,
                f32_from_const(material, offset + 100 - shift)?,
                f32_from_const(material, offset + 104 - shift)?,
            ],
            bottom_color: [
                f32_from_const(material, offset + 112 - shift)?,
                f32_from_const(material, offset + 116 - shift)?,
                f32_from_const(material, offset + 120 - shift)?,
            ],

            packed_map_texture_transform: [
                f32_from_const(material, offset + 144 - shift)?,
                f32_from_const(material, offset + 148 - shift)?,
                f32_from_const(material, offset + 152 - shift)?,
                f32_from_const(material, offset + 156 - shift)?,
            ],
            extra_data: None,
        };

        if !is_layer1 {
            data.extra_data = Some(ExtraLayerData {
                opacity: f32_from_const(material, offset + 40)?,
                height_blend_range: f32_from_const(material, offset + 44)?,
                height_accumulation: f32_from_const(material, offset + 48)?,
            });
        }

        Ok(data)
    }
}

#[derive(Default, Debug, Serialize)]
pub struct RohgLayer {
    color_blend_mode: i32,
    normal_blend_mode: i32,
    invert_height_blend: bool,
    texture_bomb_enabled: bool,
    texture_bomb_height_blend_enabled: bool,
    texture_bomb_offset_strength: f32,
    texture_bomb_mask_contrast: f32,
    texture_bomb_height_mask_range: f32,
    micro_tessellation_scale: f32,
    height_scale: f32,
    roughness_white: f32,
    roughness_black: f32,
    ior: f32,
    normal_intensity: f32,
    metallic: f32,
    top_color: [f32; 3],
    mid_color: [f32; 3],
    bottom_color: [f32; 3],
    normal_map_texture_transform: [f32; 4],
    control_map_texture_transform: [f32; 4],
    extra_data: Option<ExtraLayerData>,
}

impl RohgLayer {
    pub fn read(
        material: &mut Material,
        offset: usize,
        is_layer1: bool,
        is_alt: bool,
    ) -> anyhow::Result<Self> {
        let shift = if is_layer1 {
            8
        } else if is_alt {
            12
        } else {
            0
        };
        let secondary_shift = if is_layer1 { 12 } else { 0 };
        let tertiary_shift = if is_layer1 { 4 } else { 0 };

        let mut data = Self {
            color_blend_mode: i32_from_const(material, offset)?,
            normal_blend_mode: i32_from_const(material, offset + 4)?,
            invert_height_blend: bool_from_const(material, offset + 8)?,
            texture_bomb_enabled: bool_from_const(material, offset + 12)?,
            texture_bomb_height_blend_enabled: bool_from_const(material, offset + 16)?,
            texture_bomb_offset_strength: f32_from_const(material, offset + 20)?,
            texture_bomb_mask_contrast: f32_from_const(material, offset + 24)?,
            texture_bomb_height_mask_range: f32_from_const(material, offset + 28)?,
            micro_tessellation_scale: f32_from_const(material, offset + 32)?,
            height_scale: f32_from_const(material, offset + 36)?,

            roughness_white: f32_from_const(material, offset + 64 - shift)?,
            roughness_black: f32_from_const(material, offset + 68 - shift)?,
            ior: f32_from_const(material, offset + 72 - shift)?,
            normal_intensity: f32_from_const(material, offset + 76 - shift)?,
            metallic: f32_from_const(material, offset + 80 - shift)?,

            top_color: [
                f32_from_const(material, offset + 84 - shift)?,
                f32_from_const(material, offset + 88 - shift)?,
                f32_from_const(material, offset + 92 - shift)?,
            ],
            mid_color: [
                f32_from_const(material, offset + 96 - shift - secondary_shift)?,
                f32_from_const(material, offset + 100 - shift - secondary_shift)?,
                f32_from_const(material, offset + 104 - shift - secondary_shift)?,
            ],
            bottom_color: [
                f32_from_const(material, offset + 112 - shift - secondary_shift)?,
                f32_from_const(material, offset + 116 - shift - secondary_shift)?,
                f32_from_const(material, offset + 120 - shift - secondary_shift)?,
            ],

            normal_map_texture_transform: [
                f32_from_const(material, offset + 144 - shift + tertiary_shift)?,
                f32_from_const(material, offset + 148 - shift + tertiary_shift)?,
                f32_from_const(material, offset + 152 - shift + tertiary_shift)?,
                f32_from_const(material, offset + 156 - shift + tertiary_shift)?,
            ],
            control_map_texture_transform: [
                f32_from_const(material, offset + 176 - shift + tertiary_shift)?,
                f32_from_const(material, offset + 180 - shift + tertiary_shift)?,
                f32_from_const(material, offset + 184 - shift + tertiary_shift)?,
                f32_from_const(material, offset + 188 - shift + tertiary_shift)?,
            ],

            extra_data: None,
        };

        if shift == 0 {
            data.extra_data = Some(ExtraLayerData {
                opacity: f32_from_const(material, offset + 40)?,
                height_blend_range: f32_from_const(material, offset + 44)?,
                height_accumulation: f32_from_const(material, offset + 48)?,
            });
        }

        Ok(data)
    }
}

#[derive(Default, Debug, Serialize)]
pub struct RohmLayer {
    color_blend_mode: i32,
    normal_blend_mode: i32,
    invert_height_blend: bool,
    texture_bomb_enabled: bool,
    texture_bomb_height_blend_enabled: bool,
    texture_bomb_offset_strength: f32,
    texture_bomb_mask_contrast: f32,
    texture_bomb_height_mask_range: f32,
    micro_tessellation_scale: f32,
    height_scale: f32,
    roughness_white: f32,
    roughness_black: f32,
    ior: f32,
    normal_intensity: f32,
    metallic_white: f32,
    metallic_black: f32,
    color_tint: [f32; 3],
    color_map_texture_transform: [f32; 4],
    normal_map_texture_transform: [f32; 4],
    control_map_texture_transform: [f32; 4],
    extra_data: Option<ExtraLayerData>,
}

impl RohmLayer {
    pub fn read(
        material: &mut Material,
        offset: usize,
        is_layer1: bool,
        is_other: bool,
    ) -> anyhow::Result<Self> {
        let mut shift = if is_layer1 { 8 } else { 0 };
        let secondary_shift = if is_layer1 { 12 } else { 0 };
        let tertiary_shift = if is_layer1 { 8 } else { 0 };
        shift = if is_other { 12 } else { shift };
        shift = if is_layer1 && is_other { 4 } else { shift };
        let mut data = Self {
            color_blend_mode: i32_from_const(material, offset)?,
            normal_blend_mode: i32_from_const(material, offset + 4)?,
            invert_height_blend: bool_from_const(material, offset + 8)?,
            texture_bomb_enabled: bool_from_const(material, offset + 12)?,
            texture_bomb_height_blend_enabled: bool_from_const(material, offset + 16)?,
            texture_bomb_offset_strength: f32_from_const(material, offset + 20)?,
            texture_bomb_mask_contrast: f32_from_const(material, offset + 24)?,
            texture_bomb_height_mask_range: f32_from_const(material, offset + 28)?,
            micro_tessellation_scale: f32_from_const(material, offset + 32)?,
            height_scale: f32_from_const(material, offset + 36)?,
            roughness_white: f32_from_const(material, offset + 64 - shift)?,
            roughness_black: f32_from_const(material, offset + 68 - shift)?,
            ior: f32_from_const(material, offset + 72 - shift)?,
            normal_intensity: f32_from_const(material, offset + 76 - shift)?,
            metallic_white: f32_from_const(material, offset + 80 - shift)?,
            metallic_black: f32_from_const(material, offset + 84 - shift)?,

            color_tint: [
                f32_from_const(material, offset + 96 - shift - tertiary_shift)?,
                f32_from_const(material, offset + 100 - shift - tertiary_shift)?,
                f32_from_const(material, offset + 104 - shift - tertiary_shift)?,
            ],

            color_map_texture_transform: [
                f32_from_const(material, offset + 128 - shift - secondary_shift)?,
                f32_from_const(material, offset + 132 - shift - secondary_shift)?,
                f32_from_const(material, offset + 136 - shift - secondary_shift)?,
                f32_from_const(material, offset + 140 - shift - secondary_shift)?,
            ],

            normal_map_texture_transform: [
                f32_from_const(material, offset + 160 - shift - secondary_shift)?,
                f32_from_const(material, offset + 164 - shift - secondary_shift)?,
                f32_from_const(material, offset + 168 - shift - secondary_shift)?,
                f32_from_const(material, offset + 172 - shift - secondary_shift)?,
            ],

            control_map_texture_transform: [
                f32_from_const(material, offset + 192 - shift - secondary_shift)?,
                f32_from_const(material, offset + 196 - shift - secondary_shift)?,
                f32_from_const(material, offset + 200 - shift - secondary_shift)?,
                f32_from_const(material, offset + 204 - shift - secondary_shift)?,
            ],

            extra_data: None,
        };

        if shift == 0 {
            data.extra_data = Some(ExtraLayerData {
                opacity: f32_from_const(material, offset + 40)?,
                height_blend_range: f32_from_const(material, offset + 44)?,
                height_accumulation: f32_from_const(material, offset + 48)?,
            });
        }

        Ok(data)
    }
}

#[derive(Default, Debug, Serialize)]
pub struct LevelLayer {
    pub layer_type: LayerType,
    pub rohg: Option<RohgLayer>,
    pub rohm: Option<RohmLayer>,
    pub nnhg: Option<NnhgLayer>,
}

#[derive(Default, Debug, Serialize)]
pub struct ConeMapInfo {
    pub parallax_depth: f32,
    pub parallax_height_offset: f32,
    pub quality: f32,
    pub cone_step_fade_near: f32,
    pub cone_step_fade_far: f32,
    pub conemap_texture_transform: [f32; 4],
}

impl ConeMapInfo {
    pub fn read(material: &mut Material, offset: usize) -> anyhow::Result<Self> {
        Ok(Self {
            parallax_depth: f32_from_const(material, offset)?,
            parallax_height_offset: f32_from_const(material, offset + 4)?,
            quality: f32_from_const(material, offset + 8)?,
            cone_step_fade_near: f32_from_const(material, offset + 12)?,
            cone_step_fade_far: f32_from_const(material, offset + 16)?,
            conemap_texture_transform: [
                f32_from_const(material, offset + 32)?,
                f32_from_const(material, offset + 36)?,
                f32_from_const(material, offset + 40)?,
                f32_from_const(material, offset + 44)?,
            ],
        })
    }
}

#[derive(Default, Debug, Serialize)]
pub struct LayeredLevel {
    pub level_type: LevelType,
    pub conemap_info: Option<ConeMapInfo>,
    pub macro_mask_info: Option<MacroMaskInfo>,
    pub layers: Option<Vec<LevelLayer>>,
}

#[derive(Default, Debug, Serialize)]
pub struct Material {
    pub shader: i32,
    pub textures: HashMap<TextureType, i32>,
    pub shader_type: ShaderType,
    pub alpha_blend_mode: String,
    pub style_info: Option<StyleInfo>,
    pub diffuse_info: Option<DiffuseInfo>,
    pub illum_info: Option<SelfIllum>,
    pub decal_slots: Option<DecalSlot>,
    pub color_decal: Option<ColorDecal>,
    pub meter: Option<Meter>,
    pub skin: Option<SkinShader>,
    pub eye: Option<EyeShader>,
    pub hair: Option<Hair>,
    pub layered_level: Option<LayeredLevel>,
    #[serde(skip)]
    pub material_constants: Vec<u8>,
}
