use anyhow::Result;
use byteorder::LE;
use byteorder::ReadBytesExt;
use std::io::Read;
use std::io::Seek;

#[derive(Debug, Default)]
pub struct StaticData {
    pub rotated_node_count: u16,
    pub translated_node_count: u16,
    pub scaled_node_count: u16,
    pub error_value: f32,
    pub compression_rate: f32,
    pub translation_data_offset: u32,
    pub scale_data_offset: u32,
    pub rotations: Vec<i16>,
    pub positions: Vec<i16>,
    pub scales: Vec<i16>,
}

impl StaticData {
    pub fn from_reader(reader: &mut (impl Read + Seek)) -> Result<Self> {
        reader.seek_relative(2)?; // skip codec
        let mut static_data = Self {
            rotated_node_count: reader.read_u16::<LE>()?,
            translated_node_count: reader.read_u16::<LE>()?,
            scaled_node_count: reader.read_u16::<LE>()?,
            error_value: reader.read_f32::<LE>()?,
            compression_rate: reader.read_f32::<LE>()?,
            translation_data_offset: reader.read_u32::<LE>()?,
            scale_data_offset: reader.read_u32::<LE>()?,
            rotations: Vec::new(),
            positions: Vec::new(),
            scales: Vec::new(),
        };
        reader.seek_relative(24)?;
        for _ in 0..static_data.rotated_node_count {
            static_data.rotations.push(reader.read_i16::<LE>()?);
        }
        for _ in 0..static_data.translated_node_count {
            static_data.positions.push(reader.read_i16::<LE>()?);
        }
        for _ in 0..static_data.scaled_node_count {
            static_data.scales.push(reader.read_i16::<LE>()?);
        }
        Ok(static_data)
    }
}
