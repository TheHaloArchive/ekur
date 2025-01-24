use serde_with::base64::Base64;
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

use anyhow::Result;
use serde::Serialize;
use serde_with::serde_as;

use crate::definitions::material::{
    MaterialStyleShaderSupportedLayers, MaterialStyleShaderSupportsDamageEnum, MaterialTag,
};

const NORMAL_MAP: i32 = 2142563353;
const MASK0_TEXTURE: i32 = -1869712910;
const MASK1_TEXTURE: i32 = -1677269129;
const ASG_TEXTURE: i32 = -447337164;
const TEXEL_DENSITY: i32 = 523899303;

#[derive(Default, Debug, Serialize, PartialEq, Eq, Hash)]
pub enum TextureType {
    #[default]
    Normal,
    AsgTexture,
    Mask0Texture,
    Mask1Texture,
    Unknown,
}

#[derive(Default, Debug, Serialize)]
pub struct Texture(i32);

#[derive(Default, Debug, Serialize)]
pub struct StyleInfo {
    stylelist: i32,
    region_name: i32,
    base_intention: i32,
    mask0_red_intention: i32,
    mask0_green_intention: i32,
    mask0_blue_intention: i32,
    mask1_red_intention: i32,
    mask1_green_intention: i32,
    mask1_blue_intention: i32,
    supported_layers: u8,
    enable_damage: bool,
}

#[serde_as]
#[derive(Default, Debug, Serialize)]
pub struct Material {
    textures: HashMap<TextureType, Texture>,
    texel_density: (f32, f32),
    material_offset: (f32, f32),
    style_info: StyleInfo,
    #[serde_as(as = "Base64")]
    material_constants: Vec<u8>,
}

impl Material {
    pub fn from_mat(mat: &MaterialTag) -> Self {
        let mut material = Material {
            texel_density: (1.0, 1.0),
            ..Default::default()
        };
        for param in &mat.material_parameters.elements {
            match param.parameter_name.0 {
                NORMAL_MAP => {
                    material
                        .textures
                        .insert(TextureType::Normal, Texture(param.bitmap.global_id));
                }
                MASK0_TEXTURE => {
                    material
                        .textures
                        .insert(TextureType::Mask0Texture, Texture(param.bitmap.global_id));
                }
                MASK1_TEXTURE => {
                    material
                        .textures
                        .insert(TextureType::Mask1Texture, Texture(param.bitmap.global_id));
                }
                ASG_TEXTURE => {
                    material
                        .textures
                        .insert(TextureType::AsgTexture, Texture(param.bitmap.global_id));
                }
                TEXEL_DENSITY => {
                    material.texel_density = (param.real.0, param.vector.x);
                    material.material_offset = (param.vector.y, param.vector.z);
                }
                _ => {
                    material
                        .textures
                        .insert(TextureType::Unknown, Texture(param.bitmap.global_id));
                }
            };
        }
        if let Some(post) = &mat.post_process_definition.elements.first() {
            post.textures.elements.iter().for_each(|t| {
                material
                    .textures
                    .insert(TextureType::Unknown, Texture(t.bitmap_reference.global_id));
            });
            material.material_constants = post
                .material_constants
                .elements
                .iter()
                .flat_map(|c| {
                    [
                        c.register.x.to_be_bytes(),
                        c.register.y.to_be_bytes(),
                        c.register.z.to_be_bytes(),
                        c.register.w.to_be_bytes(),
                    ]
                    .concat()
                })
                .collect();
        }
        let style = &mat.style_info.elements[0];
        material.style_info.base_intention = style.base_intention.0;
        material.style_info.mask0_red_intention = style.mask0_red_channel_intention.0;
        material.style_info.mask0_green_intention = style.mask0_green_channel_intention.0;
        material.style_info.mask0_blue_intention = style.mask0_blue_channel_intention.0;

        material.style_info.mask1_red_intention = style.mask1_red_channel_intention.0;
        material.style_info.mask1_green_intention = style.mask1_green_channel_intention.0;
        material.style_info.mask1_blue_intention = style.mask1_blue_channel_intention.0;

        material.style_info.region_name = style.region_name.0;
        material.style_info.stylelist = style.material_style.global_id;
        material.style_info.enable_damage =
            style.requires_damage.0 == MaterialStyleShaderSupportsDamageEnum::Yes;
        material.style_info.supported_layers = match style.supported_layers.0 {
            MaterialStyleShaderSupportedLayers::Supports1Layer => 1,
            MaterialStyleShaderSupportedLayers::Supports4Layers => 4,
            MaterialStyleShaderSupportedLayers::Supports7Layers => 7,
            MaterialStyleShaderSupportedLayers::LayerShaderDisabled => 0,
        };
        material
    }
}

pub fn process_materials(materials: &HashMap<i32, MaterialTag>, save_path: &str) -> Result<()> {
    for (id, mat) in materials.iter() {
        if mat.style_info.elements.is_empty() {
            continue;
        }
        let material = Material::from_mat(mat);
        let mut path = PathBuf::from(format!("{save_path}/materials"));
        path.push(id.to_string());
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &material)?;
    }
    Ok(())
}
