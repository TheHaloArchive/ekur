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
}
