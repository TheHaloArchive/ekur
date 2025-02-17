# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import cast
from bpy.types import (
    NodeSocketColor,
    NodeSocketFloat,
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTexImage,
    ShaderNodeTree,
)

from ..json_definitions import CommonMaterial
from ..nodes.diffuse_shader import DiffuseShader
from ..utils import create_node, read_texture


class DiffuseShaderType:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self.create_nodes()

    def get_textures(self, nodes: ShaderNodeGroup) -> None:
        if self.material["textures"].get("Color"):
            img = self.create_image(0, str(self.material["textures"]["Color"]))
            if img.image:
                img.image.colorspace_settings.name = "sRGB"  # pyright: ignore[reportAttributeAccessIssue]
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[0])
            _ = self.tree.links.new(img.outputs[1], nodes.inputs[11])

        if self.material["textures"].get("Control"):
            img = self.create_image(-100, str(self.material["textures"]["Control"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[1])

        if self.material["textures"].get("Normal"):
            img = self.create_image(-200, str(self.material["textures"]["Normal"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[2])

    def create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, DiffuseShader().node_tree)

        if self.material["diffuse_info"]:
            info = self.material["diffuse_info"]

            roughness_white = cast(NodeSocketFloat, shader.inputs[3])
            roughness_white.default_value = info["roughness_white"]

            roughness_black = cast(NodeSocketFloat, shader.inputs[4])
            roughness_black.default_value = info["roughness_black"]

            metallic_white = cast(NodeSocketFloat, shader.inputs[5])
            metallic_white.default_value = info["metallic_white"]

            metallic_black = cast(NodeSocketFloat, shader.inputs[6])
            metallic_black.default_value = info["metallic_black"]

            em_tint = cast(NodeSocketColor, shader.inputs[7])
            em_tint.default_value = (*info["si_color_tint"], 1.0)

            em_intensity = cast(NodeSocketFloat, shader.inputs[9])
            em_intensity.default_value = info["si_intensity"]

            em_amount = cast(NodeSocketFloat, shader.inputs[8])
            em_amount.default_value = info["si_amount"]

            color_tint = cast(NodeSocketColor, shader.inputs[10])
            color_tint.default_value = (*info["color_tint"], 1.0)

            self.get_textures(shader)
            material_output = create_node(self.tree.nodes, 0, 0, ShaderNodeOutputMaterial)
            material_output.target = "ALL"
            material_output.location = (200, 0)
            _ = self.tree.links.new(shader.outputs[0], material_output.inputs[0])

    def create_image(self, y: int, name: str) -> ShaderNodeTexImage:
        texture = create_node(self.tree.nodes, -300, y, ShaderNodeTexImage)
        texture.hide = True
        texture.image = read_texture(name)
        return texture
