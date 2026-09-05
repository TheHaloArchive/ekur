/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use bitflags::bitflags;
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{
        AnyTag, FieldArray, FieldBlock, FieldDwordInteger, FieldReference, FieldStringId,
        FieldWordFlags,
    },
};

bitflags! {
    #[derive(Default, Debug)]
    pub struct StructureBspFlags: u16 {
        const UNUSED = 1 << 0;
        const VISTA_BSP = 1 << 1;
        const ISOLATED_NAV_GENERATION = 1 << 2;
        const CUSTOM_GRAVITY_SCALE = 1 << 3;
        const DISABLE_STREAMING_SUBREGIONS = 1 << 4;
        const AUTOMATICALLY_GENERATED = 1 << 5;
        const HLOD_BSP = 1 << 6;
        const MAY_NOT_CONTAIN_TERRAIN = 1 << 7;
        const EXCLUDE_FROM_FAR_FIELD = 1 << 8;
        const IGNORE_BSP_IN_REGIONS = 1 << 9;
        const ISOLATED_ACOUSTICS_GENERATION = 1 << 10;
        const DISABLE_ACOUSTICS_GENERATION = 1 << 11;
        const FORGEABLE_BSP = 1 << 12;
    }
}

#[derive(Default, Debug, TagStructure)]
#[data(size(220))]
pub struct StructureBspBlock {
    #[data(offset(0x00))]
    pub structure_bsp: FieldReference,
    #[data(offset(0x1C))]
    pub structure_metadata: FieldReference,
    #[data(offset(0x38))]
    pub load_variant_name: FieldStringId,
    #[data(offset(0x40))]
    pub flags: FieldWordFlags<StructureBspFlags>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(4))]
pub struct ZoneFlagWord {
    #[data(offset(0x00))]
    pub flags: FieldDwordInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(1112))]
pub struct ZoneSetBlock {
    #[data(offset(0x000))]
    pub name: FieldStringId,
    #[data(offset(0x120))]
    #[data(count(32))]
    pub bsp_zone_flags: FieldArray<ZoneFlagWord>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(164))]
pub struct TerrainBlock {
    #[data(offset(0x00))]
    pub terrain_system: FieldReference,
    #[data(offset(0x74))]
    pub runtime_terrain: FieldReference,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0xC70))]
pub struct LevelTag {
    #[data(offset(0x000))]
    pub any_tag: AnyTag,
    #[data(offset(0x664))]
    pub terrains: FieldBlock<TerrainBlock>,
    #[data(offset(0x7AC))]
    pub structure_bsps: FieldBlock<StructureBspBlock>,
    #[data(offset(0x82C))]
    pub zone_sets: FieldBlock<ZoneSetBlock>,
}
