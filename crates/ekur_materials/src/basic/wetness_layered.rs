use anyhow::Result;
use ekur_definitions::material::MaterialPostProcessing;

use crate::{
    utils::{bool_from_const, f32_from_const, get_post_texture},
    {Material, ShaderType, TextureType, WetnessLayered},
};

pub(crate) fn handle_wetness_layered(
    post: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut params = WetnessLayered::default();

    get_post_texture(post, material, 0, TextureType::Wetness)?;

    params.wetness_map_texture_transform = [
        f32_from_const(material, 16)?,
        f32_from_const(material, 20)?,
        f32_from_const(material, 24)?,
        f32_from_const(material, 28)?,
    ];

    params.wetness_height_offset = f32_from_const(material, 32)?;
    params.wetness_previous_height_influence = f32_from_const(material, 36)?;
    params.wetness_height_blend_contrast = f32_from_const(material, 40)?;

    params.wetness_color_tint = [
        f32_from_const(material, 48)?,
        f32_from_const(material, 52)?,
        f32_from_const(material, 56)?,
    ];

    params.wetness_puddle_offset = f32_from_const(material, 60)?;
    params.wetness_puddle_height_blend_contrast = f32_from_const(material, 64)?;

    get_post_texture(post, material, 68, TextureType::WetnessPuddleNormal)?;

    params.wetness_puddle_normal_map_texture_transform = [
        f32_from_const(material, 80)?,
        f32_from_const(material, 84)?,
        f32_from_const(material, 88)?,
        f32_from_const(material, 92)?,
    ];

    params.wetness_puddle_normal_map_uv_scale = f32_from_const(material, 96)?;

    params.wetness_puddle_panning_speed = [
        f32_from_const(material, 100)?,
        f32_from_const(material, 104)?,
    ];

    params.wetness_puddle_normal_intensity = f32_from_const(material, 108)?;

    params.wetness_sediment_offset = f32_from_const(material, 112)?;
    params.wetness_sediment_depth = f32_from_const(material, 116)?;

    params.wetness_sediment_color = [
        f32_from_const(material, 128)?,
        f32_from_const(material, 132)?,
        f32_from_const(material, 136)?,
    ];

    params.wetness_sediment_opacity = f32_from_const(material, 140)?;
    params.debug_wetness_layers = bool_from_const(material, 144)?;

    get_post_texture(post, material, 148, TextureType::MacroMaskMap)?;

    params.macro_mask_map_texture_transform = [
        f32_from_const(material, 160)?,
        f32_from_const(material, 164)?,
        f32_from_const(material, 168)?,
        f32_from_const(material, 172)?,
    ];

    get_post_texture(post, material, 176, TextureType::MacroNormal)?;

    params.macro_normal_texture_transform = [
        f32_from_const(material, 192)?,
        f32_from_const(material, 196)?,
        f32_from_const(material, 200)?,
        f32_from_const(material, 204)?,
    ];

    params.macro_normal_intensity = f32_from_const(material, 208)?;
    params.macro_color_map_uvmode_worldtopdown = bool_from_const(material, 212)?;

    get_post_texture(post, material, 216, TextureType::MacroColor)?;

    params.macro_color_map_texture_transform = [
        f32_from_const(material, 224)?,
        f32_from_const(material, 228)?,
        f32_from_const(material, 232)?,
        f32_from_const(material, 236)?,
    ];

    get_post_texture(post, material, 240, TextureType::MacroCohmap)?;

    params.macro_coh_texture_transform = [
        f32_from_const(material, 256)?,
        f32_from_const(material, 260)?,
        f32_from_const(material, 264)?,
        f32_from_const(material, 268)?,
    ];

    params.macro_height_scale = f32_from_const(material, 272)?;

    params.layer1_tile = [
        f32_from_const(material, 276)?,
        f32_from_const(material, 280)?,
    ];

    params.layer1_height_scale = f32_from_const(material, 284)?;
    params.layer1_height_accumulation = f32_from_const(material, 288)?;

    get_post_texture(post, material, 292, TextureType::Layer1Color)?;

    params.layer1_color_map_texture_transform = [
        f32_from_const(material, 304)?,
        f32_from_const(material, 308)?,
        f32_from_const(material, 312)?,
        f32_from_const(material, 316)?,
    ];

    get_post_texture(post, material, 320, TextureType::Layer1DetailNormal)?;

    params.layer1_normal_map_texture_transform = [
        f32_from_const(material, 336)?,
        f32_from_const(material, 340)?,
        f32_from_const(material, 344)?,
        f32_from_const(material, 348)?,
    ];

    get_post_texture(post, material, 352, TextureType::Layer1Rohm)?;

    params.layer1_rohm_map_texture_transform = [
        f32_from_const(material, 368)?,
        f32_from_const(material, 372)?,
        f32_from_const(material, 376)?,
        f32_from_const(material, 380)?,
    ];

    params.layer1_normal_intensity = f32_from_const(material, 384)?;

    params.layer1_color_tint = [
        f32_from_const(material, 388)?,
        f32_from_const(material, 392)?,
        f32_from_const(material, 396)?,
    ];

    params.layer1_macro_color_intensity = f32_from_const(material, 400)?;
    params.layer1_roughness_white = f32_from_const(material, 404)?;
    params.layer1_roughness_black = f32_from_const(material, 408)?;
    params.layer1_ior = f32_from_const(material, 412)?;
    params.layer1_porosity = f32_from_const(material, 416)?;
    params.layer1_metallic_remap_white = f32_from_const(material, 420)?;
    params.layer1_metallic_remap_black = f32_from_const(material, 424)?;

    params.layer2_enable_roughness = bool_from_const(material, 428)?;
    params.layer2_enable_metallic = bool_from_const(material, 432)?;
    params.layer2_enable_ior = bool_from_const(material, 436)?;
    params.layer2_enable_porosity = bool_from_const(material, 440)?;

    params.layer2_tile = [
        f32_from_const(material, 448)?,
        f32_from_const(material, 452)?,
    ];

    params.layer2_height_offset = f32_from_const(material, 456)?;
    params.layer2_height_scale = f32_from_const(material, 460)?;
    params.layer2_invert_current_height = bool_from_const(material, 464)?;
    params.layer2_previous_height_influence = f32_from_const(material, 468)?;
    params.layer2_curvature_height_influence = f32_from_const(material, 472)?;
    params.layer2_occlusion_height_influence = f32_from_const(material, 476)?;
    params.layer2_height_blend_range = f32_from_const(material, 480)?;
    params.layer2_height_accumulation = f32_from_const(material, 484)?;
    params.layer2_opacity = f32_from_const(material, 488)?;
    params.layer2_occlude_macro = bool_from_const(material, 492)?;

    get_post_texture(post, material, 496, TextureType::Layer2DetailNormal)?;

    params.layer2_normal_map_texture_transform = [
        f32_from_const(material, 512)?,
        f32_from_const(material, 516)?,
        f32_from_const(material, 520)?,
        f32_from_const(material, 524)?,
    ];

    get_post_texture(post, material, 528, TextureType::Layer2Control)?;

    params.layer2_control_map_texture_transform = [
        f32_from_const(material, 544)?,
        f32_from_const(material, 548)?,
        f32_from_const(material, 552)?,
        f32_from_const(material, 556)?,
    ];

    params.layer2_normal_intensity = f32_from_const(material, 560)?;

    params.layer2_top_color = [
        f32_from_const(material, 564)?,
        f32_from_const(material, 568)?,
        f32_from_const(material, 572)?,
    ];
    params.layer2_mid_color = [
        f32_from_const(material, 576)?,
        f32_from_const(material, 580)?,
        f32_from_const(material, 584)?,
    ];
    params.layer2_bottom_color = [
        f32_from_const(material, 592)?,
        f32_from_const(material, 596)?,
        f32_from_const(material, 600)?,
    ];

    params.layer2_macro_color_intensity = f32_from_const(material, 604)?;
    params.layer2_roughness_white = f32_from_const(material, 608)?;
    params.layer2_roughness_black = f32_from_const(material, 612)?;
    params.layer2_ior = f32_from_const(material, 616)?;
    params.layer2_porosity = f32_from_const(material, 620)?;
    params.layer2_metallic = f32_from_const(material, 624)?;

    params.layer3_enable_roughness = bool_from_const(material, 628)?;
    params.layer3_enable_metallic = bool_from_const(material, 632)?;
    params.layer3_enable_ior = bool_from_const(material, 636)?;
    params.layer3_enable_porosity = bool_from_const(material, 640)?;

    params.layer3_tile = [
        f32_from_const(material, 644)?,
        f32_from_const(material, 648)?,
    ];

    params.layer3_height_offset = f32_from_const(material, 652)?;
    params.layer3_height_scale = f32_from_const(material, 656)?;
    params.layer3_invert_current_height = bool_from_const(material, 660)?;
    params.layer3_previous_height_influence = f32_from_const(material, 664)?;
    params.layer3_curvature_height_influence = f32_from_const(material, 668)?;
    params.layer3_occlusion_height_influence = f32_from_const(material, 672)?;
    params.layer3_height_blend_range = f32_from_const(material, 676)?;
    params.layer3_opacity = f32_from_const(material, 680)?;
    params.layer3_occlude_macro = bool_from_const(material, 684)?;

    get_post_texture(post, material, 688, TextureType::Layer3Color)?;

    params.layer3_color_map_texture_transform = [
        f32_from_const(material, 704)?,
        f32_from_const(material, 708)?,
        f32_from_const(material, 712)?,
        f32_from_const(material, 716)?,
    ];

    params.layer3_color_tint = [
        f32_from_const(material, 720)?,
        f32_from_const(material, 724)?,
        f32_from_const(material, 728)?,
    ];

    params.layer3_roughness_white = f32_from_const(material, 732)?;
    params.layer3_roughness_black = f32_from_const(material, 736)?;
    params.layer3_metallic_remap_white = f32_from_const(material, 740)?;
    params.layer3_metallic_remap_black = f32_from_const(material, 744)?;
    params.layer3_macro_color_intensity = f32_from_const(material, 748)?;
    params.layer3_ior = f32_from_const(material, 752)?;
    params.layer3_porosity = f32_from_const(material, 756)?;

    get_post_texture(post, material, 944, TextureType::Layer3Rohm)?;
    params.layer3_rohm_map_texture_transform = [
        f32_from_const(material, 960)?,
        f32_from_const(material, 964)?,
        f32_from_const(material, 968)?,
        f32_from_const(material, 972)?,
    ];

    params.layer4_enable_roughness = bool_from_const(material, 760)?;
    params.layer4_enable_metallic = bool_from_const(material, 764)?;
    params.layer4_enable_ior = bool_from_const(material, 768)?;
    params.layer4_enable_porosity = bool_from_const(material, 772)?;

    params.layer4_tile = [
        f32_from_const(material, 776)?,
        f32_from_const(material, 780)?,
    ];

    params.layer4_height_offset = f32_from_const(material, 784)?;
    params.layer4_height_scale = f32_from_const(material, 788)?;
    params.layer4_invert_current_height = bool_from_const(material, 792)?;
    params.layer4_previous_height_influence = f32_from_const(material, 796)?;
    params.layer4_curvature_height_influence = f32_from_const(material, 800)?;
    params.layer4_occlusion_height_influence = f32_from_const(material, 804)?;
    params.layer4_height_blend_range = f32_from_const(material, 808)?;
    params.layer4_height_accumulation = f32_from_const(material, 812)?;
    params.layer4_opacity = f32_from_const(material, 816)?;
    params.layer4_occlude_macro = bool_from_const(material, 820)?;

    get_post_texture(post, material, 824, TextureType::Layer4Color)?;

    params.layer4_color_map_texture_transform = [
        f32_from_const(material, 832)?,
        f32_from_const(material, 836)?,
        f32_from_const(material, 840)?,
        f32_from_const(material, 844)?,
    ];

    get_post_texture(post, material, 848, TextureType::Layer4DetailNormal)?;

    params.layer4_normal_map_texture_transform = [
        f32_from_const(material, 864)?,
        f32_from_const(material, 868)?,
        f32_from_const(material, 872)?,
        f32_from_const(material, 876)?,
    ];

    params.layer4_normal_intensity = f32_from_const(material, 880)?;

    params.layer4_color_tint = [
        f32_from_const(material, 884)?,
        f32_from_const(material, 888)?,
        f32_from_const(material, 892)?,
    ];

    params.layer4_fresnel_color_tint = [
        f32_from_const(material, 896)?,
        f32_from_const(material, 900)?,
        f32_from_const(material, 904)?,
    ];

    params.layer4_fresnel_intensity = f32_from_const(material, 908)?;
    params.layer4_fresnel_exponent = f32_from_const(material, 912)?;

    params.layer4_roughness_white = f32_from_const(material, 916)?;
    params.layer4_roughness_black = f32_from_const(material, 920)?;
    params.layer4_metallic_remap_white = f32_from_const(material, 924)?;
    params.layer4_metallic_remap_black = f32_from_const(material, 928)?;
    params.layer4_macro_color_intensity = f32_from_const(material, 932)?;
    params.layer4_ior = f32_from_const(material, 936)?;
    params.layer4_porosity = f32_from_const(material, 940)?;

    get_post_texture(post, material, 976, TextureType::Layer4Rohm)?;
    params.layer4_rohm_map_texture_transform = [
        f32_from_const(material, 992)?,
        f32_from_const(material, 996)?,
        f32_from_const(material, 1000)?,
        f32_from_const(material, 1004)?,
    ];

    params.macro_color_intensity = f32_from_const(material, 1008)?;
    params.macro_cavity_exponent = f32_from_const(material, 1012)?;
    params.macro_cavity_intensity = f32_from_const(material, 1016)?;

    get_post_texture(post, material, 1056, TextureType::Cubemap)?;

    material.wetness_layered = Some(params);
    material.shader_type = ShaderType::WetnessLayered;
    Ok(())
}
