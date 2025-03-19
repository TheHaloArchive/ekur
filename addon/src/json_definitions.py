# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from collections import OrderedDict
from typing import Self, TypedDict

__all__ = [
    "StyleInfo",
    "get_intentions",
    "DecalSlot",
    "DiffuseInfo",
    "SelfIllum",
    "CommonMaterial",
    "CommonLayer",
    "CommonRegion",
    "CommonCoating",
    "CoatingGlobalEntry",
    "CoatingGlobalEntries",
    "CommonStyleListEntry",
    "CommonStyleList",
    "CustomizationAttachment",
    "CustomizationPermutation",
    "CustomizationRegion",
    "CustomizationTheme",
    "CustomizationGlobals",
    "CustomizationKit",
    "Instance",
    "Level",
    "ColorDecal",
    "ForgeObjectRepresentation",
    "ForgeObject",
    "ForgeObjectCategory",
    "ForgeObjectDefinition",
    "PermutationName",
    "NameRegion",
    "Armor",
    "CylixVanityResponse",
    "IndexEntry",
    "CylixIndex",
    "Identifier",
    "RegionData",
    "CoreRegion",
    "CylixCore",
    "Asset",
    "Coating",
    "Attachment",
]


class StyleInfo(TypedDict):
    texel_density: tuple[float, float]
    material_offset: tuple[float, float]
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


class DecalSlot(TypedDict):
    top_color: tuple[float, float, float]
    mid_color: tuple[float, float, float]
    bot_color: tuple[float, float, float]
    roughness_white: float
    roughness_black: float
    metallic: float


class DiffuseInfo(TypedDict):
    metallic_white: float
    metallic_black: float
    roughness_white: float
    roughness_black: float
    si_color_tint: tuple[float, float, float]
    si_intensity: float
    si_amount: float
    color_tint: tuple[float, float, float]


class SelfIllum(TypedDict):
    color: tuple[float, float, float]
    intensity: float
    opacity: float


class ColorDecal(TypedDict):
    opacity: float
    metallic: float
    roughness: float


class SkinInfo(TypedDict):
    sss_strength: float
    specular_intensity: float
    specular_white: float
    specular_black: float
    pore_normal_intensity: float
    micro_normal_intensity: float
    micro_normal_scale: tuple[float, float]


class HairInfo(TypedDict):
    tint_color: tuple[float, float, float]
    roughness_white: float
    roughness_black: float
    ior: float


class CommonMaterial(TypedDict):
    textures: dict[str, int]
    shader_type: str
    alpha_blend_mode: str
    style_info: StyleInfo | None
    diffuse_info: DiffuseInfo | None
    illum_info: SelfIllum | None
    decal_slots: DecalSlot | None
    color_decal: ColorDecal | None
    skin: SkinInfo | None
    hair: HairInfo | None


class CommonLayer(TypedDict):
    index: int
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
    reference: str
    name: str


class CommonStyleList(TypedDict):
    default_style: CommonStyleListEntry
    styles: OrderedDict[str, CommonStyleListEntry]


class CustomizationAttachment(TypedDict):
    tag_id: int
    marker_name: int
    model: int


class CustomizationPermutation(TypedDict):
    name: int
    attachment: CustomizationAttachment | None


class CustomizationRegion(TypedDict):
    name: str
    name_int: int
    permutations: list[CustomizationPermutation]
    permutation_regions: list[int]


class CustomizationKit(TypedDict):
    name: int
    regions: list[CustomizationRegion]


class CustomizationTheme(TypedDict):
    name: str
    variant_name: int
    attachments: list[CustomizationAttachment]
    regions: list[CustomizationRegion]
    prosthetics: list[CustomizationRegion]
    body_types: list[CustomizationRegion]
    kits: list[CustomizationKit]


class CustomizationGlobals(TypedDict):
    model: int
    themes: list[CustomizationTheme]


class Instance(TypedDict):
    global_id: int
    position: tuple[float, float, float]
    scale: tuple[float, float, float]
    forward: tuple[float, float, float]
    left: tuple[float, float, float]
    up: tuple[float, float, float]
    material: list[int]
    bounding_box_index: int


class Level(TypedDict):
    instances: list[Instance]


class ForgeObjectRepresentation(TypedDict):
    name: str
    name_int: int
    model: int
    variant: int


class ForgeObject(TypedDict):
    name: str
    id: int
    representations: list[ForgeObjectRepresentation]


class ForgeObjectCategory(TypedDict):
    name: str
    sub_categories: list[Self] | None
    objects: list[ForgeObject] | None


class ForgeObjectDefinition(TypedDict):
    root_categories: list[ForgeObjectCategory]
    objects: dict[str, ForgeObject]


class PermutationName(TypedDict):
    name: str


class NameRegion(TypedDict):
    name: str
    permutations: dict[str, PermutationName]


class Armor(TypedDict):
    core: str
    theme: str
    coating: str
    helmet: str
    helmetAttachment: str
    visor: str
    chestAttachment: str
    leftShoulderPad: str
    rightShoulderPad: str
    gloves: str
    wristAttachment: str
    kneepads: str
    hipAttachment: str


class CylixVanityResponse(TypedDict):
    armor: Armor


class IndexEntry(TypedDict):
    title: str
    res: str
    type: str


class CylixIndex(TypedDict):
    manifest: list[tuple[str, IndexEntry]]


class Identifier(TypedDict):
    m_identifier: int


class RegionData(TypedDict):
    RegionId: Identifier
    PermutationId: Identifier


class ProstheticRegion(TypedDict):
    Full: list[RegionData]
    Half: list[RegionData]
    Extremity: list[RegionData]


class CoreRegion(TypedDict):
    BaseRegionData: list[RegionData]
    BodyTypeSmallOverrides: list[RegionData]
    BodyTypeLargeOverrides: list[RegionData]
    ProstheticLeftArmOverrides: ProstheticRegion
    ProstheticRightArmOverrides: ProstheticRegion
    ProstheticLeftLegOverrides: ProstheticRegion
    ProstheticRightLegOverrides: ProstheticRegion


class CylixCore(TypedDict):
    CoreRegionData: CoreRegion


class Asset(TypedDict):
    RegionData: list[RegionData]


class Coating(TypedDict):
    StyleId: Identifier


class Attachment(TypedDict):
    TagId: int
