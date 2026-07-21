# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import logging
from typing import cast

from bpy.types import (
    ShaderNodeGroup,
    ShaderNodeMapping,
    ShaderNodeOutputMaterial,
    ShaderNodeTexCoord,
    ShaderNodeTree,
)

from ..json_definitions import CommonMaterial
from ..nodes.skin import Skin
from ..utils import assign_value, create_image, create_node, create_link

__all__ = ["SkinShader"]


class SkinShader:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self._create_nodes()

    def _create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, Skin().node_tree)

        if not self.material["skin"]:
            logging.warning("Skin material has no skin key, this shouldn't happen!")
            return
        info = self.material["skin"]
        assign_value(shader, 6, info["sss_strength"])
        assign_value(shader, 7, info["specular_intensity"])
        assign_value(shader, 8, info["specular_white"])
        assign_value(shader, 9, info["specular_black"])
        assign_value(shader, 10, info["pore_normal_intensity"])
        assign_value(shader, 11, info["micro_normal_intensity"])

        if self.material["textures"].get("Color"):
            img = create_image(self.tree.nodes, -100, str(self.material["textures"]["Color"]))
            if img.image and img.image.colorspace_settings:
                img.image.colorspace_settings.name = "sRGB"  # ty: ignore[invalid-assignment]
            create_link(self.tree.links, img, shader, 0, 0)

        if self.material["textures"].get("Normal"):
            img = create_image(self.tree.nodes, -400, str(self.material["textures"]["Normal"]))
            create_link(self.tree.links, img, shader, 0, 3)

        if self.material["textures"].get("AORoughnessTransmission"):
            img = create_image(
                self.tree.nodes, -200, str(self.material["textures"]["AORoughnessTransmission"])
            )
            create_link(self.tree.links, img, shader, 0, 1)

        if self.material["textures"].get("SpecScatterPore"):
            img = create_image(
                self.tree.nodes, -300, str(self.material["textures"]["SpecScatterPore"])
            )
            create_link(self.tree.links, img, shader, 0, 2)

        if self.material["textures"].get("PoreNormal"):
            img = create_image(self.tree.nodes, -500, str(self.material["textures"]["PoreNormal"]))
            create_link(self.tree.links, img, shader, 0, 4)

        if self.material["textures"].get("DetailNormal"):
            mapping = create_node(self.tree.nodes, 0, 0, ShaderNodeMapping)
            texture_coordinate = create_node(self.tree.nodes, 0, 0, ShaderNodeTexCoord)
            create_link(self.tree.links, texture_coordinate, mapping, 2, 0)
            assign_value(mapping, 3, (*info["micro_normal_scale"], info["micro_normal_scale"][0]))
            img = create_image(
                self.tree.nodes, -600, str(self.material["textures"]["DetailNormal"])
            )
            create_link(self.tree.links, mapping, img, 0, 0)
            create_link(self.tree.links, img, shader, 0, 5)

        material_output = create_node(self.tree.nodes, 200, 0, ShaderNodeOutputMaterial)
        create_link(self.tree.links, shader, material_output, 0, 0)
