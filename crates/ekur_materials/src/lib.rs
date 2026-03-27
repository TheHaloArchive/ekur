/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
mod basic;
mod layered;
pub mod process;
mod utils;

use serde::Serialize;
use std::collections::HashMap;

#[derive(Default, Debug, Serialize)]
pub enum ShaderType {
    #[default]
    Unknown,
    Layered,
    Diffuse,
    Decal,
    SelfIllum,
    ConesteppedLevel,
    ColorDecal,
    ConesteppedDecal,
    Meter,
    SkinShader,
    EyeShader,
    Hair,
    ForerunnerLayered,
    ForestGold,
    WetnessLayered,
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
    Layer1Rohm,
    Layer2DetailNormal,
    Layer2Control,
    Layer3Color,
    Layer3Rohm,
    Layer3DetailNormal,
    Layer3Control,
    Layer4Control,
    Layer4Color,
    Layer4DetailNormal,
    Layer4Rohm,
    Wetness,
    WetnessPuddleNormal,
    MacroColor,
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
pub struct ConemappedLevel {
    pub macro_mask_transform: [f32; 2],
    pub macro_normal_transform: [f32; 2],
    pub macro_normal_intensity: f32,
    pub macro_cohmap_transform: [f32; 2],
    pub macro_height_scale: f32,
    pub macro_conemap_transform: [f32; 2],
    pub macro_cone_depth: f32,
    pub macro_cone_offset: f32,
    pub macro_cone_quality: f32,
    pub macro_noise_transform: [f32; 2],
    pub macro_noise_color: [f32; 3],
    pub macro_noise_roughness: f32,
    pub macro_noise_remap_white: f32,
    pub macro_noise_remap_black: f32,
    pub macro_noise_detail_remap_white: f32,
    pub macro_noise_detail_remap_black: f32,
    pub macro_noise_opacity: f32,
    pub base_normal_intensity: f32,
    pub base_normal_transform: [f32; 2],
    pub base_control_transform: [f32; 2],
    pub base_height_scale: f32,
    pub base_top_color: [f32; 3],
    pub base_mid_color: [f32; 3],
    pub base_bottom_color: [f32; 3],
    pub base_roughness_white: f32,
    pub base_roughness_black: f32,
    pub base_metallic: f32,
    pub base_curvature_height_influence: f32,
    pub base_edge_wear_offset: f32,
    pub base_edge_wear_contrast: f32,
    pub base_edge_wear_opacity: f32,
    pub base_edge_wear_color: [f32; 3],
    pub base_edge_wear_roughness: f32,
    pub shared_control_transform: [f32; 2],
    pub burnt_gradient_transform: [f32; 2],
    pub layer2_height_scale: f32,
    pub char_height_scale: f32,
    pub char_height_offset: f32,
    pub char_opacity: f32,
    pub char_top_color: [f32; 3],
    pub char_mid_color: [f32; 3],
    pub char_bot_color: [f32; 3],
    pub char_roughness_white: f32,
    pub char_roughness_black: f32,
    pub rust_height_scale: f32,
    pub rust_height_offset: f32,
    pub rust_staining_offset: f32,
    pub rust_falloff_color: [f32; 3],
    pub rust_heavy_rust_offset: f32,
    pub rust_heavy_rust_falloff_paint_opacity: f32,
    pub rust_secondary_top_color: [f32; 3],
    pub rust_secondary_mid_color: [f32; 3],
    pub rust_secondary_bottom_color: [f32; 3],
    pub rust_secondary_color_start: f32,
    pub rust_secondary_color_end: f32,
    pub rust_top_color: [f32; 3],
    pub rust_mid_color: [f32; 3],
    pub rust_bottom_color: [f32; 3],
    pub rust_normal_intensity_new: f32,
    pub rust_heavy_rust_edge_start: f32,
    pub rust_heavy_rust_edge_end: f32,
    pub rust_roughness_white: f32,
    pub rust_roughness_black: f32,
    pub rust_metallic: f32,
    pub burnt_height_offset: f32,
    pub burnt_opacity: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct ColorDecal {
    pub opacity: f32,
    pub metallic: f32,
    pub roughness: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct ConesteppedDecal {
    pub parallax_depth: f32,
    pub parallax_height_offset: f32,
    pub normal_intensity: f32,
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

#[derive(Default, Debug, Serialize)]
pub struct LevelLayer {
    pub height_scale: f32,
    pub roughness_white: f32,
    pub roughness_black: f32,
    pub opacity: f32,
    pub ior: f32,
    pub uses_single_metallic: bool,
    pub uses_color_gradient: bool,
    pub uses_packed: bool,
    pub metallic: f32,
    pub metallic_white: f32,
    pub metallic_black: f32,
    pub normal_intensity: f32,
    pub top_color: (f32, f32, f32),
    pub mid_color: (f32, f32, f32),
    pub bot_color: (f32, f32, f32),
    pub color_tint: (f32, f32, f32),
}

#[derive(Default, Debug, Serialize)]
pub struct RegularLevelShader {
    pub macro_normal_intensity: f32,
    pub macro_color_intensity: f32,
    pub macro_roughness_intensity: f32,
    pub macro_occlusion_intensity: f32,
    pub macro_metallic_intensity: f32,
    pub macro_cavity_intensity: f32,
    pub macro_cavity_exponent: f32,
    pub layers: Vec<LevelLayer>,
}

#[derive(Default, Debug, Serialize)]
pub struct ForerunnerLayered {
    pub layer1_normal_texture_transform: [f32; 4],
    pub macro_mask_map_texture_transform: [f32; 4],

    pub layer1_enable_normal_mirror_bitmap_transform: bool,
    pub layer1_enable_normal_mirror_y_bitmap_transform: bool,
    pub layer1_bitmap_transform_scale: [f32; 2],
    pub layer1_normal_intensity: f32,

    pub layer1_cone_texture_texture_transform: [f32; 4],
    pub cone_offset: f32,
    pub layer1_cone_depth: f32,
    pub layer1_cone_quality: f32,
    pub layer1_conestep_fade_start: f32,
    pub layer1_conestep_fade_end: f32,

    pub layer1_coh_texture_texture_transform: [f32; 4],
    pub layer1_base_rohg_texture_texture_transform: [f32; 4],

    pub layer1_color: [f32; 3],
    pub layer1_color_b: [f32; 3],
    pub layer1_metallic: f32,
    pub layer1_ior: f32,
    pub layer1_height_scale: f32,
    pub layer1_base_roughness: f32,
    pub layer1_curvature_roughness_add: f32,

    pub layer1_macro_graphic_texture_transform: [f32; 4],
    pub layer1_macro_graphic_uv: i32,
    pub layer1_macro_graphic_offset: f32,
    pub layer1_macro_graphic_blend_contrast: f32,
    pub layer1_macro_graphic_pattern_masking: f32,
    pub layer1_macro_pattern_opacity: f32,
    pub layer1_macro_graphic_color: [f32; 3],
    pub layer1_macro_roughness: f32,

    pub layer1_submask_texture_transform: [f32; 4],

    pub layer1_primary_graphic_offset: f32,
    pub layer1_primary_graphic_blend_contrast: f32,
    pub layer1_primary_graphic_opacity: f32,
    pub layer1_primary_graphic_color: [f32; 3],
    pub layer1_primary_graphic_color_b: [f32; 3],
    pub layer1_primary_graphic_roughness: f32,

    pub layer1_secondary_graphic_offset: f32,
    pub layer1_secondary_graphic_blend_contrast: f32,
    pub layer1_secondary_pattern_opacity: f32,

    pub layer1_emissive_color: [f32; 3],
    pub emissive_enable_single_float_colors: bool,

    pub layer1_secondary_graphic_color: [f32; 3],
    pub color_r: f32,
    pub color_g: f32,
    pub color_b: f32,

    pub layer1_secondary_graphic_color_b: [f32; 3],
    pub layer1_secondary_graphic_roughness: f32,
    pub layer1_tertiary_pattern_opacity: f32,

    pub layer1_greeble_color: f32,
    pub layer1_greeble_roughness: f32,
    pub layer1_greeble_graphic_pattern_masking: f32,
    pub layer1_greeble_invert_graphic_pattern_masking: bool,
    pub layer1_greeble_opacity: f32,

    pub layer1_wear_offset: f32,
    pub layer1_wear_blend_contrast: f32,
    pub layer1_wear_height_scale: f32,
    pub layer1_wear_curvature_influence: f32,
    pub layer1_wear_opacity: f32,
    pub layer1_wear_color: f32,
    pub layer1_wear_roughness: f32,

    pub layer1_staining_rohg_texture_transform: [f32; 4],
    pub layer1_emissive_pattern_remap_white: f32,
    pub layer1_emissive_pattern_remap_black: f32,

    pub layer1_staining_color: [f32; 3],
    pub layer1_staining_roughness: f32,
    pub layer1_emissive_amount: f32,
    pub layer1_staining_opacity: f32,

    pub layer1_emissive_lens_opacity: f32,
    pub layer1_emissive_lens_color: [f32; 3],

    pub layer1_staining_macro_uv_scale: [f32; 2],
    pub layer1_staining_macro_min: f32,
    pub layer1_staining_macro_max: f32,

    pub layer1_staining_med_uv_scale: [f32; 2],
    pub layer1_staining_med_distance_start: f32,
    pub layer1_staining_med_distance_end: f32,
    pub layer1_staining_med_min: f32,
    pub layer1_staining_med_max: f32,

    pub layer1_emissive_lens_roughness: f32,
    pub layer1_emissive_intensity: f32,
    pub layer1_emissive_lens_metallic: f32,

    pub layer2_enable_roughness: bool,
    pub layer2_enable_metallic: bool,
    pub layer2_enable_ior: bool,
    pub layer2_tile: [f32; 2],
    pub layer2_invert_height_blend: bool,
    pub layer2_height_offset: f32,
    pub layer2_height_blend_range: f32,
    pub layer2_height_scale: f32,
    pub layer2_curvature_height_influence: f32,
    pub layer2_occlusion_height_influence: f32,
    pub layer2_height_accumulation: f32,
    pub layer2_opacity: f32,

    pub layer2_normal_map_texture_transform: [f32; 4],
    pub layer2_control_map_texture_transform: [f32; 4],
    pub layer2_normal_intensity: f32,
    pub layer2_enable_additive_normal: bool,

    pub layer2_top_color: [f32; 3],
    pub layer2_mid_color: [f32; 3],
    pub layer2_bottom_color: [f32; 3],
    pub layer2_roughness_white: f32,
    pub layer2_roughness_black: f32,
    pub layer2_ior: f32,
    pub layer2_metallic: f32,

    pub layer3_enable_roughness: bool,
    pub layer3_enable_metallic: bool,
    pub layer3_enable_ior: bool,
    pub layer3_tile: [f32; 2],
    pub layer3_invert_height_blend: bool,
    pub layer3_height_offset: f32,
    pub layer3_height_scale: f32,
    pub layer3_curvature_height_influence: f32,
    pub layer3_occlusion_height_influence: f32,
    pub layer3_height_blend_range: f32,
    pub layer3_height_accumulation: f32,
    pub layer3_opacity: f32,

    pub layer3_normal_map_texture_transform: [f32; 4],
    pub layer3_control_map_texture_transform: [f32; 4],
    pub layer3_normal_intensity: f32,
    pub layer3_enable_additive_normal: bool,

    pub layer3_top_color: [f32; 3],
    pub layer3_mid_color: [f32; 3],
    pub layer3_bottom_color: [f32; 3],

    pub layer3_secondary_color_start: f32,
    pub layer3_secondary_color_end: f32,
    pub layer3_secondary_top_color: [f32; 3],
    pub layer3_secondary_mid_color: [f32; 3],
    pub layer3_secondary_bottom_color: [f32; 3],

    pub layer3_roughness_white: f32,
    pub layer3_roughness_black: f32,
    pub layer3_metallic: f32,
    pub layer3_ior: f32,

    pub layer4_tile: [f32; 2],
    pub layer4_invert_height_blend: bool,
    pub layer4_height_offset: f32,
    pub layer4_height_blend_range: f32,
    pub layer4_height_scale: f32,
    pub layer4_curvature_height_influence: f32,
    pub layer4_occlusion_height_influence: f32,
    pub layer4_opacity: f32,

    pub layer4_control_map_texture_transform: [f32; 4],
}

#[derive(Default, Debug, Serialize)]
pub struct ForestGold {
    // ─────────────────────────────────────────────
    // Layer 2 (top layer)
    // ─────────────────────────────────────────────
    pub layer2_enable_color_overlay: bool,
    pub layer2_enable_specular: bool,
    pub layer2_uvmode_uv3: bool,

    pub layer2_normal_map_texture_transform: [f32; 4],
    pub layer2_control_map_texture_transform: [f32; 4],

    pub layer2_height_offset: f32,
    pub layer2_height_scale: f32,
    pub layer2_previous_height_influence: f32,
    pub layer2_curvature_height_influence: f32,
    pub layer2_occlusion_height_influence: f32,
    pub layer2_height_blend_range: f32,
    pub layer2_opacity: f32,

    pub layer2_top_color: [f32; 3],
    pub layer2_mid_color: [f32; 3],
    pub layer2_bottom_color: [f32; 3],

    pub layer2_enable_secondary_color: bool,
    pub layer2_secondary_color_start: f32,
    pub layer2_secondary_color_end: f32,
    pub layer2_secondary_top_color: [f32; 3],
    pub layer2_secondary_mid_color: [f32; 3],
    pub layer2_secondary_bottom_color: [f32; 3],

    pub layer2_enable_fresnel: bool,
    pub layer2_fresnel_color_tint: [f32; 3],
    pub layer2_fresnel_intensity: f32,
    pub layer2_fresnel_exponent: f32,
    pub layer2_fresnel_opacity: f32,

    pub layer2_roughness_white: f32,
    pub layer2_roughness_black: f32,
    pub layer2_ior: f32,
    pub layer2_metallic: f32,

    // ─────────────────────────────────────────────
    // Macro
    // ─────────────────────────────────────────────
    pub layer1_uvmode_uv3: bool,
    pub macro_uvmode_uv3: bool,

    pub macro_mask_map_texture_transform: [f32; 4],
    pub macro_normal_texture_transform: [f32; 4],
    pub macro_coh_texture_transform: [f32; 4],

    pub macro_normal_intensity: f32,
    pub macro_height_scale: f32,

    // ─────────────────────────────────────────────
    // Layer 1 (base)
    // ─────────────────────────────────────────────
    pub layer1_color_map_texture_transform: [f32; 4],
    pub layer1_normal_map_texture_transform: [f32; 4],
    pub layer1_rohm_map_texture_transform: [f32; 4],
    pub layer1_emissive_map_texture_transform: [f32; 4],

    pub layer1_height_scale: f32,
    pub layer1_height_accumulation: f32,
    pub layer1_normal_intensity: f32,
    pub layer1_color_saturation: f32,
    pub layer1_color_tint: [f32; 3],

    pub layer1_enable_fresnel: bool,
    pub layer1_fresnel_color_tint: [f32; 3],
    pub layer1_fresnel_intensity: f32,
    pub layer1_fresnel_exponent: f32,
    pub layer1_fresnel_opacity: f32,

    pub layer1_roughness_white: f32,
    pub layer1_roughness_black: f32,
    pub layer1_ior: f32,
    pub layer1_metallic_remap_white: f32,
    pub layer1_metallic_remap_black: f32,

    pub layer1_emissive_color: [f32; 3],
    pub layer1_emissive_amount: f32,
    pub layer1_emissive_intensity: f32,

    // ─────────────────────────────────────────────
    // Macro emissive / misc
    // ─────────────────────────────────────────────
    pub use_cohe_alpha: bool,

    pub macro_emissive_color: [f32; 3],
    pub macro_emissive_amount: f32,
    pub macro_emissive_intensity: f32,

    pub macro_cavity_exponent: f32,
    pub macro_cavity_intensity: f32,

    pub layer2_normal_intensity: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct WetnessLayered {
    // ─────────────────────────────────────────────
    // Wetness
    // ─────────────────────────────────────────────
    pub wetness_map_texture_transform: [f32; 4],
    pub wetness_height_offset: f32,
    pub wetness_previous_height_influence: f32,
    pub wetness_height_blend_contrast: f32,
    pub wetness_color_tint: [f32; 3],
    pub wetness_puddle_offset: f32,
    pub wetness_puddle_height_blend_contrast: f32,

    pub wetness_puddle_normal_map_texture_transform: [f32; 4],
    pub wetness_puddle_normal_map_uv_scale: f32,
    pub wetness_puddle_panning_speed: [f32; 2],
    pub wetness_puddle_normal_intensity: f32,

    pub wetness_sediment_offset: f32,
    pub wetness_sediment_depth: f32,
    pub wetness_sediment_color: [f32; 3],
    pub wetness_sediment_opacity: f32,

    pub debug_wetness_layers: bool,

    // ─────────────────────────────────────────────
    // Macro
    // ─────────────────────────────────────────────
    pub macro_mask_map_texture_transform: [f32; 4],
    pub macro_normal_texture_transform: [f32; 4],
    pub macro_normal_intensity: f32,

    pub macro_color_map_uvmode_worldtopdown: bool,
    pub macro_color_map_texture_transform: [f32; 4],
    pub macro_coh_texture_transform: [f32; 4],

    pub macro_height_scale: f32,

    // ─────────────────────────────────────────────
    // Layer 1
    // ─────────────────────────────────────────────
    pub layer1_tile: [f32; 2],
    pub layer1_height_scale: f32,
    pub layer1_height_accumulation: f32,

    pub layer1_color_map_texture_transform: [f32; 4],
    pub layer1_normal_map_texture_transform: [f32; 4],
    pub layer1_rohm_map_texture_transform: [f32; 4],

    pub layer1_normal_intensity: f32,
    pub layer1_color_tint: [f32; 3],
    pub layer1_macro_color_intensity: f32,

    pub layer1_roughness_white: f32,
    pub layer1_roughness_black: f32,
    pub layer1_ior: f32,
    pub layer1_porosity: f32,
    pub layer1_metallic_remap_white: f32,
    pub layer1_metallic_remap_black: f32,

    // ─────────────────────────────────────────────
    // Layer 2
    // ─────────────────────────────────────────────
    pub layer2_enable_roughness: bool,
    pub layer2_enable_metallic: bool,
    pub layer2_enable_ior: bool,
    pub layer2_enable_porosity: bool,

    pub layer2_tile: [f32; 2],
    pub layer2_height_offset: f32,
    pub layer2_height_scale: f32,
    pub layer2_invert_current_height: bool,
    pub layer2_previous_height_influence: f32,
    pub layer2_curvature_height_influence: f32,
    pub layer2_occlusion_height_influence: f32,
    pub layer2_height_blend_range: f32,
    pub layer2_height_accumulation: f32,
    pub layer2_opacity: f32,
    pub layer2_occlude_macro: bool,

    pub layer2_normal_map_texture_transform: [f32; 4],
    pub layer2_control_map_texture_transform: [f32; 4],
    pub layer2_rohm_map_texture_transform: [f32; 4],
    pub layer2_normal_intensity: f32,

    pub layer2_top_color: [f32; 3],
    pub layer2_mid_color: [f32; 3],
    pub layer2_bottom_color: [f32; 3],

    pub layer2_macro_color_intensity: f32,
    pub layer2_roughness_white: f32,
    pub layer2_roughness_black: f32,
    pub layer2_ior: f32,
    pub layer2_porosity: f32,
    pub layer2_metallic: f32,

    // ─────────────────────────────────────────────
    // Layer 3
    // ─────────────────────────────────────────────
    pub layer3_enable_roughness: bool,
    pub layer3_enable_metallic: bool,
    pub layer3_enable_ior: bool,
    pub layer3_enable_porosity: bool,

    pub layer3_tile: [f32; 2],
    pub layer3_height_offset: f32,
    pub layer3_height_scale: f32,
    pub layer3_invert_current_height: bool,
    pub layer3_previous_height_influence: f32,
    pub layer3_curvature_height_influence: f32,
    pub layer3_occlusion_height_influence: f32,
    pub layer3_height_blend_range: f32,
    pub layer3_opacity: f32,
    pub layer3_occlude_macro: bool,

    pub layer3_color_map_texture_transform: [f32; 4],
    pub layer3_rohm_map_texture_transform: [f32; 4],
    pub layer3_color_tint: [f32; 3],
    pub layer3_roughness_white: f32,
    pub layer3_roughness_black: f32,
    pub layer3_metallic_remap_white: f32,
    pub layer3_metallic_remap_black: f32,
    pub layer3_macro_color_intensity: f32,
    pub layer3_ior: f32,
    pub layer3_porosity: f32,

    // ─────────────────────────────────────────────
    // Layer 4
    // ─────────────────────────────────────────────
    pub layer4_enable_roughness: bool,
    pub layer4_enable_metallic: bool,
    pub layer4_enable_ior: bool,
    pub layer4_enable_porosity: bool,

    pub layer4_tile: [f32; 2],
    pub layer4_height_offset: f32,
    pub layer4_height_scale: f32,
    pub layer4_invert_current_height: bool,
    pub layer4_previous_height_influence: f32,
    pub layer4_curvature_height_influence: f32,
    pub layer4_occlusion_height_influence: f32,
    pub layer4_height_blend_range: f32,
    pub layer4_height_accumulation: f32,
    pub layer4_opacity: f32,
    pub layer4_occlude_macro: bool,

    pub layer4_color_map_texture_transform: [f32; 4],
    pub layer4_normal_map_texture_transform: [f32; 4],
    pub layer4_rohm_map_texture_transform: [f32; 4],
    pub layer4_normal_intensity: f32,

    pub layer4_color_tint: [f32; 3],
    pub layer4_fresnel_color_tint: [f32; 3],
    pub layer4_fresnel_intensity: f32,
    pub layer4_fresnel_exponent: f32,

    pub layer4_roughness_white: f32,
    pub layer4_roughness_black: f32,
    pub layer4_metallic_remap_white: f32,
    pub layer4_metallic_remap_black: f32,
    pub layer4_macro_color_intensity: f32,
    pub layer4_ior: f32,
    pub layer4_porosity: f32,

    // ─────────────────────────────────────────────
    // Macro misc
    // ─────────────────────────────────────────────
    pub macro_color_intensity: f32,
    pub macro_cavity_exponent: f32,
    pub macro_cavity_intensity: f32,
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
    pub conemapped_level: Option<ConemappedLevel>,
    pub color_decal: Option<ColorDecal>,
    pub conestepped_decal: Option<ConesteppedDecal>,
    pub meter: Option<Meter>,
    pub skin: Option<SkinShader>,
    pub eye: Option<EyeShader>,
    pub hair: Option<Hair>,
    pub level: Option<RegularLevelShader>,
    pub forerunner_layered: Option<ForerunnerLayered>,
    pub forest_gold: Option<ForestGold>,
    pub wetness_layered: Option<WetnessLayered>,
    #[serde(skip)]
    pub material_constants: Vec<u8>,
}
