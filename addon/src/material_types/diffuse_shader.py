# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from bpy.types import (
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
        self.material = material
        self.tree = material_tree
        self.create_nodes()

    def get_textures(self, nodes: ShaderNodeGroup) -> None:
        if self.material["textures"].get("Color"):
            img = self.create_image(0, str(self.material["textures"]["Color"]))
            img.image.colorspace_settings.name = "sRGB"  # pyright: ignore[reportAttributeAccessIssue]
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[0])

        if self.material["textures"].get("Control"):
            img = self.create_image(-100, str(self.material["textures"]["Control"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[1])

        if self.material["textures"].get("Normal"):
            img = self.create_image(-200, str(self.material["textures"]["Normal"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[2])

    def create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = DiffuseShader().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        if self.material["diffuse_info"]:
            info = self.material["diffuse_info"]

            roughness_white: NodeSocketFloat = shader.inputs[3]
            roughness_white.default_value = info["roughness_white"]

            roughness_black: NodeSocketFloat = shader.inputs[4]
            roughness_black.default_value = info["roughness_black"]

            metallic_white: NodeSocketFloat = shader.inputs[5]
            metallic_white.default_value = info["metallic_white"]

            metallic_black: NodeSocketFloat = shader.inputs[6]
            metallic_black.default_value = info["metallic_black"]

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
