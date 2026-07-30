use anyhow::Result;
use byteorder::LE;
use byteorder::ReadBytesExt;
use ekur_definitions::render_model::NodeBlock;
use infinite_rs::tag::types::common_types::FieldRealQuaternion;
use std::io::Read;

use ekur_definitions::animations::Quaternion8ByteRevised;

#[derive(Default, Debug, Clone, Copy)]
pub struct Quaternion {
    pub x: f32,
    pub y: f32,
    pub z: f32,
    pub w: f32,
}

impl Quaternion {
    pub const IDENTITY: Self = Self {
        x: 0.0,
        y: 0.0,
        z: 0.0,
        w: 1.0,
    };

    pub fn from_quantized(reader: &mut impl Read) -> Result<Self> {
        let x = reader.read_i16::<LE>()? as f32 / 32767.0;
        let y = reader.read_i16::<LE>()? as f32 / 32767.0;
        let z = reader.read_i16::<LE>()? as f32 / 32767.0;
        let w = reader.read_i16::<LE>()? as f32 / 32767.0;
        Ok(Self { x, y, z, w })
    }

    pub fn from_reader(reader: &mut impl Read) -> Result<Self> {
        let x = reader.read_f32::<LE>()?;
        let y = reader.read_f32::<LE>()?;
        let z = reader.read_f32::<LE>()?;
        let w = reader.read_f32::<LE>()?;
        Ok(Self { x, y, z, w })
    }

    pub fn from_field(field: &FieldRealQuaternion) -> Self {
        Self {
            x: field.x,
            y: field.y,
            z: field.z,
            w: field.w,
        }
    }

    pub fn from_quantized_xyzw(data: &Quaternion8ByteRevised) -> Self {
        Self {
            x: data.x.0 as f32 / 32767.0,
            y: data.y.0 as f32 / 32767.0,
            z: data.z.0 as f32 / 32767.0,
            w: data.w.0 as f32 / 32767.0,
        }
    }

    pub fn normalized(&self) -> Self {
        let magnitude =
            (self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w).sqrt();
        if magnitude == 0.0 {
            Self::default()
        } else {
            Self {
                x: self.x / magnitude,
                y: self.y / magnitude,
                z: self.z / magnitude,
                w: self.w / magnitude,
            }
        }
    }

    pub fn from_node(node: &NodeBlock) -> Self {
        Self {
            x: node.rotation.x,
            y: node.rotation.y,
            z: node.rotation.z,
            w: node.rotation.w,
        }
    }

    pub fn from_tuple((x, y, z, w): (f32, f32, f32, f32)) -> Self {
        Self { x, y, z, w }
    }

    pub fn conjugate(&self) -> Self {
        Self {
            x: -self.x,
            y: -self.y,
            z: -self.z,
            w: self.w,
        }
    }
}
