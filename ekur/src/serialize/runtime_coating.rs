/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use crate::definitions::{coating_swatch::CoatingSwatchPODTag, runtime_style::RuntimeCoatingStyle};

use super::common_coating::{CommonCoating, CommonLayer, CommonRegion};
use anyhow::Result;
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

pub fn process_runtime_coatings(
    runtime_styles: &HashMap<i32, RuntimeCoatingStyle>,
    coating_swatches: &HashMap<i32, CoatingSwatchPODTag>,
    save_path: &str,
) -> Result<()> {
    for (id, style) in runtime_styles {
        let mut common_coating = CommonCoating::default();

        for region in &style.regions.elements {
            let mut common_region = CommonRegion::default();
            for (idx, intention) in region.intentions.elements.iter().enumerate() {
                let common_layer =
                    CommonLayer::from_runtime(&intention.info, coating_swatches, idx as i32);
                common_region.layers.insert(intention.name.0, common_layer);
            }
            common_coating.regions.insert(region.name.0, common_region);
        }

        common_coating.grime_swatch =
            CommonLayer::from_runtime(&style.info.grime_swatch, coating_swatches, 0);
        common_coating.grime_amount = style.info.grime_amount.0;
        common_coating.scratch_amount = style.info.scratch_amount.0;

        let mut path = PathBuf::from(format!("{save_path}/styles/"));
        path.push(id.to_string());
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &common_coating)?;
    }

    Ok(())
}
