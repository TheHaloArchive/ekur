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
from ..nodes.diffuse_shader import DiffuseShader
from ..utils import assign_value, create_node, read_texture

__all__ = ["DiffuseShaderType"]


class DiffuseShaderType:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self._create_nodes()

    def _get_textures(self, nodes: ShaderNodeGroup) -> None:
        if self.material["textures"].get("Color"):
            img = self._create_image(0, str(self.material["textures"]["Color"]))
            if img.image:
                img.image.colorspace_settings.name = "sRGB"  # pyright: ignore[reportAttributeAccessIssue]
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[0])
            _ = self.tree.links.new(img.outputs[1], nodes.inputs[11])

        control = self.material["textures"].get("Control")
        if control and control != 11617:
            img = self._create_image(-100, str(control))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[1])
        else:
            assign_value(nodes, 1, (0.0, 1.0, 0.0, 0.0))

        if self.material["textures"].get("Normal"):
            img = self._create_image(-200, str(self.material["textures"]["Normal"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[2])

    def _create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, DiffuseShader().node_tree)

        if self.material["diffuse_info"]:
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

    def _create_image(self, y: int, name: str) -> ShaderNodeTexImage:
        texture = create_node(self.tree.nodes, -300, y, ShaderNodeTexImage)
        texture.hide = True
        texture.image = read_texture(name)
        return texture
