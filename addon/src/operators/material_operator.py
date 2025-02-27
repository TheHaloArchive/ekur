# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
from pathlib import Path
from typing import final

from bpy.types import Context, Operator, ShaderNodeTree

from ..json_definitions import CommonMaterial, CommonStyleList
from ..material_types.decal_shader import DecalShader
from ..material_types.diffuse_shader import DiffuseShaderType
from ..material_types.layered_shader import LayeredShader
from ..material_types.illum_shader import IllumShader
from ..material_types.color_decal import ColorDecalShader
from ..utils import get_data_folder, get_materials, read_json_file, remove_nodes

__all__ = ["ImportMaterialOperator"]


@final
class ImportMaterialOperator(Operator):
    bl_idname = "ekur.importmaterial"
    bl_label = "Import"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}
        data = get_data_folder()
        materials = get_materials()

        for slot in materials:
            if not slot.material:
                continue
            node_tree = slot.material.node_tree
            name = slot.name
            if len(slot.name.split(".")) > 1:
                name = slot.name.split(".")[0]

            definition_path = Path(f"{data}/materials/{name}.json")
            if not definition_path.exists():
                logging.warning(f"Material path does not exist!: {definition_path}")
                continue

            if not node_tree:
                continue

            remove_nodes(node_tree)
            material = read_json_file(definition_path, CommonMaterial)
            self.run_material(material, node_tree)

        return {"FINISHED"}

    def run_material(self, material: CommonMaterial, node_tree: ShaderNodeTree) -> None:
        data = get_data_folder()
        match material["shader_type"]:
            case "Layered":
                if material["style_info"] is not None:
                    styles_path = Path(
                        f"{data}/stylelists/{material['style_info']['stylelist']}.json"
                    )
                    if not styles_path.exists():
                        logging.warning(f"Styles path does not exist!: {styles_path}")
                        return
                    styles = read_json_file(styles_path, CommonStyleList)
                    layered_shader = LayeredShader(node_tree, material, styles, data)
                    layered_shader.create_textures()
                    layered_shader.process_styles()

            case "Diffuse":
                _ = DiffuseShaderType(material, node_tree)
            case "Decal":
                _ = DecalShader(material, node_tree)
            case "SelfIllum":
                _ = IllumShader(material, node_tree)
            case "ColorDecal":
                _ = ColorDecalShader(material, node_tree)
            case "Unknown":
                pass
            case _:
                logging.error(f"Unknown shader type!: {material['shader_type']}")
