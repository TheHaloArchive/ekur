/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::collections::{HashMap, HashSet};

use crate::definitions::coating_swatch::CoatingSwatchPODTag;
use crate::definitions::material_swatch::MaterialSwatchTag;
use crate::loader::module::{decompress_file, extract_bitmaps};

use super::dds_header::construct_dds_header;
use crate::definitions::bitmap::{Bitmap, BitmapData, BitmapType, TextureFlags};
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
    textures: Vec<i32>,
    coating_swatches: &HashMap<i32, CoatingSwatchPODTag>,
    material_swatches: &HashMap<i32, MaterialSwatchTag>,
) -> HashSet<i32> {
    let mut bitmaps = HashSet::new();
    bitmaps.extend(textures);
    for cmsw in coating_swatches {
        let gradient = cmsw.1.color_gradient_map.global_id;
        let normal = cmsw.1.normal_detail_map.global_id;
        bitmaps.insert(gradient);
        bitmaps.insert(normal);
    }
    for mat in material_swatches {
        bitmaps.insert(mat.1.color_gradient_map.global_id);
        bitmaps.insert(mat.1.normal_detail_map.global_id);
    }
    bitmaps
}

pub fn extract_all_bitmaps(
    modules: &mut [ModuleFile],
    textures: Vec<i32>,
    coating_swatches: &HashMap<i32, CoatingSwatchPODTag>,
    material_swatches: &HashMap<i32, MaterialSwatchTag>,
    save_path: &str,
) -> Result<()> {
    let bitmaps = collect_bitmaps(textures, coating_swatches, material_swatches);
    for idx in bitmaps {
        if idx == -1 {
            continue;
        }
        let module = modules
            .iter_mut()
            .find(|x| x.files.iter().any(|m| m.tag_id == idx));
        if let Some(module) = module {
            let index = module.files.iter().position(|m| m.tag_id == idx).unwrap();
            let tag = module.read_tag(index as u32)?;
            let mut m = Bitmap::default();
            tag.unwrap().read_metadata(&mut m)?;
            for (bitmidx, bitmap) in m.bitmaps.elements.iter_mut().enumerate() {
                if m.flags
                    .0
                    .contains(TextureFlags::VALIDATE_HAS_CUSTOM_MIPMAPS)
                    | (bitmap.bitmap_type.0 == BitmapType::CubeMap)
                {
                    bitmap.mipmap_count.0 = 1;
                }
                let index = extract_bitmaps(module, index, bitmidx, bitmap, m.bitmaps.size)?;
                if let Some(index) = index {
                    let data = decompress_file(index, module)?;
                    save_bitmap(
                        &data,
                        &format!("{}_{}", m.any_tag.internal_struct.tag_id, bitmidx),
                        bitmap,
                        save_path,
                    )?;
                }
            }
        } else {
            continue;
        }
    }
    Ok(())
}
