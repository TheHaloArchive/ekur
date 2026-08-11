use crate::{
    NodeTransform, Skeleton, TrackSource,
    codecs::Codec,
    datatypes::{
        flag_data::FlagData, jma_kind::JmaKind, movement::MovementFrame, quaternion::Quaternion,
        vector::Vector3,
    },
    resolve_bones,
};

pub fn advance_movement(
    translation: &mut Vector3,
    rotation: &mut Quaternion,
    local: &MovementFrame,
    absolute: bool,
) {
    if absolute {
        translation.x = local.dx;
        translation.y = local.dy;
        translation.z = local.dz;
        return;
    }
    let world = rotation.rotate(Vector3 {
        x: local.dx,
        y: local.dy,
        z: local.dz,
    });
    translation.x += world.x;
    translation.y += world.y;
    translation.z += world.z;
    *rotation = (*rotation * local.rotation).normalized();
}

pub fn compose_frame_bone(
    transform: NodeTransform,
    bone_idx: usize,
    accumulated_translation: Vector3,
    accumulated_rotation: Quaternion,
    kind: JmaKind,
) -> NodeTransform {
    let mut t = transform.translation;
    let mut q = transform.rotation;

    if kind.folds_movement() && bone_idx == 0 {
        t = Vector3 {
            x: t.x + accumulated_translation.x,
            y: t.y + accumulated_translation.y,
            z: t.z + accumulated_translation.z,
        };
        q = accumulated_rotation * q;
    }

    NodeTransform {
        translation: t,
        rotation: q,
        scale: transform.scale,
    }
}

fn frame_index(len: usize, frame: usize) -> usize {
    if len == 0 { 0 } else { frame.min(len - 1) }
}

fn pick_rotation(
    codec: &Codec,
    source: TrackSource,
    frame: usize,
    default: Quaternion,
) -> Quaternion {
    match source {
        TrackSource::Static(i) => codec
            .rotations
            .get(i)
            .and_then(|v| v.first())
            .copied()
            .unwrap_or(default),
        TrackSource::Animated(i) => codec
            .rotations
            .get(i)
            .and_then(|v| v.get(frame_index(v.len(), frame)))
            .copied()
            .unwrap_or(default),
        TrackSource::Identity => default,
    }
}

fn pick_translation(codec: &Codec, source: TrackSource, frame: usize, default: Vector3) -> Vector3 {
    match source {
        TrackSource::Static(i) => codec
            .translations
            .get(i)
            .and_then(|v| v.first())
            .copied()
            .unwrap_or(default),
        TrackSource::Animated(i) => codec
            .translations
            .get(i)
            .and_then(|v| v.get(frame_index(v.len(), frame)))
            .copied()
            .unwrap_or(default),
        TrackSource::Identity => default,
    }
}

fn pick_scale(codec: &Codec, source: TrackSource, frame: usize, default: f32) -> f32 {
    match source {
        TrackSource::Static(i) => codec
            .scales
            .get(i)
            .and_then(|v| v.first())
            .copied()
            .unwrap_or(default),
        TrackSource::Animated(i) => codec
            .scales
            .get(i)
            .and_then(|v| v.get(frame_index(v.len(), frame)))
            .copied()
            .unwrap_or(default),
        TrackSource::Identity => default,
    }
}

pub fn compose_pose(
    skeleton: &Skeleton,
    static_codec: &Codec,
    animated_codec: &Codec,
    static_flags: &FlagData,
    animated_flags: &FlagData,
    defaults: &[NodeTransform],
    frame_count: usize,
) -> Vec<Vec<NodeTransform>> {
    let bones = skeleton.nodes.len();
    let resolutions = resolve_bones(bones, static_flags, animated_flags);

    let frames_n = frame_count.max(1);
    let mut frames = Vec::with_capacity(frames_n);
    for f in 0..frames_n {
        let mut row = Vec::with_capacity(bones);
        for (b, res) in resolutions.iter().enumerate() {
            let default = defaults.get(b).copied().unwrap_or(NodeTransform::IDENTITY);
            let rotation = match res.rotation {
                TrackSource::Animated(_) => {
                    pick_rotation(animated_codec, res.rotation, f, default.rotation)
                }
                _ => pick_rotation(static_codec, res.rotation, 0, default.rotation),
            };
            let translation = match res.translation {
                TrackSource::Animated(_) => {
                    pick_translation(animated_codec, res.translation, f, default.translation)
                }
                _ => pick_translation(static_codec, res.translation, 0, default.translation),
            };
            let scale = match res.scale {
                TrackSource::Animated(_) => pick_scale(animated_codec, res.scale, f, default.scale),
                _ => pick_scale(static_codec, res.scale, 0, default.scale),
            };
            row.push(NodeTransform {
                rotation,
                translation,
                scale,
            });
        }
        frames.push(row);
    }
    frames
}

pub fn compose_overlay(
    skeleton: &Skeleton,
    static_codec: &Codec,
    animated_codec: &Codec,
    static_flags: &FlagData,
    animated_flags: &FlagData,
    defaults: &[NodeTransform],
    frame_count: usize,
) -> (Vec<NodeTransform>, Vec<Vec<NodeTransform>>) {
    let bones = skeleton.nodes.len();
    let resolutions = resolve_bones(bones, static_flags, animated_flags);

    let reference: Vec<NodeTransform> = resolutions
        .iter()
        .enumerate()
        .map(|(b, res)| {
            let default = defaults.get(b).copied().unwrap_or(NodeTransform::IDENTITY);
            NodeTransform {
                rotation: match res.rotation {
                    TrackSource::Static(_) => {
                        pick_rotation(static_codec, res.rotation, 0, default.rotation)
                    }
                    _ => default.rotation,
                },
                translation: match res.translation {
                    TrackSource::Static(_) => {
                        pick_translation(static_codec, res.translation, 0, default.translation)
                    }
                    _ => default.translation,
                },
                scale: match res.scale {
                    TrackSource::Static(_) => pick_scale(static_codec, res.scale, 0, default.scale),
                    _ => default.scale,
                },
            }
        })
        .collect();

    let frames_n = frame_count.max(1);
    let mut frames = Vec::with_capacity(frames_n);
    for f in 0..frames_n {
        let mut row = Vec::with_capacity(bones);
        for (b, res) in resolutions.iter().enumerate() {
            let r = reference[b];
            let rotation = match res.rotation {
                TrackSource::Animated(_) => {
                    let delta =
                        pick_rotation(animated_codec, res.rotation, f, Quaternion::IDENTITY);
                    r.rotation * delta
                }
                _ => r.rotation,
            };
            let translation = match res.translation {
                TrackSource::Animated(_) => {
                    let d =
                        pick_translation(animated_codec, res.translation, f, Vector3::default());
                    Vector3 {
                        x: r.translation.x + d.x,
                        y: r.translation.y + d.y,
                        z: r.translation.z + d.z,
                    }
                }
                _ => r.translation,
            };
            let scale = match res.scale {
                TrackSource::Animated(_) => r.scale * pick_scale(animated_codec, res.scale, f, 1.0),
                _ => r.scale,
            };
            row.push(NodeTransform {
                rotation,
                translation,
                scale,
            });
        }
        frames.push(row);
    }

    (reference, frames)
}

pub fn compose_replacement(
    skeleton: &Skeleton,
    animated_codec: &Codec,
    animated_flags_only: &FlagData,
    defaults: &[NodeTransform],
    frame_count: usize,
) -> Vec<Vec<NodeTransform>> {
    let bones = skeleton.nodes.len();
    let empty = FlagData::default();
    let resolutions = resolve_bones(bones, &empty, animated_flags_only);

    let frames_n = frame_count.max(1);
    let mut frames = Vec::with_capacity(frames_n);
    for f in 0..frames_n {
        let mut row = Vec::with_capacity(bones);
        for (b, res) in resolutions.iter().enumerate() {
            let default = defaults.get(b).copied().unwrap_or(NodeTransform::IDENTITY);
            let rotation = match res.rotation {
                TrackSource::Animated(_) => {
                    pick_rotation(animated_codec, res.rotation, f, default.rotation)
                }
                _ => default.rotation,
            };
            let translation = match res.translation {
                TrackSource::Animated(_) => {
                    pick_translation(animated_codec, res.translation, f, default.translation)
                }
                _ => default.translation,
            };
            let scale = match res.scale {
                TrackSource::Animated(_) => pick_scale(animated_codec, res.scale, f, default.scale),
                _ => default.scale,
            };
            row.push(NodeTransform {
                rotation,
                translation,
                scale,
            });
        }
        frames.push(row);
    }
    frames
}
