# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging

from typing import cast
from bpy.types import (
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTree,
    ShaderNodeUVMap,
)

from ..nodes.hair import Hair
from ..utils import assign_value, create_image, create_node
from ..json_definitions import CommonMaterial

__all__ = ["HairShader"]


class HairShader:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self._create_nodes()

    def _get_textures(self, nodes: ShaderNodeGroup) -> None:
        if self.material["textures"].get("Color"):
            img = create_image(self.tree.nodes, -100, str(self.material["textures"]["Color"]))
            if img.image and img.image.colorspace_settings:
                img.image.colorspace_settings.name = "sRGB"  # pyright: ignore[reportAttributeAccessIssue]
            else:
                logging.warning("Image node does not have image colorspace or image texture!")
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[0])
            _ = self.tree.links.new(img.outputs[1], nodes.inputs[1])

        if self.material["textures"].get("Control"):
            img = create_image(self.tree.nodes, -200, str(self.material["textures"]["Control"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[2])

        if self.material["textures"].get("Normal"):
            img = create_image(self.tree.nodes, -300, str(self.material["textures"]["Normal"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[3])

        if self.material["textures"].get("AO"):
            img = create_image(self.tree.nodes, -400, str(self.material["textures"]["AO"]))
            uv_map = create_node(self.tree.nodes, 0, 0, ShaderNodeUVMap)
            uv_map.uv_map = "UV1"
            _ = self.tree.links.new(uv_map.outputs[0], img.inputs[0])
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[6])

    def _create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, Hair().node_tree)

        if not self.material["hair"]:
            logging.warning("Hair material has no hair key, this shouldn't happen!")
            return
        info = self.material["hair"]
        assign_value(shader, 4, (*info["tint_color"], 1.0))

        self._get_textures(shader)
        material_output = create_node(self.tree.nodes, 200, 0, ShaderNodeOutputMaterial)
        _ = self.tree.links.new(shader.outputs[0], material_output.inputs[0])
