/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::tag::types::common_types::FieldRealQuaternion;

use crate::definitions::render_model::NodeBlock;

#[derive(Default, Debug)]
pub(super) struct Bone {
    pub(super) name: i32,
    pub(super) parent_index: i32,
    pub(super) rotation_matrix: [[f32; 4]; 4],
    pub(super) transformation_matrix: [[f32; 4]; 4],
    pub(super) world_transform: [[f32; 4]; 4],
}

pub fn create_matrix_from_quaternion(quaternion: &FieldRealQuaternion) -> [[f32; 4]; 4] {
    let xx = quaternion.x * quaternion.x;
    let yy = quaternion.y * quaternion.y;
    let zz = quaternion.z * quaternion.z;

    let xy = quaternion.x * quaternion.y;
    let wz = quaternion.z * quaternion.w;
    let xz = quaternion.z * quaternion.x;
    let wy = quaternion.y * quaternion.w;
    let yz = quaternion.y * quaternion.z;
    let wx = quaternion.x * quaternion.w;

    [
        [1.0 - 2.0 * (yy + zz), 2.0 * (xy + wz), 2.0 * (xz - wy), 0.0],
        [2.0 * (xy - wz), 1.0 - 2.0 * (zz + xx), 2.0 * (yz + wx), 0.0],
        [2.0 * (xz + wy), 2.0 * (yz - wx), 1.0 - 2.0 * (yy + xx), 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
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

    bone.rotation_matrix = create_matrix_from_quaternion(rot2);
    bone.transformation_matrix = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [pos2.x, pos2.y, pos2.z, 1.0],
    ];

    bone.world_transform = [
        [fw.x, fw.y, fw.z, 0.0],
        [lf.x, lf.y, lf.z, 0.0],
        [up.x, up.y, up.z, 0.0],
        [po.x, po.y, po.z, 1.0],
    ];
    bone
}
