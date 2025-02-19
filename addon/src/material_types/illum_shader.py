# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import cast
from bpy.types import (
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTexImage,
    ShaderNodeTree,
)

from ..json_definitions import CommonMaterial
from ..nodes.illum import SelfIllum
from ..utils import assign_value, create_node, read_texture

EMPTY_TEXTURES = [10098, 580203186]

__all__ = ["IllumShader"]


class IllumShader:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self.create_nodes()

    def create_image(self, y: int, name: str) -> ShaderNodeTexImage:
        texture = create_node(self.tree.nodes, -300, y, ShaderNodeTexImage)
        texture.hide = True
        texture.image = read_texture(name)
        return texture

    def get_textures(self, nodes: ShaderNodeGroup) -> None:
        col = self.material["textures"].get("Color")
        if col:
            col = self.create_image(-100, str(col))
            _ = self.tree.links.new(col.outputs[0], nodes.inputs[0])

        alpha_map = self.material["textures"].get("AlphaMap")
        if alpha_map:
            img = self.create_image(-200, str(alpha_map))
            if alpha_map in EMPTY_TEXTURES and col:
                _ = self.tree.links.new(col.outputs[0], nodes.inputs[1])
            else:
                _ = self.tree.links.new(img.outputs[0], nodes.inputs[1])

    def create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, SelfIllum().node_tree)

        if self.material["illum_info"]:
            info = self.material["illum_info"]
            assign_value(shader, 3, info["opacity"])
            assign_value(shader, 2, (*info["color"], 1.0))
            assign_value(shader, 4, info["intensity"])

            self.get_textures(shader)
            material_output = create_node(self.tree.nodes, 0, 0, ShaderNodeOutputMaterial)
            material_output.target = "ALL"
            material_output.location = (200, 0)
            _ = self.tree.links.new(shader.outputs[0], material_output.inputs[0])
