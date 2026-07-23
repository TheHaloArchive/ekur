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

from ..utils import assign_value, create_node, create_socket, create_link

__all__ = ["HeightAccumL1"]


class HeightAccumL1:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("HeightAccum L1")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="HeightAccum L1")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Result", NodeSocketFloat, False)
        _ = create_socket(interface, "HeightScale", NodeSocketFloat)
        _ = create_socket(interface, "Control.Z", NodeSocketFloat)
        _ = create_socket(interface, "Layerweight", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        links = self.node_tree.links

        clamp = create_node(nodes, 333, 18, ShaderNodeClamp)
        clamp.clamp_type = "MINMAX"
        assign_value(clamp, 1, 0.0)
        assign_value(clamp, 2, 4.0)

        math = create_node(nodes, -323, 138, ShaderNodeMath)
        math.operation = "MULTIPLY"
        math.use_clamp = False

        math_001 = create_node(nodes, -140, 91, ShaderNodeMath)
        math_001.operation = "SUBTRACT"
        math_001.use_clamp = False

        math_002 = create_node(nodes, 50, 71, ShaderNodeMath)
        math_002.operation = "ADD"
        math_002.use_clamp = False

        math_003 = create_node(nodes, -229, -95, ShaderNodeMath)
        math_003.operation = "MULTIPLY"
        math_003.use_clamp = False

        group_output = create_node(nodes, 523, 0, NodeGroupOutput)
        group_input = create_node(nodes, -695, -5, NodeGroupInput)

        create_link(links, math, math_001, 0, 0)
        create_link(links, math_001, math_002, 0, 0)
        create_link(links, math_003, math_002, 0, 1)
        create_link(links, math_002, clamp, 0, 0)
        create_link(links, group_input, math, 1, 1)
        create_link(links, group_input, math, 0, 0)
        create_link(links, group_input, math_001, 0, 1)
        create_link(links, group_input, math_003, 0, 0)
        create_link(links, group_input, math_003, 2, 1)
        create_link(links, clamp, group_output, 0, 0)
