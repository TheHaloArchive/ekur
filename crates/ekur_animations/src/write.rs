use std::{
    fs::File,
    io::{BufWriter, Write},
    path::Path,
};

use crate::{
    NodeTransform, Skeleton,
    compose::{advance_movement, compose_frame_bone},
    datatypes::{
        jma_kind::JmaKind, movement::MovementData, quaternion::Quaternion, vector::Vector3,
    },
};
use anyhow::Result;
use byteorder::{LE, WriteBytesExt};
use ekur_definitions::animations::MovementDataType;

fn write_transform(writer: &mut impl Write, t: NodeTransform) -> Result<()> {
    let p = t.translation;
    write_f32_slice(writer, &[p.x, p.y, p.z])?;

    let q = t.rotation;
    write_f32_slice(writer, &[q.w, q.x, q.y, q.z])?;
    write_f32_slice(writer, &[t.scale])?;
    Ok(())
}

fn write_f32_slice(writer: &mut impl Write, values: &[f32]) -> Result<()> {
    for &v in values {
        let normalized = if v == -0.0 { 0.0 } else { v };
        writer.write_f32::<LE>(normalized)?;
    }
    Ok(())
}

fn write_string(writer: &mut impl Write, s: &str) -> Result<()> {
    let bytes = s.as_bytes();
    writer.write_u32::<LE>(bytes.len() as u32)?;
    writer.write_all(bytes)?;
    Ok(())
}

pub fn write_animation(
    path: &Path,
    skeleton: &Skeleton,
    codec_frames: &[Vec<NodeTransform>],
    leading: &[NodeTransform],
    kind: JmaKind,
    movement: &MovementData,
) -> Result<()> {
    let codec_count = codec_frames.len();
    let total_frames = codec_count
        + if kind.appends_held_frame() && codec_count > 0 {
            1
        } else {
            0
        };

    let mut file = File::create(path)?;
    let mut writer = BufWriter::new(&mut file);
    writer.write_u32::<LE>(total_frames as u32)?;
    writer.write_u32::<LE>(skeleton.nodes.len() as u32)?;
    writer.write_u8(kind.prepends_rest_pose() as u8)?;

    for node in &skeleton.nodes {
        write_string(&mut writer, &node.name)?;
        writer.write_i16::<LE>(node.first_child)?;
        writer.write_i16::<LE>(node.next_sibling)?;
    }

    if kind.prepends_rest_pose() {
        for transform in leading {
            write_transform(&mut writer, *transform)?;
        }
    }

    if codec_count == 0 {
        writer.flush()?;
        return Ok(());
    }

    let mut accumulated_translation = Vector3::default();
    let mut accumulated_rotation = Quaternion::IDENTITY;
    let absolute = movement.kind == MovementDataType::XYZAbsolute;

    for (frame_idx, frame) in codec_frames.iter().enumerate() {
        for (bone_idx, transform) in frame.iter().enumerate() {
            let composed = compose_frame_bone(
                *transform,
                bone_idx,
                accumulated_translation,
                accumulated_rotation,
                kind,
            );
            write_transform(&mut writer, composed)?;
        }

        if kind.folds_movement()
            && let Some(local) = movement.frames.get(frame_idx)
        {
            advance_movement(
                &mut accumulated_translation,
                &mut accumulated_rotation,
                local,
                absolute,
            );
        }
    }

    if kind.appends_held_frame() {
        let last_idx = codec_count - 1;
        for (bone_idx, transform) in codec_frames[last_idx].iter().enumerate() {
            let composed = compose_frame_bone(
                *transform,
                bone_idx,
                accumulated_translation,
                accumulated_rotation,
                kind,
            );
            write_transform(&mut writer, composed)?;
        }
    }

    writer.flush()?;
    Ok(())
}
