# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import logging
from typing import cast

from bpy.types import (
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTree,
)

from ..json_definitions import CommonMaterial
from ..nodes.color_decal import ColorDecal
from ..utils import assign_value, create_image, create_node, create_link

__all__ = ["ColorDecalShader"]


class ColorDecalShader:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self._create_nodes()

    def _create_nodes(self) -> None:
        shader = create_node(self.tree.nodes, 0, 0, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, ColorDecal().node_tree)

        if not self.material["color_decal"]:
            logging.warning("Color decal material has no color_decal key, this shouldn't happen!")
            return
        info = self.material["color_decal"]
        assign_value(shader, 2, info["roughness"])
        assign_value(shader, 3, info["opacity"])
        assign_value(shader, 4, info["metallic"])

        if self.material["textures"].get("Color"):
            img = create_image(self.tree.nodes, -100, str(self.material["textures"]["Color"]))
            if img.image and img.image.colorspace_settings:
                img.image.colorspace_settings.name = "sRGB"  # ty: ignore[invalid-assignment]
            else:
                logging.warning("Image node does not have image colorspace or image texture!")
                return
            create_link(self.tree.links, img, shader, 0, 0)
            create_link(self.tree.links, img, shader, 1, 1)

        if self.material["textures"].get("AlphaMap"):
            img = create_image(self.tree.nodes, -200, str(self.material["textures"]["AlphaMap"]))
            create_link(self.tree.links, img, shader, 0, 1)

        material_output = create_node(self.tree.nodes, 200, 0, ShaderNodeOutputMaterial)
        create_link(self.tree.links, shader, material_output, 0, 0)
