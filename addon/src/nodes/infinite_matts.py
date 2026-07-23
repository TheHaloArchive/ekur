# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeClamp,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
)

from ..utils import assign_value, create_node, create_socket, create_link

__all__ = ["InfiniteMatts"]


class InfiniteMatts:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Infinite Matts")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Infinite Matts")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Color", NodeSocketFloat, False)
        _ = create_socket(interface, "ASG Control", NodeSocketColor)
        _ = create_socket(interface, "RGB Control", NodeSocketColor)
        _ = create_socket(interface, "Blue Control", NodeSocketColor)
        _ = create_socket(interface, "Slot 1", NodeSocketFloat)
        _ = create_socket(interface, "Slot 2", NodeSocketFloat)
        _ = create_socket(interface, "Slot 3", NodeSocketFloat)
        _ = create_socket(interface, "Slot 4", NodeSocketFloat)
        _ = create_socket(interface, "Slot 5", NodeSocketFloat)
        _ = create_socket(interface, "Slot 6", NodeSocketFloat)
        _ = create_socket(interface, "Slot 7", NodeSocketFloat)
        _ = create_socket(interface, "Grime", NodeSocketFloat)
        _ = create_socket(interface, "Scratch", NodeSocketFloat)
        _ = create_socket(interface, "Scratch Amount", NodeSocketFloat)
        _ = create_socket(interface, "Grime Amount", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        slot1_2 = create_node(self.node_tree.nodes, -708, 11, ShaderNodeMix)
        slot1_2.clamp_factor = False
        slot3 = create_node(self.node_tree.nodes, -490, 11, ShaderNodeMix)
        slot4 = create_node(self.node_tree.nodes, -249, 11, ShaderNodeMix)
        slot5 = create_node(self.node_tree.nodes, -10, 11, ShaderNodeMix)
        slot6 = create_node(self.node_tree.nodes, 231, 11, ShaderNodeMix)
        slot7 = create_node(self.node_tree.nodes, 427, 11, ShaderNodeMix)
        scratch = create_node(self.node_tree.nodes, 640, 11, ShaderNodeMix)
        scratch.clamp_factor = False
        grime = create_node(self.node_tree.nodes, 880, -50, ShaderNodeMix)
        input = create_node(self.node_tree.nodes, -1130, -250, NodeGroupInput)
        output = create_node(self.node_tree.nodes, 1368, 11, NodeGroupOutput)
        srgb1 = create_node(self.node_tree.nodes, -915, 310, ShaderNodeSeparateColor)
        srgb2 = create_node(self.node_tree.nodes, -915, -150, ShaderNodeSeparateColor)
        srgb3 = create_node(self.node_tree.nodes, -615, -270, ShaderNodeSeparateColor)

        clamp = create_node(self.node_tree.nodes, 1134, 11, ShaderNodeClamp)
        clamp.clamp_type = "MINMAX"
        assign_value(clamp, 1, 0.0)
        assign_value(clamp, 2, 1.0)

        add = create_node(self.node_tree.nodes, -436, -718, ShaderNodeMath)
        add.use_clamp = True
        assign_value(add, 2, 0.5)

        subtract = create_node(self.node_tree.nodes, -700, -710, ShaderNodeMath)
        subtract.operation = "SUBTRACT"
        assign_value(subtract, 1, 1.0)

        subtract2 = create_node(self.node_tree.nodes, -700, -900, ShaderNodeMath)
        subtract2.operation = "SUBTRACT"
        assign_value(subtract2, 1, 1.0)

        add2 = create_node(self.node_tree.nodes, -450, -900, ShaderNodeMath)
        add2.use_clamp = True

        links = self.node_tree.links
        create_link(links, input, srgb3, 2, 0)
        create_link(links, input, srgb2, 1, 0)
        create_link(links, slot1_2, slot3, 2, 6)
        create_link(links, srgb2, slot1_2, 0, 0)
        create_link(links, slot3, slot4, 2, 6)
        create_link(links, srgb2, slot3, 1, 0)
        create_link(links, slot4, slot5, 2, 6)
        create_link(links, srgb2, slot4, 2, 0)
        create_link(links, slot5, slot6, 2, 6)
        create_link(links, srgb3, slot5, 0, 0)
        create_link(links, srgb3, slot6, 1, 0)
        create_link(links, input, slot1_2, 3, 6)
        create_link(links, input, slot1_2, 4, 7)
        create_link(links, input, slot3, 5, 7)
        create_link(links, input, slot4, 6, 7)
        create_link(links, input, slot5, 7, 7)
        create_link(links, input, slot6, 8, 7)
        create_link(links, input, slot7, 9, 7)
        create_link(links, input, grime, 10, 7)
        create_link(links, slot7, grime, 2, 6)
        create_link(links, subtract2, add2, 0, 1)
        create_link(links, input, srgb1, 0, 0)
        create_link(links, srgb1, add2, 2, 0)
        create_link(links, input, subtract2, 13, 0)
        create_link(links, add2, grime, 0, 0)
        create_link(links, subtract, add, 0, 1)
        create_link(links, input, subtract, 12, 0)
        create_link(links, srgb1, add, 1, 0)
        create_link(links, input, slot1_2, 3, 2)
        create_link(links, input, slot1_2, 4, 3)
        create_link(links, slot1_2, slot3, 0, 2)
        create_link(links, input, slot3, 5, 3)
        create_link(links, slot3, slot4, 0, 2)
        create_link(links, input, slot4, 6, 3)
        create_link(links, slot4, slot5, 0, 2)
        create_link(links, input, slot5, 7, 3)
        create_link(links, slot5, slot6, 0, 2)
        create_link(links, input, slot6, 8, 3)
        create_link(links, input, grime, 10, 3)
        create_link(links, clamp, output, 0, 0)
        create_link(links, grime, clamp, 0, 0)
        create_link(links, slot6, slot7, 0, 2)
        create_link(links, slot7, scratch, 0, 2)
        create_link(links, scratch, grime, 0, 2)
        create_link(links, add, scratch, 0, 0)
        create_link(links, input, slot7, 9, 3)
        create_link(links, input, scratch, 11, 3)
        create_link(links, srgb3, slot7, 2, 0)
