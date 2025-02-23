# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import cast
from bpy.types import (
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTexImage,
    ShaderNodeTree,
)

from ..nodes.color_decal import ColorDecal

from ..utils import assign_value, create_node, read_texture
from ..json_definitions import CommonMaterial

__all__ = ["ColorDecalShader"]


class ColorDecalShader:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self.create_nodes()

    def _create_image(self, y: int, name: str) -> ShaderNodeTexImage:
        texture = create_node(self.tree.nodes, -300, y, ShaderNodeTexImage)
        texture.hide = True
        texture.image = read_texture(name)
        return texture

    def create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, ColorDecal().node_tree)

        if self.material["color_decal"]:
            info = self.material["color_decal"]
            assign_value(shader, 2, info["roughness"])
            assign_value(shader, 3, info["opacity"])
            assign_value(shader, 4, info["metallic"])

            if self.material["textures"].get("Color"):
                img = self._create_image(-100, str(self.material["textures"]["Color"]))
                _ = self.tree.links.new(img.outputs[0], shader.inputs[0])
                _ = self.tree.links.new(img.outputs[1], shader.inputs[1])

            material_output = create_node(self.tree.nodes, 0, 0, ShaderNodeOutputMaterial)
            material_output.target = "ALL"
            material_output.location = (200, 0)
            _ = self.tree.links.new(shader.outputs[0], material_output.inputs[0])
