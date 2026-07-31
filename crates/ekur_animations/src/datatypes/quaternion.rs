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
            Self::IDENTITY
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

    pub fn from_yaw(yaw: f32) -> Self {
        let half = yaw * 0.5;
        Self {
            x: 0.0,
            y: 0.0,
            z: half.sin(),
            w: half.cos(),
        }
    }

    pub fn from_angle_axis(x: f32, y: f32, z: f32) -> Self {
        let angle = (x * x + y * y + z * z).sqrt();
        if angle <= 1e-8 {
            return Self::IDENTITY;
        }
        let (s, c) = (angle * 0.5).sin_cos();
        let k = s / angle;
        Self {
            x: x * k,
            y: y * k,
            z: z * k,
            w: c,
        }
    }

    pub fn decompress_revised_quat(reader: &mut impl Read) -> Result<Self> {
        let v3 = reader.read_i16::<LE>()?;
        let v4 = reader.read_i16::<LE>()?;
        let v5 = reader.read_i16::<LE>()?;
        const SQRT_HALF: f32 = 0.707_106_77;
        let i = ((v3 & !1i16) as f32 / i16::MAX as f32) * SQRT_HALF;
        let j = ((v4 & !1i16) as f32 / i16::MAX as f32) * SQRT_HALF;
        let k = ((v5 & !1i16) as f32 / i16::MAX as f32) * SQRT_HALF;
        let mut missing = (1.0 - i * i - j * j - k * k).max(0.0).sqrt();
        if v3 & 1 != 0 {
            missing = -missing;
        }
        let component_index = ((v5 & 1) as usize) | ((2 * (v4 & 1)) as usize);

        let mut output = [0.0f32; 4];
        output[(component_index + 1) & 3] = i;
        output[(component_index + 2) & 3] = j;
        output[(component_index + 3) & 3] = k;
        output[component_index] = missing;
        Ok(Self {
            x: output[0],
            y: output[1],
            z: output[2],
            w: output[3],
        }
        .normalized())
    }

    pub fn rotate(
        &self,
        v: crate::datatypes::vector::Vector3,
    ) -> crate::datatypes::vector::Vector3 {
        let axis = crate::datatypes::vector::Vector3 {
            x: self.x,
            y: self.y,
            z: self.z,
        };
        let uv = axis.cross(v);
        let uuv = axis.cross(uv);
        crate::datatypes::vector::Vector3 {
            x: v.x + 2.0 * (self.w * uv.x + uuv.x),
            y: v.y + 2.0 * (self.w * uv.y + uuv.y),
            z: v.z + 2.0 * (self.w * uv.z + uuv.z),
        }
    }
}

impl std::ops::Mul for Quaternion {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        Self {
            w: self.w * rhs.w - self.x * rhs.x - self.y * rhs.y - self.z * rhs.z,
            x: self.w * rhs.x + self.x * rhs.w + self.y * rhs.z - self.z * rhs.y,
            y: self.w * rhs.y - self.x * rhs.z + self.y * rhs.w + self.z * rhs.x,
            z: self.w * rhs.z + self.x * rhs.y - self.y * rhs.x + self.z * rhs.w,
        }
    }
}
