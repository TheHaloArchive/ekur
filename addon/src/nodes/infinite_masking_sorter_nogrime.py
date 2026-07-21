# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
)

from ..utils import create_node, create_socket, create_link

__all__ = ["InfiniteMaskingSorterNoGrime"]


class InfiniteMaskingSorterNoGrime:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get(
            "Infinite Masking Sorter noGrime"
        )
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Infinite Masking Sorter noGrime"
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
        _ = create_socket(interface, "Slot 1", NodeSocketFloat)
        _ = create_socket(interface, "Slot 2", NodeSocketFloat)
        _ = create_socket(interface, "Slot 3", NodeSocketFloat)
        _ = create_socket(interface, "Slot 4", NodeSocketFloat)
        _ = create_socket(interface, "Slot 5", NodeSocketFloat)
        _ = create_socket(interface, "Slot 6", NodeSocketFloat)
        _ = create_socket(interface, "Slot 7", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        input = create_node(self.node_tree.nodes, -1320, 140, NodeGroupInput)
        output = create_node(self.node_tree.nodes, 838, -165, NodeGroupOutput)
        srgb1 = create_node(self.node_tree.nodes, -1080, 340, ShaderNodeSeparateColor)
        srgb2 = create_node(self.node_tree.nodes, -1080, 220, ShaderNodeSeparateColor)

        slot1_2 = create_node(self.node_tree.nodes, -817, 105, ShaderNodeMix)
        slot3 = create_node(self.node_tree.nodes, -520, 20, ShaderNodeMix)
        slot4 = create_node(self.node_tree.nodes, -250, -66, ShaderNodeMix)
        slot5 = create_node(self.node_tree.nodes, 0, -140, ShaderNodeMix)
        slot6 = create_node(self.node_tree.nodes, 240, -220, ShaderNodeMix)
        slot7 = create_node(self.node_tree.nodes, 567, -155, ShaderNodeMix)

        links = self.node_tree.links
        create_link(links, input, srgb2, 2, 0)
        create_link(links, input, srgb1, 1, 0)
        create_link(links, slot1_2, slot3, 2, 6)
        create_link(links, srgb1, slot1_2, 0, 0)
        create_link(links, slot3, slot4, 2, 6)
        create_link(links, srgb1, slot3, 1, 0)
        create_link(links, slot4, slot5, 2, 6)
        create_link(links, srgb1, slot4, 2, 0)
        create_link(links, slot5, slot6, 2, 6)
        create_link(links, srgb2, slot5, 0, 0)
        create_link(links, srgb2, slot6, 1, 0)
        create_link(links, slot6, slot7, 2, 6)
        create_link(links, input, slot1_2, 3, 6)
        create_link(links, input, slot1_2, 4, 7)
        create_link(links, input, slot3, 5, 7)
        create_link(links, input, slot4, 6, 7)
        create_link(links, input, slot5, 7, 7)
        create_link(links, input, slot6, 8, 7)
        create_link(links, input, slot7, 9, 7)
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
        create_link(links, slot6, slot7, 0, 2)
        create_link(links, input, slot7, 9, 3)
        create_link(links, srgb2, slot7, 2, 0)
        create_link(links, slot7, output, 0, 0)
