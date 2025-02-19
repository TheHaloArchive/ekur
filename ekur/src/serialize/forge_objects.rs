use std::collections::HashMap;

use anyhow::Result;

use crate::definitions::{
    crates::CrateDefinition, forge_object_definition::ForgeObjectData,
    forge_object_manifest::ForgeObjectManifest, model::ModelDefinition,
};

pub fn process_forge_objects(
    objects: &HashMap<i32, ForgeObjectData>,
    manifest: &ForgeObjectManifest,
    crates: &HashMap<i32, CrateDefinition>,
    models: &HashMap<i32, ModelDefinition>,
) -> Result<()> {
    for entries in &manifest.entries.elements {
        let definition = objects.get(&entries.forge_object.global_id);
        let Some(def) = definition else { continue };
        let object = def.object_representations.elements.first();
        let Some(rep) = object else { continue };
        let crate_obj = crates.get(&rep.object_definition.global_id);
        let Some(crat) = crate_obj else { continue };
        let model = models.get(&crat.model.global_id);
        let Some(mode) = model else { continue };
    }
    Ok(())
}
