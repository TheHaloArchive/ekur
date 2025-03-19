use anyhow::Result;

use crate::definitions::material::MaterialPostProcessing;

use super::{
    common_utils::{f32_from_const, get_post_texture},
    serde_definitions::{Material, RegularLevelShader, ShaderType, TextureType},
};

pub(super) fn handle_regular_level(
    post: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut regular_level = RegularLevelShader::default();
    get_post_texture(post, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post, material, 8, TextureType::MacroNormal)?;
    regular_level.macro_normal_intensity = f32_from_const(material, 32)?;
    get_post_texture(post, material, 36, TextureType::Color)?;
    regular_level.macro_color_intensity = f32_from_const(material, 64)?;
    get_post_texture(post, material, 68, TextureType::Control)?;
    regular_level.macro_roughness_intensity = f32_from_const(material, 96)?;
    regular_level.macro_occlusion_intensity = f32_from_const(material, 100)?;
    regular_level.macro_metallic_intensity = f32_from_const(material, 104)?;
    regular_level.macro_cavity_intensity = f32_from_const(material, 108)?;
    regular_level.macro_cavity_exponent = f32_from_const(material, 112)?;
    regular_level.layer1_height_scale = f32_from_const(material, 152)?;
    regular_level.layer1_roughness_white = f32_from_const(material, 172)?;
    regular_level.layer1_roughness_black = f32_from_const(material, 176)?;
    regular_level.layer1_ior = f32_from_const(material, 180)?;
    regular_level.layer1_normal_intensity = f32_from_const(material, 184)?;
    regular_level.layer1_metallic = f32_from_const(material, 188)?;
    regular_level.layer1_top_color = (
        f32_from_const(material, 192)?,
        f32_from_const(material, 196)?,
        f32_from_const(material, 200)?,
    );
    regular_level.layer1_mid_color = (
        f32_from_const(material, 208)?,
        f32_from_const(material, 212)?,
        f32_from_const(material, 216)?,
    );
    regular_level.layer1_bot_color = (
        f32_from_const(material, 224)?,
        f32_from_const(material, 228)?,
        f32_from_const(material, 232)?,
    );
    regular_level.layer1_normal_transform = [
        f32_from_const(material, 256)?,
        f32_from_const(material, 260)?,
    ];
    regular_level.layer1_control_transform = [
        f32_from_const(material, 288)?,
        f32_from_const(material, 292)?,
    ];
    get_post_texture(post, material, 236, TextureType::Layer1Normal)?;
    get_post_texture(post, material, 272, TextureType::Layer1Control)?;
    regular_level.layer2_height_scale = f32_from_const(material, 340)?;
    regular_level.layer2_opacity = f32_from_const(material, 344)?;
    regular_level.layer2_roughness_white = f32_from_const(material, 368)?;
    regular_level.layer2_roughness_black = f32_from_const(material, 372)?;
    regular_level.layer2_ior = f32_from_const(material, 376)?;
    regular_level.layer2_normal_intensity = f32_from_const(material, 380)?;
    regular_level.layer2_metallic_white = f32_from_const(material, 384)?;
    regular_level.layer2_metallic_black = f32_from_const(material, 388)?;
    regular_level.layer2_color_tint = (
        f32_from_const(material, 400)?,
        f32_from_const(material, 404)?,
        f32_from_const(material, 408)?,
    );
    get_post_texture(post, material, 412, TextureType::Layer2Color)?;
    get_post_texture(post, material, 448, TextureType::Layer2Normal)?;
    get_post_texture(post, material, 480, TextureType::Layer2Control)?;
    regular_level.layer2_color_transform = [
        f32_from_const(material, 432)?,
        f32_from_const(material, 436)?,
    ];
    regular_level.layer2_normal_transform = [
        f32_from_const(material, 464)?,
        f32_from_const(material, 468)?,
    ];
    regular_level.layer2_control_transform = [
        f32_from_const(material, 496)?,
        f32_from_const(material, 500)?,
    ];
    regular_level.layer3_height_scale = f32_from_const(material, 548)?;
    regular_level.layer3_opacity = f32_from_const(material, 552)?;
    regular_level.layer3_roughness_white = f32_from_const(material, 576)?;
    regular_level.layer3_roughness_black = f32_from_const(material, 580)?;
    regular_level.layer3_ior = f32_from_const(material, 584)?;
    regular_level.layer3_normal_intensity = f32_from_const(material, 588)?;
    regular_level.layer3_metallic_white = f32_from_const(material, 592)?;
    regular_level.layer3_metallic_black = f32_from_const(material, 596)?;
    regular_level.layer3_color_tint = (
        f32_from_const(material, 608)?,
        f32_from_const(material, 612)?,
        f32_from_const(material, 616)?,
    );
    get_post_texture(post, material, 620, TextureType::Layer3Color)?;
    get_post_texture(post, material, 656, TextureType::Layer3Normal)?;
    get_post_texture(post, material, 688, TextureType::Layer3Control)?;
    regular_level.layer3_color_transform = [
        f32_from_const(material, 640)?,
        f32_from_const(material, 644)?,
    ];
    regular_level.layer3_normal_transform = [
        f32_from_const(material, 672)?,
        f32_from_const(material, 676)?,
    ];
    regular_level.layer3_control_transform = [
        f32_from_const(material, 704)?,
        f32_from_const(material, 708)?,
    ];

    regular_level.layer4_height_scale = f32_from_const(material, 756)?;
    regular_level.layer4_opacity = f32_from_const(material, 760)?;
    regular_level.layer4_roughness_white = f32_from_const(material, 784)?;
    regular_level.layer4_roughness_black = f32_from_const(material, 788)?;
    regular_level.layer4_ior = f32_from_const(material, 792)?;
    regular_level.layer4_normal_intensity = f32_from_const(material, 796)?;
    regular_level.layer4_metallic = f32_from_const(material, 800)?;
    regular_level.layer4_top_color = (
        f32_from_const(material, 804)?,
        f32_from_const(material, 808)?,
        f32_from_const(material, 812)?,
    );
    regular_level.layer4_mid_color = (
        f32_from_const(material, 816)?,
        f32_from_const(material, 820)?,
        f32_from_const(material, 824)?,
    );
    regular_level.layer4_bot_color = (
        f32_from_const(material, 832)?,
        f32_from_const(material, 836)?,
        f32_from_const(material, 840)?,
    );
    get_post_texture(post, material, 844, TextureType::Layer4Packed)?;
    regular_level.layer4_packed_transform = [
        f32_from_const(material, 864)?,
        f32_from_const(material, 868)?,
    ];

    material.level = Some(regular_level);
    material.shader_type = ShaderType::RegularLevelShader;
    Ok(())
}
