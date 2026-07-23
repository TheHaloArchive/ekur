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

__all__ = ["InfiniteMaskingSorterNoGrimeCol"]


class InfiniteMaskingSorterNoGrimeCol:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get(
            "Infinite Masking Sorter noGrime Col"
        )
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Infinite Masking Sorter noGrime Col"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Color", NodeSocketColor, False)
        _ = create_socket(interface, "ASG", NodeSocketColor)
        _ = create_socket(interface, "Mask_0", NodeSocketColor)
        _ = create_socket(interface, "Mask_1", NodeSocketColor)
        _ = create_socket(interface, "Grime Amount", NodeSocketFloat)
        _ = create_socket(interface, "Slot 1", NodeSocketColor)
        _ = create_socket(interface, "Slot 2", NodeSocketColor)
        _ = create_socket(interface, "Slot 3", NodeSocketColor)
        _ = create_socket(interface, "Slot 4", NodeSocketColor)
        _ = create_socket(interface, "Slot 5", NodeSocketColor)
        _ = create_socket(interface, "Slot 6", NodeSocketColor)
        _ = create_socket(interface, "Slot 7", NodeSocketColor)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        input = create_node(self.node_tree.nodes, -1320, 140, NodeGroupInput)
        output = create_node(self.node_tree.nodes, 988, 12, NodeGroupOutput)
        srgb1 = create_node(self.node_tree.nodes, -1080, 340, ShaderNodeSeparateColor)
        srgb2 = create_node(self.node_tree.nodes, -1080, 220, ShaderNodeSeparateColor)

        slot1_2 = create_node(self.node_tree.nodes, -760, 120, ShaderNodeMix)
        slot3 = create_node(self.node_tree.nodes, -520, 27, ShaderNodeMix)
        slot4 = create_node(self.node_tree.nodes, -241, -40, ShaderNodeMix)
        slot5 = create_node(self.node_tree.nodes, 10, -100, ShaderNodeMix)
        slot6 = create_node(self.node_tree.nodes, 275, -144, ShaderNodeMix)
        slot7 = create_node(self.node_tree.nodes, 542, -186, ShaderNodeMix)

        for node in [slot1_2, slot3, slot4, slot5, slot6, slot7]:
            node.data_type = "RGBA"
            node.clamp_factor = True

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
        create_link(links, input, slot1_2, 4, 6)
        create_link(links, input, slot1_2, 5, 7)
        create_link(links, input, slot3, 6, 7)
        create_link(links, input, slot4, 7, 7)
        create_link(links, input, slot5, 8, 7)
        create_link(links, input, slot6, 9, 7)
        create_link(links, input, slot7, 10, 7)
        create_link(links, srgb2, slot7, 2, 0)
        create_link(links, slot7, output, 2, 0)
