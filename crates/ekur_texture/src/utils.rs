/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use ekur_definitions::bitmap::BitmapData;

use anyhow::Result;
use infinite_rs::{ModuleFile, module::file::DataOffsetType};
use std::io::{Read, Seek, SeekFrom};

pub(crate) fn decompress_file(index: i32, module: &mut ModuleFile) -> Result<Vec<u8>> {
    let file = &mut module.files[usize::try_from(index)?];
    let capacity = if file.uncompressed_actual_resource_size != 0 {
        u64::from(file.uncompressed_actual_resource_size)
    } else {
        u64::from(file.total_uncompressed_size)
    };
    let mut buffer = Vec::with_capacity(usize::try_from(capacity)?);
    if let Some(reader) = file.data_stream.as_mut() {
        reader.seek(SeekFrom::Start(
            u64::from(file.uncompressed_header_size) + u64::from(file.uncompressed_tag_data_size),
        ))?;
        reader.read_to_end(&mut buffer)?;
    }
    file.data_stream = None;
    Ok(buffer)
}

pub(crate) fn extract_bitmaps(
    module: &mut ModuleFile,
    index: usize,
    bitm_index: usize,
    bitmap: &mut BitmapData,
    bitmap_count: u32,
) -> Result<Option<i32>> {
    let mut file_index = index;
    let mut non_hd1_index;

    // Initial file check
    {
        let file = &module.files[file_index];
        non_hd1_index = file.resource_index + file.resource_count - 1;

        if bitmap_count == 1 && file.uncompressed_actual_resource_size == 0 {
            file_index =
                module.resource_indices[usize::try_from(non_hd1_index)?] as usize - bitm_index;
        } else if file.uncompressed_actual_resource_size != 0 {
            file_index = index;
        } else {
            file_index = module.resource_indices[usize::try_from(file.resource_index)?] as usize
                + bitm_index;
        }
    }
    module.read_tag(u32::try_from(file_index)?)?;

    // HD1 check
    {
        let file = &module.files[file_index];
        if file.data_offset_flags.contains(DataOffsetType::USE_HD1) && !module.use_hd1 {
            non_hd1_index -= 1;
            file_index =
                module.resource_indices[usize::try_from(non_hd1_index)?] as usize - bitm_index;
            module.read_tag(u32::try_from(file_index)?)?;
            bitmap.width.0 /= 2;
            bitmap.height.0 /= 2;
        }
    }

    // Resource data check
    {
        let file = &module.files[file_index];

        if file.resource_count > 0 {
            let new_resource_index = file.resource_index + file.resource_count - 1;
            file_index = module.resource_indices[usize::try_from(new_resource_index)?] as usize;

            let new_resource = &module.files[file_index];
            if new_resource
                .data_offset_flags
                .contains(DataOffsetType::USE_HD1)
                && !module.use_hd1
            {
                file_index = module.resource_indices
                    [usize::try_from(file.resource_index + file.resource_count - 2)?]
                    as usize;
                bitmap.width.0 /= 2;
                bitmap.height.0 /= 2;
            }
            module.read_tag(u32::try_from(file_index)?)?;
        }
    }

    Ok(Some(i32::try_from(file_index)?))
}
