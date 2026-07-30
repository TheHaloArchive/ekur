use bitflags::bitflags;
use infinite_rs::{
    TagStructure,
    tag::types::common_types::{
        AnyTag, FieldBlock, FieldCharEnum, FieldData, FieldDwordInteger, FieldLongInteger,
        FieldReal, FieldRealPoint3D, FieldRealQuaternion, FieldShortBlockIndex, FieldShortInteger,
        FieldStringId, FieldTagResource, FieldWordFlags, FieldWordInteger,
    },
};
use num_enum::TryFromPrimitive;

#[derive(Default, Debug, TryFromPrimitive, PartialEq)]
#[repr(u8)]
pub enum MovementDataType {
    #[default]
    None,
    DxDy,
    DxDyDyaw,
    DxDyDzDyaw,
    DxDyDzDangleAxis,
    XYZAbsolute,
    Auto,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x4C))]
pub struct AnimationDataSizes {
    #[data(offset(0x00))]
    pub static_node_flags: FieldLongInteger,
    #[data(offset(0x04))]
    pub animated_node_flags: FieldLongInteger,
    #[data(offset(0x08))]
    pub movement_data: FieldLongInteger,
    #[data(offset(0x0C))]
    pub pill_offset_data: FieldLongInteger,
    #[data(offset(0x10))]
    pub default_data: FieldLongInteger,
    #[data(offset(0x14))]
    pub uncompressed_data: FieldLongInteger,
    #[data(offset(0x18))]
    pub compressed_data: FieldLongInteger,
    #[data(offset(0x1C))]
    pub blend_screen_data: FieldLongInteger,
    #[data(offset(0x20))]
    pub object_space_offset_data: FieldLongInteger,
    #[data(offset(0x24))]
    pub ik_chain_event_data: FieldLongInteger,
    #[data(offset(0x28))]
    pub ik_chain_control_data: FieldLongInteger,
    #[data(offset(0x2C))]
    pub ik_chain_proxy_data: FieldLongInteger,
    #[data(offset(0x30))]
    pub ik_chain_pole_vector_data: FieldLongInteger,
    #[data(offset(0x34))]
    pub uncompressed_object_space_data: FieldLongInteger,
    #[data(offset(0x38))]
    pub fik_anchor_data: FieldLongInteger,
    #[data(offset(0x3C))]
    pub uncompressed_object_space_node_flags: FieldLongInteger,
    #[data(offset(0x40))]
    pub compressed_event_curve: FieldLongInteger,
    #[data(offset(0x44))]
    pub compressed_static_pose: FieldLongInteger,
    #[data(offset(0x48))]
    pub user_parameter: FieldLongInteger,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x18C))]
pub struct AnimationTagResourceMember {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub animation_checksum: FieldDwordInteger,
    #[data(offset(0x08))]
    pub frame_count: FieldShortInteger,
    #[data(offset(0x0A))]
    pub node_count: FieldWordInteger,
    #[data(offset(0x0C))]
    pub movement_data_type: FieldCharEnum<MovementDataType>,
    #[data(offset(0x128))]
    pub animation_data_sizes: AnimationDataSizes,
    #[data(offset(0x174))]
    pub animation_data: FieldData,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x14))]
pub struct ModelAnimationGroupResource {
    #[data(offset(0x00))]
    pub group_members: FieldBlock<AnimationTagResourceMember>,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x14))]
pub struct ModelAnimationTagResource {
    #[data(offset(0x00))]
    pub reference_count: FieldLongInteger,
    #[data(offset(0x04))]
    pub tag_resource: FieldTagResource<ModelAnimationGroupResource>,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x04))]
pub struct AnimationResourceIndex {
    #[data(offset(0x00))]
    pub resource_group: FieldShortBlockIndex,
    #[data(offset(0x02))]
    pub resource_member_index: FieldShortInteger,
}

#[derive(Debug, Default, TryFromPrimitive)]
#[repr(u8)]
pub enum AnimationType {
    #[default]
    None,
    Base,
    Overlay,
    Replacement,
}

#[derive(Debug, Default, TryFromPrimitive)]
#[repr(u8)]
pub enum CompressionType {
    #[default]
    BestScore,
    BestCompression,
    LightCompression,
    BestAccuracy,
    ACLAuto,
    OldVodec,
    ReachMediumCompression,
    ReachRoughCompression,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x78))]
pub struct ModelAnimation {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub frame_count: FieldShortInteger,
    #[data(offset(0x06))]
    pub node_count: FieldWordInteger,
    #[data(offset(0x08))]
    pub animation_type: FieldCharEnum<AnimationType>,
    #[data(offset(0x09))]
    pub frame_info_type: FieldCharEnum<MovementDataType>,
    #[data(offset(0x0A))]
    pub desired_frame_info_type: FieldCharEnum<MovementDataType>,
    #[data(offset(0x0B))]
    pub desired_compression: FieldCharEnum<CompressionType>,
    #[data(offset(0x0C))]
    pub current_compression: FieldCharEnum<CompressionType>,
    #[data(offset(0x74))]
    pub resource_index: AnimationResourceIndex,
}

bitflags! {
    #[derive(Default, Debug)]
    pub struct AnimationNodeModelFlags : u16 {
        const PRIMARY_MODEL = 1 << 0;
        const SECONDARY_MODEL = 1 << 1;
        const LOCAL_ROOT = 1 << 2;
        const LEFT_HAND = 1 << 3;
        const RIGHT_HAND = 1 << 4;
        const LEFT_ARM_MEMBER = 1 << 5;
        const DETAIL_JOINT = 1 << 6;
    }
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x18))]
pub struct SkeletonBone {
    #[data(offset(0x00))]
    pub name: FieldStringId,
    #[data(offset(0x04))]
    pub next_sibling_node_index: FieldShortBlockIndex,
    #[data(offset(0x06))]
    pub first_child_node_index: FieldShortBlockIndex,
    #[data(offset(0x08))]
    pub parent_node_index: FieldShortBlockIndex,
    #[data(offset(0x0A))]
    pub model_flags: FieldWordFlags<AnimationNodeModelFlags>,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x08))]
pub struct Quaternion8ByteRevised {
    #[data(offset(0x00))]
    pub x: FieldShortInteger,
    #[data(offset(0x02))]
    pub y: FieldShortInteger,
    #[data(offset(0x04))]
    pub z: FieldShortInteger,
    #[data(offset(0x06))]
    pub w: FieldShortInteger,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x0C))]
pub struct SharedStaticDataCodecTranslation {
    #[data(offset(0x00))]
    pub x: FieldReal,
    #[data(offset(0x04))]
    pub y: FieldReal,
    #[data(offset(0x08))]
    pub z: FieldReal,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x04))]
pub struct SharedStaticDataCodecScale {
    #[data(offset(0x00))]
    pub scale: FieldReal,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(60))]
pub struct AdditionalNodeData {
    #[data(offset(0x00))]
    pub node_name: FieldStringId,
    #[data(offset(0x04))]
    pub default_rotation: FieldRealQuaternion,
    #[data(offset(20))]
    pub default_translation: FieldRealPoint3D,
    #[data(offset(32))]
    pub default_scale: FieldReal,
}

#[derive(Debug, Default, TagStructure)]
#[data(size(0x488))]
pub struct AnimationGraph {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(192))]
    pub skeleton_bones: FieldBlock<SkeletonBone>,
    #[data(offset(432))]
    pub animations: FieldBlock<ModelAnimation>,
    #[data(offset(1056))]
    pub additional_node_data: FieldBlock<AdditionalNodeData>,
    #[data(offset(0x434))]
    pub tag_resource_groups: FieldBlock<ModelAnimationTagResource>,
    #[data(offset(0x448))]
    pub rotations: FieldBlock<Quaternion8ByteRevised>,
    #[data(offset(0x45C))]
    pub positions: FieldBlock<SharedStaticDataCodecTranslation>,
    #[data(offset(0x470))]
    pub scales: FieldBlock<SharedStaticDataCodecScale>,
}

#[derive(Debug, Default, TryFromPrimitive, PartialEq)]
#[repr(u8)]
pub enum CodecType {
    #[default]
    NoCompression,
    UncompressedStatic,
    UncompressedAnimated,
    _8ByteQuantizedRotationOnly,
    ByteKeyframeLightlyQuantized,
    WordKeyframeLightlyQuantized,
    ReverseByteKeyframeLightlyQuantized,
    ReverseWordKeyframeLightlyQuantized,
    BlendScreen,
    Curve,
    RevisedCurve,
    SharedStatic,
    AnimationCompressionLibrary,
}
