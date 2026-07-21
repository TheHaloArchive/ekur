# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketFloat,
    NodeSocketVector,
    NodeTree,
    ShaderNodeCombineXYZ,
    ShaderNodeMapping,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeUVMap,
)

from ..utils import assign_value, create_node, create_socket, create_link

__all__ = ["BetterUVScaling"]


class BetterUVScaling:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("BetterUVScaling")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="BetterUVScaling")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Finalized Scale", NodeSocketVector, False)
        _ = create_socket(interface, "Base Scale X", NodeSocketFloat)
        _ = create_socket(interface, "Base Scale Y", NodeSocketFloat)
        _ = create_socket(interface, "Detail Scale X", NodeSocketFloat)
        _ = create_socket(interface, "Detail Scale Y", NodeSocketFloat)
        _ = create_socket(interface, "Alternative Transform X", NodeSocketFloat)
        _ = create_socket(interface, "Alternative Transform Y", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        output = create_node(self.node_tree.nodes, 961, 158, NodeGroupOutput)
        mapping = create_node(self.node_tree.nodes, 796, 250, ShaderNodeMapping)
        combinexyz = create_node(self.node_tree.nodes, 208, 466, ShaderNodeCombineXYZ)
        combinexyz2 = create_node(self.node_tree.nodes, -392, -127, ShaderNodeCombineXYZ)
        input = create_node(self.node_tree.nodes, -972, 0, NodeGroupInput)
        mix = create_node(self.node_tree.nodes, -217, 212, ShaderNodeMix)
        mix2 = create_node(self.node_tree.nodes, 13, 205, ShaderNodeMix)
        add = create_node(self.node_tree.nodes, -15, -136, ShaderNodeMath)

        math_8 = create_node(self.node_tree.nodes, -393, -342, ShaderNodeMath)
        math_8.operation = "WRAP"
        assign_value(math_8, 1, 1.0)
        assign_value(math_8, 2, 0.0)

        subtract = create_node(self.node_tree.nodes, -214, -225, ShaderNodeMath)
        subtract.operation = "SUBTRACT"
        assign_value(subtract, 0, 1.0)

        multiply = create_node(self.node_tree.nodes, -588, -428, ShaderNodeMath)
        multiply.operation = "MULTIPLY"

        multiply2 = create_node(self.node_tree.nodes, -606, -156, ShaderNodeMath)
        multiply2.operation = "MULTIPLY"

        subtract2 = create_node(self.node_tree.nodes, -424, 59, ShaderNodeMath)
        subtract2.operation = "SUBTRACT"
        assign_value(subtract2, 0, 1.0)

        compare = create_node(self.node_tree.nodes, -402, 488, ShaderNodeMath)
        compare.operation = "COMPARE"
        assign_value(compare, 1, 0.5)
        assign_value(compare, 2, 0.0)

        compare2 = create_node(self.node_tree.nodes, -165, 522, ShaderNodeMath)
        compare2.operation = "COMPARE"
        assign_value(compare2, 1, 1.0)
        assign_value(compare2, 2, 0.0)

        uvmap = create_node(self.node_tree.nodes, 215, 134, ShaderNodeUVMap)
        uvmap.uv_map = "UV0"

        links = self.node_tree.links
        create_link(links, math_8, subtract, 0, 1)
        create_link(links, uvmap, mapping, 0, 0)
        create_link(links, combinexyz, mapping, 0, 1)
        create_link(links, multiply, math_8, 0, 0)
        create_link(links, multiply2, combinexyz2, 0, 0)
        create_link(links, multiply, combinexyz2, 0, 1)
        create_link(links, combinexyz2, mapping, 0, 3)
        create_link(links, subtract, add, 0, 1)
        create_link(links, compare, mix, 0, 0)
        create_link(links, subtract2, mix, 0, 6)
        create_link(links, mix, mix2, 2, 6)
        create_link(links, compare2, mix2, 0, 0)
        create_link(links, add, combinexyz, 0, 1)
        create_link(links, input, multiply2, 0, 0)
        create_link(links, input, combinexyz, 4, 0)
        create_link(links, input, subtract2, 5, 1)
        create_link(links, input, compare, 5, 0)
        create_link(links, input, compare2, 5, 0)
        create_link(links, mapping, output, 0, 0)
        create_link(links, input, mix, 5, 7)
        create_link(links, subtract2, mix, 0, 2)
        create_link(links, input, mix, 5, 3)
        create_link(links, mix, mix2, 0, 2)
        create_link(links, input, mix2, 5, 3)
        create_link(links, mix2, add, 0, 0)
        create_link(links, input, multiply2, 2, 1)
        create_link(links, input, multiply, 3, 1)
        create_link(links, input, multiply, 1, 0)
