/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use bitflags::bitflags;
use infinite_rs::tag::types::common_types::{
    AnyTag, FieldBlock, FieldByteInteger, FieldCharEnum, FieldLongFlags, FieldShortEnum,
    FieldShortInteger,
};
use infinite_rs::TagStructure;
use num_enum::TryFromPrimitive;

#[derive(Debug, Default, TryFromPrimitive, PartialEq, Eq)]
#[repr(u16)]
pub enum BitmapFormat {
    #[default]
    A8Unorm000A,
    R8UnormRrr1,
    R8UnormRrrr,
    R8g8UnormRrrg,
    Unused1,
    Unused2,
    B5g6r5Unorm,
    Unused3,
    B5g6r5a1Unorm,
    B4g4r4a4Unorm,
    B8g8r8x8Unorm,
    B8g8r8a8Unorm,
    Unused4,
    DeprecatedDxt5BiasAlpha,
    Bc1UnormDxt1,
    Bc2UnormDxt3,
    Bc3UnormDxt5,
    DeprecatedA4r4g4b4Font,
    Unused7,
    Unused8,
    DeprecatedSoftwareRgbfp32,
    Unused9,
    R8g8SnormV8u8,
    DeprecatedG8b8,
    R32g32b32a32FloatAbgrfp32,
    R16g16b16a16FloatAbgrfp16,
    R16FloatRrr1,
    R16FloatR000,
    R8g8b8a8SnormQ8w8v8u8,
    R10g10b10a2UnormA2r10g10b10,
    R16g16b16a16UnormA16b16g16r16,
    R16g16SnormV16u16,
    R16UnormRrr0L16,
    R16g16UnormR16g16,
    R16g16b16a16SnormSignedr16g16b16a16,
    DeprecatedDxt3a,
    Bc4UnormRrrrDxt5a,
    Bc4SnormRrrr,
    DeprecatedDxt3a1111,
    Bc5SnormDxn,
    DeprecatedCtx1,
    DeprecatedDxt3aAlphaOnly,
    DeprecatedDxt3aMonochromeOnly,
    Bc4Unorm000RDxt5aAlpha,
    Bc4UnormRrr1Dxt5aMono,
    Bc5UnormRrrgDxnMonoAlpha,
    Bc5SnormRrrgDxnMonoAlphaSigned,
    Bc6hUf16,
    Bc6hSf16,
    Bc7Unorm,
    D24UnormS8UintDepth24,
    R11g11b10Float,
    R16g16Float,
}

#[derive(Debug, Default, TryFromPrimitive, PartialEq, Eq)]
#[repr(u8)]
pub enum BitmapType {
    #[default]
    Texture2D,
    Texture3D,
    CubeMap,
    Array,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x28))]
pub struct BitmapData {
    #[data(offset(0x00))]
    pub width: FieldShortInteger,
    #[data(offset(0x02))]
    pub height: FieldShortInteger,
    #[data(offset(0x04))]
    pub depth: FieldShortInteger,
    #[data(offset(0x06))]
    pub bitmap_type: FieldCharEnum<BitmapType>,
    #[data(offset(0x08))]
    pub format: FieldShortEnum<BitmapFormat>,
    #[data(offset(0x0C))]
    pub mipmap_count: FieldByteInteger,
}

bitflags! {
    #[derive(Default, Debug)]
    pub struct TextureFlags: u32 {
        const TILED = 1 << 0;
        const USE_LESS_BLURRY_BUMP_MAP = 1 << 1;
        const DITHER_WHEN_COMPRESSION = 1 << 2;
        const GENERATE_RANDOM_SPRITES = 1 << 3;
        const IGNORE_ALPHA_CHANNEL = 1 << 4;
        const ALPHA_CHANNEL_STORES_TRANSPARENCY = 1 << 5;
        const PRESERVE_ALPHA_CHANNEL_IN_MIPMAPS = 1 << 6;
        const ONLY_USE_ON_DEMAND = 1 << 7;
        const APPLY_MAX_RESOLUTION_AFTER_SLICING = 1 << 8;
        const PREFILTER_CUBEMAPS = 1 << 9;
        const HAS_VALID_MIN_AND_MAX_VALUES = 1 << 10;
        const SDF_ONLY_STORE_INSIDE_VALUES = 1 << 11;
        const SDF_STORE_DIRECTION = 1 << 12;
        const SDF_STORE_INITIAL_VALUES_IN_ALPHA_CHANNEL = 1 << 13;
        const HAS_CUSTOM_MIPMAPS = 1 << 14;
        const VALIDATE_HAS_CUSTOM_MIPMAPS = 1 << 15;
        const IS_LIGHT_PROBES = 1 << 16;
    }
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0xE8))]
pub struct Bitmap {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x20))]
    pub flags: FieldLongFlags<TextureFlags>,
    #[data(offset(0xD4))]
    pub bitmaps: FieldBlock<BitmapData>,
}
