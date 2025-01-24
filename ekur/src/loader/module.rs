use crate::definitions::bitmap::BitmapData;
use std::{collections::HashMap, path::Path};

use anyhow::Result;
use infinite_rs::{
    module::file::{DataOffsetType, TagStructure},
    ModuleFile,
};
use std::io::SeekFrom;
use std::io::{Read, Seek};

pub fn load_modules<P: AsRef<Path>>(deploy_path: P) -> infinite_rs::Result<Vec<ModuleFile>> {
    let mut modules = Vec::new();
    for entry in walkdir::WalkDir::new(deploy_path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        if entry.file_type().is_file() {
            let file_path = entry.path().to_str().unwrap();
            if file_path.ends_with(".module") && !file_path.contains("ds") {
                let module = ModuleFile::from_path(file_path);
                match module {
                    Ok(_) => {
                        modules.push(module?);
                        println!("Read module: {}", file_path);
                    }
                    Err(err) => {
                        println!("Failed on file: {}", file_path);
                        return Err(err);
                    }
                };
            }
        }
    }
    Ok(modules)
}

pub fn get_tags<T: TagStructure + Default>(
    tag_group: &str,
    module: &mut ModuleFile,
) -> Result<HashMap<i32, T>> {
    let mut tags = HashMap::new();
    for idx in 0..module.files.len() {
        if module.files[idx].tag_group == tag_group {
            let tag = module.read_tag(idx as u32)?.unwrap();
            let mut mat = T::default();
            tag.read_metadata(&mut mat)?;
            tags.insert(tag.tag_id, mat);
        }
    }
    Ok(tags)
}

pub fn decompress_file(index: i32, module: &mut ModuleFile) -> Result<Vec<u8>> {
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
    Ok(buffer)
}

pub fn extract_bitmaps(
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
