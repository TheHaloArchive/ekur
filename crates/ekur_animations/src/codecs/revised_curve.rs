use std::io::{Read, Seek, SeekFrom};

use anyhow::Result;

use byteorder::{LE, ReadBytesExt};

use crate::{
    codecs::{Codec, CodecHeader},
    datatypes::{quaternion::Quaternion, vector::Vector3},
};

#[derive(Default, Debug)]
pub struct RevisedCurve {
    pub header: CodecHeader,
    pub translation_data_offset: u32,
    pub scale_data_offset: u32,
    pub payload_data_offset: u32,
    pub frame_count: i16,
    pub rotations: Vec<Vec<Quaternion>>,
    pub translations: Vec<Vec<Vector3>>,
    pub scales: Vec<Vec<f32>>,
}

fn read_curve_keyframe_deltas(mut reader: impl Seek + Read, key_count: u16) -> Result<Vec<u32>> {
    let mut keyframes = Vec::with_capacity(key_count as usize + 1);
    keyframes.push(0u32);
    let mut total = 0u32;
    for _ in 0..key_count {
        total = total.saturating_add(reader.read_u8()? as u32);
        keyframes.push(total);
    }
    Ok(keyframes)
}

fn curve_tangent_scalar(tangent_signed: i32, p1: f32, p2: f32) -> f32 {
    let t = tangent_signed as f32 / 7.0;
    t.abs() * (t * 0.3) + (p2 - p1)
}

fn curve_tangent_quat(
    it: i32,
    jt: i32,
    kt: i32,
    wt: i32,
    p1: Quaternion,
    p2: Quaternion,
) -> Quaternion {
    Quaternion {
        x: curve_tangent_scalar(it, p1.x, p2.x),
        y: curve_tangent_scalar(jt, p1.y, p2.y),
        z: curve_tangent_scalar(kt, p1.z, p2.z),
        w: curve_tangent_scalar(wt, p1.w, p2.w),
    }
}

fn curve_position_scalar(t: f32, tan1: f32, tan2: f32, p1: f32, p2: f32) -> f32 {
    let t2 = t * t;
    let t3 = t2 * t;
    let h1 = 2.0 * t3 - 3.0 * t2 + 1.0;
    let h2 = t3 - 2.0 * t2 + t;
    let h3 = 3.0 * t2 - 2.0 * t3;
    let h4 = t3 - t2;
    h1 * p1 + h2 * tan1 + h3 * p2 + h4 * tan2
}

fn curve_position_quat(
    t: f32,
    tan1: Quaternion,
    tan2: Quaternion,
    p1: Quaternion,
    p2: Quaternion,
) -> Quaternion {
    Quaternion {
        x: curve_position_scalar(t, tan1.x, tan2.x, p1.x, p2.x),
        y: curve_position_scalar(t, tan1.y, tan2.y, p1.y, p2.y),
        z: curve_position_scalar(t, tan1.z, tan2.z, p1.z, p2.z),
        w: curve_position_scalar(t, tan1.w, tan2.w, p1.w, p2.w),
    }
    .normalized()
}

fn curve_tangent_vec(xt: i32, yt: i32, zt: i32, p1: Vector3, p2: Vector3) -> Vector3 {
    Vector3 {
        x: curve_tangent_scalar(xt, p1.x, p2.x),
        y: curve_tangent_scalar(yt, p1.y, p2.y),
        z: curve_tangent_scalar(zt, p1.z, p2.z),
    }
}

fn curve_position_vec(t: f32, tan1: Vector3, tan2: Vector3, p1: Vector3, p2: Vector3) -> Vector3 {
    Vector3 {
        x: curve_position_scalar(t, tan1.x, tan2.x, p1.x, p2.x),
        y: curve_position_scalar(t, tan1.y, tan2.y, p1.y, p2.y),
        z: curve_position_scalar(t, tan1.z, tan2.z, p1.z, p2.z),
    }
}

fn read_curve_translation_node(mut c: impl Seek + Read, frames: i16) -> Result<Vec<Vector3>> {
    c.read_u16::<LE>()?; // unused
    let key_count = c.read_u16::<LE>()?;
    let flags = c.read_u8()?;
    c.read_u8()?; // unused
    c.read_u16::<LE>()?; // unused
    let offset_x = c.read_f32::<LE>()?;
    let offset_y = c.read_f32::<LE>()?;
    let offset_z = c.read_f32::<LE>()?;
    let scale = c.read_f32::<LE>()?;
    let keyframes = if flags & 1 == 0 {
        read_curve_keyframe_deltas(&mut c, key_count)?
    } else {
        Vec::new()
    };

    let mut out = Vec::with_capacity(frames as usize);
    let mut p1 = Vector3::default();
    let mut p2 = Vector3::default();
    let mut tangent_bytes = [0u8; 3];
    let mut current_kf = 0u32;
    let mut next_kf = 0u32;
    let mut keyframe_index = 0usize;
    for frame_index in 0..frames as u32 {
        let v = if flags & 1 != 0 {
            Vector3 {
                x: c.read_i16::<LE>()? as f32 / i16::MAX as f32,
                y: c.read_i16::<LE>()? as f32 / i16::MAX as f32,
                z: c.read_i16::<LE>()? as f32 / i16::MAX as f32,
            }
        } else {
            if keyframe_index < keyframes.len()
                && keyframes[keyframe_index] == frame_index
                && frame_index < frames as u32 - 1
            {
                let x1 = c.read_i16::<LE>()? as f32 / i16::MAX as f32;
                let y1 = c.read_i16::<LE>()? as f32 / i16::MAX as f32;
                let z1 = c.read_i16::<LE>()? as f32 / i16::MAX as f32;
                tangent_bytes = [c.read_u8()?, c.read_u8()?, c.read_u8()?];
                let x2 = c.read_i16::<LE>()? as f32 / i16::MAX as f32;
                let y2 = c.read_i16::<LE>()? as f32 / i16::MAX as f32;
                let z2 = c.read_i16::<LE>()? as f32 / i16::MAX as f32;
                p1 = Vector3 {
                    x: x1,
                    y: y1,
                    z: z1,
                };
                p2 = Vector3 {
                    x: x2,
                    y: y2,
                    z: z2,
                };
                current_kf = keyframes[keyframe_index];
                next_kf = keyframes
                    .get(keyframe_index + 1)
                    .copied()
                    .unwrap_or(current_kf + 1);
                keyframe_index += 1;
                c.seek_relative(-6)?;
            }
            let span = (next_kf.saturating_sub(current_kf) as f32).max(1.0);
            let t = (frame_index.saturating_sub(current_kf) as f32) / span;
            let tan1 = curve_tangent_vec(
                ((tangent_bytes[0] >> 4) as i32) - 7,
                ((tangent_bytes[1] >> 4) as i32) - 7,
                ((tangent_bytes[2] >> 4) as i32) - 7,
                p1,
                p2,
            );
            let tan2 = curve_tangent_vec(
                ((tangent_bytes[0] & 0x0F) as i32) - 7,
                ((tangent_bytes[1] & 0x0F) as i32) - 7,
                ((tangent_bytes[2] & 0x0F) as i32) - 7,
                p1,
                p2,
            );
            curve_position_vec(t, tan1, tan2, p1, p2)
        };
        out.push(Vector3 {
            x: scale * v.x + offset_x,
            y: scale * v.y + offset_y,
            z: scale * v.z + offset_z,
        });
    }
    Ok(out)
}

fn read_curve_scale_node(mut c: impl Seek + Read, frames: i16) -> Result<Vec<f32>> {
    c.read_u16::<LE>()?;
    let key_count = c.read_u16::<LE>()?;
    let flags = c.read_u8()?;
    c.read_u8()?;
    c.read_u16::<LE>()?;
    let offset = c.read_f32::<LE>()?;
    let scale = c.read_f32::<LE>()?;
    let keyframes = if flags & 1 == 0 {
        read_curve_keyframe_deltas(&mut c, key_count)?
    } else {
        Vec::new()
    };

    let mut out = Vec::with_capacity(frames as usize);
    let mut p1 = 0.0f32;
    let mut p2 = 0.0f32;
    let mut tangent_byte = 0u8;
    let mut current_kf = 0u32;
    let mut next_kf = 0u32;
    let mut keyframe_index = 0usize;
    for frame_index in 0..frames as u32 {
        let v = if flags & 1 != 0 {
            c.read_i16::<LE>()? as f32 / i16::MAX as f32
        } else {
            if keyframe_index < keyframes.len()
                && keyframes[keyframe_index] == frame_index
                && frame_index < frames as u32 - 1
            {
                p1 = c.read_i16::<LE>()? as f32 / i16::MAX as f32;
                tangent_byte = c.read_u8()?;
                p2 = c.read_i16::<LE>()? as f32 / i16::MAX as f32;
                current_kf = keyframes[keyframe_index];
                next_kf = keyframes
                    .get(keyframe_index + 1)
                    .copied()
                    .unwrap_or(current_kf + 1);
                keyframe_index += 1;
                c.seek_relative(-2)?;
            }
            let span = (next_kf.saturating_sub(current_kf) as f32).max(1.0);
            let t = (frame_index.saturating_sub(current_kf) as f32) / span;
            let tan1 = curve_tangent_scalar(((tangent_byte >> 4) as i32) - 7, p1, p2);
            let tan2 = curve_tangent_scalar(((tangent_byte & 0x0F) as i32) - 7, p1, p2);
            curve_position_scalar(t, tan1, tan2, p1, p2)
        };
        out.push(v * scale + offset);
    }
    Ok(out)
}

fn read_curve_rotation_node(mut c: impl Seek + Read, frames: i16) -> Result<Vec<Quaternion>> {
    c.read_u16::<LE>()?; // unused
    let key_count = c.read_u16::<LE>()?;
    let flags = c.read_u8()?;
    c.read_u8()?; // unused
    c.read_i16::<LE>()?; // unused
    let keyframes = if flags & 1 == 0 {
        read_curve_keyframe_deltas(&mut c, key_count)?
    } else {
        Vec::new()
    };

    let mut out = Vec::with_capacity(frames as usize);
    let mut p1 = Quaternion::IDENTITY;
    let mut p2 = Quaternion::IDENTITY;
    let mut tangent_bytes = [0u8; 4];
    let mut current_kf = 0u32;
    let mut next_kf = 0u32;
    let mut keyframe_index = 0usize;
    for frame_index in 0..frames as u32 {
        let q = if flags & 1 != 0 {
            Quaternion::decompress_revised_quat(&mut c)?
        } else {
            if keyframe_index < keyframes.len()
                && keyframes[keyframe_index] == frame_index
                && frame_index < frames as u32 - 1
            {
                p1 = Quaternion::decompress_revised_quat(&mut c)?;
                tangent_bytes = [c.read_u8()?, c.read_u8()?, c.read_u8()?, c.read_u8()?];
                p2 = Quaternion::decompress_revised_quat(&mut c)?;
                current_kf = keyframes[keyframe_index];
                next_kf = keyframes
                    .get(keyframe_index + 1)
                    .copied()
                    .unwrap_or(current_kf + 1);
                keyframe_index += 1;
                c.seek_relative(-6)?; // p2 becomes next segment's p1
            }
            let span = (next_kf.saturating_sub(current_kf) as f32).max(1.0);
            let t = (frame_index.saturating_sub(current_kf) as f32) / span;
            let tan1 = curve_tangent_quat(
                ((tangent_bytes[0] >> 4) as i32) - 7,
                ((tangent_bytes[1] >> 4) as i32) - 7,
                ((tangent_bytes[2] >> 4) as i32) - 7,
                ((tangent_bytes[3] >> 4) as i32) - 7,
                p1,
                p2,
            );
            let tan2 = curve_tangent_quat(
                ((tangent_bytes[0] & 0x0F) as i32) - 7,
                ((tangent_bytes[1] & 0x0F) as i32) - 7,
                ((tangent_bytes[2] & 0x0F) as i32) - 7,
                ((tangent_bytes[3] & 0x0F) as i32) - 7,
                p1,
                p2,
            );
            curve_position_quat(t, tan1, tan2, p1, p2)
        };
        out.push(q);
    }
    Ok(out)
}

impl RevisedCurve {
    pub fn from_reader(mut reader: impl Seek + Read, frame_count: i16) -> Result<Self> {
        reader.seek_relative(2)?;
        let header = CodecHeader::read(&mut reader)?;
        let mut curve = Self {
            header,
            frame_count,
            translation_data_offset: reader.read_u32::<LE>()?,
            scale_data_offset: reader.read_u32::<LE>()?,
            payload_data_offset: reader.read_u32::<LE>()?,
            rotations: Vec::new(),
            translations: Vec::new(),
            scales: Vec::new(),
        };
        reader.seek_relative(8)?;
        curve.process(&mut reader)?;
        Ok(curve)
    }

    fn process(&mut self, mut reader: impl Read + Seek) -> Result<()> {
        let mut rotation_offsets = Vec::new();
        for _ in 0..self.header.rotated_node_count {
            rotation_offsets.push(reader.read_u32::<LE>()?);
        }

        let mut rotations = Vec::with_capacity(self.header.rotated_node_count as usize);
        let mut translations = Vec::with_capacity(self.header.translated_node_count as usize);
        let mut scales = Vec::with_capacity(self.header.scaled_node_count as usize);

        for &node_off in &rotation_offsets {
            reader.seek(std::io::SeekFrom::Start(
                self.payload_data_offset as u64 + node_off as u64,
            ))?;
            rotations.push(read_curve_rotation_node(&mut reader, self.frame_count)?);
        }

        if self.header.translated_node_count > 0 {
            reader.seek(SeekFrom::Start(
                self.payload_data_offset as u64 + self.translation_data_offset as u64,
            ))?;
            let mut trans_offsets = Vec::with_capacity(self.header.translated_node_count as usize);
            for _ in 0..self.header.translated_node_count {
                trans_offsets.push(reader.read_u32::<LE>()? as usize);
            }
            for &node_off in &trans_offsets {
                reader.seek(SeekFrom::Start(
                    self.payload_data_offset as u64 + node_off as u64,
                ))?;
                translations.push(read_curve_translation_node(&mut reader, self.frame_count)?);
            }
        }

        if self.header.scaled_node_count > 0 {
            reader.seek(SeekFrom::Start(
                self.payload_data_offset as u64 + self.scale_data_offset as u64,
            ))?;
            let mut scale_offsets = Vec::with_capacity(self.header.scaled_node_count as usize);
            for _ in 0..self.header.scaled_node_count {
                scale_offsets.push(reader.read_u32::<LE>()? as usize);
            }
            for &node_off in &scale_offsets {
                reader.seek(SeekFrom::Start(
                    self.payload_data_offset as u64 + node_off as u64,
                ))?;
                scales.push(read_curve_scale_node(&mut reader, self.frame_count)?);
            }
        }

        self.scales = scales;
        self.rotations = rotations;
        self.translations = translations;

        Ok(())
    }

    pub fn into_codec(self) -> Codec {
        Codec {
            rotations: self.rotations,
            translations: self.translations,
            scales: self.scales,
        }
    }
}
