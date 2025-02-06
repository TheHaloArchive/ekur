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

from ..json_definitions import CommonMaterial
from ..nodes.illum import SelfIllum
from ..utils import create_node, read_texture


class IllumShader:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material = material
        self.tree = material_tree
        self.create_nodes()

    def get_textures(self, nodes: ShaderNodeGroup) -> None:
        col = self.material["textures"].get("Color")
        if col:
            col = self.create_image(-100, str(col))
            _ = self.tree.links.new(col.outputs[0], nodes.inputs[0])

        alpha_map = self.material["textures"].get("AlphaMap")
        if alpha_map:
            img = self.create_image(-200, str(alpha_map))
            if (alpha_map == 10098 or alpha_map == 580203186) and col:
                _ = self.tree.links.new(col.outputs[0], nodes.inputs[1])
            else:
                _ = self.tree.links.new(img.outputs[0], nodes.inputs[1])

    def create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = SelfIllum().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        if self.material["illum_info"]:
            info = self.material["illum_info"]

            opacity: NodeSocketFloat = shader.inputs[3]
            opacity.default_value = info["opacity"]

            color: NodeSocketColor = shader.inputs[2]
            color.default_value = (*info["color"], 1.0)

            intensity: NodeSocketFloat = shader.inputs[4]
            intensity.default_value = info["intensity"]

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
