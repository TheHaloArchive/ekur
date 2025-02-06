# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
from pathlib import Path

from bpy.types import Context, Operator, ShaderNodeTree

from .json_definitions import CommonMaterial, CommonStyleList
from .material_types.decal_shader import DecalShader
from .material_types.diffuse_shader import DiffuseShaderType
from .material_types.layered_shader import LayeredShader
from .utils import get_materials, read_json_file, remove_nodes


class ImportMaterialOperator(Operator):
    bl_idname = "ekur.importmaterial"
    bl_label = "Import"

    def execute(self, context: Context | None) -> set[str]:
        data = context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder  # pyright: ignore[reportAttributeAccessIssue]
        materials = get_materials()

        for slot in materials:
            node_tree = slot.material.node_tree
            name = slot.name
            if len(slot.name.split(".")) > 1:
                name = slot.name.split(".")[0]

            definition_path = Path(f"{data}/materials/{name}.json")
            if not definition_path.exists():
                logging.warning(f"Material path does not exist!: {definition_path}")
                continue

            remove_nodes(node_tree)
            material: CommonMaterial = read_json_file(definition_path)
            if not node_tree:
                continue
            self.run_material(context, material, node_tree)
        return {"FINISHED"}

    def run_material(
        self, context: Context | None, material: CommonMaterial, node_tree: ShaderNodeTree
    ) -> None:
        data = context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder  # pyright: ignore[reportAttributeAccessIssue]
        match material["shader_type"]:
            case "LayeredShader":
                if material["style_info"] is not None:
                    styles_path = Path(
                        f"{data}/stylelists/{material['style_info']['stylelist']}.json"
                    )
                    if not styles_path.exists():
                        logging.warning(f"Styles path does not exist!: {styles_path}")
                        return
                    styles: CommonStyleList = read_json_file(styles_path)
                    layered_shader = LayeredShader(node_tree, material, styles, data)
                    layered_shader.create_textures()
                    layered_shader.process_styles()

            case "DiffuseShader":
                _ = DiffuseShaderType(material, node_tree)
            case "DecalShader":
                _ = DecalShader(material, node_tree)
            case "Unknown":
                pass
            case _:
                logging.error(f"Unknown shader type!: {material['shader_type']}")
