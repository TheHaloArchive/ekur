use crate::{
    codecs::{Codec, static_data::StaticData},
    datatypes::{flag_data::FlagData, quaternion::Quaternion, vector::Vector3},
};
use std::{collections::HashMap, fs::create_dir_all, io::Write, path::PathBuf};
use std::{
    fs::File,
    io::{BufWriter, Cursor},
};
use std::{io::Seek, ops::Mul};

use anyhow::Result;
use infinite_rs::ModuleFile;
use num_enum::TryFromPrimitive;

use crate::codecs::quantized_rotation_only::QuantizedRotationOnly;

use ekur_definitions::{
    animations::{
        AnimationGraph, AnimationTagResourceMember,
        CodecType::{self},
        SkeletonBone,
    },
    model::ModelDefinition,
    render_model::{NodeBlock, RenderModel},
};

mod codecs;
pub mod datatypes;

#[derive(Debug, Default)]
pub struct SharedStaticPool {
    pub rotations: Vec<Quaternion>,
    pub translations: Vec<Vector3>,
    pub scales: Vec<f32>,
}

fn decode_shared_static(buffer: &[u8], tag_data: &AnimationTagResourceMember) -> Option<Codec> {
    let pool = SharedStaticPool::default();
    let cps = tag_data.animation_data_sizes.compressed_static_pose.0 as usize;
    if cps == 0 || cps > buffer.len() {
        return None;
    }
    // `compressed_static_pose` is the last data_sizes section, so it
    // sits at the tail of the blob.
    let s = &buffer[buffer.len() - cps..];
    if s.len() < 32 || s[0] != CodecType::SharedStatic as u8 {
        return None;
    }
    let (n_rot, n_trn, n_scl) = (s[1] as usize, s[2] as usize, s[3] as usize);
    let trn_off = u32::from_le_bytes(s.get(12..16)?.try_into().ok()?) as usize;
    let scl_off = u32::from_le_bytes(s.get(16..20)?.try_into().ok()?) as usize;
    let index =
        |o: usize| -> Option<i16> { s.get(o..o + 2).map(|b| i16::from_le_bytes([b[0], b[1]])) };
    let mut rotations = Vec::with_capacity(n_rot);
    for k in 0..n_rot {
        let idx = index(32 + 2 * k)?;
        let q = (idx >= 0)
            .then(|| pool.rotations.get(idx as usize).copied())
            .flatten();
        rotations.push(vec![q.unwrap_or(Quaternion::IDENTITY)]);
    }
    let mut translations = Vec::with_capacity(n_trn);
    for k in 0..n_trn {
        let idx = index(trn_off + 2 * k)?;
        let t = (idx >= 0)
            .then(|| pool.translations.get(idx as usize).copied())
            .flatten();
        translations.push(vec![t.unwrap_or_default()]);
    }
    let mut scales = Vec::with_capacity(n_scl);
    for k in 0..n_scl {
        let idx = index(scl_off + 2 * k)?;
        let v = (idx >= 0)
            .then(|| pool.scales.get(idx as usize).copied())
            .flatten();
        scales.push(vec![v.unwrap_or(1.0)]);
    }
    Some(Codec {
        codec_type: CodecType::SharedStatic,
        frame_count: 1,
        rotations,
        translations,
        scales,
    })
}

fn process_codecs(
    tag_resource: &AnimationTagResourceMember,
    frame_count: i16,
) -> Result<(Codec, Codec, FlagData, FlagData)> {
    let buffer = Cursor::new(&tag_resource.animation_data.data);
    if tag_resource.animation_data.data.len() <= 0 {
        return Ok((
            Codec::default(),
            Codec::default(),
            FlagData::default(),
            FlagData::default(),
        ));
    }
    let codec = CodecType::try_from_primitive(tag_resource.animation_data.data[0])?;
    let static_first_size = tag_resource.animation_data_sizes.static_node_flags.0;
    let has_static_stream = codec == CodecType::UncompressedStatic && static_first_size > 0;

    let static_tracks = if has_static_stream {
        QuantizedRotationOnly::from_reader(buffer, 1, true)?
            .into_codec(CodecType::UncompressedStatic)
    } else if let Some(tracks) =
        decode_shared_static(&tag_resource.animation_data.data, tag_resource)
    {
        // Halo 4: the static rest pose is a `SharedStatic` (codec 11)
        // stream of int16 indices into the graph-level shared pool.
        tracks
    } else {
        // No static stream — start with empty static tracks so
        // pose composition has something to fall back to. The
        // animated stream then starts at offset 0.
        Codec {
            codec_type: CodecType::UncompressedStatic,
            frame_count: 1,
            rotations: Vec::new(),
            translations: Vec::new(),
            scales: Vec::new(),
        }
    };

    let frame_count = tag_resource.frame_count.0;
    let static_size = static_first_size;
    let animated_offset = static_size as usize;
    let animated_blob_len = tag_resource.animation_data_sizes.animated_node_flags.0;

    let anim_end = (animated_offset as usize + animated_blob_len as usize)
        .min(tag_resource.animation_data.data.len());
    let anim_blob = &tag_resource.animation_data.data[0..anim_end];
    let anim_byte = anim_blob[0];
    let codec = CodecType::try_from_primitive(anim_byte)?;
    let mut reader = Cursor::new(anim_blob);
    //println!("{codec:#?}");
    let tracks = match codec {
        CodecType::NoCompression => Codec::default(),
        CodecType::UncompressedStatic => Codec::default(),
        CodecType::UncompressedAnimated => {
            QuantizedRotationOnly::from_reader(&mut reader, frame_count, false)?
                .into_codec(CodecType::UncompressedAnimated)
        }
        CodecType::_8ByteQuantizedRotationOnly => {
            QuantizedRotationOnly::from_reader(&mut reader, frame_count, true)?
                .into_codec(CodecType::_8ByteQuantizedRotationOnly)
        }
        CodecType::ByteKeyframeLightlyQuantized => Codec::default(),
        CodecType::WordKeyframeLightlyQuantized => Codec::default(),
        CodecType::ReverseByteKeyframeLightlyQuantized => Codec::default(),
        CodecType::ReverseWordKeyframeLightlyQuantized => Codec::default(),
        CodecType::BlendScreen => {
            QuantizedRotationOnly::from_reader(&mut reader, frame_count, false)?
                .into_codec(CodecType::BlendScreen)
        }
        CodecType::Curve => Codec::default(),
        CodecType::RevisedCurve => Codec::default(),
        CodecType::SharedStatic => Codec::default(),
        CodecType::AnimationCompressionLibrary => Codec::default(),
    };
    let last_pos = reader.stream_position()?;
    let mut reader = Cursor::new(&tag_resource.animation_data.data);
    reader.seek_relative(last_pos as i64)?;

    let static_info = FlagData::from_reader(
        &mut reader,
        tag_resource.animation_data_sizes.pill_offset_data.0 as u32,
    )?;
    let animated_info = FlagData::from_reader(
        &mut reader,
        tag_resource.animation_data_sizes.movement_data.0 as u32,
    )?;

    Ok((static_tracks, tracks, static_info, animated_info))
}

fn construct_data(
    static_data: Codec,
    anim_data: Codec,
    stat_inf: FlagData,
    anim_inf: FlagData,
    render_model: &RenderModel,
    shared_data: &AnimationGraph,
    frame_count: i16,
) -> (Vec<Vec<Quaternion>>, Vec<Vec<Vector3>>, Vec<Vec<f32>>) {
    let mut static_rotation_index = 0;
    let mut animated_rotation_index = 0;
    let mut static_translation_index = 0;
    let mut animated_translation_index = 0;
    let mut static_scale_index = 0;
    let mut animated_scale_index = 0;

    let mut quaternions = Vec::new();
    let mut translations = Vec::new();
    let mut scales = Vec::new();

    let nodes = &render_model.nodes.elements;

    for (index, node) in nodes.iter().enumerate() {
        let mut rotation_frames = Vec::new();
        let mut translation_frames = Vec::new();
        let mut scale_frames = Vec::new();

        for fram_index in 0..(frame_count - 1) {
            if static_data.rotations.is_empty() && anim_data.rotations.is_empty() {
                continue;
            }
            let is_rot_static = stat_inf.rotation[index];
            let is_rot_anim = stat_inf.rotation[index];
        }

        if *stat_inf.rotation.get(index).as_deref().unwrap_or(&false) {
            static_rotation_index += 1;
        }
        if *anim_inf.rotation.get(index).as_deref().unwrap_or(&false) {
            animated_rotation_index += 1;
        }
        if *stat_inf.translation.get(index).as_deref().unwrap_or(&false) {
            static_translation_index += 1;
        }
        if *anim_inf.translation.get(index).as_deref().unwrap_or(&false) {
            animated_translation_index += 1;
        }
        if *stat_inf.scale.get(index).as_deref().unwrap_or(&false) {
            static_scale_index += 1;
        }
        if *anim_inf.scale.get(index).as_deref().unwrap_or(&false) {
            animated_scale_index += 1;
        }

        quaternions.push(rotation_frames);
        translations.push(translation_frames);
        scales.push(scale_frames);
    }
    (quaternions, translations, scales)
}

#[derive(Default, Debug)]
struct Node {
    name: String,
    parent_node: i16,
    first_child_node: i16,
    next_subling_node: i16,
    translation: (f32, f32, f32),
    rotation: (f32, f32, f32, f32),
    scale: f32,
}

#[derive(Default, Debug)]
struct Frame {
    nodes: Vec<Node>,
}

fn create_frames(
    quaternions: Vec<Vec<Quaternion>>,
    translations: Vec<Vec<Vector3>>,
    scales: Vec<Vec<f32>>,
    node_count: u32,
    frame_count: i16,
) -> Vec<Frame> {
    let mut all_frames = Vec::new();
    for frame_index in 0..frame_count {
        let mut frame = Frame::default();
        for node_index in 0..node_count {
            let mut node = Node::default();
            let v3 = &translations[node_index as usize][frame_index as usize];
            node.translation = (v3.x, v3.y, v3.z);
            let q4 = &quaternions[node_index as usize][frame_index as usize];
            node.rotation = (q4.x, q4.y, q4.z, q4.w);
            node.scale = scales[node_index as usize][frame_index as usize];
            frame.nodes.push(node);
        }
        all_frames.push(frame);
    }
    all_frames
}

fn export_animation(
    anim_id: i32,
    render_model_id: i32,
    graph_id: i32,
    frames: &[Frame],
    nodes: &[NodeBlock],
    skeleton_bones: &[SkeletonBone],
    string_ids: &HashMap<i32, String>,
    save_path: &str,
) -> Result<()> {
    let mut file = File::create(format!(
        "{}/anims/{}_{}_{}.jmm",
        save_path, render_model_id, anim_id, graph_id
    ))?;
    let mut bufwriter = BufWriter::new(&mut file);

    let number_of_shared_nodes = nodes
        .iter()
        .filter(|x| {
            skeleton_bones
                .iter()
                .map(|x| x.name.0)
                .collect::<Vec<_>>()
                .contains(&x.name.0)
        })
        .count();

    writeln!(bufwriter, "{}", 16392)?;
    writeln!(bufwriter, "{}", frames.len())?;
    writeln!(bufwriter, "{}", 30)?;
    writeln!(bufwriter, "{}", 1)?;
    writeln!(bufwriter, "unnamedActor")?;
    writeln!(bufwriter, "{}", number_of_shared_nodes)?;
    writeln!(bufwriter, "{}", 0)?; // NodeListChecksum placeholder

    for node in nodes {
        let skeleton_bone = skeleton_bones.iter().find(|x| x.name.0 == node.name.0);
        if let Some(bone) = skeleton_bone {
            writeln!(
                bufwriter,
                "{}",
                string_ids
                    .get(&node.name.0)
                    .unwrap_or(&node.name.0.to_string())
            )?;
            writeln!(bufwriter, "{}", bone.first_child_node_index.0)?;
            writeln!(bufwriter, "{}", bone.next_sibling_node_index.0)?;
        }
    }

    for frame in frames {
        for node in &frame.nodes {
            let quaternion = Quaternion::from_tuple(node.rotation);
            let conjugate = quaternion.conjugate();
            let translation = node.translation;
            let scale = node.scale;

            writeln!(
                bufwriter,
                "{}\t{}\t{}",
                translation.0, translation.1, translation.2
            )?;
            writeln!(
                bufwriter,
                "{}\t{}\t{}\t{}",
                conjugate.x, conjugate.y, conjugate.z, conjugate.w
            )?;
            writeln!(bufwriter, "{}", scale)?;
        }
    }

    bufwriter.flush()?;

    Ok(())
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

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Matrix4 {
    pub m: [[f32; 4]; 4],
}

impl Matrix4 {
    pub const IDENTITY: Self = Self {
        m: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
    };

    pub fn from_loc_rot_scale(t: Vector3, q: Quaternion, s: f32) -> Self {
        let r = q.normalized();
        // 3×3 rotation from the quaternion.
        let (x, y, z, w) = (r.x, r.y, r.z, r.w);
        let (xx, yy, zz) = (x * x, y * y, z * z);
        let (xy, xz, yz) = (x * y, x * z, y * z);
        let (wx, wy, wz) = (w * x, w * y, w * z);
        let r00 = 1.0 - 2.0 * (yy + zz);
        let r01 = 2.0 * (xy - wz);
        let r02 = 2.0 * (xz + wy);
        let r10 = 2.0 * (xy + wz);
        let r11 = 1.0 - 2.0 * (xx + zz);
        let r12 = 2.0 * (yz - wx);
        let r20 = 2.0 * (xz - wy);
        let r21 = 2.0 * (yz + wx);
        let r22 = 1.0 - 2.0 * (xx + yy);
        Self {
            m: [
                [r00 * s, r01 * s, r02 * s, t.x],
                [r10 * s, r11 * s, r12 * s, t.y],
                [r20 * s, r21 * s, r22 * s, t.z],
                [0.0, 0.0, 0.0, 1.0],
            ],
        }
    }

    pub fn inverse(&self) -> Self {
        let a = &self.m;
        let (a00, a01, a02) = (a[0][0], a[0][1], a[0][2]);
        let (a10, a11, a12) = (a[1][0], a[1][1], a[1][2]);
        let (a20, a21, a22) = (a[2][0], a[2][1], a[2][2]);
        let det = a00 * (a11 * a22 - a12 * a21) - a01 * (a10 * a22 - a12 * a20)
            + a02 * (a10 * a21 - a11 * a20);
        if det.abs() < 1e-20 {
            return Self::IDENTITY;
        }
        let inv = 1.0 / det;
        // Inverse of the 3×3 (transpose of cofactor matrix × 1/det).
        let i00 = (a11 * a22 - a12 * a21) * inv;
        let i01 = (a02 * a21 - a01 * a22) * inv;
        let i02 = (a01 * a12 - a02 * a11) * inv;
        let i10 = (a12 * a20 - a10 * a22) * inv;
        let i11 = (a00 * a22 - a02 * a20) * inv;
        let i12 = (a02 * a10 - a00 * a12) * inv;
        let i20 = (a10 * a21 - a11 * a20) * inv;
        let i21 = (a01 * a20 - a00 * a21) * inv;
        let i22 = (a00 * a11 - a01 * a10) * inv;
        let (tx, ty, tz) = (a[0][3], a[1][3], a[2][3]);
        // -inv3x3 * t
        let nx = -(i00 * tx + i01 * ty + i02 * tz);
        let ny = -(i10 * tx + i11 * ty + i12 * tz);
        let nz = -(i20 * tx + i21 * ty + i22 * tz);
        Self {
            m: [
                [i00, i01, i02, nx],
                [i10, i11, i12, ny],
                [i20, i21, i22, nz],
                [0.0, 0.0, 0.0, 1.0],
            ],
        }
    }

    pub fn decompose(&self) -> (Vector3, Quaternion, f32) {
        let a = &self.m;
        let t = Vector3 {
            x: a[0][3],
            y: a[1][3],
            z: a[2][3],
        };
        // Column lengths = per-axis scale.
        let sx = (a[0][0] * a[0][0] + a[1][0] * a[1][0] + a[2][0] * a[2][0]).sqrt();
        let sy = (a[0][1] * a[0][1] + a[1][1] * a[1][1] + a[2][1] * a[2][1]).sqrt();
        let sz = (a[0][2] * a[0][2] + a[1][2] * a[1][2] + a[2][2] * a[2][2]).sqrt();
        let scale = (sx + sy + sz) / 3.0;
        // Normalized rotation matrix columns.
        let (ix, iy, iz) = (safe_div(sx), safe_div(sy), safe_div(sz));
        let r00 = a[0][0] * ix;
        let r01 = a[0][1] * iy;
        let r02 = a[0][2] * iz;
        let r10 = a[1][0] * ix;
        let r11 = a[1][1] * iy;
        let r12 = a[1][2] * iz;
        let r20 = a[2][0] * ix;
        let r21 = a[2][1] * iy;
        let r22 = a[2][2] * iz;
        let q = quat_from_mat3([[r00, r01, r02], [r10, r11, r12], [r20, r21, r22]]);
        (t, q, scale)
    }
}

fn quat_from_mat3(r: [[f32; 3]; 3]) -> Quaternion {
    let trace = r[0][0] + r[1][1] + r[2][2];
    let q = if trace > 0.0 {
        let s = (trace + 1.0).sqrt() * 2.0;
        Quaternion {
            w: 0.25 * s,
            x: (r[2][1] - r[1][2]) / s,
            y: (r[0][2] - r[2][0]) / s,
            z: (r[1][0] - r[0][1]) / s,
        }
    } else if r[0][0] > r[1][1] && r[0][0] > r[2][2] {
        let s = (1.0 + r[0][0] - r[1][1] - r[2][2]).sqrt() * 2.0;
        Quaternion {
            w: (r[2][1] - r[1][2]) / s,
            x: 0.25 * s,
            y: (r[0][1] + r[1][0]) / s,
            z: (r[0][2] + r[2][0]) / s,
        }
    } else if r[1][1] > r[2][2] {
        let s = (1.0 + r[1][1] - r[0][0] - r[2][2]).sqrt() * 2.0;
        Quaternion {
            w: (r[0][2] - r[2][0]) / s,
            x: (r[0][1] + r[1][0]) / s,
            y: 0.25 * s,
            z: (r[1][2] + r[2][1]) / s,
        }
    } else {
        let s = (1.0 + r[2][2] - r[0][0] - r[1][1]).sqrt() * 2.0;
        Quaternion {
            w: (r[1][0] - r[0][1]) / s,
            x: (r[0][2] + r[2][0]) / s,
            y: (r[1][2] + r[2][1]) / s,
            z: 0.25 * s,
        }
    };
    q.normalized()
}

fn safe_div(s: f32) -> f32 {
    if s.abs() < 1e-12 { 0.0 } else { 1.0 / s }
}

impl Mul for Matrix4 {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        let mut out = [[0.0f32; 4]; 4];
        for (r, out_row) in out.iter_mut().enumerate() {
            for (c, out_cell) in out_row.iter_mut().enumerate() {
                *out_cell = self.m[r][0] * rhs.m[0][c]
                    + self.m[r][1] * rhs.m[1][c]
                    + self.m[r][2] * rhs.m[2][c]
                    + self.m[r][3] * rhs.m[3][c];
            }
        }
        Self { m: out }
    }
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
                .unwrap_or(&bone.name.0.to_string())
                .clone(),
            first_child: bone.first_child_node_index.0,
            next_sibling: bone.next_sibling_node_index.0,
            parent: bone.parent_node_index.0,
        };
        nodes.push(node);
    }
    Skeleton { nodes }
}

/// One bone's transform at one frame — the unit JMA writes per
/// `(frame, node)` cell.
#[derive(Debug, Clone, Default, Copy)]
pub struct NodeTransform {
    pub rotation: Quaternion,
    pub translation: Vector3,
    pub scale: f32,
}

impl NodeTransform {
    /// Identity transform: rotation `(0,0,0,1)`, translation
    /// `(0,0,0)`, scale `1.0`. Useful as a fallback when no rest
    /// pose is available — note `Default` is all-zeros (rotation
    /// included) which is *not* identity.
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
    render_model: &Option<RenderModel>,
    strings: &HashMap<i32, String>,
) -> Vec<NodeTransform> {
    // Lower priority: jmad's `additional node data`, indexed per skeleton
    // node. Reach/H4 store these in object/model space; H2/H3 store them
    // parent-local. Build the per-node table first so we can convert the
    // whole object-space set to local in one parent-aware pass.
    let mut anim_by_name: HashMap<String, NodeTransform> = HashMap::new();
    for block in &jmad.additional_node_data.elements {
        anim_by_name.insert(
            strings
                .get(&block.node_name.0)
                .unwrap_or(&block.node_name.0.to_string())
                .clone(),
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
    // Reach/H4 `additional node data` is object-space → convert to local
    // (Foundry's world_to_local). H2/H3 are already local — leave as-is.
    anim = skeleton.object_to_local(&anim);

    // Higher priority: render_model `nodes[]` (always parent-local). Build
    // a name lookup and overlay it on top of the (now-local) anim defaults.
    let mut rm_by_name: HashMap<String, NodeTransform> = HashMap::new();
    if let Some(render_model) = render_model {
        for node in &render_model.nodes.elements {
            rm_by_name.insert(
                strings
                    .get(&node.name.0)
                    .unwrap_or(&node.name.0.to_string())
                    .clone(),
                NodeTransform {
                    translation: Vector3::from_field(&node.position),
                    rotation: Quaternion::from_field(&node.rotation),
                    // Render_model's `default scale` is buried inside the
                    // inverse matrix; animation rest poses have scale=1.0.
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

fn process_animations(
    animation_graph: &AnimationGraph,
    render_model: &RenderModel,
    save_path: &str,
    strings: &HashMap<i32, String>,
) -> Result<()> {
    for anim in &animation_graph.animations.elements {
        let groups = &animation_graph.tag_resource_groups.elements;
        //let skeleton = create_skeleton(animation_graph, strings);
        //let defaults = build_defaults(&skeleton, animation_graph, &None, strings);

        let indices = &anim.resource_index;
        let group = groups.get(indices.resource_group.0 as usize);
        let group_member = if let Some(group) = group {
            let group_members = &group.tag_resource.data.group_members.elements;
            let group_member = group_members.get(indices.resource_member_index.0 as usize);
            if let Some(group_member) = group_member {
                group_member
            } else {
                return Ok(());
            }
        } else {
            return Ok(());
        };

        let (static_data, anim_data, static_inf, animated_inf) =
            process_codecs(group_member, anim.frame_count.0)?;
        let (qts, trs, scl) = construct_data(
            static_data,
            anim_data,
            static_inf,
            animated_inf,
            &render_model,
            &animation_graph,
            anim.frame_count.0,
        );
        /*
        let frames = create_frames(
            qts,
            trs,
            scl,
            render_model.nodes.size as u32,
            anim.frame_count.0,
        );

        export_animation(
            anim.name.0,
            render_model.any_tag.internal_struct.tag_id,
            animation_graph.any_tag.internal_struct.tag_id,
            &frames,
            &render_model.nodes.elements,
            &animation_graph.skeleton_bones.elements,
            &strings,
            &save_path,
        )?;*/
    }
    Ok(())
}

pub fn extract_animations(
    modules: &mut [ModuleFile],
    strings: &HashMap<i32, String>,
    anim_tags: &HashMap<i32, AnimationGraph>,
    hlmt_tags: &HashMap<i32, ModelDefinition>,
    mode_tags: &HashMap<(usize, usize, i32), RenderModel>,
    save_path: &str,
) -> Result<()> {
    let mut save_paths = PathBuf::from(save_path);
    save_paths.push("anims/");
    create_dir_all(&save_paths)?;
    for (id, hlmt) in hlmt_tags {
        let mode = mode_tags
            .iter()
            .find(|x| x.1.any_tag.internal_struct.tag_id == hlmt.render_model.global_id);
        let anim_tag = anim_tags.get(&hlmt.animation.global_id);
        if let Some(anim_tag) = anim_tag
            && let Some(mode) = mode
        {
            process_animations(anim_tag, mode.1, save_path, strings)?;
        }
    }

    Ok(())
}
