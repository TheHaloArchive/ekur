/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use anyhow::Result;

use crate::definitions::material::{MaterialPostProcessing, MaterialTag};

use super::serde_definitions::{Material, TextureType};

pub(super) fn get_post_texture(
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
            .insert(texture_type, tex.bitmap_reference.global_id);
    };
    Ok(())
}

pub(super) fn f32_from_const(material: &mut Material, start_index: usize) -> Result<f32> {
    let val =
        f32::from_ne_bytes(material.material_constants[start_index..start_index + 4].try_into()?);
    Ok(val)
}

pub(super) fn f32_from_params(mat: &MaterialTag, name: i32) -> Result<f32> {
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

pub(super) fn collect_constants(mat: &MaterialTag, material: &mut Material) -> Result<()> {
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
