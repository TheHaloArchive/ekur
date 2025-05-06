# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeTree,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
    NodeSocketFloat,
)

from ..utils import assign_value, create_node, create_socket

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
        _ = links.new(input.outputs[2], srgb3.inputs[0])
        _ = links.new(input.outputs[1], srgb1.inputs[0])
        _ = links.new(input.outputs[0], srgb2.inputs[0])
        _ = links.new(slot1_2.outputs[2], slot3.inputs[6])
        _ = links.new(srgb1.outputs[0], slot1_2.inputs[0])
        _ = links.new(slot3.outputs[2], slot4.inputs[6])
        _ = links.new(srgb1.outputs[1], slot3.inputs[0])
        _ = links.new(slot4.outputs[2], slot5.inputs[6])
        _ = links.new(srgb1.outputs[2], slot4.inputs[0])
        _ = links.new(slot5.outputs[2], slot6.inputs[6])
        _ = links.new(srgb3.outputs[0], slot5.inputs[0])
        _ = links.new(srgb3.outputs[1], slot6.inputs[0])
        _ = links.new(input.outputs[4], slot1_2.inputs[6])
        _ = links.new(input.outputs[5], slot1_2.inputs[7])
        _ = links.new(input.outputs[6], slot3.inputs[7])
        _ = links.new(input.outputs[7], slot4.inputs[7])
        _ = links.new(input.outputs[8], slot5.inputs[7])
        _ = links.new(input.outputs[9], slot6.inputs[7])
        _ = links.new(input.outputs[3], subtract.inputs[0])
        _ = links.new(subtract.outputs[0], add.inputs[0])
        _ = links.new(srgb2.outputs[2], add.inputs[1])
        _ = links.new(slot7.outputs[2], grime.inputs[6])
        _ = links.new(slot6.outputs[2], slot7.inputs[6])
        _ = links.new(add.outputs[0], grime.inputs[0])
        _ = links.new(srgb3.outputs[2], slot7.inputs[0])
        _ = links.new(input.outputs[10], slot7.inputs[7])
        _ = links.new(input.outputs[11], grime.inputs[7])
        _ = links.new(input.outputs[4], slot1_2.inputs[2])
        _ = links.new(input.outputs[5], slot1_2.inputs[3])
        _ = links.new(slot1_2.outputs[0], slot3.inputs[2])
        _ = links.new(input.outputs[6], slot3.inputs[3])
        _ = links.new(slot3.outputs[0], slot4.inputs[2])
        _ = links.new(input.outputs[7], slot4.inputs[3])
        _ = links.new(slot4.outputs[0], slot5.inputs[2])
        _ = links.new(input.outputs[8], slot5.inputs[3])
        _ = links.new(slot5.outputs[0], slot6.inputs[2])
        _ = links.new(input.outputs[9], slot6.inputs[3])
        _ = links.new(slot6.outputs[0], slot7.inputs[2])
        _ = links.new(input.outputs[10], slot7.inputs[3])
        _ = links.new(slot7.outputs[0], grime.inputs[2])
        _ = links.new(input.outputs[11], grime.inputs[3])
        _ = links.new(grime.outputs[0], output.inputs[0])
