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

__all__ = ["InfiniteColor"]


class InfiniteColor:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Infinite Color")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Infinite Color")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Color", NodeSocketColor, False)
        _ = create_socket(interface, "ASG Control", NodeSocketColor)
        _ = create_socket(interface, "Mask 0", NodeSocketColor)
        _ = create_socket(interface, "Mask 1", NodeSocketColor)
        _ = create_socket(interface, "Slot 1", NodeSocketColor)
        _ = create_socket(interface, "Slot 2", NodeSocketColor)
        _ = create_socket(interface, "Slot 3", NodeSocketColor)
        _ = create_socket(interface, "Slot 4", NodeSocketColor)
        _ = create_socket(interface, "Slot 5", NodeSocketColor)
        _ = create_socket(interface, "Slot 6", NodeSocketColor)
        _ = create_socket(interface, "Grime", NodeSocketColor)
        _ = create_socket(interface, "Dust", NodeSocketColor)
        _ = create_socket(interface, "Scratch", NodeSocketColor)
        _ = create_socket(interface, "Color Override", NodeSocketColor)
        _ = create_socket(interface, "Color Override Toggle", NodeSocketColor)
        _ = create_socket(interface, "Grime Amount", NodeSocketFloat)
        _ = create_socket(interface, "Scratch Amount", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        input = create_node(self.node_tree.nodes, -1253, -12, NodeGroupInput)
        output = create_node(self.node_tree.nodes, 2253, 11, NodeGroupOutput)

        srgb1 = create_node(self.node_tree.nodes, -963, 163, ShaderNodeSeparateColor)
        srgb2 = create_node(self.node_tree.nodes, -980, 344, ShaderNodeSeparateColor)
        srgb3 = create_node(self.node_tree.nodes, -978, 534, ShaderNodeSeparateColor)

        slot1_2 = create_node(self.node_tree.nodes, -883, -9, ShaderNodeMix)
        slot1_2.label = "Slot 1 and 2"
        slot1_2.clamp_factor = True
        slot1_2.data_type = "RGBA"

        slot3 = create_node(self.node_tree.nodes, -668, -11, ShaderNodeMix)
        slot3.label = "Slot 3"
        slot3.clamp_factor = True
        slot3.data_type = "RGBA"

        slot4 = create_node(self.node_tree.nodes, -476, -9, ShaderNodeMix)
        slot4.label = "Slot 4"
        slot4.clamp_factor = True
        slot4.data_type = "RGBA"

        slot5 = create_node(self.node_tree.nodes, -236, -9, ShaderNodeMix)
        slot5.label = "Slot 5"
        slot5.clamp_factor = True
        slot5.data_type = "RGBA"

        slot6 = create_node(self.node_tree.nodes, 3, -9, ShaderNodeMix)
        slot6.label = "Slot 6"
        slot6.clamp_factor = True
        slot6.data_type = "RGBA"

        zone7 = create_node(self.node_tree.nodes, 288, -4, ShaderNodeMix)
        zone7.label = "Zone 7"
        zone7.clamp_factor = True
        zone7.data_type = "RGBA"

        emblem = create_node(self.node_tree.nodes, 509, 3, ShaderNodeMix)
        emblem.label = "Emblem"
        emblem.clamp_factor = True
        emblem.data_type = "RGBA"

        dust = create_node(self.node_tree.nodes, 705, 3, ShaderNodeMix)
        dust.data_type = "RGBA"

        final_mix = create_node(self.node_tree.nodes, 917, 16, ShaderNodeMix)
        final_mix.clamp_result = True
        final_mix.data_type = "RGBA"

        subtract = create_node(self.node_tree.nodes, -613, -604, ShaderNodeMath)
        subtract.operation = "SUBTRACT"
        assign_value(subtract, 1, 1.0)

        subtract2 = create_node(self.node_tree.nodes, -640, -426, ShaderNodeMath)
        subtract2.operation = "SUBTRACT"
        assign_value(subtract2, 1, 1.0)

        math1 = create_node(self.node_tree.nodes, -426, -607, ShaderNodeMath)
        math1.use_clamp = True

        add = create_node(self.node_tree.nodes, -423, -429, ShaderNodeMath)
        add.operation = "ADD"
        add.use_clamp = True

        links = self.node_tree.links
        create_link(links, input, srgb1, 2, 0)
        create_link(links, input, srgb2, 1, 0)
        create_link(links, input, srgb3, 0, 0)
        create_link(links, srgb2, slot1_2, 0, 0)
        create_link(links, srgb2, slot3, 1, 0)
        create_link(links, srgb2, slot4, 2, 0)
        create_link(links, srgb1, slot5, 0, 0)
        create_link(links, srgb1, slot6, 1, 0)
        create_link(links, srgb1, zone7, 2, 0)
        create_link(links, slot1_2, slot3, 2, 6)
        create_link(links, slot3, slot4, 2, 6)
        create_link(links, slot4, slot5, 2, 6)
        create_link(links, slot5, slot6, 2, 6)
        create_link(links, slot6, zone7, 2, 6)
        create_link(links, zone7, emblem, 2, 6)
        create_link(links, emblem, dust, 2, 6)
        create_link(links, dust, final_mix, 2, 6)
        create_link(links, input, slot1_2, 4, 7)
        create_link(links, input, slot3, 5, 7)
        create_link(links, input, slot4, 6, 7)
        create_link(links, input, slot5, 7, 7)
        create_link(links, input, slot6, 8, 7)
        create_link(links, input, final_mix, 9, 7)
        create_link(links, input, zone7, 10, 7)
        create_link(links, input, dust, 11, 7)
        create_link(links, input, emblem, 12, 7)
        create_link(links, input, subtract, 14, 0)
        create_link(links, input, subtract2, 15, 0)
        create_link(links, srgb3, math1, 2, 0)
        create_link(links, subtract, math1, 0, 1)
        create_link(links, subtract2, add, 0, 1)
        create_link(links, srgb3, add, 1, 0)
        create_link(links, input, emblem, 13, 0)
        create_link(links, math1, final_mix, 0, 0)
        create_link(links, final_mix, output, 2, 0)
        create_link(links, input, slot1_2, 3, 6)
        create_link(links, add, dust, 0, 0)
