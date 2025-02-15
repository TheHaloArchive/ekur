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


class InfiniteColor:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Infinite Color")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Infinite Color",
            )
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
        _ = links.new(input.outputs[2], srgb1.inputs[0])
        _ = links.new(input.outputs[1], srgb2.inputs[0])
        _ = links.new(input.outputs[0], srgb3.inputs[0])
        _ = links.new(srgb2.outputs[0], slot1_2.inputs[0])
        _ = links.new(srgb2.outputs[1], slot3.inputs[0])
        _ = links.new(srgb2.outputs[2], slot4.inputs[0])
        _ = links.new(srgb1.outputs[0], slot5.inputs[0])
        _ = links.new(srgb1.outputs[1], slot6.inputs[0])
        _ = links.new(srgb1.outputs[2], zone7.inputs[0])
        _ = links.new(slot1_2.outputs[2], slot3.inputs[6])
        _ = links.new(slot3.outputs[2], slot4.inputs[6])
        _ = links.new(slot4.outputs[2], slot5.inputs[6])
        _ = links.new(slot5.outputs[2], slot6.inputs[6])
        _ = links.new(slot6.outputs[2], zone7.inputs[6])
        _ = links.new(zone7.outputs[2], emblem.inputs[6])
        _ = links.new(emblem.outputs[2], dust.inputs[6])
        _ = links.new(dust.outputs[2], final_mix.inputs[6])
        _ = links.new(input.outputs[4], slot1_2.inputs[7])
        _ = links.new(input.outputs[5], slot3.inputs[7])
        _ = links.new(input.outputs[6], slot4.inputs[7])
        _ = links.new(input.outputs[7], slot5.inputs[7])
        _ = links.new(input.outputs[8], slot6.inputs[7])
        _ = links.new(input.outputs[9], final_mix.inputs[7])
        _ = links.new(input.outputs[10], zone7.inputs[7])
        _ = links.new(input.outputs[11], dust.inputs[7])
        _ = links.new(input.outputs[12], emblem.inputs[7])
        _ = links.new(input.outputs[14], subtract.inputs[0])
        _ = links.new(input.outputs[15], subtract2.inputs[0])
        _ = links.new(srgb3.outputs[2], math1.inputs[0])
        _ = links.new(subtract.outputs[0], math1.inputs[1])
        _ = links.new(subtract2.outputs[0], add.inputs[1])
        _ = links.new(srgb3.outputs[1], add.inputs[0])
        _ = links.new(input.outputs[13], emblem.inputs[0])
        _ = links.new(math1.outputs[0], final_mix.inputs[0])
        _ = links.new(final_mix.outputs[2], output.inputs[0])
        _ = links.new(input.outputs[3], slot1_2.inputs[6])
        _ = links.new(add.outputs[0], dust.inputs[0])
