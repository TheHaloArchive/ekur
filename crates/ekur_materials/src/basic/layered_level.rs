/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use anyhow::Result;
use ekur_definitions::material::MaterialPostProcessing;

use crate::{
    ConeMapInfo, LayerType, LayeredLevel, LevelLayer, LevelType, MacroMaskInfo, Material,
    NnhgLayer, RohgLayer, RohmLayer, ShaderType, TextureType, utils::get_post_texture,
};

pub(crate) fn handle_rohg_3_rohm_1_mm(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    get_post_texture(post_process, material, 36, TextureType::MacroControl)?;
    level_shader.macro_mask_info = Some(MacroMaskInfo::read(material, 16)?);
    level_shader.level_type = LevelType::Rohg3Rohm1MM;

    let layer1 = RohgLayer::read(material, 84, true, false)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 240, TextureType::Layer1Control)?;
    get_post_texture(post_process, material, 204, TextureType::Layer1Normal)?;

    let layer2 = RohgLayer::read(material, 272, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 432, TextureType::Layer2Control)?;
    get_post_texture(post_process, material, 396, TextureType::Layer2Normal)?;

    let layer3 = RohgLayer::read(material, 464, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 624, TextureType::Layer3Control)?;
    get_post_texture(post_process, material, 588, TextureType::Layer3Normal)?;

    let layer4 = RohmLayer::read(material, 656, false, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 764, TextureType::Layer4Color)?;
    get_post_texture(post_process, material, 832, TextureType::Layer4Control)?;
    get_post_texture(post_process, material, 800, TextureType::Layer4Normal)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohm_2_pack_2_mm(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    get_post_texture(post_process, material, 36, TextureType::MacroControl)?;
    level_shader.macro_mask_info = Some(MacroMaskInfo::read(material, 16)?);
    level_shader.level_type = LevelType::Rohm2Pack2MM;

    let layer1 = RohmLayer::read(material, 84, true, false)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 176, TextureType::Layer1Color)?;
    get_post_texture(post_process, material, 240, TextureType::Layer1Control)?;
    get_post_texture(post_process, material, 208, TextureType::Layer1Normal)?;

    let layer2 = RohmLayer::read(material, 272, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer2),
        ..Default::default()
    };

    get_post_texture(post_process, material, 380, TextureType::Layer2Color)?;
    get_post_texture(post_process, material, 448, TextureType::Layer2Control)?;
    get_post_texture(post_process, material, 416, TextureType::Layer2Normal)?;

    let layer3 = NnhgLayer::read(material, 480, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::NnhgLayer,
        nnhg: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 604, TextureType::Layer3Packed)?;

    let layer4 = NnhgLayer::read(material, 640, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::NnhgLayer,
        nnhg: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 764, TextureType::Layer4Packed)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohm_3_rohg_1_mm_cone(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 48, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 56, TextureType::MacroNormal)?;
    get_post_texture(post_process, material, 84, TextureType::MacroControl)?;
    get_post_texture(post_process, material, 20, TextureType::MacroConemap)?;
    level_shader.macro_mask_info = Some(MacroMaskInfo::read(material, 64)?);
    level_shader.conemap_info = Some(ConeMapInfo::read(material, 0)?);
    level_shader.level_type = LevelType::Rohm3Rohg1MMCone;

    let layer1 = RohmLayer::read(material, 132, true, false)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 224, TextureType::Layer1Color)?;
    get_post_texture(post_process, material, 288, TextureType::Layer1Control)?;
    get_post_texture(post_process, material, 256, TextureType::Layer1Normal)?;

    let layer2 = RohgLayer::read(material, 320, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer2),
        ..Default::default()
    };

    get_post_texture(post_process, material, 480, TextureType::Layer2Control)?;
    get_post_texture(post_process, material, 444, TextureType::Layer2Normal)?;

    let layer3 = RohmLayer::read(material, 512, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 620, TextureType::Layer3Color)?;
    get_post_texture(post_process, material, 688, TextureType::Layer3Control)?;
    get_post_texture(post_process, material, 656, TextureType::Layer3Normal)?;

    let layer4 = RohmLayer::read(material, 720, false, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 828, TextureType::Layer4Color)?;
    get_post_texture(post_process, material, 896, TextureType::Layer4Control)?;
    get_post_texture(post_process, material, 864, TextureType::Layer4Normal)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohm_3_mm(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    get_post_texture(post_process, material, 36, TextureType::MacroControl)?;
    level_shader.macro_mask_info = Some(MacroMaskInfo::read(material, 16)?);
    level_shader.level_type = LevelType::Rohm3MM;

    let layer1 = RohmLayer::read(material, 84, true, false)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 176, TextureType::Layer1Color)?;
    get_post_texture(post_process, material, 240, TextureType::Layer1Control)?;
    get_post_texture(post_process, material, 208, TextureType::Layer1Normal)?;

    let layer2 = RohmLayer::read(material, 272, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 380, TextureType::Layer2Color)?;
    get_post_texture(post_process, material, 448, TextureType::Layer2Control)?;
    get_post_texture(post_process, material, 416, TextureType::Layer2Normal)?;

    let layer3 = RohmLayer::read(material, 480, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 588, TextureType::Layer3Color)?;
    get_post_texture(post_process, material, 656, TextureType::Layer3Control)?;
    get_post_texture(post_process, material, 624, TextureType::Layer3Normal)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohg_4_mm(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    get_post_texture(post_process, material, 36, TextureType::MacroControl)?;
    level_shader.macro_mask_info = Some(MacroMaskInfo::read(material, 16)?);
    level_shader.level_type = LevelType::Rohg4MM;

    let layer1 = RohgLayer::read(material, 84, true, false)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 240, TextureType::Layer1Control)?;
    get_post_texture(post_process, material, 204, TextureType::Layer1Normal)?;

    let layer2 = RohgLayer::read(material, 272, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 432, TextureType::Layer2Control)?;
    get_post_texture(post_process, material, 396, TextureType::Layer2Normal)?;

    let layer3 = RohgLayer::read(material, 464, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 588, TextureType::Layer3Normal)?;
    get_post_texture(post_process, material, 624, TextureType::Layer3Control)?;

    let layer4 = RohgLayer::read(material, 656, false, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 780, TextureType::Layer4Normal)?;
    get_post_texture(post_process, material, 816, TextureType::Layer4Control)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohm_2_rohg_2_mm(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    get_post_texture(post_process, material, 36, TextureType::MacroControl)?;
    level_shader.macro_mask_info = Some(MacroMaskInfo::read(material, 16)?);
    level_shader.level_type = LevelType::Rohm2Rohg2MM;

    let layer1 = RohmLayer::read(material, 84, true, false)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 176, TextureType::Layer1Color)?;
    get_post_texture(post_process, material, 240, TextureType::Layer1Control)?;
    get_post_texture(post_process, material, 208, TextureType::Layer1Normal)?;

    let layer2 = RohmLayer::read(material, 272, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 380, TextureType::Layer2Color)?;
    get_post_texture(post_process, material, 448, TextureType::Layer2Control)?;
    get_post_texture(post_process, material, 416, TextureType::Layer2Normal)?;

    let layer3 = RohgLayer::read(material, 480, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 604, TextureType::Layer3Normal)?;
    get_post_texture(post_process, material, 640, TextureType::Layer3Control)?;

    let layer4 = RohgLayer::read(material, 672, false, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 796, TextureType::Layer4Normal)?;
    get_post_texture(post_process, material, 832, TextureType::Layer4Control)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohm_2_rohg_2(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    level_shader.level_type = LevelType::Rohm2Rohg2NoControl;

    let layer1 = RohmLayer::read(material, 44, false, true)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 140, TextureType::Layer1Color)?;
    get_post_texture(post_process, material, 208, TextureType::Layer1Control)?;
    get_post_texture(post_process, material, 176, TextureType::Layer1Normal)?;

    let layer2 = RohgLayer::read(material, 240, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 400, TextureType::Layer2Control)?;
    get_post_texture(post_process, material, 364, TextureType::Layer2Normal)?;

    let layer3 = RohgLayer::read(material, 432, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 592, TextureType::Layer3Control)?;
    get_post_texture(post_process, material, 556, TextureType::Layer3Normal)?;

    let layer4 = RohmLayer::read(material, 624, false, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 732, TextureType::Layer4Color)?;
    get_post_texture(post_process, material, 800, TextureType::Layer4Control)?;
    get_post_texture(post_process, material, 768, TextureType::Layer4Normal)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohm_1_rohg_2_nnhg_1(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    level_shader.level_type = LevelType::Rohm1Rohg2Nnhg1NoControl;

    let layer1 = RohgLayer::read(material, 44, false, true)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 192, TextureType::Layer1Control)?;
    get_post_texture(post_process, material, 156, TextureType::Layer1Normal)?;

    let layer2 = RohgLayer::read(material, 224, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 348, TextureType::Layer2Packed)?;

    let layer3 = RohmLayer::read(material, 384, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 492, TextureType::Layer3Color)?;
    get_post_texture(post_process, material, 560, TextureType::Layer3Control)?;
    get_post_texture(post_process, material, 528, TextureType::Layer3Normal)?;

    let layer4 = RohgLayer::read(material, 592, false, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 752, TextureType::Layer4Control)?;
    get_post_texture(post_process, material, 716, TextureType::Layer4Normal)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohg_3_rohm_1(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    level_shader.level_type = LevelType::Rohg3Rohm1NoControl;

    let layer1 = RohgLayer::read(material, 44, false, true)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 192, TextureType::Layer1Control)?;
    get_post_texture(post_process, material, 156, TextureType::Layer1Normal)?;

    let layer2 = RohgLayer::read(material, 224, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 384, TextureType::Layer2Control)?;
    get_post_texture(post_process, material, 348, TextureType::Layer2Normal)?;

    let layer3 = RohgLayer::read(material, 416, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 576, TextureType::Layer3Control)?;
    get_post_texture(post_process, material, 540, TextureType::Layer3Normal)?;

    let layer4 = RohmLayer::read(material, 608, false, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 716, TextureType::Layer4Color)?;
    get_post_texture(post_process, material, 784, TextureType::Layer4Control)?;
    get_post_texture(post_process, material, 752, TextureType::Layer4Normal)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohg_2_rohm_2_mm_alt(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    get_post_texture(post_process, material, 36, TextureType::MacroControl)?;
    level_shader.macro_mask_info = Some(MacroMaskInfo::read(material, 16)?);
    level_shader.level_type = LevelType::Rohm2Rohg2MM;

    let layer1 = RohmLayer::read(material, 84, true, false)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 176, TextureType::Layer1Color)?;
    get_post_texture(post_process, material, 240, TextureType::Layer1Control)?;
    get_post_texture(post_process, material, 208, TextureType::Layer1Normal)?;

    let layer2 = RohgLayer::read(material, 272, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 432, TextureType::Layer2Control)?;
    get_post_texture(post_process, material, 396, TextureType::Layer2Normal)?;

    let layer3 = RohgLayer::read(material, 464, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 624, TextureType::Layer3Control)?;
    get_post_texture(post_process, material, 588, TextureType::Layer3Normal)?;

    let layer4 = RohmLayer::read(material, 656, false, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 764, TextureType::Layer4Color)?;
    get_post_texture(post_process, material, 832, TextureType::Layer4Control)?;
    get_post_texture(post_process, material, 800, TextureType::Layer4Normal)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohg_2_rohm_1_nnhg_1_mm(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    get_post_texture(post_process, material, 36, TextureType::MacroColor)?;
    get_post_texture(post_process, material, 68, TextureType::MacroControl)?;
    level_shader.macro_mask_info = Some(MacroMaskInfo::read(material, 16)?);
    level_shader.level_type = LevelType::Rohg2Rohm1Nnhg1MM;

    let layer1 = RohgLayer::read(material, 116, true, false)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 236, TextureType::Layer1Normal)?;
    get_post_texture(post_process, material, 272, TextureType::Layer1Control)?;

    let layer2 = RohgLayer::read(material, 304, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 428, TextureType::Layer2Normal)?;
    get_post_texture(post_process, material, 464, TextureType::Layer2Control)?;

    let layer3 = RohmLayer::read(material, 496, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 604, TextureType::Layer3Color)?;
    get_post_texture(post_process, material, 640, TextureType::Layer3Normal)?;
    get_post_texture(post_process, material, 672, TextureType::Layer3Control)?;

    let layer4 = NnhgLayer::read(material, 704, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::NnhgLayer,
        nnhg: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 828, TextureType::Layer4Packed)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohg_1_rohm_2_nnhg_1_mm(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    get_post_texture(post_process, material, 8, TextureType::MacroNormal)?;
    get_post_texture(post_process, material, 36, TextureType::MacroControl)?;
    level_shader.macro_mask_info = Some(MacroMaskInfo::read(material, 16)?);
    level_shader.level_type = LevelType::Rohg1Rohm2Nnhg1MM;

    let layer1 = RohgLayer::read(material, 84, true, false)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 204, TextureType::Layer1Normal)?;
    get_post_texture(post_process, material, 240, TextureType::Layer1Control)?;

    let layer2 = RohmLayer::read(material, 272, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 380, TextureType::Layer2Color)?;
    get_post_texture(post_process, material, 416, TextureType::Layer2Normal)?;
    get_post_texture(post_process, material, 448, TextureType::Layer2Control)?;

    let layer3 = RohmLayer::read(material, 480, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 588, TextureType::Layer3Color)?;
    get_post_texture(post_process, material, 624, TextureType::Layer3Normal)?;
    get_post_texture(post_process, material, 656, TextureType::Layer3Control)?;

    let layer4 = NnhgLayer::read(material, 688, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::NnhgLayer,
        nnhg: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 812, TextureType::Layer4Packed)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohm_2_rohg_1_nnhg_1(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    level_shader.level_type = LevelType::Rohm2Rohg1Nnhg1;

    let layer1 = RohmLayer::read(material, 16, false, true)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 112, TextureType::Layer1Color)?;
    get_post_texture(post_process, material, 144, TextureType::Layer1Normal)?;
    get_post_texture(post_process, material, 176, TextureType::Layer1Control)?;

    let layer2 = RohmLayer::read(material, 208, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 316, TextureType::Layer2Color)?;
    get_post_texture(post_process, material, 352, TextureType::Layer2Normal)?;
    get_post_texture(post_process, material, 384, TextureType::Layer2Control)?;

    let layer3 = RohgLayer::read(material, 416, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 540, TextureType::Layer3Normal)?;
    get_post_texture(post_process, material, 576, TextureType::Layer3Control)?;

    let layer4 = NnhgLayer::read(material, 608, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::NnhgLayer,
        nnhg: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 732, TextureType::Layer4Packed)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohm_3_nnhg_1(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    level_shader.level_type = LevelType::Rohm3Nnhg1;

    let layer1 = RohmLayer::read(material, 16, true, true)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 112, TextureType::Layer1Color)?;
    get_post_texture(post_process, material, 144, TextureType::Layer1Normal)?;
    get_post_texture(post_process, material, 176, TextureType::Layer1Control)?;

    let layer2 = RohmLayer::read(material, 208, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 316, TextureType::Layer2Color)?;
    get_post_texture(post_process, material, 352, TextureType::Layer2Normal)?;
    get_post_texture(post_process, material, 384, TextureType::Layer2Control)?;

    let layer3 = RohmLayer::read(material, 416, false, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 524, TextureType::Layer3Color)?;
    get_post_texture(post_process, material, 560, TextureType::Layer3Normal)?;
    get_post_texture(post_process, material, 592, TextureType::Layer3Control)?;

    let layer4 = NnhgLayer::read(material, 624, false)?;
    let norm_layer4 = LevelLayer {
        layer_type: LayerType::NnhgLayer,
        nnhg: Some(layer4),
        ..Default::default()
    };
    get_post_texture(post_process, material, 748, TextureType::Layer4Packed)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3, norm_layer4]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}

pub(crate) fn handle_rohm_1_rohg_1_nnhg_1(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut level_shader = LayeredLevel::default();
    get_post_texture(post_process, material, 0, TextureType::MacroMaskMap)?;
    level_shader.level_type = LevelType::Rohm1Rohg1Nnhg1;

    let layer1 = RohmLayer::read(material, 16, true, true)?;
    let norm_layer1 = LevelLayer {
        layer_type: LayerType::RohmLayer,
        rohm: Some(layer1),
        ..Default::default()
    };
    get_post_texture(post_process, material, 112, TextureType::Layer1Color)?;
    get_post_texture(post_process, material, 144, TextureType::Layer1Normal)?;
    get_post_texture(post_process, material, 176, TextureType::Layer1Control)?;

    let layer2 = RohgLayer::read(material, 208, false, false)?;
    let norm_layer2 = LevelLayer {
        layer_type: LayerType::RohgLayer,
        rohg: Some(layer2),
        ..Default::default()
    };
    get_post_texture(post_process, material, 332, TextureType::Layer2Normal)?;
    get_post_texture(post_process, material, 368, TextureType::Layer2Control)?;

    let layer3 = NnhgLayer::read(material, 400, false)?;
    let norm_layer3 = LevelLayer {
        layer_type: LayerType::NnhgLayer,
        nnhg: Some(layer3),
        ..Default::default()
    };
    get_post_texture(post_process, material, 524, TextureType::Layer3Packed)?;

    level_shader.layers = Some(vec![norm_layer1, norm_layer2, norm_layer3]);
    material.layered_level = Some(level_shader);
    material.shader_type = ShaderType::LayeredLevel;
    Ok(())
}
