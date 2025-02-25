/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::collections::{HashMap, HashSet};

use crate::definitions::coating_swatch::CoatingSwatchPODTag;
use crate::definitions::material_swatch::MaterialSwatchTag;
use crate::loader::module::{decompress_file, extract_bitmaps};
use crate::materials::serde_definitions::TextureType;

use super::dds_header::construct_dds_header;
use crate::definitions::bitmap::{Bitmap, BitmapData, BitmapFormat, BitmapType, TextureFlags};
use anyhow::Result;
use image_dds::{
    error::{CreateImageError, SurfaceError},
    image_from_dds,
};
use infinite_rs::ModuleFile;

fn save_bitmap(data: &[u8], name: &str, bitmap: &BitmapData, save_path: &str) -> Result<()> {
    let dds = construct_dds_header(bitmap, data)?;
    let image = image_from_dds(&dds, 0);
    match image {
        Ok(image) => image.save_with_format(
            format!("{save_path}/bitmaps/{name}.png"),
            image::ImageFormat::Png,
        )?,
        Err(CreateImageError::DecompressSurface(SurfaceError::UnsupportedDdsFormat(format))) => {
            println!("[UnsupportedFormat]: {:#?}", format.dxgi.unwrap());
        }
        Err(CreateImageError::DecompressSurface(SurfaceError::MipmapDataOutOfBounds {
            layer: l,
            mipmap: m,
        })) => {
            println!("[MipMapError]: {name}: layer: {l}, mipmap: {m}");
        }
        Err(a) => println!("{a:#?}"),
    }
    Ok(())
}

fn collect_bitmaps(
    textures: Vec<(TextureType, i32)>,
    coating_swatches: &HashMap<i32, CoatingSwatchPODTag>,
    material_swatches: &HashMap<i32, MaterialSwatchTag>,
) -> HashSet<(TextureType, i32)> {
    let mut bitmaps = HashSet::new();
    bitmaps.extend(textures);
    for cmsw in coating_swatches {
        let gradient = cmsw.1.color_gradient_map.global_id;
        let normal = cmsw.1.normal_detail_map.global_id;
        bitmaps.insert((TextureType::Control, gradient));
        bitmaps.insert((TextureType::Normal, normal));
    }
    for mat in material_swatches {
        bitmaps.insert((TextureType::Control, mat.1.color_gradient_map.global_id));
        bitmaps.insert((TextureType::Normal, mat.1.normal_detail_map.global_id));
    }
    bitmaps
}

pub fn extract_all_bitmaps(
    modules: &mut [ModuleFile],
    textures: Vec<(TextureType, i32)>,
    coating_swatches: &HashMap<i32, CoatingSwatchPODTag>,
    material_swatches: &HashMap<i32, MaterialSwatchTag>,
    save_path: &str,
) -> Result<()> {
    let bitmaps = collect_bitmaps(textures, coating_swatches, material_swatches);
    std::fs::create_dir_all(format!("{}/bitmaps/", save_path))?;
    let mut processed_bitmaps = HashSet::new();
    for (tex_type, idx) in bitmaps {
        if idx == -1 {
            continue;
        }
        if processed_bitmaps.contains(&idx) {
            continue;
        } else {
            processed_bitmaps.insert(idx);
        }

        let module = modules
            .iter_mut()
            .find(|x| x.files.iter().any(|m| m.tag_id == idx));
        let Some(module) = module else {
            continue;
        };

        let index = module.files.iter().position(|m| m.tag_id == idx).unwrap();
        let tag = module.read_tag(index as u32)?;
        let Some(tag) = tag else {
            continue;
        };
        let mut bitmap = Bitmap::default();
        tag.read_metadata(&mut bitmap)?;
        for (bitmidx, bitm) in bitmap.bitmaps.elements.iter_mut().enumerate() {
            if bitmap
                .flags
                .0
                .contains(TextureFlags::VALIDATE_HAS_CUSTOM_MIPMAPS)
                | (bitm.bitmap_type.0 == BitmapType::CubeMap)
            {
                bitm.mipmap_count.0 = 1;
            }
            let index = extract_bitmaps(module, index, bitmidx, bitm, bitmap.bitmaps.size)?;
            let Some(index) = index else {
                continue;
            };
            let data = decompress_file(index, module)?;
            let mut name = format! {"{}_{}", bitmap.any_tag.internal_struct.tag_id, bitmidx};
            if tex_type == TextureType::Asg && bitm.format.0 == BitmapFormat::Bc7Unorm {
                name = format! {"{}_t", name};
            }
            save_bitmap(&data, &name, bitm, save_path)?;
        }
    }
    Ok(())
}
