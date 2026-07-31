use std::io::{Read, Seek};

use anyhow::Result;

use byteorder::{LE, ReadBytesExt};

use crate::{
    codecs::Codec,
    datatypes::{quaternion::Quaternion, vector::Vector3},
};

#[derive(Default, Debug)]
pub struct QuantizedRotationOnly {
    pub rotated_node_count: u16,
    pub translated_node_count: u16,
    pub scaled_node_count: u16,
    _error_value: f32,
    _compression_rate: f32,
    pub frame_count: i16,
    _translation_data_offset: u32,
    _scale_data_offset: u32,
    _scaled_node_size: u32,
    _translated_node_size: u32,
    _rotated_node_size: u32,
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
        let mut qrot = Self {
            rotated_node_count: reader.read_u16::<LE>()?,
            translated_node_count: reader.read_u16::<LE>()?,
            scaled_node_count: reader.read_u16::<LE>()?,
            _error_value: reader.read_f32::<LE>()?,
            _compression_rate: reader.read_f32::<LE>()?,
            _translation_data_offset: reader.read_u32::<LE>()?,
            _scale_data_offset: reader.read_u32::<LE>()?,
            _scaled_node_size: reader.read_u32::<LE>()?,
            _translated_node_size: reader.read_u32::<LE>()?,
            _rotated_node_size: reader.read_u32::<LE>()?,
            frame_count,
            quat_8byte,
            ..Default::default()
        };

        reader.seek_relative(12)?;
        qrot.process(&mut reader)?;
        Ok(qrot)
    }

    fn process(&mut self, reader: &mut (impl Read + Seek)) -> Result<()> {
        for _ in 0..self.rotated_node_count {
            let mut quat_list = Vec::new();
            for _ in 0..self.frame_count {
                let q = if self.quat_8byte {
                    Quaternion::from_quantized(reader)?
                } else {
                    Quaternion::from_reader(reader)?
                };
                quat_list.push(q.normalized());
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

    pub fn into_codec(self) -> Codec {
        Codec {
            rotations: self.rotations,
            translations: self.translations,
            scales: self.scales,
        }
    }
}
