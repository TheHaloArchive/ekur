# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
)

from ..utils import create_node, create_socket


class Emission:
    def __init__(self) -> None:
        self.node_tree = bpy.data.node_groups.get("Emission")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Emission",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
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
        _: NodeSocketFloat = subtract.inputs[1]
        _.default_value = 1.0

        add = create_node(self.node_tree.nodes, -250, -720, ShaderNodeMath)
        add.operation = "ADD"
        add.use_clamp = True

        links = self.node_tree.links
        _ = links.new(input.outputs[2], srgb1.inputs[0])
        _ = links.new(slot1_2.outputs[2], slot3.inputs[6])
        _ = links.new(srgb2.outputs[0], slot1_2.inputs[0])
        _ = links.new(slot3.outputs[2], slot4.inputs[6])
        _ = links.new(srgb2.outputs[1], slot3.inputs[0])
        _ = links.new(slot4.outputs[2], slot5.inputs[6])
        _ = links.new(srgb2.outputs[2], slot4.inputs[0])
        _ = links.new(slot5.outputs[2], slot6.inputs[6])
        _ = links.new(srgb1.outputs[0], slot5.inputs[0])
        _ = links.new(srgb1.outputs[1], slot6.inputs[0])
        _ = links.new(input.outputs[3], slot1_2.inputs[6])
        _ = links.new(input.outputs[4], slot1_2.inputs[7])
        _ = links.new(input.outputs[5], slot3.inputs[7])
        _ = links.new(input.outputs[6], slot4.inputs[7])
        _ = links.new(input.outputs[7], slot5.inputs[7])
        _ = links.new(input.outputs[8], slot6.inputs[7])
        _ = links.new(input.outputs[9], slot7.inputs[7])
        _ = links.new(input.outputs[1], srgb2.inputs[0])
        _ = links.new(slot6_1.outputs[2], slot7.inputs[6])
        _ = links.new(slot6.outputs[2], slot6_1.inputs[6])
        _ = links.new(input.outputs[10], slot6_1.inputs[7])
        _ = links.new(subtract.outputs[0], add.inputs[1])
        _ = links.new(input.outputs[11], subtract.inputs[0])
        _ = links.new(add.outputs[0], slot6_1.inputs[0])
        _ = links.new(input.outputs[0], srgb3.inputs[0])
        _ = links.new(srgb3.outputs[2], add.inputs[0])
        _ = links.new(input.outputs[3], slot1_2.inputs[2])
        _ = links.new(input.outputs[4], slot1_2.inputs[3])
        _ = links.new(slot1_2.outputs[0], slot3.inputs[2])
        _ = links.new(input.outputs[5], slot3.inputs[3])
        _ = links.new(slot3.outputs[0], slot4.inputs[2])
        _ = links.new(input.outputs[6], slot4.inputs[3])
        _ = links.new(slot4.outputs[0], slot5.inputs[2])
        _ = links.new(input.outputs[7], slot5.inputs[3])
        _ = links.new(slot5.outputs[0], slot6.inputs[2])
        _ = links.new(input.outputs[8], slot6.inputs[3])
        _ = links.new(slot6.outputs[0], slot6_1.inputs[2])
        _ = links.new(input.outputs[10], slot6_1.inputs[3])
        _ = links.new(slot6_1.outputs[0], slot7.inputs[2])
        _ = links.new(input.outputs[9], slot7.inputs[3])
        _ = links.new(slot7.outputs[0], output.inputs[0])
        _ = links.new(srgb1.outputs[2], slot7.inputs[0])
