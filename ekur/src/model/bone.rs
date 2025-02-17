/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::tag::types::common_types::FieldRealQuaternion;
use nalgebra::{Matrix4, Vector4};

use crate::definitions::render_model::NodeBlock;

#[derive(Default, Debug)]
pub(super) struct Bone {
    pub(super) name: i32,
    pub(super) parent_index: i32,
    pub(super) local_transform: [[f32; 4]; 4],
    pub(super) world_transform: [[f32; 4]; 4],
}

pub fn create_matrix_from_quaternion(quaternion: &FieldRealQuaternion) -> Matrix4<f32> {
    let xx = quaternion.x * quaternion.x;
    let yy = quaternion.y * quaternion.y;
    let zz = quaternion.z * quaternion.z;

    let xy = quaternion.x * quaternion.y;
    let wz = quaternion.z * quaternion.w;
    let xz = quaternion.z * quaternion.x;
    let wy = quaternion.y * quaternion.w;
    let yz = quaternion.y * quaternion.z;
    let wx = quaternion.x * quaternion.w;

    Matrix4::from_columns(&[
        Vector4::new(1.0 - 2.0 * (yy + zz), 2.0 * (xy + wz), 2.0 * (xz - wy), 0.0),
        Vector4::new(2.0 * (xy - wz), 1.0 - 2.0 * (zz + xx), 2.0 * (yz + wx), 0.0),
        Vector4::new(2.0 * (xz + wy), 2.0 * (yz - wx), 1.0 - 2.0 * (yy + xx), 0.0),
        Vector4::new(0.0, 0.0, 0.0, 1.0),
    ])
}

pub(super) fn create_node(node: &NodeBlock) -> Bone {
    let mut bone = Bone {
        name: node.name.0,
        parent_index: node.parent_index.0 as i32,
        ..Default::default()
    };

    let pos2 = &node.position;
    let rot2 = &node.rotation;
    let fw = &node.inverse_forward;
    let lf = &node.inverse_left;
    let up = &node.inverse_up;
    let po = &node.inverse_position;

    let rot_matrix = create_matrix_from_quaternion(rot2);
    let trans_matrix = Matrix4::from_columns(&[
        Vector4::new(1.0, 0.0, 0.0, 0.0),
        Vector4::new(0.0, 1.0, 0.0, 0.0),
        Vector4::new(0.0, 0.0, 1.0, 0.0),
        Vector4::new(pos2.x, pos2.y, pos2.z, 1.0),
    ]);

    let local_transform = trans_matrix * rot_matrix;

    let world_transform = Matrix4::from_columns(&[
        Vector4::new(fw.x, fw.y, fw.z, 0.0),
        Vector4::new(lf.x, lf.y, lf.z, 0.0),
        Vector4::new(up.x, up.y, up.z, 0.0),
        Vector4::new(po.x, po.y, po.z, 1.0),
    ]);

    let world_transform = world_transform.try_inverse().unwrap_or(Matrix4::identity());
    bone.local_transform = local_transform.data.0;
    bone.world_transform = world_transform.data.0;
    bone
}
