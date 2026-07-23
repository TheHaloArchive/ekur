# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeMath,
    ShaderNodeMix,
)

from ..utils import assign_value, create_node, create_socket, create_link

__all__ = ["RoughnessMath"]


class RoughnessMath:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Roughness Math")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Roughness Math")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if not self.node_tree:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Color", NodeSocketColor, False)
        _ = create_socket(interface, "Base", NodeSocketFloat)
        _ = create_socket(interface, "Exponent", NodeSocketFloat)
        _ = create_socket(interface, "Roughness Black", NodeSocketColor)
        _ = create_socket(interface, "Roughness White", NodeSocketColor)

    def create_nodes(self) -> None:
        if not self.node_tree:
            return
        nodes = self.node_tree.nodes
        output = create_node(nodes, 538, 0, NodeGroupOutput)
        input = create_node(nodes, -422, 0, NodeGroupInput)

        multiply = create_node(nodes, 57, 200, ShaderNodeMath)
        multiply.operation = "MULTIPLY"

        divide = create_node(nodes, -90, 15, ShaderNodeMath)
        divide.operation = "DIVIDE"
        assign_value(divide, 1, 4.0)

        multiply2 = create_node(nodes, 73, -132, ShaderNodeMath)
        multiply2.operation = "MULTIPLY"

        mix = create_node(nodes, 272, 40, ShaderNodeMix)
        mix.data_type = "RGBA"

        links = self.node_tree.links
        create_link(links, input, divide, 1, 0)
        create_link(links, divide, multiply, 0, 1)
        create_link(links, input, multiply, 2, 0)
        create_link(links, multiply, mix, 0, 6)
        create_link(links, input, mix, 0, 0)
        create_link(links, multiply2, mix, 0, 7)
        create_link(links, input, multiply2, 3, 0)
        create_link(links, divide, multiply2, 0, 1)
        create_link(links, mix, output, 2, 0)
