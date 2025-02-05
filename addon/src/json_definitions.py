# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from collections import OrderedDict
from typing import TypedDict


class StyleInfo(TypedDict):
    stylelist: int
    region_name: int
    base_intention: int
    mask0_red_intention: int
    mask0_green_intention: int
    mask0_blue_intention: int
    mask1_red_intention: int
    mask1_green_intention: int
    mask1_blue_intention: int
    supported_layers: int
    enable_damage: bool


def get_intentions(style_info: StyleInfo) -> list[int]:
    return [
        style_info["base_intention"],
        style_info["mask0_red_intention"],
        style_info["mask0_green_intention"],
        style_info["mask0_blue_intention"],
        style_info["mask1_red_intention"],
        style_info["mask1_green_intention"],
        style_info["mask1_blue_intention"],
    ]


class CommonMaterial(TypedDict):
    textures: dict[str, int]
    texel_density: tuple[float, float]
    material_offset: tuple[float, float]
    style_info: StyleInfo
    material_constants: str


class CommonLayer(TypedDict):
    disabled: bool
    gradient_transform: tuple[float, float]
    normal_transform: tuple[float, float]
    gradient_bitmap: int
    normal_bitmap: int
    roughness: float
    roughness_white: float
    roughness_black: float
    metallic: float
    emissive_amount: float
    top_color: tuple[float, float, float]
    mid_color: tuple[float, float, float]
    bot_color: tuple[float, float, float]
    scratch_roughness: float
    scratch_metallic: float
    scratch_color: tuple[float, float, float]


class CommonRegion(TypedDict):
    layers: dict[str, CommonLayer]


class CommonCoating(TypedDict):
    grime_amount: float
    scratch_amount: float
    grime_swatch: CommonLayer
    regions: dict[str, CommonRegion]


class CoatingGlobalEntry(TypedDict):
    fallback: int
    layer: CommonLayer


class CoatingGlobalEntries(TypedDict):
    entries: dict[str, CoatingGlobalEntry]


class CommonStyleListEntry(TypedDict):
    reference: int
    name: str


class CommonStyleList(TypedDict):
    default_style: CommonStyleListEntry
    styles: OrderedDict[str, CommonStyleListEntry]
