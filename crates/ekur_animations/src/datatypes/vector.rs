use byteorder::ReadBytesExt;
use infinite_rs::tag::types::common_types::FieldRealPoint3D;
use std::io::Read;

use anyhow::Result;
use byteorder::LE;

use ekur_definitions::{animations::SharedStaticDataCodecTranslation, render_model::NodeBlock};

#[derive(Default, Debug, Clone, Copy)]
pub struct Vector3 {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Vector3 {
    pub fn from_reader(reader: &mut impl Read) -> Result<Self> {
        let x = reader.read_f32::<LE>()?;
        let y = reader.read_f32::<LE>()?;
        let z = reader.read_f32::<LE>()?;
        Ok(Self { x, y, z })
    }

    pub fn from_field(field: &FieldRealPoint3D) -> Self {
        Self {
            x: field.x,
            y: field.y,
            z: field.z,
        }
    }

    pub fn from_shared(shared: &SharedStaticDataCodecTranslation) -> Self {
        Self {
            x: shared.x.0,
            y: shared.y.0,
            z: shared.z.0,
        }
    }

    pub fn from_node(node: &NodeBlock) -> Self {
        Self {
            x: node.position.x,
            y: node.position.y,
            z: node.position.z,
        }
    }

    pub fn mul_add(&self, extent: Self, min: Self) -> Self {
        Self {
            x: self.x * extent.x + min.x,
            y: self.y * extent.y + min.y,
            z: self.z * extent.z + min.z,
        }
    }

    pub fn cross(&self, rhs: Self) -> Self {
        Self {
            x: self.y * rhs.z - self.z * rhs.y,
            y: self.z * rhs.x - self.x * rhs.z,
            z: self.x * rhs.y - self.y * rhs.x,
        }
    }
}
