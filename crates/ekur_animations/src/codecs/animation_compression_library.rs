use std::io::{Read, Seek};

use anyhow::Result;

use crate::{
    codecs::{Codec, CodecHeader},
    datatypes::{quaternion::Quaternion, vector::Vector3},
};

#[derive(Default, Debug)]
pub struct AnimationCompressionLibrary {
    pub _header: CodecHeader,
    pub _frame_count: i16,
    pub rotations: Vec<Vec<Quaternion>>,
    pub translations: Vec<Vec<Vector3>>,
    pub scales: Vec<Vec<f32>>,
}

impl AnimationCompressionLibrary {
    pub fn from_reader(mut reader: impl Seek + Read, frame_count: i16) -> Result<Self> {
        reader.seek_relative(2)?;
        let qrot = Self {
            _header: CodecHeader::read(&mut reader)?,
            _frame_count: frame_count,
            ..Default::default()
        };
        Ok(qrot)
    }

    pub fn into_codec(self) -> Codec {
        Codec {
            rotations: self.rotations,
            translations: self.translations,
            scales: self.scales,
        }
    }
}
