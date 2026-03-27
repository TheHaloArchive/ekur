/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use ekur_definitions::bitmap::{BitmapData, BitmapFormat as BF, BitmapType};

use anyhow::Result;
use ddsfile::{AlphaMode, Caps2, D3D10ResourceDimension, Dds, DxgiFormat, NewDxgiParams};

fn dxgi_from_bitmap_format(form: &BF) -> DxgiFormat {
    match form {
        BF::Bc1UnormDxt1 => DxgiFormat::BC1_UNorm,
        BF::Bc5SnormDxn | BF::Bc5SnormRrrgDxnMonoAlphaSigned => DxgiFormat::BC5_SNorm,
        BF::Bc7Unorm => DxgiFormat::BC7_UNorm,
        BF::Bc3UnormDxt5 => DxgiFormat::BC3_UNorm,
        BF::B8g8r8a8Unorm => DxgiFormat::B8G8R8A8_UNorm,
        BF::Bc4Unorm000R | BF::Bc4UnormRrr1D | BF::Bc4UnormRrrrDxt5a => DxgiFormat::BC4_UNorm,
        BF::R16g16b16a16FloatAbgrfp16 => DxgiFormat::R16G16B16A16_Float,
        BF::R16g16b16a16SnormSignedr16g16b16a16 => DxgiFormat::R16G16B16A16_SNorm,
        BF::R8UnormRrrr | BF::R8UnormRrr1 | BF::A8Unorm000A => DxgiFormat::R8_UNorm,
        BF::R32g32b32a32FloatAbgrfp32 => DxgiFormat::R32G32B32A32_Float,
        BF::R8g8b8a8SnormQ8w8v8u8 => DxgiFormat::R8G8B8A8_SNorm,
        BF::R16UnormRrr0L16 => DxgiFormat::R16_UNorm,
        BF::R10g10b10a2UnormA2r10g10b10 => DxgiFormat::R10G10B10A2_UNorm,
        BF::Bc6hUf16 => DxgiFormat::BC6H_UF16,
        BF::R8g8UnormRrrg => DxgiFormat::R8G8_UNorm,
        BF::R16g16b16a16UnormA16b16g16r16 => DxgiFormat::R16G16B16A16_UNorm,
        BF::Bc5UnormRrrgDxnMonoAlpha => DxgiFormat::BC5_UNorm,
        BF::R8g8SnormV8u8 => DxgiFormat::R8G8_SNorm,
        BF::R16g16Float => DxgiFormat::R16G16_Float,
        BF::R11g11b10Float => DxgiFormat::R11G11B10_Float,
        BF::R16FloatR000 | BF::R16FloatRrr1 => DxgiFormat::R16_Float,
        BF::R16g16UnormR16g16 => DxgiFormat::R16G16_UNorm,
        BF::B5g6r5Unorm | BF::B5g6r5a1Unorm => DxgiFormat::B5G6R5_UNorm,
        BF::B4g4r4a4Unorm => DxgiFormat::B4G4R4A4_UNorm,
        BF::B8g8r8x8Unorm => DxgiFormat::B8G8R8X8_UNorm,
        BF::Bc2UnormDxt3 => DxgiFormat::BC2_UNorm,
        BF::R16g16SnormV16u16 => DxgiFormat::R16G16_SNorm,
        BF::Bc4SnormRrrr => DxgiFormat::BC4_SNorm,
        BF::Bc6hSf16 => DxgiFormat::BC6H_SF16,
        BF::D24UnormS8UintDepth24 => DxgiFormat::D24_UNorm_S8_UInt,
        _ => DxgiFormat::Unknown,
    }
}

pub fn construct_dds_header(bitmap: &BitmapData, data: &[u8]) -> Result<Dds> {
    let format = dxgi_from_bitmap_format(&bitmap.format.0);

    let resource_dimension = if bitmap.bitmap_type.0 == BitmapType::Texture3D {
        D3D10ResourceDimension::Texture3D
    } else {
        D3D10ResourceDimension::Texture2D
    };

    let new_dxgi = NewDxgiParams {
        height: u32::try_from(bitmap.height.0)?,
        width: u32::try_from(bitmap.width.0)?,
        depth: Some(u32::try_from(bitmap.depth.0)?),
        format,
        mipmap_levels: Some(u32::from(bitmap.mipmap_count.0)),
        array_layers: Some(u32::try_from(bitmap.depth.0)?),
        alpha_mode: AlphaMode::Straight,
        caps2: (bitmap.bitmap_type.0 == BitmapType::CubeMap).then(|| Caps2::CUBEMAP),
        is_cubemap: bitmap.bitmap_type.0 == BitmapType::CubeMap,
        resource_dimension,
    };
    let mut dds = Dds::new_dxgi(new_dxgi)?;
    dds.data = data.to_vec();
    Ok(dds)
}
