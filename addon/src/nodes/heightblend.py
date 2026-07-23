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

        create_link(links, math, math_002, 0, 0)
        create_link(links, math_002, math_003, 0, 0)
        create_link(links, math_004, math_005, 0, 0)
        create_link(links, math_005, math_003, 0, 1)
        create_link(links, math_003, clamp, 0, 0)
        create_link(links, group_input, math, 0, 0)
        create_link(links, group_input, math_002, 0, 1)
        create_link(links, group_input, math_004, 0, 0)
        create_link(links, group_input, math, 1, 1)
        create_link(links, clamp, group_output, 0, 0)
        create_link(links, group_input, math_005, 2, 1)
        create_link(links, group_input, math_004, 3, 1)
