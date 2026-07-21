# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketShader,
    NodeTree,
    ShaderNodeBsdfPrincipled,
    ShaderNodeBsdfTransparent,
    ShaderNodeInvert,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeMixShader,
    ShaderNodeNewGeometry,
)

from ..utils import assign_value, create_node, create_socket, create_link

__all__ = ["SelfIllum"]


class SelfIllum:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Self-Illumination Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Self-Illumination Shader"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        col = create_socket(interface, "Color Texture", NodeSocketColor)
        col.default_value = (1.0, 1.0, 1.0, 1.0)
        alp = create_socket(interface, "Alpha Texture", NodeSocketColor)
        alp.default_value = (1.0, 1.0, 1.0, 1.0)
        _ = create_socket(interface, "Color", NodeSocketColor)
        _ = create_socket(interface, "Opacity", NodeSocketFloat)
        _ = create_socket(interface, "Intensity", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        input = create_node(nodes, 0, 0, NodeGroupInput)
        output = create_node(nodes, 0, 0, NodeGroupOutput)
        bsdf = create_node(nodes, 0, 0, ShaderNodeBsdfPrincipled)
        mult = create_node(nodes, 0, 0, ShaderNodeMath)
        mult.operation = "MULTIPLY"

        mult_2 = create_node(nodes, 0, 0, ShaderNodeMix)
        mult_2.data_type = "RGBA"
        mult_2.blend_type = "MULTIPLY"
        assign_value(mult_2, 0, 1.0)

        geometry = create_node(nodes, 0, 0, ShaderNodeNewGeometry)
        mix_shader = create_node(nodes, 0, 0, ShaderNodeMixShader)
        transparent = create_node(nodes, 0, 0, ShaderNodeBsdfTransparent)
        invert = create_node(nodes, 0, 0, ShaderNodeInvert)

        links = self.node_tree.links
        create_link(links, input, mult_2, 0, 6)
        create_link(links, input, mult_2, 2, 7)
        create_link(links, mult_2, bsdf, 2, 0)
        create_link(links, mult_2, bsdf, 2, 27)
        create_link(links, input, mult, 1, 0)
        create_link(links, input, mult, 3, 1)
        create_link(links, input, bsdf, 4, 28)
        create_link(links, mult, bsdf, 0, 4)
        create_link(links, geometry, invert, 6, 1)
        create_link(links, invert, mix_shader, 0, 0)
        create_link(links, transparent, mix_shader, 0, 1)
        create_link(links, bsdf, mix_shader, 0, 2)
        create_link(links, mix_shader, output, 0, 0)
