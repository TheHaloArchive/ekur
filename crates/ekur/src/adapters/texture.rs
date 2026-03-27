/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use ekur_definitions::{coating_swatch::CoatingSwatchPODTag, material_swatch::MaterialSwatchTag};
use ekur_materials::TextureType;
use ekur_texture::process::process_image;

use anyhow::Result;
use image::ImageFormat;
use infinite_rs::ModuleFile;
use std::{
    collections::{HashMap, HashSet},
    fs::create_dir_all,
    path::PathBuf,
};

pub(crate) fn extract_texture(
    modules: &mut [ModuleFile],
    mut textures: HashMap<i32, TextureType>,
    coat_swatches: &HashMap<i32, CoatingSwatchPODTag>,
    mat_swatches: &HashMap<i32, MaterialSwatchTag>,
    save_path: &str,
) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    save_path.push("bitmaps/");
    create_dir_all(&save_path)?;
    let mut processed_textures = HashSet::new();

    for swatch in coat_swatches.values() {
        textures.insert(swatch.color_gradient_map.global_id, TextureType::Control);
        textures.insert(swatch.normal_detail_map.global_id, TextureType::Normal);
    }
    for swatch in mat_swatches.values() {
        textures.insert(swatch.color_gradient_map.global_id, TextureType::Control);
        textures.insert(swatch.normal_detail_map.global_id, TextureType::Normal);
    }

    for texture in textures.iter() {
        if processed_textures.contains(texture.0) {
            continue;
        }
        let images = process_image(modules, texture)?;
        for (image_data, name) in images {
            save_path.push(name);
            save_path.add_extension("png");
            image_data.save_with_format(&save_path, ImageFormat::Png)?;
            save_path.pop();
        }
        processed_textures.insert(*texture.0);
    }
    Ok(())
}
