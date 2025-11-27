# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
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

from ..utils import assign_value, create_node, create_socket

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
        _ = links.new(math_8.outputs[0], subtract.inputs[1])
        _ = links.new(uvmap.outputs[0], mapping.inputs[0])
        _ = links.new(combinexyz.outputs[0], mapping.inputs[1])
        _ = links.new(multiply.outputs[0], math_8.inputs[0])
        _ = links.new(multiply2.outputs[0], combinexyz2.inputs[0])
        _ = links.new(multiply.outputs[0], combinexyz2.inputs[1])
        _ = links.new(combinexyz2.outputs[0], mapping.inputs[3])
        _ = links.new(subtract.outputs[0], add.inputs[1])
        _ = links.new(compare.outputs[0], mix.inputs[0])
        _ = links.new(subtract2.outputs[0], mix.inputs[6])
        _ = links.new(mix.outputs[2], mix2.inputs[6])
        _ = links.new(compare2.outputs[0], mix2.inputs[0])
        _ = links.new(add.outputs[0], combinexyz.inputs[1])
        _ = links.new(input.outputs[0], multiply2.inputs[0])
        _ = links.new(input.outputs[4], combinexyz.inputs[0])
        _ = links.new(input.outputs[5], subtract2.inputs[1])
        _ = links.new(input.outputs[5], compare.inputs[0])
        _ = links.new(input.outputs[5], compare2.inputs[0])
        _ = links.new(mapping.outputs[0], output.inputs[0])
        _ = links.new(input.outputs[5], mix.inputs[7])
        _ = links.new(subtract2.outputs[0], mix.inputs[2])
        _ = links.new(input.outputs[5], mix.inputs[3])
        _ = links.new(mix.outputs[0], mix2.inputs[2])
        _ = links.new(input.outputs[5], mix2.inputs[3])
        _ = links.new(mix2.outputs[0], add.inputs[0])
        _ = links.new(input.outputs[2], multiply2.inputs[1])
        _ = links.new(input.outputs[3], multiply.inputs[1])
        _ = links.new(input.outputs[1], multiply.inputs[0])
