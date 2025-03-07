# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import cast
from bpy.types import (
    ShaderNodeGroup,
    ShaderNodeMapping,
    ShaderNodeOutputMaterial,
    ShaderNodeTexCoord,
    ShaderNodeTexImage,
    ShaderNodeTree,
)

from ..nodes.skin import Skin
from ..utils import assign_value, create_node, read_texture
from ..json_definitions import CommonMaterial

__all__ = ["SkinShader"]


class SkinShader:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self._create_nodes()

    def _create_image(self, y: int, name: str) -> ShaderNodeTexImage:
        texture = create_node(self.tree.nodes, -300, y, ShaderNodeTexImage)
        texture.hide = True
        texture.image = read_texture(name)
        return texture

    def _create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, Skin().node_tree)

        if self.material["skin"]:
            info = self.material["skin"]
            assign_value(shader, 6, info["sss_strength"])
            assign_value(shader, 7, info["specular_intensity"])
            assign_value(shader, 8, info["specular_white"])
            assign_value(shader, 9, info["specular_black"])
            assign_value(shader, 10, info["pore_normal_intensity"])
            assign_value(shader, 11, info["micro_normal_intensity"])

            if self.material["textures"].get("Color"):
                img = self._create_image(-100, str(self.material["textures"]["Color"]))
                if img.image:
                    img.image.colorspace_settings.name = "sRGB"  # pyright: ignore[reportAttributeAccessIssue]
                _ = self.tree.links.new(img.outputs[0], shader.inputs[0])

            if self.material["textures"].get("Normal"):
                img = self._create_image(-400, str(self.material["textures"]["Normal"]))
                _ = self.tree.links.new(img.outputs[0], shader.inputs[3])

            if self.material["textures"].get("AORoughnessTransmission"):
                img = self._create_image(
                    -200, str(self.material["textures"]["AORoughnessTransmission"])
                )
                _ = self.tree.links.new(img.outputs[0], shader.inputs[1])

            if self.material["textures"].get("SpecScatterPore"):
                img = self._create_image(-300, str(self.material["textures"]["SpecScatterPore"]))
                _ = self.tree.links.new(img.outputs[0], shader.inputs[2])

            if self.material["textures"].get("PoreNormal"):
                img = self._create_image(-500, str(self.material["textures"]["PoreNormal"]))
                _ = self.tree.links.new(img.outputs[0], shader.inputs[4])

            if self.material["textures"].get("DetailNormal"):
                mapping = create_node(self.tree.nodes, 0, 0, ShaderNodeMapping)
                texture_coordinate = create_node(self.tree.nodes, 0, 0, ShaderNodeTexCoord)
                _ = self.tree.links.new(texture_coordinate.outputs[2], mapping.inputs[0])
                assign_value(
                    mapping,
                    3,
                    (
                        info["micro_normal_scale"][0],
                        info["micro_normal_scale"][1],
                        info["micro_normal_scale"][0],
                    ),
                )
                img = self._create_image(-600, str(self.material["textures"]["DetailNormal"]))
                _ = self.tree.links.new(mapping.outputs[0], img.inputs[0])
                _ = self.tree.links.new(img.outputs[0], shader.inputs[5])

            material_output = create_node(self.tree.nodes, 200, 0, ShaderNodeOutputMaterial)
            _ = self.tree.links.new(shader.outputs[0], material_output.inputs[0])
