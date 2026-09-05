/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use ekur_definitions::bitmap::{Bitmap, BitmapFormat};

use anyhow::Result;
use infinite_rs::ModuleFile;
use std::io::{Read, Seek, SeekFrom};

struct CatalogEntry {
    width: usize,
    height: usize,
    is_height: bool,
}

pub struct TileStore {
    module: usize,
    resource_index: i32,
    resource_count: i32,
    entries: Vec<CatalogEntry>,
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
        let file = &module.files[file_index];
        let (resource_index, resource_count) = (file.resource_index, file.resource_count);
        let Some(tag) = module.read_tag(u32::try_from(file_index)?)? else {
            return Ok(None);
        };
        let bitmap = tag.read_metadata::<Bitmap>()?;
        module.files[file_index].data_stream = None;

        let entries: Vec<CatalogEntry> = bitmap
            .bitmaps
            .elements
            .iter()
            .map(|data| CatalogEntry {
                width: data.width.0.max(0) as usize,
                height: data.height.0.max(0) as usize,
                is_height: data.format.0 == BitmapFormat::R16UnormRrr0L16,
            })
            .collect();
        if entries.len() != usize::try_from(resource_count.max(0))? {
            return Ok(None);
        }
        Ok(Some(Self {
            module: module_index,
            resource_index,
            resource_count,
            entries,
        }))
    }

    pub fn is_height(&self, tile: u32) -> bool {
        usize::try_from(tile)
            .ok()
            .and_then(|tile| self.entries.get(tile))
            .is_some_and(|entry| entry.is_height)
    }

    pub fn height_edge(&self) -> Option<usize> {
        self.entries
            .iter()
            .find(|entry| entry.is_height && entry.width > 1 && entry.width == entry.height)
            .map(|entry| entry.width)
    }

    pub fn height_tile(&self, tile: u32, modules: &mut [ModuleFile]) -> Result<Option<Vec<u16>>> {
        let index = usize::try_from(tile)?;
        let Some(entry) = self.entries.get(index) else {
            return Ok(None);
        };
        if !entry.is_height || i32::try_from(index)? >= self.resource_count {
            return Ok(None);
        }
        let module = &mut modules[self.module];
        let resource = usize::try_from(self.resource_index)? + index;
        let Some(&file_index) = module.resource_indices.get(resource) else {
            return Ok(None);
        };
        let file_index = usize::try_from(file_index)?;
        module.read_tag(u32::try_from(file_index)?)?;

        let file = &mut module.files[file_index];
        let expected = entry.width * entry.height * 2;
        let mut payload = vec![0u8; expected];
        let read = if let Some(reader) = file.data_stream.as_mut() {
            reader.seek(SeekFrom::Start(
                u64::from(file.uncompressed_header_size)
                    + u64::from(file.uncompressed_tag_data_size),
            ))?;
            reader.read_exact(&mut payload).is_ok()
        } else {
            false
        };
        file.data_stream = None;
        if !read {
            return Ok(None);
        }
        Ok(Some(
            payload
                .chunks_exact(2)
                .map(|pair| u16::from_le_bytes([pair[0], pair[1]]))
                .collect(),
        ))
    }
}
