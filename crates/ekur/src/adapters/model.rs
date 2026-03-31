/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::utils::get_tags_w_index;
use ekur_definitions::{
    particle_model::ParticleModel, render_model::RenderModel, runtime_geo::RuntimeGeo,
};
use ekur_model::serialize::write::{process_model, process_particle, process_rtgo};

use anyhow::Result;
use infinite_rs::ModuleFile;
use std::{
    collections::HashMap,
    fs::{File, create_dir_all},
    io::{BufWriter, Write},
    path::PathBuf,
};

const MODE_GROUP: &str = "mode";
const PMDF_GROUP: &str = "pmdf";
const RTGO_GROUP: &str = "rtgo";

pub(crate) fn extract_models(
    modules: &mut [ModuleFile],
    strings: &HashMap<i32, String>,
    save_path: &str,
) -> Result<()> {
    let mut save_path = PathBuf::from(save_path);
    save_path.push("models/");
    create_dir_all(&save_path)?;
    save_path.pop();
    save_path.push("runtime_geo/");
    create_dir_all(&save_path)?;
    save_path.pop();
    save_path.push("particle_models/");
    create_dir_all(&save_path)?;
    save_path.pop();

    let mut models = HashMap::new();
    let mut part_models = HashMap::new();
    let mut runtime_geo = HashMap::new();

    for (idx, module) in modules.iter_mut().enumerate() {
        models.extend(get_tags_w_index::<RenderModel>(MODE_GROUP, module, idx)?);
        part_models.extend(get_tags_w_index::<ParticleModel>(PMDF_GROUP, module, idx)?);
        runtime_geo.extend(get_tags_w_index::<RuntimeGeo>(RTGO_GROUP, module, idx)?);
    }
    save_path.push("models/");
    for model in models {
        let model_data = process_model(model.1, (model.0.0, model.0.1), modules, strings)?;
        save_path.push(model.0.2.to_string());
        save_path.add_extension("ekur");
        let file = File::create(&save_path)?;
        let mut writer = BufWriter::new(file);
        writer.write_all(&model_data)?;
        save_path.pop();
    }
    save_path.pop();
    save_path.push("particle_models/");
    for model in part_models {
        let model_data = process_particle(model.1, (model.0.0, model.0.1), modules)?;
        save_path.push(model.0.2.to_string());
        save_path.add_extension("ekur");
        let file = File::create(&save_path)?;
        let mut writer = BufWriter::new(file);
        writer.write_all(&model_data)?;
        save_path.pop();
    }
    save_path.pop();
    save_path.push("runtime_geo/");
    for model in runtime_geo {
        let model_data = process_rtgo(model.1, (model.0.0, model.0.1), modules, strings)?;
        save_path.push(model.0.2.to_string());
        save_path.add_extension("ekur");
        let file = File::create(&save_path)?;
        let mut writer = BufWriter::new(file);
        writer.write_all(&model_data)?;
        save_path.pop();
    }
    Ok(())
}
