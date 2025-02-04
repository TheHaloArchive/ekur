# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
)

from ..utils import create_node, create_socket


class InfiniteMaskingSorterNoGrimeCol:
    def __init__(self) -> None:
        self.node_tree = bpy.data.node_groups.get("Infinite Masking Sorter noGrime Col")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Infinite Masking Sorter noGrime Col",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
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

    def create_nodes(self) -> None:
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
        _ = links.new(input.outputs[2], srgb2.inputs[0])
        _ = links.new(input.outputs[1], srgb1.inputs[0])
        _ = links.new(slot1_2.outputs[2], slot3.inputs[6])
        _ = links.new(srgb1.outputs[0], slot1_2.inputs[0])
        _ = links.new(slot3.outputs[2], slot4.inputs[6])
        _ = links.new(srgb1.outputs[1], slot3.inputs[0])
        _ = links.new(slot4.outputs[2], slot5.inputs[6])
        _ = links.new(srgb1.outputs[2], slot4.inputs[0])
        _ = links.new(slot5.outputs[2], slot6.inputs[6])
        _ = links.new(srgb2.outputs[0], slot5.inputs[0])
        _ = links.new(srgb2.outputs[1], slot6.inputs[0])
        _ = links.new(slot6.outputs[2], slot7.inputs[6])
        _ = links.new(input.outputs[4], slot1_2.inputs[6])
        _ = links.new(input.outputs[5], slot1_2.inputs[7])
        _ = links.new(input.outputs[6], slot3.inputs[7])
        _ = links.new(input.outputs[7], slot4.inputs[7])
        _ = links.new(input.outputs[8], slot5.inputs[7])
        _ = links.new(input.outputs[9], slot6.inputs[7])
        _ = links.new(input.outputs[10], slot7.inputs[7])
        _ = links.new(srgb2.outputs[2], slot7.inputs[0])
        _ = links.new(slot7.outputs[2], output.inputs[0])
