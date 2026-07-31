use std::io::{Read, Seek};

use anyhow::Result;
use bitvec::vec::BitVec;

#[derive(Debug, Default)]
pub struct FlagData {
    pub rotation: BitVec<u8>,
    pub translation: BitVec<u8>,
    pub scale: BitVec<u8>,
}

impl FlagData {
    pub fn from_reader(mut reader: impl Seek + Read, size: u32) -> Result<Self> {
        let mut flags = Self::default();
        if size != 0 && (size as f32 / 3.0) >= 1.0 {
            let mut flag_buffer = vec![0; size as usize];
            reader.read_exact(&mut flag_buffer)?;
            let statics = flag_buffer.chunks(size as usize / 3).collect::<Vec<_>>();
            flags.rotation = BitVec::<u8>::from_slice(statics[0]);
            flags.translation = BitVec::<u8>::from_slice(statics[1]);
            flags.scale = BitVec::<u8>::from_slice(statics[2]);
        };
        Ok(flags)
    }

    pub fn from_slice(data: &[u8]) -> Self {
        let mut flags = Self::default();
        if !data.is_empty() && data.len().is_multiple_of(3) {
            let per = data.len() / 3;
            flags.rotation = BitVec::<u8>::from_slice(&data[0..per]);
            flags.translation = BitVec::<u8>::from_slice(&data[per..2 * per]);
            flags.scale = BitVec::<u8>::from_slice(&data[2 * per..3 * per]);
        }
        flags
    }
}

pub fn bit_is_set(bits: &BitVec<u8>, index: usize) -> bool {
    let bytes = bits.as_raw_slice();
    let byte_idx = index / 8;
    let bit_idx = index % 8;
    bytes
        .get(byte_idx)
        .map(|b| (b >> bit_idx) & 1 != 0)
        .unwrap_or(false)
}

pub fn popcount_below(bits: &BitVec<u8>, index: usize) -> usize {
    let bytes = bits.as_raw_slice();
    let full_bytes = index / 8;
    let mut count = 0usize;
    for &b in bytes.iter().take(full_bytes) {
        count += b.count_ones() as usize;
    }
    if let Some(&b) = bytes.get(full_bytes) {
        let rem = index % 8;
        if rem > 0 {
            let mask = ((1u32 << rem) - 1) as u8;
            count += (b & mask).count_ones() as usize;
        }
    }
    count
}
