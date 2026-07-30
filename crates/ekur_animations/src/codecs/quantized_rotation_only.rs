use std::io::{BufReader, Cursor, Read, Seek};

use anyhow::Result;

use byteorder::{LE, ReadBytesExt};
use ekur_definitions::animations::CodecType;

use crate::{
    codecs::Codec,
    datatypes::{quaternion::Quaternion, vector::Vector3},
};

#[derive(Default, Debug)]
pub struct QuantizedRotationOnly {
    pub rotated_node_count: u16,
    pub translated_node_count: u16,
    pub scaled_node_count: u16,
    error_value: f32,
    compression_rate: f32,
    pub frame_count: i16,
    translation_data_offset: u32,
    scale_data_offset: u32,
    scaled_node_size: u32,
    translated_node_size: u32,
    rotated_node_size: u32,
    pub rotations: Vec<Vec<Quaternion>>,
    pub translations: Vec<Vec<Vector3>>,
    pub scales: Vec<Vec<f32>>,
    pub quat_8byte: bool,
}

impl QuantizedRotationOnly {
    pub fn from_reader(
        mut reader: impl Seek + Read,
        frame_count: i16,
        quat_8byte: bool,
    ) -> Result<Self> {
        reader.seek_relative(2)?;
        let mut qrot = Self::default();
        qrot.rotated_node_count = reader.read_u16::<LE>()?;
        qrot.translated_node_count = reader.read_u16::<LE>()?;
        qrot.scaled_node_count = reader.read_u16::<LE>()?;
        qrot.error_value = reader.read_f32::<LE>()?;
        qrot.compression_rate = reader.read_f32::<LE>()?;
        qrot.translation_data_offset = reader.read_u32::<LE>()?;
        qrot.scale_data_offset = reader.read_u32::<LE>()?;
        qrot.scaled_node_size = reader.read_u32::<LE>()?;
        qrot.translated_node_size = reader.read_u32::<LE>()?;
        qrot.rotated_node_size = reader.read_u32::<LE>()?;
        qrot.frame_count = frame_count;
        qrot.quat_8byte = quat_8byte;
        reader.seek_relative(12)?;
        qrot.process(&mut reader)?;
        Ok(qrot)
    }

    fn process(&mut self, reader: &mut (impl Read + Seek)) -> Result<()> {
        for _ in 0..self.rotated_node_count {
            let mut quat_list = Vec::new();
            for _ in 0..self.frame_count {
                if self.quat_8byte {
                    quat_list.push(Quaternion::from_quantized(reader)?);
                } else {
                    quat_list.push(Quaternion::from_reader(reader)?);
                }
            }
            self.rotations.push(quat_list);
        }
        for _ in 0..self.translated_node_count {
            let mut trans_list = Vec::new();
            for _ in 0..self.frame_count {
                trans_list.push(Vector3::from_reader(reader)?);
            }
            self.translations.push(trans_list);
        }
        for _ in 0..self.scaled_node_count {
            let mut scale_list = Vec::new();
            for _ in 0..self.frame_count {
                scale_list.push(reader.read_f32::<LE>()?);
            }
            self.scales.push(scale_list);
        }
        Ok(())
    }

    pub fn into_codec(self, codec_type: CodecType) -> Codec {
        Codec {
            rotations: self.rotations,
            translations: self.translations,
            scales: self.scales,
            codec_type: codec_type,
            frame_count: self.frame_count,
        }
    }
}
