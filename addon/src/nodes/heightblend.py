# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeClamp,
    ShaderNodeMath,
)

from ..utils import assign_value, create_node, create_socket

__all__ = ["HeightBlend"]


class HeightBlend:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("HeightBlend")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="HeightBlend")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "HeightBlend", NodeSocketFloat, False)
        _ = create_socket(interface, "Height Scale", NodeSocketFloat)
        _ = create_socket(interface, "Control.Z", NodeSocketFloat)
        _ = create_socket(interface, "LayerWeight", NodeSocketFloat)
        _ = create_socket(interface, "Value", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        links = self.node_tree.links

        math = create_node(nodes, -327, 76, ShaderNodeMath)
        math.operation = "MULTIPLY"
        math.use_clamp = False

        math_002 = create_node(nodes, -128, 90, ShaderNodeMath)
        math_002.operation = "SUBTRACT"
        math_002.use_clamp = False

        math_003 = create_node(nodes, 93, 66, ShaderNodeMath)
        math_003.operation = "ADD"
        math_003.use_clamp = False

        math_004 = create_node(nodes, -331, -90, ShaderNodeMath)
        math_004.operation = "ADD"
        math_004.use_clamp = False

        math_005 = create_node(nodes, -134, -88, ShaderNodeMath)
        math_005.operation = "MULTIPLY"
        math_005.use_clamp = False

        clamp = create_node(nodes, 331, 76, ShaderNodeClamp)
        clamp.clamp_type = "MINMAX"
        assign_value(clamp, 1, 0.0)
        assign_value(clamp, 2, 4.0)

        group_output = create_node(nodes, 521, 0, NodeGroupOutput)
        group_input = create_node(nodes, -623, 1, NodeGroupInput)

        _ = links.new(math.outputs[0], math_002.inputs[0])
        _ = links.new(math_002.outputs[0], math_003.inputs[0])
        _ = links.new(math_004.outputs[0], math_005.inputs[0])
        _ = links.new(math_005.outputs[0], math_003.inputs[1])
        _ = links.new(math_003.outputs[0], clamp.inputs[0])
        _ = links.new(group_input.outputs[0], math.inputs[0])
        _ = links.new(group_input.outputs[0], math_002.inputs[1])
        _ = links.new(group_input.outputs[0], math_004.inputs[0])
        _ = links.new(group_input.outputs[1], math.inputs[1])
        _ = links.new(clamp.outputs[0], group_output.inputs[0])
        _ = links.new(group_input.outputs[2], math_005.inputs[1])
        _ = links.new(group_input.outputs[3], math_004.inputs[1])
