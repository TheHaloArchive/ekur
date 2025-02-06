# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from bpy.types import (
    NodeSocketColor,
    NodeSocketFloat,
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTexImage,
    ShaderNodeTree,
)

from ..nodes.decal import Decal

from ..utils import create_node, read_texture
from ..json_definitions import CommonMaterial


class DecalShader:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material = material
        self.tree = material_tree
        self.create_nodes()

    def get_textures(self, nodes: ShaderNodeGroup) -> None:
        if self.material["textures"].get("ControlTexture"):
            img = self.create_image(-100, str(self.material["textures"]["ControlTexture"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[0])

        if self.material["textures"].get("Normal"):
            img = self.create_image(-200, str(self.material["textures"]["Normal"]))
            _ = self.tree.links.new(img.outputs[0], nodes.inputs[1])

    def create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = Decal().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        if self.material["decal_slots"]:
            info = self.material["decal_slots"]

            top_color: NodeSocketColor = shader.inputs[4]
            top_color.default_value = (*info["top_color"], 1.0)
            mid_color: NodeSocketColor = shader.inputs[3]
            mid_color.default_value = (*info["mid_color"], 1.0)
            bot_color: NodeSocketColor = shader.inputs[2]
            bot_color.default_value = (*info["bot_color"], 1.0)

            roughness_white: NodeSocketFloat = shader.inputs[5]
            roughness_white.default_value = info["roughness_white"]

            roughness_black: NodeSocketFloat = shader.inputs[6]
            roughness_black.default_value = info["roughness_black"]

            metallic: NodeSocketFloat = shader.inputs[7]
            metallic.default_value = info["metallic"]

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
