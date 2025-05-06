# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging

from typing import cast
from bpy.types import (
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTree,
)

from .material_types import MaterialType
from ..constants import EMPTY_CONTROL, EMPTY_TEXTURES
from ..json_definitions import CommonMaterial
from ..nodes.diffuse_shader import DiffuseShader
from ..utils import assign_value, create_image, create_node

__all__ = ["DiffuseShaderType"]


class DiffuseShaderType(MaterialType):
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self._create_nodes()

    def _get_textures(self, nodes: ShaderNodeGroup) -> None:
        if self.material["textures"].get("Color"):
            img = create_image(self.tree.nodes, 0, str(self.material["textures"]["Color"]))
            if img.image and img.image.colorspace_settings:
                img.image.colorspace_settings.name = "sRGB"  # pyright: ignore[reportAttributeAccessIssue]
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[0])
            _ = self.tree.links.new(img.outputs[1], nodes.inputs[11])

        control = self.material["textures"].get("Control")
        if control and control != EMPTY_CONTROL:
            img = create_image(self.tree.nodes, -100, str(control))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[1])

        if self.material["textures"].get("Normal"):
            img = create_image(self.tree.nodes, -200, str(self.material["textures"]["Normal"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[2])

        alpha_map = self.material["textures"].get("AlphaMap")
        if alpha_map and alpha_map not in EMPTY_TEXTURES:
            img = create_image(self.tree.nodes, -300, str(alpha_map))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[11])

    def _create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, DiffuseShader().node_tree)

        if not self.material["diffuse_info"]:
            logging.warning("Diffuse material has no diffuse_info key, this shouldn't happen!")
            return
        info = self.material["diffuse_info"]
        assign_value(shader, 3, info["roughness_white"])
        assign_value(shader, 4, info["roughness_black"])
        assign_value(shader, 5, info["metallic_white"])
        assign_value(shader, 6, info["metallic_black"])
        assign_value(shader, 7, (*info["si_color_tint"], 1.0))
        assign_value(shader, 8, info["si_amount"])
        assign_value(shader, 9, info["si_intensity"])
        assign_value(shader, 10, (*info["color_tint"], 1.0))

        self._get_textures(shader)
        material_output = create_node(self.tree.nodes, 200, 0, ShaderNodeOutputMaterial)
        _ = self.tree.links.new(shader.outputs[0], material_output.inputs[0])
