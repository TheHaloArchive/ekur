# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import (
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    ShaderNodeCombineColor,
    ShaderNodeMath,
    ShaderNodeSeparateColor,
    NodeGroupInput,
)

from ..utils import create_node, create_socket


class MaskToggles:
    def __init__(self) -> None:
        self.node_tree = bpy.data.node_groups.get("Mask Toggles")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Mask Toggles",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        interface = self.node_tree.interface
        _ = create_socket(interface, "Mask_0", NodeSocketColor, False)
        _ = create_socket(interface, "Mask_1", NodeSocketColor, False)
        _ = create_socket(interface, "Mask_0", NodeSocketColor)
        _ = create_socket(interface, "Mask_1", NodeSocketColor)
        _ = create_socket(interface, "Zone 2 Toggle", NodeSocketFloat)
        _ = create_socket(interface, "Zone 3 Toggle", NodeSocketFloat)
        _ = create_socket(interface, "Zone 4 Toggle", NodeSocketFloat)
        _ = create_socket(interface, "Zone 5 Toggle", NodeSocketFloat)
        _ = create_socket(interface, "Zone 6 Toggle", NodeSocketFloat)
        _ = create_socket(interface, "Zone 7 Toggle", NodeSocketFloat)

    def create_nodes(self) -> None:
        nodes = self.node_tree.nodes

        combine_mask0 = create_node(nodes, 575, 5, ShaderNodeCombineColor)
        output = create_node(nodes, 855, -51, NodeGroupOutput)
        group_input = create_node(nodes, -366, -19, NodeGroupInput)

        sep_mask0 = create_node(nodes, -36, 97, ShaderNodeSeparateColor)
        sep_mask1 = create_node(nodes, -102, -288, ShaderNodeSeparateColor)
        combine_mask1 = create_node(nodes, 555, -274, ShaderNodeCombineColor)

        subtract_r = create_node(nodes, 136, 20, ShaderNodeMath)
        subtract_r.operation = "SUBTRACT"
        r: NodeSocketFloat = subtract_r.inputs[1]
        r.default_value = 1.0

        add_r = create_node(nodes, 318, 25, ShaderNodeMath)
        add_r.operation = "ADD"
        add_r.use_clamp = True

        subtract_g = create_node(nodes, 139, -20, ShaderNodeMath)
        subtract_g.operation = "SUBTRACT"
        g: NodeSocketFloat = subtract_g.inputs[1]
        g.default_value = 1.0

        add_g = create_node(nodes, 322, -18, ShaderNodeMath)
        add_g.operation = "ADD"
        add_g.use_clamp = True

        subtract_b = create_node(nodes, 135, -63, ShaderNodeMath)
        subtract_b.operation = "SUBTRACT"
        b: NodeSocketFloat = subtract_b.inputs[1]
        b.default_value = 1.0

        add_b = create_node(nodes, 321, -56, ShaderNodeMath)
        add_b.operation = "ADD"
        add_b.use_clamp = True

        subtract_r2 = create_node(nodes, 119, -285, ShaderNodeMath)
        subtract_r2.operation = "SUBTRACT"
        r2: NodeSocketFloat = subtract_r2.inputs[1]
        r2.default_value = 1.0

        add_r2 = create_node(nodes, 318, -281, ShaderNodeMath)
        add_r2.operation = "ADD"
        add_r2.use_clamp = True

        subtract_g2 = create_node(nodes, 124, -322, ShaderNodeMath)
        subtract_g2.operation = "SUBTRACT"
        g2: NodeSocketFloat = subtract_g2.inputs[1]
        g2.default_value = 1.0

        add_g2 = create_node(nodes, 336, -346, ShaderNodeMath)
        add_g2.operation = "ADD"
        add_g2.use_clamp = True

        subtract_b2 = create_node(nodes, 108, -420, ShaderNodeMath)
        subtract_b2.operation = "SUBTRACT"
        b2: NodeSocketFloat = subtract_b2.inputs[1]
        b2.default_value = 1.0

        add_b2 = create_node(nodes, 336, -424, ShaderNodeMath)
        add_b2.operation = "ADD"
        add_b2.use_clamp = True

        links = self.node_tree.links
        _ = links.new(group_input.outputs[0], sep_mask0.inputs[0])
        _ = links.new(group_input.outputs[1], sep_mask1.inputs[0])
        _ = links.new(combine_mask0.outputs[0], output.inputs[0])
        _ = links.new(combine_mask1.outputs[0], output.inputs[1])
        _ = links.new(subtract_r.outputs[0], add_r.inputs[1])
        _ = links.new(group_input.outputs[2], subtract_r.inputs[0])
        _ = links.new(sep_mask0.outputs[0], add_r.inputs[0])
        _ = links.new(add_r.outputs[0], combine_mask0.inputs[0])
        _ = links.new(subtract_g.outputs[0], add_g.inputs[1])
        _ = links.new(sep_mask0.outputs[1], subtract_g.inputs[0])
        _ = links.new(group_input.outputs[3], add_g.inputs[0])
        _ = links.new(add_g.outputs[0], combine_mask0.inputs[1])
        _ = links.new(subtract_b.outputs[0], add_b.inputs[1])
        _ = links.new(sep_mask0.outputs[2], subtract_b.inputs[0])
        _ = links.new(group_input.outputs[4], add_b.inputs[0])
        _ = links.new(add_b.outputs[0], combine_mask0.inputs[2])
        _ = links.new(subtract_r2.outputs[0], add_r2.inputs[1])
        _ = links.new(sep_mask1.outputs[0], subtract_r2.inputs[0])
        _ = links.new(add_r2.outputs[0], combine_mask1.inputs[0])
        _ = links.new(group_input.outputs[5], add_r2.inputs[0])
        _ = links.new(subtract_g2.outputs[0], add_g2.inputs[1])
        _ = links.new(group_input.outputs[6], subtract_g2.inputs[0])
        _ = links.new(sep_mask1.outputs[1], add_g2.inputs[0])
        _ = links.new(add_g2.outputs[0], combine_mask1.inputs[1])
        _ = links.new(subtract_b2.outputs[0], add_b2.inputs[1])
        _ = links.new(group_input.outputs[7], subtract_b2.inputs[0])
        _ = links.new(sep_mask1.outputs[2], add_b2.inputs[0])
        _ = links.new(add_b2.outputs[0], combine_mask1.inputs[2])
