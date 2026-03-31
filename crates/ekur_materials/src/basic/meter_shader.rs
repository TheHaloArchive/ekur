/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use anyhow::Result;
use ekur_definitions::material::MaterialPostProcessing;

use crate::utils::{f32_from_const, get_post_texture};

use crate::{Material, Meter, ShaderType, TextureType};

pub(crate) fn handle_meter_shader(
    post_process: &MaterialPostProcessing,
    material: &mut Material,
) -> Result<()> {
    let mut meter_shader = Meter::default();
    get_post_texture(post_process, material, 0, TextureType::Meter)?;
    meter_shader.meter_off_color = (
        f32_from_const(material, 32)?,
        f32_from_const(material, 36)?,
        f32_from_const(material, 40)?,
    );
    meter_shader.meter_on_color = (
        f32_from_const(material, 48)?,
        f32_from_const(material, 52)?,
        f32_from_const(material, 56)?,
    );
    meter_shader.meter_value = f32_from_const(material, 60)?;
    meter_shader.meter_intensity = f32_from_const(material, 64)?;
    material.meter = Some(meter_shader);
    material.shader_type = ShaderType::Meter;
    Ok(())
}
