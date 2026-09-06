/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use ekur_definitions::bitmap::{Bitmap, BitmapFormat};
use ekur_texture::{decompress_file, extract_bitmaps, process::decode_bitmap_data};

use anyhow::Result;
use infinite_rs::ModuleFile;

pub type SurfaceTile = (Vec<u8>, u32, u32, String);

pub struct TileStore {
    module: usize,
    file_index: usize,
    bitmap: Bitmap,
}

impl TileStore {
    pub fn open(bitmap_id: i32, modules: &mut [ModuleFile]) -> Result<Option<Self>> {
        if bitmap_id == -1 {
            return Ok(None);
        }
        let found = modules
            .iter()
            .enumerate()
            .find_map(|(module_index, module)| {
                module
                    .files
                    .iter()
                    .position(|file| file.tag_id == bitmap_id && file.tag_group == "bitm")
                    .map(|file_index| (module_index, file_index))
            });
        let Some((module_index, file_index)) = found else {
            return Ok(None);
        };

        let module = &mut modules[module_index];
        let resource_count = module.files[file_index].resource_count;
        let Some(tag) = module.read_tag(u32::try_from(file_index)?)? else {
            return Ok(None);
        };
        let bitmap = tag.read_metadata::<Bitmap>()?;
        module.files[file_index].data_stream = None;

        if bitmap.bitmaps.elements.len() != usize::try_from(resource_count.max(0))? {
            return Ok(None);
        }

        Ok(Some(Self {
            module: module_index,
            file_index,
            bitmap,
        }))
    }

    pub fn is_height(&self, tile: u32) -> bool {
        usize::try_from(tile)
            .ok()
            .and_then(|tile| self.bitmap.bitmaps.elements.get(tile))
            .is_some_and(|entry| entry.format.0 == BitmapFormat::R16UnormRrr0L16)
    }

    pub fn height_edge(&self) -> Option<usize> {
        self.bitmap
            .bitmaps
            .elements
            .iter()
            .find(|entry| {
                entry.format.0 == BitmapFormat::R16UnormRrr0L16
                    && entry.width.0 > 1
                    && entry.width.0 == entry.height.0
            })
            .map(|entry| entry.width.0.max(0) as usize)
    }

    pub fn height_tile(
        &mut self,
        tile: u32,
        modules: &mut [ModuleFile],
    ) -> Result<Option<Vec<u16>>> {
        let index = usize::try_from(tile)?;
        let bitmap_count = self.bitmap.bitmaps.size;
        let Some(entry) = self.bitmap.bitmaps.elements.get_mut(index) else {
            return Ok(None);
        };
        if entry.format.0 != BitmapFormat::R16UnormRrr0L16 {
            return Ok(None);
        }

        let module = &mut modules[self.module];
        let Some(file_index) =
            extract_bitmaps(module, self.file_index, index, entry, bitmap_count)?
        else {
            return Ok(None);
        };
        let expected = entry.width.0.max(0) as usize * entry.height.0.max(0) as usize * 2;
        let payload = decompress_file(file_index, module)?;
        if payload.len() < expected {
            return Ok(None);
        }

        Ok(Some(
            payload[..expected]
                .chunks_exact(2)
                .map(|pair| u16::from_le_bytes([pair[0], pair[1]]))
                .collect(),
        ))
    }

    pub fn surface_tile(
        &mut self,
        tile: u32,
        modules: &mut [ModuleFile],
    ) -> Result<Option<SurfaceTile>> {
        let index = usize::try_from(tile)?;
        let bitmap_count = self.bitmap.bitmaps.size;
        let Some(entry) = self.bitmap.bitmaps.elements.get_mut(index) else {
            return Ok(None);
        };
        if entry.format.0 == BitmapFormat::R16UnormRrr0L16 {
            return Ok(None);
        }
        let slug = format!("{:?}", entry.format.0).to_lowercase();

        let module = &mut modules[self.module];
        let Some(file_index) =
            extract_bitmaps(module, self.file_index, index, entry, bitmap_count)?
        else {
            return Ok(None);
        };
        let payload = decompress_file(file_index, module)?;
        let image = decode_bitmap_data(entry, &payload)?;
        let (width, height) = image.dimensions();
        Ok(Some((image.into_raw(), width, height, slug)))
    }
}
