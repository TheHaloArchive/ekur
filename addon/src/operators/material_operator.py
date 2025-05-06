# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
from pathlib import Path
from typing import final

import bpy
from bpy.types import Context, MaterialSlot, Operator, ShaderNodeTree

from ..ui.material_options import get_material_options
from ..json_definitions import CommonMaterial, CommonStyleList
from ..material_types.hair_shader import HairShader
from ..material_types.skin_shader import SkinShader
from ..material_types.decal_shader import DecalShader
from ..material_types.diffuse_shader import DiffuseShaderType
from ..material_types.layered_shader import LayeredShader
from ..material_types.illum_shader import IllumShader
from ..material_types.color_decal import ColorDecalShader
from ..utils import get_data_folder, read_json_file, remove_nodes

__all__ = ["ImportMaterialOperator"]


def get_materials() -> list[MaterialSlot]:
    """Get all materials from the selected objects or all objects in the scene.

    Returns:
        A list of all material slots.
    """
    data_source = bpy.data.objects
    properties = get_material_options()
    if properties.selected_only:
        data_source = bpy.context.selected_objects
    meshes = [obj for obj in data_source if obj.type == "MESH"]
    return [mat_slot for obj in meshes for mat_slot in obj.material_slots]


def import_materials() -> None:
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
        if not node_tree:
            continue

        remove_nodes(node_tree)
        material = read_json_file(definition_path, CommonMaterial)
        if material is None:
            return
        run_material(material, node_tree)


def run_material(material: CommonMaterial, node_tree: ShaderNodeTree) -> None:
    data = get_data_folder()
    match material["shader_type"]:
        case "Layered":
            if material["style_info"] is not None:
                styles_path = Path(f"{data}/stylelists/{material['style_info']['stylelist']}.json")
                if not styles_path.exists():
                    logging.warning(f"Styles path does not exist!: {styles_path}")
                    return
                styles = read_json_file(styles_path, CommonStyleList)
                if styles is None:
                    return
                layered_shader = LayeredShader(node_tree, material, styles)
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
        case "SkinShader":
            _ = SkinShader(material, node_tree)
        case "Hair":
            _ = HairShader(material, node_tree)
        case "Unknown":
            pass
        case _:
            logging.error(f"Unknown shader type!: {material['shader_type']}")


@final
class ImportMaterialOperator(Operator):
    bl_idname = "ekur.importmaterial"
    bl_label = "Import"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}
        import_materials()
        return {"FINISHED"}
