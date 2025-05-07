# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
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

from ..utils import assign_value, create_node, create_socket

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
        _ = links.new(input.outputs[2], srgb3.inputs[0])
        _ = links.new(input.outputs[1], srgb2.inputs[0])
        _ = links.new(slot1_2.outputs[2], slot3.inputs[6])
        _ = links.new(srgb2.outputs[0], slot1_2.inputs[0])
        _ = links.new(slot3.outputs[2], slot4.inputs[6])
        _ = links.new(srgb2.outputs[1], slot3.inputs[0])
        _ = links.new(slot4.outputs[2], slot5.inputs[6])
        _ = links.new(srgb2.outputs[2], slot4.inputs[0])
        _ = links.new(slot5.outputs[2], slot6.inputs[6])
        _ = links.new(srgb3.outputs[0], slot5.inputs[0])
        _ = links.new(srgb3.outputs[1], slot6.inputs[0])
        _ = links.new(input.outputs[3], slot1_2.inputs[6])
        _ = links.new(input.outputs[4], slot1_2.inputs[7])
        _ = links.new(input.outputs[5], slot3.inputs[7])
        _ = links.new(input.outputs[6], slot4.inputs[7])
        _ = links.new(input.outputs[7], slot5.inputs[7])
        _ = links.new(input.outputs[8], slot6.inputs[7])
        _ = links.new(input.outputs[9], slot7.inputs[7])
        _ = links.new(input.outputs[10], grime.inputs[7])
        _ = links.new(slot7.outputs[2], grime.inputs[6])
        _ = links.new(subtract2.outputs[0], add2.inputs[1])
        _ = links.new(input.outputs[0], srgb1.inputs[0])
        _ = links.new(srgb1.outputs[2], add2.inputs[0])
        _ = links.new(input.outputs[13], subtract2.inputs[0])
        _ = links.new(add2.outputs[0], grime.inputs[0])
        _ = links.new(subtract.outputs[0], add.inputs[1])
        _ = links.new(input.outputs[12], subtract.inputs[0])
        _ = links.new(srgb1.outputs[1], add.inputs[0])
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
        _ = links.new(input.outputs[10], grime.inputs[3])
        _ = links.new(clamp.outputs[0], output.inputs[0])
        _ = links.new(grime.outputs[0], clamp.inputs[0])
        _ = links.new(slot6.outputs[0], slot7.inputs[2])
        _ = links.new(slot7.outputs[0], scratch.inputs[2])
        _ = links.new(scratch.outputs[0], grime.inputs[2])
        _ = links.new(add.outputs[0], scratch.inputs[0])
        _ = links.new(input.outputs[9], slot7.inputs[3])
        _ = links.new(input.outputs[11], scratch.inputs[3])
        _ = links.new(srgb3.outputs[2], slot7.inputs[0])
