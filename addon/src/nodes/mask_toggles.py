# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeCombineColor,
    ShaderNodeMath,
    ShaderNodeSeparateColor,
)

from ..utils import assign_value, create_node, create_socket, create_link

__all__ = ["MaskToggles"]


class MaskToggles:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Mask Toggles")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Mask Toggles")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if not self.node_tree:
            return
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
        if not self.node_tree:
            return
        nodes = self.node_tree.nodes

        combine_mask0 = create_node(nodes, 575, 5, ShaderNodeCombineColor)
        output = create_node(nodes, 855, -51, NodeGroupOutput)
        group_input = create_node(nodes, -366, -19, NodeGroupInput)

        sep_mask0 = create_node(nodes, -36, 97, ShaderNodeSeparateColor)
        sep_mask1 = create_node(nodes, -102, -288, ShaderNodeSeparateColor)
        combine_mask1 = create_node(nodes, 555, -274, ShaderNodeCombineColor)

        subtract_r = create_node(nodes, 136, 20, ShaderNodeMath)
        subtract_r.operation = "SUBTRACT"
        assign_value(subtract_r, 1, 1.0)

        add_r = create_node(nodes, 318, 25, ShaderNodeMath)
        add_r.operation = "ADD"
        add_r.use_clamp = True

        subtract_g = create_node(nodes, 139, -20, ShaderNodeMath)
        subtract_g.operation = "SUBTRACT"
        assign_value(subtract_g, 1, 1.0)

        add_g = create_node(nodes, 322, -18, ShaderNodeMath)
        add_g.operation = "ADD"
        add_g.use_clamp = True

        subtract_b = create_node(nodes, 135, -63, ShaderNodeMath)
        subtract_b.operation = "SUBTRACT"
        assign_value(subtract_b, 1, 1.0)

        add_b = create_node(nodes, 321, -56, ShaderNodeMath)
        add_b.operation = "ADD"
        add_b.use_clamp = True

        subtract_r2 = create_node(nodes, 119, -285, ShaderNodeMath)
        subtract_r2.operation = "SUBTRACT"
        assign_value(subtract_r2, 1, 1.0)

        add_r2 = create_node(nodes, 318, -281, ShaderNodeMath)
        add_r2.operation = "ADD"
        add_r2.use_clamp = True

        subtract_g2 = create_node(nodes, 124, -322, ShaderNodeMath)
        subtract_g2.operation = "SUBTRACT"
        assign_value(subtract_g2, 1, 1.0)

        add_g2 = create_node(nodes, 336, -346, ShaderNodeMath)
        add_g2.operation = "ADD"
        add_g2.use_clamp = True

        subtract_b2 = create_node(nodes, 108, -420, ShaderNodeMath)
        subtract_b2.operation = "SUBTRACT"
        assign_value(subtract_b2, 1, 1.0)

        add_b2 = create_node(nodes, 336, -424, ShaderNodeMath)
        add_b2.operation = "ADD"
        add_b2.use_clamp = True

        links = self.node_tree.links
        create_link(links, group_input, sep_mask0, 0, 0)
        create_link(links, group_input, sep_mask1, 1, 0)
        create_link(links, combine_mask0, output, 0, 0)
        create_link(links, combine_mask1, output, 0, 1)
        create_link(links, subtract_r, add_r, 0, 1)
        create_link(links, group_input, subtract_r, 2, 0)
        create_link(links, sep_mask0, add_r, 0, 0)
        create_link(links, add_r, combine_mask0, 0, 0)
        create_link(links, subtract_g, add_g, 0, 1)
        create_link(links, sep_mask0, subtract_g, 1, 0)
        create_link(links, group_input, add_g, 3, 0)
        create_link(links, add_g, combine_mask0, 0, 1)
        create_link(links, subtract_b, add_b, 0, 1)
        create_link(links, sep_mask0, subtract_b, 2, 0)
        create_link(links, group_input, add_b, 4, 0)
        create_link(links, add_b, combine_mask0, 0, 2)
        create_link(links, subtract_r2, add_r2, 0, 1)
        create_link(links, sep_mask1, subtract_r2, 0, 0)
        create_link(links, add_r2, combine_mask1, 0, 0)
        create_link(links, group_input, add_r2, 5, 0)
        create_link(links, subtract_g2, add_g2, 0, 1)
        create_link(links, group_input, subtract_g2, 6, 0)
        create_link(links, sep_mask1, add_g2, 1, 0)
        create_link(links, add_g2, combine_mask1, 0, 1)
        create_link(links, subtract_b2, add_b2, 0, 1)
        create_link(links, group_input, subtract_b2, 7, 0)
        create_link(links, sep_mask1, add_b2, 2, 0)
        create_link(links, add_b2, combine_mask1, 0, 2)
