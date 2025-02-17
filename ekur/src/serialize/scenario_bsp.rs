use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;
use nalgebra::{Matrix4, Vector4};
use serde::Serialize;

use crate::definitions::{render_model::MeshFlags, scenario::ScenarioStructureBsp};

#[derive(Default, Debug, Serialize)]
pub struct Instance {
    pub global_id: i32,
    pub scale: [f32; 3],
    pub position: [f32; 3],
    pub rotation: [f32; 4],
    pub material: Vec<i32>,
}

#[derive(Default, Debug, Serialize)]
pub struct Level {
    pub instances: Vec<Instance>,
}

fn create_quat_from_rotation_matrix(matrix: &Matrix4<f32>) -> [f32; 4] {
    let trace = matrix[(0, 0)] + matrix[(1, 1)] + matrix[(2, 2)];
    let mut q = [0.0f32; 4]; // [x, y, z, w]

    if trace > 0.0 {
        let s = (trace + 1.0).sqrt();
        q[3] = s * 0.5; // w
        let s = 0.5 / s;
        q[0] = (matrix[(2, 1)] - matrix[(1, 2)]) * s; // x
        q[1] = (matrix[(0, 2)] - matrix[(2, 0)]) * s; // y
        q[2] = (matrix[(1, 0)] - matrix[(0, 1)]) * s; // z
    } else if matrix[(0, 0)] >= matrix[(1, 1)] && matrix[(0, 0)] >= matrix[(2, 2)] {
        let s = (1.0 + matrix[(0, 0)] - matrix[(1, 1)] - matrix[(2, 2)]).sqrt();
        let inv_s = 0.5 / s;
        q[0] = 0.5 * s; // x
        q[1] = (matrix[(1, 0)] + matrix[(0, 1)]) * inv_s; // y
        q[2] = (matrix[(2, 0)] + matrix[(0, 2)]) * inv_s; // z
        q[3] = (matrix[(2, 1)] - matrix[(1, 2)]) * inv_s; // w
    } else if matrix[(1, 1)] > matrix[(2, 2)] {
        let s = (1.0 + matrix[(1, 1)] - matrix[(0, 0)] - matrix[(2, 2)]).sqrt();
        let inv_s = 0.5 / s;
        q[0] = (matrix[(1, 0)] + matrix[(0, 1)]) * inv_s; // x
        q[1] = 0.5 * s; // y
        q[2] = (matrix[(2, 1)] + matrix[(1, 2)]) * inv_s; // z
        q[3] = (matrix[(0, 2)] - matrix[(2, 0)]) * inv_s; // w
    } else {
        let s = (1.0 + matrix[(2, 2)] - matrix[(0, 0)] - matrix[(1, 1)]).sqrt();
        let inv_s = 0.5 / s;
        q[0] = (matrix[(2, 0)] + matrix[(0, 2)]) * inv_s; // x
        q[1] = (matrix[(2, 1)] + matrix[(1, 2)]) * inv_s; // y
        q[2] = 0.5 * s; // z
        q[3] = (matrix[(1, 0)] - matrix[(0, 1)]) * inv_s; // w
    }

    q
}
pub fn process_scenarios(
    scenarios: &HashMap<i32, ScenarioStructureBsp>,
    save_path: &str,
) -> Result<()> {
    for levl in scenarios {
        let scenario = levl.1;
        let mut level = Level::default();
        for instance in &scenario.bsp_geometry_instances.elements {
            let mut inst = Instance::default();
            if instance.runtime_geo.global_id == -1 {
                continue;
            }
            if instance
                .flags_override
                .0
                .contains(MeshFlags::MESH_IS_CUSTOM_SHADOW_CASTER)
            {
                continue;
            }
            inst.global_id = instance.runtime_geo.global_id;

            let rotmat = Matrix4::from_columns(&[
                Vector4::new(
                    instance.forward.x,
                    instance.forward.y,
                    instance.forward.z,
                    0.0,
                ),
                Vector4::new(instance.left.x, instance.left.y, instance.left.z, 0.0),
                Vector4::new(instance.up.x, instance.up.y, instance.up.z, 0.0),
                Vector4::new(0.0, 0.0, 0.0, 1.0),
            ]);

            let rotation = create_quat_from_rotation_matrix(&rotmat);
            inst.rotation = rotation;
            inst.position = [
                instance.position.x,
                instance.position.y,
                instance.position.z,
            ];
            inst.scale = [
                instance.transform_scale.x,
                instance.transform_scale.y,
                instance.transform_scale.z,
            ];

            inst.material = instance
                .material
                .elements
                .iter()
                .map(|x| x.material.global_id)
                .collect();
            level.instances.push(inst);
        }
        let mut path = PathBuf::from(format!("{save_path}/levels/"));
        path.push(levl.0.to_string());
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &level)?;
    }
    Ok(())
}
