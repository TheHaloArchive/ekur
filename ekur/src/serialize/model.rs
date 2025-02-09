/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;
use infinite_rs::tag::types::common_types::FieldRealQuaternion;
use nalgebra::{Matrix4, Vector4};
use serde::Serialize;

use crate::definitions::render_model::{MarkerGroupBlock, NodeBlock, RegionBlock, RenderModel};

#[derive(Default, Debug, Serialize)]
pub struct Bone {
    name: i32,
    parent_index: i32,
    local_transform: [[f32; 4]; 4],
    world_transform: [[f32; 4]; 4],
}

#[derive(Default, Debug, Serialize)]
pub struct Marker {
    position: [f32; 3],
    rotation: [f32; 4],
    region_index: i8,
    permutation_index: i32,
    bone_index: i8,
}

#[derive(Default, Debug, Serialize)]
pub struct MarkerGroup {
    name: i32,
    markers: Vec<Marker>,
}

#[derive(Default, Debug, Serialize)]
pub struct Permutation {
    name: i32,
    section_count: u16,
    section_index: i16,
}

#[derive(Default, Debug, Serialize)]
pub struct Region {
    name: i32,
    permutations: Vec<Permutation>,
}

#[derive(Default, Debug, Serialize)]
pub struct Model {
    regions: Vec<Region>,
    bones: Vec<Bone>,
    markers: Vec<MarkerGroup>,
    materials: Vec<i32>,
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

fn create_node(node: &NodeBlock) -> Bone {
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

fn create_markers(marker: &MarkerGroupBlock) -> Vec<Marker> {
    let mut markers = Vec::new();
    for marker in marker.markers.elements.iter() {
        let ser_marker = Marker {
            position: [
                marker.translation.x,
                marker.translation.y,
                marker.translation.z,
            ],
            rotation: [
                marker.rotation.x,
                marker.rotation.y,
                marker.rotation.z,
                marker.rotation.w,
            ],
            region_index: marker.region_index.0,
            permutation_index: marker.permutation_index.0,
            bone_index: marker.node_index.0,
        };
        markers.push(ser_marker);
    }
    markers
}

fn create_region(region: &RegionBlock) -> Region {
    let mut reg = Region {
        name: region.name.0,
        permutations: Vec::new(),
    };
    for perm in region.permutations.elements.iter() {
        let permutation = Permutation {
            name: perm.name.0,
            section_count: perm.section_count.0,
            section_index: perm.section_index.0,
        };
        reg.permutations.push(permutation);
    }
    reg
}

pub fn process_models(models: &HashMap<i32, RenderModel>, save_path: &str) -> Result<()> {
    for model in models {
        let mut ser_model = Model::default();
        for region in &model.1.regions.elements {
            let reg = create_region(region);
            ser_model.regions.push(reg);
        }

        for node in &model.1.nodes.elements {
            let bone = create_node(node);
            ser_model.bones.push(bone);
        }
        for marker in &model.1.marker_groups.elements {
            let mark = MarkerGroup {
                name: marker.name.0,
                markers: create_markers(marker),
            };
            ser_model.markers.push(mark);
        }
        ser_model.materials = model
            .1
            .materials
            .elements
            .iter()
            .map(|x| x.material.global_id)
            .collect();
        let mut path = PathBuf::from(format!("{save_path}/models/"));
        path.push(model.0.to_string());
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &ser_model)?;
    }

    Ok(())
}
