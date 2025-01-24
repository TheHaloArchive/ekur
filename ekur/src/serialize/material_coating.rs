use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;

use crate::definitions::{
    material_palette::MaterialPaletteTag, material_styles::MaterialStylesTag,
    material_swatch::MaterialSwatchTag,
};

use super::{
    common_coating::{CommonCoating, CommonLayer, CommonRegion},
    common_styles::{CommonStyleList, CommonStyleListEntry},
};

pub fn process_material_coatings(
    styles: &HashMap<i32, MaterialStylesTag>,
    palettes: &HashMap<i32, MaterialPaletteTag>,
    material_swatches: &HashMap<i32, MaterialSwatchTag>,
    save_path: &str,
    mappings: &HashMap<i32, String>,
) -> Result<()> {
    for (id, style) in styles {
        let mut style_list = CommonStyleList::default();
        for coating in &style.styles.elements {
            let mut common_coating = CommonCoating::default();
            let material_palette = palettes
                .get(&coating.palette.global_id)
                .expect("invalid mwpl");
            for region in &coating.regions.elements {
                let mut common_region = CommonRegion::default();
                for (i, layer) in region.layers.elements.iter().enumerate() {
                    let intention = material_palette
                        .swatches
                        .elements
                        .iter()
                        .find(|x| x.name.0 == layer.name.0);
                    if intention.is_none() {
                        continue;
                    }
                    let swatch = material_swatches.get(&intention.unwrap().swatch.global_id);
                    if swatch.is_none() {
                        continue;
                    }
                    let layer_c = CommonLayer::from_material(swatch.unwrap(), intention.unwrap());
                    let region = &style
                        .regions
                        .elements
                        .iter()
                        .find(|x| x.name.0 == region.name.0);
                    if region.is_none() {
                        continue;
                    }
                    let layer_name = &region.unwrap().intention_conversion_list.elements.get(i);
                    let layer_nam;
                    if let Some(layer_name) = layer_name {
                        layer_nam = layer_name.intention_name.0;
                    } else {
                        layer_nam = layer.name.0;
                    }
                    common_region.layers.insert(layer_nam, layer_c);
                }
                common_coating.regions.insert(region.name.0, common_region);
                common_coating.grime_amount = coating.grime_amount.0;
                common_coating.scratch_amount = coating.scratch_amount.0;
                let grime_intention = material_palette
                    .swatches
                    .elements
                    .iter()
                    .find(|x| x.name.0 == coating.grime_type.0);
                if grime_intention.is_none() {
                    common_coating.grime_swatch.disabled = true;
                } else {
                    let swatch = material_swatches
                        .get(&grime_intention.unwrap().swatch.global_id)
                        .expect("swatch not found");
                    common_coating.grime_swatch =
                        CommonLayer::from_material(swatch, grime_intention.unwrap());
                }
                let mut path = PathBuf::from(format!("{save_path}/styles/{id}_{}", coating.name.0));
                path.set_extension("json");
                let file = File::create(path)?;
                let reader = BufWriter::new(file);
                serde_json::to_writer(reader, &common_coating)?;
            }
            style_list.styles.insert(
                coating.name.0,
                CommonStyleListEntry {
                    reference: format!("{id}_{}", coating.name.0),
                    name: mappings
                        .get(&coating.name.0)
                        .cloned()
                        .unwrap_or(coating.name.0.to_string()),
                },
            );
        }
        let mut path = PathBuf::from(format!("{save_path}/stylelists/{id}"));
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &style_list)?;
    }
    Ok(())
}
