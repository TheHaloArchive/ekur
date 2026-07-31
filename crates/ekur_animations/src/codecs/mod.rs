use crate::datatypes::{quaternion::Quaternion, vector::Vector3};

pub mod quantized_rotation_only;
pub mod shared_static;

#[derive(Default, Debug)]
pub struct Codec {
    pub rotations: Vec<Vec<Quaternion>>,
    pub translations: Vec<Vec<Vector3>>,
    pub scales: Vec<Vec<f32>>,
}
