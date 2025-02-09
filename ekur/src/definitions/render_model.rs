/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use bitflags::bitflags;
use infinite_rs::tag::types::common_types::{
    AnyTag, FieldBlock, FieldByteInteger, FieldCharEnum, FieldCharInteger, FieldLongEnum,
    FieldLongInteger, FieldReal, FieldRealBounds, FieldRealPoint3D, FieldRealQuaternion,
    FieldRealVector3D, FieldReference, FieldShortBlockIndex, FieldShortInteger, FieldStringId,
    FieldTagResource, FieldWordFlags, FieldWordInteger,
};
use infinite_rs::TagStructure;
use num_enum::TryFromPrimitive;

#[derive(Default, Debug, TryFromPrimitive)]
#[repr(u32)]
pub enum ResourcePackingPolicy {
    #[default]
    SingleResource,
    ResourcePerMeshPermutation,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0xC))]
pub struct PermutationBlock {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub section_index: FieldShortInteger,
    #[data(offset(0x06))]
    pub section_count: FieldWordInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(124))]
pub struct NodeBlock {
    #[data(offset(0))]
    pub name: FieldStringId,
    #[data(offset(4))]
    pub parent_index: FieldShortBlockIndex,
    #[data(offset(6))]
    pub first_child_index: FieldShortBlockIndex,
    #[data(offset(8))]
    pub next_sibling_index: FieldShortBlockIndex,
    #[data(offset(12))]
    pub position: FieldRealPoint3D,
    #[data(offset(24))]
    pub rotation: FieldRealQuaternion,
    #[data(offset(0x28))]
    pub inverse_forward: FieldRealVector3D,
    #[data(offset(0x34))]
    pub inverse_left: FieldRealVector3D,
    #[data(offset(0x40))]
    pub inverse_up: FieldRealVector3D,
    #[data(offset(0x4C))]
    pub inverse_position: FieldRealPoint3D,
    #[data(offset(0x58))]
    pub inverse_scale: FieldReal,
    #[data(offset(0x5c))]
    pub distance_from_parent: FieldReal,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x18))]
pub struct RegionBlock {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub permutations: FieldBlock<PermutationBlock>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x38))]
pub struct MarkerBlock {
    #[data(offset(0x00))]
    pub region_index: FieldCharInteger,
    #[data(offset(0x04))]
    pub permutation_index: FieldLongInteger,
    #[data(offset(0x08))]
    pub node_index: FieldCharInteger,
    #[data(offset(0x0C))]
    pub translation: FieldRealPoint3D,
    #[data(offset(0x18))]
    pub rotation: FieldRealQuaternion,
    #[data(offset(0x28))]
    pub scale: FieldReal,
    #[data(offset(0x2C))]
    pub direction: FieldRealVector3D,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x18))]
pub struct MarkerGroupBlock {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub markers: FieldBlock<MarkerBlock>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x1C))]
pub struct MaterialBlock {
    #[data(offset(0x00))]
    pub material: FieldReference,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x18))]
pub struct SubmeshBlock {
    #[data(offset(0x00))]
    pub shader_index: FieldShortBlockIndex,
    #[data(offset(0x04))]
    pub index_start: FieldLongInteger,
    #[data(offset(0x08))]
    pub index_count: FieldLongInteger,
    #[data(offset(12))]
    pub subset_index: FieldShortBlockIndex,
    #[data(offset(14))]
    pub subset_count: FieldWordInteger,
    #[data(offset(20))]
    pub vertex_count: FieldWordInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(12))]
pub struct SubsetBlock {
    #[data(offset(0))]
    pub index_start: FieldLongInteger,
    #[data(offset(4))]
    pub index_count: FieldLongInteger,
    #[data(offset(8))]
    pub submesh_index: FieldWordInteger,
    #[data(offset(10))]
    pub vertex_count: FieldWordInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(38))]
pub struct VertexBufferIndexArray {
    #[data(offset(0))]
    pub vertex_buffer_index: FieldShortInteger,
    #[data(offset(2))]
    pub vertex_buffer_index2: FieldShortInteger,
    #[data(offset(4))]
    pub vertex_buffer_index3: FieldShortInteger,
    #[data(offset(6))]
    pub vertex_buffer_index4: FieldShortInteger,
    #[data(offset(8))]
    pub vertex_buffer_index5: FieldShortInteger,
    #[data(offset(10))]
    pub vertex_buffer_index6: FieldShortInteger,
    #[data(offset(12))]
    pub vertex_buffer_index7: FieldShortInteger,
    #[data(offset(14))]
    pub vertex_buffer_index8: FieldShortInteger,
    #[data(offset(16))]
    pub vertex_buffer_index9: FieldShortInteger,
    #[data(offset(18))]
    pub vertex_buffer_index10: FieldShortInteger,
    #[data(offset(20))]
    pub vertex_buffer_index11: FieldShortInteger,
    #[data(offset(22))]
    pub vertex_buffer_index12: FieldShortInteger,
    #[data(offset(24))]
    pub vertex_buffer_index13: FieldShortInteger,
    #[data(offset(26))]
    pub vertex_buffer_index14: FieldShortInteger,
    #[data(offset(28))]
    pub vertex_buffer_index15: FieldShortInteger,
    #[data(offset(30))]
    pub vertex_buffer_index16: FieldShortInteger,
    #[data(offset(32))]
    pub vertex_buffer_index17: FieldShortInteger,
    #[data(offset(34))]
    pub vertex_buffer_index18: FieldShortInteger,
    #[data(offset(36))]
    pub vertex_buffer_index19: FieldShortInteger,
}

bitflags! {
    #[derive(Default, Debug)]
    pub struct LodFlags : u16 {
        const LOD0 = 1 << 0;
        const LOD1 = 1 << 1;
        const LOD2 = 1 << 2;
        const LOD3 = 1 << 3;
        const LOD4 = 1 << 4;
        const LOD5 = 1 << 5;
        const LOD6 = 1 << 6;
        const LOD7 = 1 << 7;
        const LOD8 = 1 << 8;
        const LOD9 = 1 << 9;
        const LOD10 = 1 << 10;
        const LOD11 = 1 << 11;
        const LOD12 = 1 << 12;
        const LOD13 = 1 << 13;
        const LOD14 = 1 << 14;
        const LOD15 = 1 << 15;
    }
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x94))]
pub struct SectionLods {
    #[data(offset(40))]
    pub submeshes: FieldBlock<SubmeshBlock>,
    #[data(offset(60))]
    pub subsections: FieldBlock<SubsetBlock>,
    #[data(offset(100))]
    pub vertex_buffer_indices: VertexBufferIndexArray,
    #[data(offset(138))]
    pub index_buffer_index: FieldShortInteger,
    #[data(offset(140))]
    pub lod_flags: FieldWordFlags<LodFlags>,
    #[data(offset(142))]
    pub lod_has_shadow_proxies: FieldWordInteger,
}

bitflags! {
    #[derive(Default, Debug)]
    pub struct MeshFlags : u16 {
        const USES_VERTEX_COLOR = 1 << 0;
        const USE_REGION_INDEX_FOR_SORTING = 1 << 1;
        const CAN_BE_RENDERED_IN_DRAW_BUNDLES = 1 << 2;
        const MESH_IS_CUSTOM_SHADOW_CASTER = 1 << 3;
        const MESH_IS_UNINDEXED = 1 << 4;
        const MESH_SHOULD_RENDER_IN_PREPASS = 1 << 5;
        const USE_UNCOMPRESSED_VERTEX_FORMAT = 1 << 6;
        const MESH_IS_PCA = 1 << 7;
        const MESH_HAS_UV2 = 1 << 8;
        const MESH_HAS_UV3 = 1 << 9;
        const USE_UV3_TANGENT_ROTATION = 1 << 10;
    }
}

#[derive(Default, Debug, TryFromPrimitive)]
#[repr(u8)]
pub enum VertexType {
    #[default]
    World,
    Rigid,
    Skinned,
    ParticleModel,
    Screen,
    Debug,
    Transparent,
    Particle,
    Removed08,
    Removed09,
    ChudSimple,
    Decorator,
    PositionOnly,
    Removed13,
    Ripple,
    Removed15,
    TessellatedTerrain,
    Empty,
    Decal,
    Removed19,
    Removed20,
    PositionOnly2,
    Tracer,
    RigidBoned,
    Removed24,
    CheapParticle,
    DqSkinned,
    Skinned8Weights,
    TessellatedVector,
    Interaction,
    NumberOfStandardVertexTypes,
}

#[derive(Default, Debug, TryFromPrimitive)]
#[repr(u8)]
pub enum IndexFormat {
    #[default]
    Default,
    LineList,
    LineStrip,
    TriangleList,
    TrianglePatch,
    TriangleStrip,
    QuadList,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x3C))]
pub struct SectionBlock {
    #[data(offset(0x00))]
    pub section_lods: FieldBlock<SectionLods>,
    #[data(offset(0x14))]
    pub mesh_flags: FieldWordFlags<MeshFlags>,
    #[data(offset(0x16))]
    pub node_index: FieldByteInteger,
    #[data(offset(0x17))]
    pub vertex_type: FieldCharEnum<VertexType>,
    #[data(offset(0x18))]
    pub use_dual_quat: FieldCharInteger,
    #[data(offset(0x19))]
    pub index_buffer_type: FieldCharEnum<IndexFormat>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(84))]
pub struct BoundingBoxBlock {
    #[data(offset(4))]
    pub x_bounds: FieldRealBounds,
    #[data(offset(12))]
    pub y_bounds: FieldRealBounds,
    #[data(offset(20))]
    pub z_bounds: FieldRealBounds,
    #[data(offset(28))]
    pub u_bounds: FieldRealBounds,
    #[data(offset(36))]
    pub v_bounds: FieldRealBounds,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(1))]
pub struct Index {
    #[data(offset(0))]
    pub index: FieldByteInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(20))]
pub struct NodeMapBlock {
    #[data(offset(0))]
    pub indices: FieldBlock<Index>,
}

#[derive(Default, Debug, TryFromPrimitive)]
#[repr(u32)]
pub enum VertexBufferUsage {
    #[default]
    Position,
    UV0,
    UV1,
    UV2,
    Color,
    Normal,
    Tangent,
    BlendIndices0,
    BlendWeights0,
    BlendIndices1,
    BlendWeights1,
    PrevPosition,
    InstanceData,
    BlendshapePosition,
    BlendshapeNormal,
    BlendshapeIndex,
    Edge,
    EdgeIndex,
    EdgeIndexInfo,
}

#[derive(Default, Debug, TryFromPrimitive)]
#[repr(u32)]
pub enum RasterizerVertexFormat {
    #[default]
    Real,
    RealVector2D,
    RealVector3D,
    RealVector4D,
    ByteVector4D,
    ByteARGBColor,
    ShortVector2D,
    ShortVector2DNormalized,
    ShortVector4DNormalized,
    WordVector2DNormalized,
    WordVector4DNormalized,
    Real16Vector2D,
    Real16Vector4D,
    Normalized101010,
    _1010102,
    _1010102SignedNormalizedPackedAsUnorm,
    Dword,
    DwordVector2D,
    _111110Float,
    ByteUnitVector3D,
    WordVector3DNormalizedWith4Word,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(80))]
pub struct RasterizerVertexBuffer {
    #[data(offset(0))]
    pub vertex_buffer_usage: FieldLongEnum<VertexBufferUsage>,
    #[data(offset(4))]
    pub format: FieldLongEnum<RasterizerVertexFormat>,
    #[data(offset(8))]
    pub stride: FieldByteInteger,
    #[data(offset(12))]
    pub count: FieldLongInteger,
    #[data(offset(16))]
    pub offset: FieldLongInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(72))]
pub struct RasterizerIndexBuffer {
    #[data(offset(0))]
    pub declaration_type: FieldCharEnum<IndexFormat>,
    #[data(offset(1))]
    pub stride: FieldCharInteger,
    #[data(offset(4))]
    pub count: FieldLongInteger,
    #[data(offset(8))]
    pub offset: FieldLongInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(312))]
pub struct RenderGeometryApiResource {
    #[data(offset(0))]
    pub vertex_buffers: FieldBlock<RasterizerVertexBuffer>,
    #[data(offset(16))]
    pub index_buffers: FieldBlock<RasterizerIndexBuffer>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(16))]
pub struct MeshResourceGroupBlock {
    #[data(offset(0))]
    pub resource: FieldTagResource<RenderGeometryApiResource>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x298))]
pub struct RenderModel {
    #[data(offset(0x00))]
    any_tag: AnyTag,
    #[data(offset(0x18))]
    pub mesh_resource_packing_policy: FieldLongEnum<ResourcePackingPolicy>,
    #[data(offset(0x28))]
    pub regions: FieldBlock<RegionBlock>,
    #[data(offset(0x40))]
    pub nodes: FieldBlock<NodeBlock>,
    #[data(offset(0x68))]
    pub marker_groups: FieldBlock<MarkerGroupBlock>,
    #[data(offset(0x7C))]
    pub materials: FieldBlock<MaterialBlock>,
    #[data(offset(0xC0))]
    pub sections: FieldBlock<SectionBlock>,
    #[data(offset(232))]
    pub bounding_boxes: FieldBlock<BoundingBoxBlock>,
    #[data(offset(252))]
    pub node_maps: FieldBlock<NodeMapBlock>,
    #[data(offset(316))]
    pub total_index_buffer_count: FieldLongInteger,
    #[data(offset(320))]
    pub total_vertex_buffer_count: FieldLongInteger,
    #[data(offset(324))]
    pub resources: FieldBlock<MeshResourceGroupBlock>,
}
