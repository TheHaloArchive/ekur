use crate::{
    codecs::{
        Codec,
        shared_static::{SharedStaticPool, build_shared_static_pool, decode_shared_static},
    },
    datatypes::{
        flag_data::{FlagData, bit_is_set, popcount_below},
        jma_kind::JmaKind,
        matrix::Matrix4,
        movement::{MovementData, read_movement_at},
        quaternion::Quaternion,
        vector::Vector3,
    },
    jma::{compose_overlay, compose_pose, compose_replacement, write_jma},
};
use std::{collections::HashMap, fs::create_dir_all, io::Cursor, path::PathBuf};

use anyhow::Result;
use num_enum::TryFromPrimitive;

use crate::codecs::quantized_rotation_only::QuantizedRotationOnly;

use ekur_definitions::{
    animations::{
        AnimationGraph, AnimationTagResourceMember,
        CodecType::{self},
    },
    model::ModelDefinition,
    render_model::RenderModel,
};

mod codecs;
pub mod datatypes;
mod jma;

fn process_codecs(
    tag_resource: &AnimationTagResourceMember,
    anim_frame_count: i16,
    shared_pool: &SharedStaticPool,
) -> Result<(Codec, Codec, FlagData, FlagData, MovementData, i16, bool)> {
    let data = &tag_resource.animation_data.data;
    let sizes = &tag_resource.animation_data_sizes;

    if data.is_empty() {
        return Ok((
            Codec::default(),
            Codec::default(),
            FlagData::default(),
            FlagData::default(),
            MovementData::default(),
            anim_frame_count.max(1),
            true,
        ));
    }

    let resolved_frame_count = if tag_resource.frame_count.0 > 0 {
        tag_resource.frame_count.0
    } else {
        anim_frame_count.max(1)
    };

    let codec = CodecType::try_from_primitive(data[0]).unwrap_or_default();

    let static_codec_size = sizes.static_node_flags.0 as usize;
    let animated_stream_size = sizes.animated_node_flags.0 as usize;
    let has_static_stream = codec == CodecType::UncompressedStatic && static_codec_size > 0;

    let static_tracks = if has_static_stream {
        let mut reader = Cursor::new(data.as_slice());
        QuantizedRotationOnly::from_reader(&mut reader, 1, true)?.into_codec()
    } else {
        decode_shared_static(data, tag_resource, shared_pool).unwrap_or_default()
    };

    let animated_offset = if has_static_stream {
        static_codec_size
    } else {
        0
    };

    let mut animated_decoded = true;
    let animated_tracks = if animated_stream_size == 0 || animated_offset >= data.len() {
        Codec::default()
    } else {
        let anim_end = (animated_offset + animated_stream_size).min(data.len());
        let anim_blob = &data[animated_offset..anim_end];
        if anim_blob.is_empty() {
            animated_decoded = false;
            Codec::default()
        } else {
            let anim_codec = CodecType::try_from_primitive(anim_blob[0]).unwrap_or_default();
            let mut reader = Cursor::new(anim_blob);
            match anim_codec {
                CodecType::UncompressedAnimated => {
                    QuantizedRotationOnly::from_reader(&mut reader, resolved_frame_count, false)?
                        .into_codec()
                }
                CodecType::_8ByteQuantizedRotationOnly => {
                    QuantizedRotationOnly::from_reader(&mut reader, resolved_frame_count, true)?
                        .into_codec()
                }
                CodecType::BlendScreen => {
                    QuantizedRotationOnly::from_reader(&mut reader, resolved_frame_count, false)?
                        .into_codec()
                }
                _ => {
                    animated_decoded = false;
                    Codec::default()
                }
            }
        }
    };

    let flags_offset = static_codec_size + animated_stream_size;
    let static_flags_size = sizes.movement_data.0 as usize;
    let animated_flags_size = sizes.pill_offset_data.0 as usize;

    let static_flags = read_flags_at(data, flags_offset, static_flags_size);
    let animated_flags = read_flags_at(data, flags_offset + static_flags_size, animated_flags_size);

    let movement_offset = flags_offset + static_flags_size + animated_flags_size;
    let movement_size = sizes.default_data.0 as usize;
    let movement = read_movement_at(
        data,
        movement_offset,
        movement_size,
        tag_resource.movement_data_type.0,
        resolved_frame_count as usize,
    );

    Ok((
        static_tracks,
        animated_tracks,
        static_flags,
        animated_flags,
        movement,
        resolved_frame_count,
        animated_decoded,
    ))
}

fn read_flags_at(data: &[u8], offset: usize, size: usize) -> FlagData {
    if size == 0 || offset.checked_add(size).is_none_or(|end| end > data.len()) {
        return FlagData::default();
    }
    FlagData::from_slice(&data[offset..offset + size])
}

#[derive(Debug, Clone, Copy)]
enum TrackSource {
    Static(usize),
    Animated(usize),
    Identity,
}

fn pick_source(
    bone: usize,
    static_bits: &bitvec::vec::BitVec<u8>,
    animated_bits: &bitvec::vec::BitVec<u8>,
) -> TrackSource {
    if bit_is_set(static_bits, bone) {
        TrackSource::Static(popcount_below(static_bits, bone))
    } else if bit_is_set(animated_bits, bone) {
        TrackSource::Animated(popcount_below(animated_bits, bone))
    } else {
        TrackSource::Identity
    }
}

#[derive(Debug, Clone, Copy)]
struct BoneResolution {
    rotation: TrackSource,
    translation: TrackSource,
    scale: TrackSource,
}

fn resolve_bones(
    bones: usize,
    static_flags: &FlagData,
    animated_flags: &FlagData,
) -> Vec<BoneResolution> {
    (0..bones)
        .map(|b| BoneResolution {
            rotation: pick_source(b, &static_flags.rotation, &animated_flags.rotation),
            translation: pick_source(b, &static_flags.translation, &animated_flags.translation),
            scale: pick_source(b, &static_flags.scale, &animated_flags.scale),
        })
        .collect()
}

#[derive(Default, Debug)]
pub struct SkeletonNode {
    name: String,
    first_child: i16,
    next_sibling: i16,
    parent: i16,
}

#[derive(Default, Debug)]
pub struct Skeleton {
    pub nodes: Vec<SkeletonNode>,
}

impl Skeleton {
    pub fn object_to_local(&self, object: &[NodeTransform]) -> Vec<NodeTransform> {
        let world: Vec<Matrix4> = object
            .iter()
            .map(|t| Matrix4::from_loc_rot_scale(t.translation, t.rotation, t.scale))
            .collect();
        self.nodes
            .iter()
            .enumerate()
            .map(|(i, n)| {
                let local = if n.parent >= 0 && (n.parent as usize) < world.len() {
                    world[n.parent as usize].inverse() * world[i]
                } else {
                    world[i]
                };
                let (translation, rotation, scale) = local.decompose();
                NodeTransform {
                    translation,
                    rotation,
                    scale,
                }
            })
            .collect()
    }
}

fn create_skeleton(animation_graph: &AnimationGraph, strings: &HashMap<i32, String>) -> Skeleton {
    let mut nodes = Vec::new();
    for bone in &animation_graph.skeleton_bones.elements {
        let node = SkeletonNode {
            name: strings
                .get(&bone.name.0)
                .cloned()
                .unwrap_or_else(|| bone.name.0.to_string()),
            first_child: bone.first_child_node_index.0,
            next_sibling: bone.next_sibling_node_index.0,
            parent: bone.parent_node_index.0,
        };
        nodes.push(node);
    }
    Skeleton { nodes }
}

#[derive(Debug, Clone, Default, Copy)]
pub struct NodeTransform {
    pub rotation: Quaternion,
    pub translation: Vector3,
    pub scale: f32,
}

impl NodeTransform {
    pub const IDENTITY: Self = Self {
        rotation: Quaternion::IDENTITY,
        translation: Vector3 {
            x: 0.0,
            y: 0.0,
            z: 0.0,
        },
        scale: 1.0,
    };
}

pub fn build_defaults(
    skeleton: &Skeleton,
    jmad: &AnimationGraph,
    render_model: Option<&RenderModel>,
    strings: &HashMap<i32, String>,
) -> Vec<NodeTransform> {
    let mut anim_by_name: HashMap<String, NodeTransform> = HashMap::new();
    for block in &jmad.additional_node_data.elements {
        anim_by_name.insert(
            strings
                .get(&block.node_name.0)
                .cloned()
                .unwrap_or_else(|| block.node_name.0.to_string()),
            NodeTransform {
                translation: Vector3::from_field(&block.default_translation),
                rotation: Quaternion::from_field(&block.default_rotation),
                scale: block.default_scale.0,
            },
        );
    }
    let mut anim: Vec<NodeTransform> = skeleton
        .nodes
        .iter()
        .map(|n| {
            anim_by_name
                .get(&n.name)
                .copied()
                .unwrap_or(NodeTransform::IDENTITY)
        })
        .collect();
    anim = skeleton.object_to_local(&anim);

    let mut rm_by_name: HashMap<String, NodeTransform> = HashMap::new();
    if let Some(render_model) = render_model {
        for node in &render_model.nodes.elements {
            rm_by_name.insert(
                strings
                    .get(&node.name.0)
                    .cloned()
                    .unwrap_or_else(|| node.name.0.to_string()),
                NodeTransform {
                    translation: Vector3::from_field(&node.position),
                    rotation: Quaternion::from_field(&node.rotation),
                    scale: 1.0,
                },
            );
        }
    }

    skeleton
        .nodes
        .iter()
        .enumerate()
        .map(|(i, node)| rm_by_name.get(&node.name).copied().unwrap_or(anim[i]))
        .collect()
}

pub fn sanitize(name: &str) -> String {
    name.chars()
        .map(|c| match c {
            ':' => ' ',
            '/' | '\\' | '*' | '?' | '"' | '<' | '>' | '|' => '_',
            c if c.is_control() => '_',
            c => c,
        })
        .collect()
}

fn process_animations(
    animation_graph: &AnimationGraph,
    render_model: &RenderModel,
    save_path: &str,
    strings: &HashMap<i32, String>,
    model_ids: &HashMap<i32, String>,
) -> Result<()> {
    let skeleton = create_skeleton(animation_graph, strings);
    if skeleton.nodes.is_empty() {
        return Ok(());
    }
    let defaults = build_defaults(&skeleton, animation_graph, Some(render_model), strings);
    let shared_pool = build_shared_static_pool(animation_graph);
    let groups = &animation_graph.tag_resource_groups.elements;

    for anim in animation_graph.animations.elements.iter() {
        let indices = &anim.resource_index;
        let Some(group) = groups.get(indices.resource_group.0 as usize) else {
            continue;
        };
        let group_members = &group.tag_resource.data.group_members.elements;
        let Some(group_member) = group_members.get(indices.resource_member_index.0 as usize) else {
            continue;
        };

        if group_member.animation_data.data.is_empty() {
            continue;
        }

        let (
            static_codec,
            animated_codec,
            static_flags,
            animated_flags,
            movement,
            frame_count,
            animated_decoded,
        ) = process_codecs(group_member, anim.frame_count.0, &shared_pool)?;

        if !animated_decoded {
            continue;
        }

        let kind = JmaKind::from_metadata(anim.animation_type.0, anim.frame_info_type.0);
        let codec_frame_count = frame_count.max(1) as usize;
        let base: Vec<NodeTransform> = defaults.clone();

        let (leading, frames) = match kind {
            JmaKind::Jmo => compose_overlay(
                &skeleton,
                &static_codec,
                &animated_codec,
                &static_flags,
                &animated_flags,
                &base,
                codec_frame_count,
            ),
            JmaKind::Jmr => {
                let body = compose_replacement(
                    &skeleton,
                    &animated_codec,
                    &animated_flags,
                    &base,
                    codec_frame_count,
                );
                (base.clone(), body)
            }
            _ => {
                let body = compose_pose(
                    &skeleton,
                    &static_codec,
                    &animated_codec,
                    &static_flags,
                    &animated_flags,
                    &base,
                    codec_frame_count,
                );
                (base.clone(), body)
            }
        };

        let name = strings
            .get(&anim.name.0)
            .cloned()
            .unwrap_or_else(|| format!("anim_{}", anim.name.0));
        let render_model_id = model_ids
            .get(&render_model.any_tag.internal_struct.tag_id)
            .unwrap_or(&render_model.any_tag.internal_struct.tag_id.to_string())
            .clone();
        let graph_id = animation_graph.any_tag.internal_struct.tag_id;
        let filename = format!(
            "{}_{}_{}.{}",
            render_model_id,
            sanitize(&name),
            graph_id,
            kind.extension()
        );

        let mut path = PathBuf::from(save_path);
        path.push("anims");
        path.push(filename);

        write_jma(
            &path,
            &skeleton,
            &frames,
            &leading,
            kind,
            "unnamedActor",
            &movement,
        )?;
    }
    Ok(())
}

pub fn extract_animations(
    strings: &HashMap<i32, String>,
    model_ids: &HashMap<i32, String>,
    anim_tags: &HashMap<i32, AnimationGraph>,
    hlmt_tags: &HashMap<i32, ModelDefinition>,
    mode_tags: &HashMap<(usize, usize, i32), RenderModel>,
    save_path: &str,
) -> Result<()> {
    let mut save_paths = PathBuf::from(save_path);
    save_paths.push("anims/");
    create_dir_all(&save_paths)?;
    for hlmt in hlmt_tags.values() {
        let mode = mode_tags
            .iter()
            .find(|x| x.1.any_tag.internal_struct.tag_id == hlmt.render_model.global_id);
        let anim_tag = anim_tags.get(&hlmt.animation.global_id);
        if let Some(anim_tag) = anim_tag
            && let Some(mode) = mode
        {
            process_animations(anim_tag, mode.1, save_path, strings, model_ids)?;
        }
    }

    Ok(())
}
