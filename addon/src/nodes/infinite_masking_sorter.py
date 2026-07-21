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
    ShaderNodeSeparateColor,
)

from ..utils import assign_value, create_node, create_socket, create_link

__all__ = ["InfiniteMaskingSorter"]


class InfiniteMaskingSorter:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Infinite Masking Sorter")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Infinite Masking Sorter"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Color", NodeSocketFloat, False)
        _ = create_socket(interface, "ASG", NodeSocketColor)
        _ = create_socket(interface, "Mask_0", NodeSocketColor)
        _ = create_socket(interface, "Mask_1", NodeSocketColor)
        _ = create_socket(interface, "Grime Amount", NodeSocketFloat)
        _ = create_socket(interface, "Slot 1", NodeSocketFloat)
        _ = create_socket(interface, "Slot 2", NodeSocketFloat)
        _ = create_socket(interface, "Slot 3", NodeSocketFloat)
        _ = create_socket(interface, "Slot 4", NodeSocketFloat)
        _ = create_socket(interface, "Slot 5", NodeSocketFloat)
        _ = create_socket(interface, "Slot 6", NodeSocketFloat)
        _ = create_socket(interface, "Slot 7", NodeSocketFloat)
        _ = create_socket(interface, "Grime", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        input = create_node(self.node_tree.nodes, -1320, 140, NodeGroupInput)
        output = create_node(self.node_tree.nodes, 967, -89, NodeGroupOutput)

        srgb1 = create_node(self.node_tree.nodes, -1080, 340, ShaderNodeSeparateColor)
        srgb2 = create_node(self.node_tree.nodes, -1080, 460, ShaderNodeSeparateColor)
        srgb3 = create_node(self.node_tree.nodes, -1080, 220, ShaderNodeSeparateColor)

        subtract = create_node(self.node_tree.nodes, -271, 502, ShaderNodeMath)
        subtract.operation = "SUBTRACT"
        assign_value(subtract, 1, 1.0)

        add = create_node(self.node_tree.nodes, -41, 500, ShaderNodeMath)
        add.operation = "ADD"
        add.use_clamp = True

        slot1_2 = create_node(self.node_tree.nodes, -760, 120, ShaderNodeMix)
        slot1_2.label = "Slot 1 and 2"

        slot3 = create_node(self.node_tree.nodes, -520, 20, ShaderNodeMix)
        slot3.label = "Slot 3"

        slot4 = create_node(self.node_tree.nodes, -250, -67, ShaderNodeMix)
        slot4.label = "Slot 4"

        slot5 = create_node(self.node_tree.nodes, -31, -223, ShaderNodeMix)
        slot5.label = "Slot 5"

        slot6 = create_node(self.node_tree.nodes, 232, -180, ShaderNodeMix)
        slot6.label = "Slot 6"

        slot7 = create_node(self.node_tree.nodes, 452, -194, ShaderNodeMix)
        slot7.label = "Slot 7"

        grime = create_node(self.node_tree.nodes, 712, -100, ShaderNodeMix)
        grime.label = "Grime"
        grime.clamp_factor = True
        grime.clamp_result = True

        links = self.node_tree.links
        create_link(links, input, srgb3, 2, 0)
        create_link(links, input, srgb1, 1, 0)
        create_link(links, input, srgb2, 0, 0)
        create_link(links, slot1_2, slot3, 2, 6)
        create_link(links, srgb1, slot1_2, 0, 0)
        create_link(links, slot3, slot4, 2, 6)
        create_link(links, srgb1, slot3, 1, 0)
        create_link(links, slot4, slot5, 2, 6)
        create_link(links, srgb1, slot4, 2, 0)
        create_link(links, slot5, slot6, 2, 6)
        create_link(links, srgb3, slot5, 0, 0)
        create_link(links, srgb3, slot6, 1, 0)
        create_link(links, input, slot1_2, 4, 6)
        create_link(links, input, slot1_2, 5, 7)
        create_link(links, input, slot3, 6, 7)
        create_link(links, input, slot4, 7, 7)
        create_link(links, input, slot5, 8, 7)
        create_link(links, input, slot6, 9, 7)
        create_link(links, input, subtract, 3, 0)
        create_link(links, subtract, add, 0, 0)
        create_link(links, srgb2, add, 2, 1)
        create_link(links, slot7, grime, 2, 6)
        create_link(links, slot6, slot7, 2, 6)
        create_link(links, add, grime, 0, 0)
        create_link(links, srgb3, slot7, 2, 0)
        create_link(links, input, slot7, 10, 7)
        create_link(links, input, grime, 11, 7)
        create_link(links, input, slot1_2, 4, 2)
        create_link(links, input, slot1_2, 5, 3)
        create_link(links, slot1_2, slot3, 0, 2)
        create_link(links, input, slot3, 6, 3)
        create_link(links, slot3, slot4, 0, 2)
        create_link(links, input, slot4, 7, 3)
        create_link(links, slot4, slot5, 0, 2)
        create_link(links, input, slot5, 8, 3)
        create_link(links, slot5, slot6, 0, 2)
        create_link(links, input, slot6, 9, 3)
        create_link(links, slot6, slot7, 0, 2)
        create_link(links, input, slot7, 10, 3)
        create_link(links, slot7, grime, 0, 2)
        create_link(links, input, grime, 11, 3)
        create_link(links, grime, output, 0, 0)
