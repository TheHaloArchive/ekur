/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::{
    dds::construct_dds_header,
    utils::{decompress_file, extract_bitmaps},
};
use ekur_definitions::bitmap::{Bitmap, BitmapFormat, BitmapType, TextureFlags};
use ekur_materials::TextureType;

use anyhow::Result;
use image_dds::{
    image::{ImageBuffer, Rgba},
    image_from_dds,
};
use infinite_rs::ModuleFile;

pub fn process_image(
    modules: &mut [ModuleFile],
    texture_def: (&i32, &TextureType),
) -> Result<Vec<(ImageBuffer<Rgba<u8>, Vec<u8>>, String)>> {
    let mut texs = Vec::new();
    let modu = modules
        .iter_mut()
        .find(|x| x.files.iter().any(|m| m.tag_id == *texture_def.0));
    let Some(modu) = modu else {
        return Ok(texs);
    };
    let index = modu.files.iter().position(|m| m.tag_id == *texture_def.0);
    let Some(index) = index else {
        return Ok(texs);
    };
    let tag = modu.read_tag(index as u32)?;
    let Some(tag) = tag else {
        return Ok(texs);
    };
    if tag.tag_id == -1 {
        return Ok(texs);
    }
    let mut bitmap = tag.read_metadata::<Bitmap>()?;
    for (bitmidx, bitm) in bitmap.bitmaps.elements.iter_mut().enumerate() {
        let mut name = format!("{}_{bitmidx}", texture_def.0);
        if bitmap
            .flags
            .0
            .contains(TextureFlags::VALIDATE_HAS_CUSTOM_MIPMAPS)
            | (bitm.bitmap_type.0 == BitmapType::CubeMap)
        {
            bitm.mipmap_count.0 = 1;
        }
        let index = extract_bitmaps(modu, index, bitmidx, bitm, bitmap.bitmaps.size)?;
        let Some(index) = index else { continue };
        let data = decompress_file(index, modu)?;
        let dds = construct_dds_header(bitm, &data)?;
        let image = image_from_dds(&dds, 0)?;
        if *texture_def.1 == TextureType::Asg && bitm.format.0 == BitmapFormat::Bc7Unorm {
            name = format!("{name}_t");
        }
        texs.push((image, name));
    }
    return Ok(texs);
}
