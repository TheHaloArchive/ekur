/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2026 The Halo Archive */
use crate::{CommonCoating, CommonLayer, CommonRegion};
use ekur_definitions::{coating_swatch::CoatingSwatchPODTag, runtime_style::RuntimeCoatingStyle};

use anyhow::Result;
use std::collections::HashMap;

pub fn process_runtime_coatings(
    runtime_styles: &HashMap<i32, RuntimeCoatingStyle>,
    coating_swatches: &HashMap<i32, CoatingSwatchPODTag>,
) -> Result<HashMap<i32, CommonCoating>> {
    let mut styles = HashMap::new();
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
        styles.insert(*id, common_coating);
    }

    Ok(styles)
}
