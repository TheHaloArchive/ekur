use std::io::{Cursor, Read, Seek, SeekFrom};

use anyhow::{Result, bail};
use bitvec::vec::BitVec;
use byteorder::{LE, ReadBytesExt};

use crate::{
    codecs::Codec,
    datatypes::{
        flag_data::{FlagData, bit_is_set},
        quaternion::Quaternion,
        vector::Vector3,
    },
};

const ACL_TAG: u32 = 0xac10_ac10;
const ALGORITHM_UNIFORMLY_SAMPLED: u8 = 0;
const UNIFORMLY_SAMPLED_VERSION: u16 = 5;
const ROTATION_FORMAT_VARIABLE: u8 = 4;
const VECTOR_FORMAT_VARIABLE: u8 = 3;
const INVALID_OFFSET_16: u16 = u16::MAX;
const TAG_SEARCH_LIMIT: usize = 256;
const COMPRESSED_CLIP_SIZE: usize = 16;

const BIT_RATE_NUM_BITS: [u8; 19] = [
    0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 32,
];
const RAW_BIT_RATE: u8 = 18;

const RANGE_ROTATIONS: u8 = 0x01;
const RANGE_TRANSLATIONS: u8 = 0x02;
const RANGE_SCALES: u8 = 0x04;

const NUM_COMPONENTS: usize = 3;
const PACKED_96_SIZE: usize = 12;

#[derive(Default, Debug, Clone, Copy)]
struct SegmentHeader {
    animated_pose_bit_size: u32,
    format_per_track_data_offset: u32,
    range_data_offset: u32,
    track_data_offset: u32,
}

impl SegmentHeader {
    fn read(reader: &mut impl Read) -> Result<Self> {
        Ok(Self {
            animated_pose_bit_size: reader.read_u32::<LE>()?,
            format_per_track_data_offset: reader.read_u32::<LE>()?,
            range_data_offset: reader.read_u32::<LE>()?,
            track_data_offset: reader.read_u32::<LE>()?,
        })
    }
}

#[derive(Default, Debug, Clone, Copy)]
struct ClipHeader {
    num_bones: u16,
    num_segments: u16,
    clip_range_reduction: u8,
    segment_range_reduction: u8,
    has_scale: bool,
    default_scale: f32,
    num_samples: u32,
    segment_start_indices_offset: u16,
    segment_headers_offset: u16,
    default_tracks_bitset_offset: u16,
    constant_tracks_bitset_offset: u16,
    constant_track_data_offset: u16,
    clip_range_data_offset: u16,
}

impl ClipHeader {
    fn read(reader: &mut impl Read) -> Result<Self> {
        let num_bones = reader.read_u16::<LE>()?;
        let num_segments = reader.read_u16::<LE>()?;
        let rotation_format = reader.read_u8()?;
        let translation_format = reader.read_u8()?;
        let scale_format = reader.read_u8()?;

        if rotation_format != ROTATION_FORMAT_VARIABLE
            || translation_format != VECTOR_FORMAT_VARIABLE
            || scale_format != VECTOR_FORMAT_VARIABLE
        {
            bail!("unsupported format");
        }

        let clip_range_reduction = reader.read_u8()?;
        let segment_range_reduction = reader.read_u8()?;
        let has_scale = reader.read_u8()? != 0;
        let default_scale = if reader.read_u8()? != 0 { 1.0 } else { 0.0 };
        reader.read_u8()?; // padding
        let num_samples = reader.read_u32::<LE>()?;
        reader.read_f32::<LE>()?; // sample rate

        Ok(Self {
            num_bones,
            num_segments,
            clip_range_reduction,
            segment_range_reduction,
            has_scale,
            default_scale,
            num_samples,
            segment_start_indices_offset: reader.read_u16::<LE>()?,
            segment_headers_offset: reader.read_u16::<LE>()?,
            default_tracks_bitset_offset: reader.read_u16::<LE>()?,
            constant_tracks_bitset_offset: reader.read_u16::<LE>()?,
            constant_track_data_offset: reader.read_u16::<LE>()?,
            clip_range_data_offset: reader.read_u16::<LE>()?,
        })
    }
}

#[derive(Default, Clone, Copy)]
struct Blocks {
    default_bitset: usize,
    constant_bitset: usize,
    constant_data: usize,
    clip_range: usize,
    animated: usize,
    formats: usize,
    ranges: usize,
}

#[derive(Default)]
struct TrackCursor {
    track_index: usize,
    constant_data: usize,
    clip_range: usize,
    format_per_track: usize,
    segment_range: usize,
    key_frame_bit: usize,
}

fn find_clip_offset(data: &[u8]) -> Option<usize> {
    let limit = TAG_SEARCH_LIMIT.min(data.len().saturating_sub(COMPRESSED_CLIP_SIZE));
    (0..=limit)
        .step_by(16)
        .find(|&offset| load_u32_le(data, offset + 8) == ACL_TAG)
}

fn load_u32_le(data: &[u8], byte_offset: usize) -> u32 {
    let mut buf = [0u8; 4];
    if byte_offset < data.len() {
        let end = (byte_offset + 4).min(data.len());
        buf[..end - byte_offset].copy_from_slice(&data[byte_offset..end]);
    }
    u32::from_le_bytes(buf)
}

fn load_u64_be(data: &[u8], byte_offset: usize) -> u64 {
    let mut buf = [0u8; 8];
    if byte_offset < data.len() {
        let end = (byte_offset + 8).min(data.len());
        buf[..end - byte_offset].copy_from_slice(&data[byte_offset..end]);
    }
    u64::from_be_bytes(buf)
}

fn vector3_from(mut component: impl FnMut(usize) -> f32) -> Vector3 {
    Vector3 {
        x: component(0),
        y: component(1),
        z: component(2),
    }
}

fn unpack_uxx(num_bits: usize, data: &[u8], bit_offset: usize) -> Vector3 {
    let mask = (1u64 << num_bits) - 1;
    let inv_max = 1.0 / mask as f32;
    vector3_from(|index| {
        let offset = bit_offset + index * num_bits;
        let word = load_u64_be(data, offset / 8) >> (64 - num_bits - (offset % 8));
        (word & mask) as f32 * inv_max
    })
}

fn unpack_96_at_bit(data: &[u8], bit_offset: usize) -> Vector3 {
    let byte_offset = bit_offset / 8;
    let shift = bit_offset % 8;
    vector3_from(|index| {
        let word = load_u64_be(data, byte_offset + index * 4);
        f32::from_bits(((word << shift) >> 32) as u32)
    })
}

fn unpack_96(data: &[u8], byte_offset: usize) -> Vector3 {
    vector3_from(|index| f32::from_bits(load_u32_le(data, byte_offset + index * 4)))
}

fn unpack_u48(data: &[u8], byte_offset: usize) -> Vector3 {
    vector3_from(|index| {
        let at = byte_offset + index * 2;
        let low = data.get(at).copied().unwrap_or(0) as u16;
        let high = data.get(at + 1).copied().unwrap_or(0) as u16;
        (low | (high << 8)) as f32 / 65535.0
    })
}

fn unpack_u24(data: &[u8], byte_offset: usize) -> Vector3 {
    vector3_from(|index| data.get(byte_offset + index).copied().unwrap_or(0) as f32 / 255.0)
}

fn bitset_test(data: &[u8], word_offset: usize, bit_index: usize) -> bool {
    let word = load_u32_le(data, word_offset + (bit_index / 32) * 4);
    word & (0x8000_0000u32 >> (bit_index % 32)) != 0
}

fn select_tracks<T: Copy>(
    tracks: &[Vec<T>],
    bits: &BitVec<u8>,
    frames: usize,
    fallback: T,
) -> Vec<Vec<T>> {
    tracks
        .iter()
        .enumerate()
        .filter(|(bone, _)| bit_is_set(bits, *bone))
        .map(|(_, track)| {
            (0..frames)
                .map(|frame| {
                    track
                        .get(frame.min(track.len().saturating_sub(1)))
                        .copied()
                        .unwrap_or(fallback)
                })
                .collect()
        })
        .collect()
}

#[derive(Default, Debug)]
pub struct AnimationCompressionLibrary {
    header: ClipHeader,
    segments: Vec<SegmentHeader>,
    rotations: Vec<Vec<Quaternion>>,
    translations: Vec<Vec<Vector3>>,
    scales: Vec<Vec<f32>>,
}

impl AnimationCompressionLibrary {
    pub fn from_bytes(data: &[u8]) -> Result<Self> {
        let Some(clip_offset) = find_clip_offset(data) else {
            bail!("could not find an ACL compressed clip tag in the codec blob");
        };

        let mut reader = Cursor::new(data);
        reader.seek(SeekFrom::Start(clip_offset as u64 + 12))?;
        let version = reader.read_u16::<LE>()?;
        let algorithm = reader.read_u8()?;
        if version != UNIFORMLY_SAMPLED_VERSION || algorithm != ALGORITHM_UNIFORMLY_SAMPLED {
            bail!("unsupported ACL clip: version {version} algorithm {algorithm}");
        }
        reader.read_u8()?; // padding

        let base = clip_offset + COMPRESSED_CLIP_SIZE;
        let mut acl = Self {
            header: ClipHeader::read(&mut reader)?,
            ..Default::default()
        };

        if acl.header.segment_headers_offset != INVALID_OFFSET_16 {
            reader.seek(SeekFrom::Start(
                (base + acl.header.segment_headers_offset as usize) as u64,
            ))?;
            for _ in 0..acl.header.num_segments {
                acl.segments.push(SegmentHeader::read(&mut reader)?);
            }
        }

        acl.decode(data, base);
        Ok(acl)
    }

    fn decode(&mut self, data: &[u8], base: usize) {
        let header = self.header;
        let num_samples = header.num_samples as usize;
        let segment_starts = self.segment_start_indices(data, base);

        let mut blocks = Blocks {
            default_bitset: base + header.default_tracks_bitset_offset as usize,
            constant_bitset: base + header.constant_tracks_bitset_offset as usize,
            constant_data: base + header.constant_track_data_offset as usize,
            clip_range: base + header.clip_range_data_offset as usize,
            ..Default::default()
        };

        let bones = header.num_bones as usize;
        let mut rotations = vec![Vec::with_capacity(num_samples); bones];
        let mut translations = vec![Vec::with_capacity(num_samples); bones];
        let mut scales = vec![Vec::with_capacity(num_samples); bones];

        for frame in 0..num_samples {
            let segment_index = segment_starts
                .iter()
                .rposition(|&start| start as usize <= frame)
                .unwrap_or(0);
            let Some(segment) = self.segments.get(segment_index) else {
                break;
            };

            blocks.animated = base + segment.track_data_offset as usize;
            blocks.formats = base + segment.format_per_track_data_offset as usize;
            blocks.ranges = base + segment.range_data_offset as usize;

            let sample = frame - segment_starts[segment_index] as usize;
            let mut cursor = TrackCursor {
                key_frame_bit: sample * segment.animated_pose_bit_size as usize,
                ..Default::default()
            };

            for bone in 0..bones {
                let rotation = self.sample(data, &mut cursor, &blocks, RANGE_ROTATIONS);
                rotations[bone]
                    .push(rotation.map_or(Quaternion::IDENTITY, Quaternion::from_dropped_w));

                let translation = self.sample(data, &mut cursor, &blocks, RANGE_TRANSLATIONS);
                translations[bone].push(translation.unwrap_or_default());

                scales[bone].push(if header.has_scale {
                    self.sample(data, &mut cursor, &blocks, RANGE_SCALES)
                        .map_or(header.default_scale, |value| value.x)
                } else {
                    1.0
                });
            }
        }

        self.rotations = rotations;
        self.translations = translations;
        self.scales = scales;
    }

    fn sample(
        &self,
        data: &[u8],
        cursor: &mut TrackCursor,
        blocks: &Blocks,
        range_flag: u8,
    ) -> Option<Vector3> {
        let track = cursor.track_index;
        cursor.track_index += 1;

        if bitset_test(data, blocks.default_bitset, track) {
            return None;
        }
        if bitset_test(data, blocks.constant_bitset, track) {
            let value = unpack_96(data, blocks.constant_data + cursor.constant_data);
            cursor.constant_data += PACKED_96_SIZE;
            return Some(value);
        }
        Some(self.decode_animated(data, cursor, blocks, range_flag))
    }

    fn decode_animated(
        &self,
        data: &[u8],
        cursor: &mut TrackCursor,
        blocks: &Blocks,
        range_flag: u8,
    ) -> Vector3 {
        let bit_rate = data
            .get(blocks.formats + cursor.format_per_track)
            .copied()
            .unwrap_or(0);
        cursor.format_per_track += 1;
        let num_bits = BIT_RATE_NUM_BITS
            .get(bit_rate as usize)
            .copied()
            .unwrap_or(0) as usize;

        let (mut value, skip_segment, skip_clip) = if bit_rate == 0 {
            (
                unpack_u48(data, blocks.ranges + cursor.segment_range),
                true,
                false,
            )
        } else if bit_rate == RAW_BIT_RATE {
            (
                unpack_96_at_bit(data, blocks.animated * 8 + cursor.key_frame_bit),
                true,
                true,
            )
        } else if num_bits == 0 {
            (Vector3::default(), true, true)
        } else {
            (
                unpack_uxx(num_bits, data, blocks.animated * 8 + cursor.key_frame_bit),
                false,
                false,
            )
        };
        cursor.key_frame_bit += num_bits * NUM_COMPONENTS;

        if self.header.segment_range_reduction & range_flag != 0 {
            if !skip_segment {
                let at = blocks.ranges + cursor.segment_range;
                value = value.mul_add(unpack_u24(data, at + NUM_COMPONENTS), unpack_u24(data, at));
            }
            cursor.segment_range += NUM_COMPONENTS * 2;
        }

        if self.header.clip_range_reduction & range_flag != 0 {
            if !skip_clip {
                let at = blocks.clip_range + cursor.clip_range;
                value = value.mul_add(unpack_96(data, at + PACKED_96_SIZE), unpack_96(data, at));
            }
            cursor.clip_range += PACKED_96_SIZE * 2;
        }

        value
    }

    fn segment_start_indices(&self, data: &[u8], base: usize) -> Vec<u32> {
        let offset = self.header.segment_start_indices_offset;
        if self.header.num_segments <= 1 || offset == INVALID_OFFSET_16 {
            return vec![0];
        }
        (0..self.header.num_segments as usize)
            .map(|index| load_u32_le(data, base + offset as usize + index * 4))
            .collect()
    }

    pub fn into_codec_for(self, animated: &FlagData, frame_count: i16) -> Codec {
        let frames = frame_count.max(1) as usize;
        Codec {
            rotations: select_tracks(
                &self.rotations,
                &animated.rotation,
                frames,
                Quaternion::IDENTITY,
            ),
            translations: select_tracks(
                &self.translations,
                &animated.translation,
                frames,
                Vector3::default(),
            ),
            scales: select_tracks(&self.scales, &animated.scale, frames, 1.0),
        }
    }
}
