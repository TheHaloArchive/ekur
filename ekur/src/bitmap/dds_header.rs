/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::definitions::bitmap::{BitmapData, BitmapFormat, BitmapType};
use anyhow::{Result, bail};
use ddsfile::{AlphaMode, Caps2, D3D10ResourceDimension, Dds, DxgiFormat, NewDxgiParams};

fn dxgi_from_bitmap_format(form: &BitmapFormat) -> Result<DxgiFormat> {
    Ok(match form {
        BitmapFormat::Bc1UnormDxt1 => DxgiFormat::BC1_UNorm,
        BitmapFormat::Bc5SnormDxn | BitmapFormat::Bc5SnormRrrgDxnMonoAlphaSigned => {
            DxgiFormat::BC5_SNorm
        }
        BitmapFormat::Bc7Unorm => DxgiFormat::BC7_UNorm,
        BitmapFormat::Bc3UnormDxt5 => DxgiFormat::BC3_UNorm,
        BitmapFormat::B8g8r8a8Unorm => DxgiFormat::B8G8R8A8_UNorm,
        BitmapFormat::Bc4Unorm000RDxt5aAlpha
        | BitmapFormat::Bc4UnormRrr1Dxt5aMono
        | BitmapFormat::Bc4UnormRrrrDxt5a => DxgiFormat::BC4_UNorm,
        BitmapFormat::R16g16b16a16FloatAbgrfp16 => DxgiFormat::R16G16B16A16_Float,
        BitmapFormat::R16g16b16a16SnormSignedr16g16b16a16 => DxgiFormat::R16G16B16A16_SNorm,
        BitmapFormat::R8UnormRrrr | BitmapFormat::R8UnormRrr1 | BitmapFormat::A8Unorm000A => {
            DxgiFormat::R8_UNorm
        }
        BitmapFormat::R32g32b32a32FloatAbgrfp32 => DxgiFormat::R32G32B32A32_Float,
        BitmapFormat::R8g8b8a8SnormQ8w8v8u8 => DxgiFormat::R8G8B8A8_SNorm,
        BitmapFormat::R16UnormRrr0L16 => DxgiFormat::R16_UNorm,
        BitmapFormat::R10g10b10a2UnormA2r10g10b10 => DxgiFormat::R10G10B10A2_UNorm,
        BitmapFormat::Bc6hUf16 => DxgiFormat::BC6H_UF16,
        BitmapFormat::R8g8UnormRrrg => DxgiFormat::R8G8_UNorm,
        BitmapFormat::R16g16b16a16UnormA16b16g16r16 => DxgiFormat::R16G16B16A16_UNorm,
        BitmapFormat::Bc5UnormRrrgDxnMonoAlpha => DxgiFormat::BC5_UNorm,
        BitmapFormat::R8g8SnormV8u8 => DxgiFormat::R8G8_SNorm,
        BitmapFormat::R16g16Float => DxgiFormat::R16G16_Float,
        BitmapFormat::R11g11b10Float => DxgiFormat::R11G11B10_Float,
        BitmapFormat::R16FloatR000 | BitmapFormat::R16FloatRrr1 => DxgiFormat::R16_Float,
        BitmapFormat::R16g16UnormR16g16 => DxgiFormat::R16G16_UNorm,
        BitmapFormat::B5g6r5Unorm | BitmapFormat::B5g6r5a1Unorm => DxgiFormat::B5G6R5_UNorm,
        BitmapFormat::B4g4r4a4Unorm => DxgiFormat::B4G4R4A4_UNorm,
        BitmapFormat::B8g8r8x8Unorm => DxgiFormat::B8G8R8X8_UNorm,
        BitmapFormat::Bc2UnormDxt3 => DxgiFormat::BC2_UNorm,
        BitmapFormat::R16g16SnormV16u16 => DxgiFormat::R16G16_SNorm,
        BitmapFormat::Bc4SnormRrrr => DxgiFormat::BC4_SNorm,
        BitmapFormat::Bc6hSf16 => DxgiFormat::BC6H_SF16,
        BitmapFormat::D24UnormS8UintDepth24 => DxgiFormat::D24_UNorm_S8_UInt,
        _ => {
            bail!("Unsupported format: {:?}", form);
        }
    })
}

pub(super) fn construct_dds_header(bitmap: &BitmapData, data: &[u8]) -> Result<Dds> {
    let format = dxgi_from_bitmap_format(&bitmap.format.0)?;
    let caps = if bitmap.bitmap_type.0 == BitmapType::CubeMap {
        Some(Caps2::CUBEMAP)
    } else {
        None
    };
    let resource_dimension = match bitmap.bitmap_type.0 {
        BitmapType::Texture2D | BitmapType::CubeMap | BitmapType::Array => {
            D3D10ResourceDimension::Texture2D
        }
        BitmapType::Texture3D => D3D10ResourceDimension::Texture3D,
    };
    let new_dxgi = NewDxgiParams {
        height: u32::try_from(bitmap.height.0)?,
        width: u32::try_from(bitmap.width.0)?,
        depth: Some(u32::try_from(bitmap.depth.0)?),
        format,
        mipmap_levels: Some(u32::from(bitmap.mipmap_count.0)),
        array_layers: Some(u32::try_from(bitmap.depth.0)?),
        alpha_mode: AlphaMode::Straight,
        caps2: caps,
        is_cubemap: bitmap.bitmap_type.0 == BitmapType::CubeMap,
        resource_dimension,
    };
    let mut dds = Dds::new_dxgi(new_dxgi)?;
    dds.data = data.to_vec();
    Ok(dds)
}
