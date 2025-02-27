# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import cast
from bpy.types import (
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTexImage,
    ShaderNodeTree,
)

from ..nodes.decal import Decal

from ..utils import assign_value, create_node, read_texture
from ..json_definitions import CommonMaterial

__all__ = ["DecalShader"]


class DecalShader:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self._create_nodes()

    def _create_image(self, y: int, name: str) -> ShaderNodeTexImage:
        texture = create_node(self.tree.nodes, -300, y, ShaderNodeTexImage)
        texture.hide = True
        texture.image = read_texture(name)
        return texture

    def _get_textures(self, nodes: ShaderNodeGroup) -> None:
        if self.material["textures"].get("Control"):
            img = self._create_image(-100, str(self.material["textures"]["Control"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[0])

        if self.material["textures"].get("Normal"):
            img = self._create_image(-200, str(self.material["textures"]["Normal"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[1])

    def _create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, Decal().node_tree)

        if self.material["decal_slots"]:
            info = self.material["decal_slots"]
            assign_value(shader, 4, (*info["top_color"], 1.0))
            assign_value(shader, 3, (*info["mid_color"], 1.0))
            assign_value(shader, 2, (*info["bot_color"], 1.0))
            assign_value(shader, 5, info["roughness_white"])
            assign_value(shader, 6, info["roughness_black"])
            assign_value(shader, 7, info["metallic"])

            self._get_textures(shader)
            material_output = create_node(self.tree.nodes, 0, 0, ShaderNodeOutputMaterial)
            material_output.target = "ALL"
            material_output.location = (200, 0)
            _ = self.tree.links.new(shader.outputs[0], material_output.inputs[0])
