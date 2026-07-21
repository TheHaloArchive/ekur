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
    ShaderNodeMath,
    ShaderNodeMixShader,
    ShaderNodeNewGeometry,
)

from ..utils import create_node, create_socket, create_link

__all__ = ["ColorDecal"]


class ColorDecal:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Color Decal Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Color Decal Shader"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        _ = create_socket(interface, "Color Texture", NodeSocketColor)
        _ = create_socket(interface, "Alpha Map", NodeSocketFloat)
        _ = create_socket(interface, "Roughness", NodeSocketFloat)
        _ = create_socket(interface, "Opacity", NodeSocketFloat)
        _ = create_socket(interface, "Metallic", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        input = create_node(nodes, 0, 0, NodeGroupInput)
        output = create_node(nodes, 0, 0, NodeGroupOutput)

        bsdf = create_node(nodes, 0, 0, ShaderNodeBsdfPrincipled)

        math = create_node(nodes, 0, 0, ShaderNodeMath)
        math.operation = "MULTIPLY"

        geometry = create_node(nodes, 0, 0, ShaderNodeNewGeometry)
        mix_shader = create_node(nodes, 0, 0, ShaderNodeMixShader)
        transparent = create_node(nodes, 0, 0, ShaderNodeBsdfTransparent)

        links = self.node_tree.links
        create_link(links, input, math, 1, 0)
        create_link(links, input, math, 3, 1)
        create_link(links, input, bsdf, 0, 0)
        create_link(links, math, bsdf, 0, 4)
        create_link(links, input, bsdf, 2, 2)
        create_link(links, input, bsdf, 4, 1)
        create_link(links, geometry, mix_shader, 6, 0)
        create_link(links, bsdf, mix_shader, 0, 1)
        create_link(links, transparent, mix_shader, 0, 2)
        create_link(links, mix_shader, output, 0, 0)
