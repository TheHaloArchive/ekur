use infinite_rs::tag::types::common_types::{
    AnyTag, FieldBlock, FieldCharInteger, FieldLongEnum, FieldLongInteger, FieldReal,
    FieldRealPoint3D, FieldRealQuaternion, FieldRealVector3D, FieldReference, FieldShortBlockIndex,
    FieldShortInteger, FieldStringId, FieldWordInteger,
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
#[data(size(0x94))]
pub struct SectionLods {}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x3C))]
pub struct SectionBlock {
    #[data(offset(0x00))]
    pub section_lods: FieldBlock<SectionLods>,
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
}
