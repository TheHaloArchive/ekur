use byteorder::{LE, ReadBytesExt};

use crate::datatypes::{quaternion::Quaternion, vector::Vector3};

pub mod animation_compression_library;
pub mod quantized_rotation_only;
pub mod revised_curve;
pub mod shared_static;

#[derive(Debug, Default)]
pub struct CodecHeader {
    pub rotated_node_count: u16,
    pub translated_node_count: u16,
    pub scaled_node_count: u16,
    _error_value: f32,
    _compression_rate: f32,
}

impl CodecHeader {
    pub fn read(reader: &mut impl std::io::Read) -> std::io::Result<Self> {
        let rotated_node_count = reader.read_u16::<LE>()?;
        let translated_node_count = reader.read_u16::<LE>()?;
        let scaled_node_count = reader.read_u16::<LE>()?;
        let error_value = reader.read_f32::<LE>()?;
        let compression_rate = reader.read_f32::<LE>()?;
        Ok(Self {
            rotated_node_count,
            translated_node_count,
            scaled_node_count,
            _error_value: error_value,
            _compression_rate: compression_rate,
        })
    }
}

#[derive(Default, Debug)]
pub struct Codec {
    pub rotations: Vec<Vec<Quaternion>>,
    pub translations: Vec<Vec<Vector3>>,
    pub scales: Vec<Vec<f32>>,
}
