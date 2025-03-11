# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import cast
from bpy.types import (
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTexImage,
    ShaderNodeTree,
    ShaderNodeUVMap,
)

from ..nodes.hair import Hair
from ..utils import assign_value, create_node, read_texture
from ..json_definitions import CommonMaterial

__all__ = ["HairShader"]


class HairShader:
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
        if self.material["textures"].get("Color"):
            img = self._create_image(-100, str(self.material["textures"]["Color"]))
            if img.image and img.image.colorspace_settings:
                img.image.colorspace_settings.name = "sRGB"  # pyright: ignore[reportAttributeAccessIssue]
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[0])
            _ = self.tree.links.new(img.outputs[1], nodes.inputs[1])

        if self.material["textures"].get("Control"):
            img = self._create_image(-200, str(self.material["textures"]["Control"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[2])

        if self.material["textures"].get("Normal"):
            img = self._create_image(-300, str(self.material["textures"]["Normal"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[3])

        if self.material["textures"].get("AO"):
            img = self._create_image(-400, str(self.material["textures"]["AO"]))
            uv_map = create_node(self.tree.nodes, 0, 0, ShaderNodeUVMap)
            uv_map.uv_map = "UV1"
            _ = self.tree.links.new(uv_map.outputs[0], img.inputs[0])
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[6])

    def _create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, Hair().node_tree)

        if self.material["hair"]:
            info = self.material["hair"]
            assign_value(shader, 4, (*info["tint_color"], 1.0))

            self._get_textures(shader)
            material_output = create_node(self.tree.nodes, 200, 0, ShaderNodeOutputMaterial)
            _ = self.tree.links.new(shader.outputs[0], material_output.inputs[0])
