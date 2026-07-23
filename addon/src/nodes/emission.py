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

__all__ = ["Emission"]


class Emission:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Emission")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Emission")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Color", NodeSocketFloat, False)
        _ = create_socket(interface, "ASG", NodeSocketColor)
        _ = create_socket(interface, "Mask 0", NodeSocketColor)
        _ = create_socket(interface, "Mask 1", NodeSocketColor)
        _ = create_socket(interface, "Slot 1", NodeSocketFloat)
        _ = create_socket(interface, "Slot 2", NodeSocketFloat)
        _ = create_socket(interface, "Slot 3", NodeSocketFloat)
        _ = create_socket(interface, "Slot 4", NodeSocketFloat)
        _ = create_socket(interface, "Slot 5", NodeSocketFloat)
        _ = create_socket(interface, "Slot 6", NodeSocketFloat)
        _ = create_socket(interface, "Slot 7", NodeSocketFloat)
        _ = create_socket(interface, "Grime", NodeSocketFloat)
        _ = create_socket(interface, "Grime Amount", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        input = create_node(self.node_tree.nodes, -1330, 52, NodeGroupInput)
        output = create_node(self.node_tree.nodes, 1149, -237, NodeGroupOutput)
        srgb1 = create_node(self.node_tree.nodes, -330, 0, ShaderNodeSeparateColor)
        srgb2 = create_node(self.node_tree.nodes, -857, -65, ShaderNodeSeparateColor)
        srgb3 = create_node(self.node_tree.nodes, -857, 153, ShaderNodeSeparateColor)

        slot1_2 = create_node(self.node_tree.nodes, -730, -300, ShaderNodeMix)
        slot1_2.label = "Slot 1 and 2"
        slot1_2.clamp_factor = True

        slot3 = create_node(self.node_tree.nodes, -490, -300, ShaderNodeMix)
        slot3.label = "Slot 3"
        slot3.clamp_factor = True

        slot4 = create_node(self.node_tree.nodes, -250, -300, ShaderNodeMix)
        slot4.label = "Slot 4"
        slot4.clamp_factor = True

        slot5 = create_node(self.node_tree.nodes, -9, -300, ShaderNodeMix)
        slot5.label = "Slot 5"
        slot5.clamp_factor = True

        slot6 = create_node(self.node_tree.nodes, 230, -300, ShaderNodeMix)
        slot6.label = "Slot 6"
        slot6.clamp_factor = True

        slot6_1 = create_node(self.node_tree.nodes, 470, -300, ShaderNodeMix)
        slot6_1.label = "Slot 6"
        slot6_1.clamp_factor = True

        slot7 = create_node(self.node_tree.nodes, 730, -300, ShaderNodeMix)
        slot7.label = "Slot 7"
        slot7.clamp_factor = True

        subtract = create_node(self.node_tree.nodes, -500, -720, ShaderNodeMath)
        subtract.operation = "SUBTRACT"
        assign_value(subtract, 1, 1.0)

        add = create_node(self.node_tree.nodes, -250, -720, ShaderNodeMath)
        add.operation = "ADD"
        add.use_clamp = True

        links = self.node_tree.links
        create_link(links, input, srgb1, 2, 0)
        create_link(links, slot1_2, slot3, 2, 6)
        create_link(links, srgb2, slot1_2, 0, 0)
        create_link(links, slot3, slot4, 2, 6)
        create_link(links, srgb2, slot3, 1, 0)
        create_link(links, slot4, slot5, 2, 6)
        create_link(links, srgb2, slot4, 2, 0)
        create_link(links, slot5, slot6, 2, 6)
        create_link(links, srgb1, slot5, 0, 0)
        create_link(links, srgb1, slot6, 1, 0)
        create_link(links, input, slot1_2, 3, 6)
        create_link(links, input, slot1_2, 4, 7)
        create_link(links, input, slot3, 5, 7)
        create_link(links, input, slot4, 6, 7)
        create_link(links, input, slot5, 7, 7)
        create_link(links, input, slot6, 8, 7)
        create_link(links, input, slot7, 9, 7)
        create_link(links, input, srgb2, 1, 0)
        create_link(links, slot6_1, slot7, 2, 6)
        create_link(links, slot6, slot6_1, 2, 6)
        create_link(links, input, slot6_1, 10, 7)
        create_link(links, subtract, add, 0, 1)
        create_link(links, input, subtract, 11, 0)
        create_link(links, add, slot6_1, 0, 0)
        create_link(links, input, srgb3, 0, 0)
        create_link(links, srgb3, add, 2, 0)
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
        create_link(links, slot6, slot6_1, 0, 2)
        create_link(links, input, slot6_1, 10, 3)
        create_link(links, slot6_1, slot7, 0, 2)
        create_link(links, input, slot7, 9, 3)
        create_link(links, slot7, output, 0, 0)
        create_link(links, srgb1, slot7, 2, 0)
