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

from ..utils import assign_value, create_node, create_socket, create_link

__all__ = ["FloatBlend"]


class FloatBlend:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Float Blend")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Float Blend")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Result", NodeSocketFloat, False)
        _ = create_socket(interface, "MacroMask Color", NodeSocketColor)
        _ = create_socket(interface, "MacroMask Alpha", NodeSocketFloat)
        _ = create_socket(interface, "Macro Control Base", NodeSocketFloat)
        _ = create_socket(interface, "Macro Control Base Intensity", NodeSocketFloat)
        _ = create_socket(interface, "Layer 1 Data", NodeSocketFloat)
        _ = create_socket(interface, "Layer 2 Data", NodeSocketFloat)
        _ = create_socket(interface, "Layer 3 Data", NodeSocketFloat)
        _ = create_socket(interface, "Layer 4 Data", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        links = self.node_tree.links

        group_output = create_node(nodes, 1797, 167, NodeGroupOutput)
        group_input = create_node(nodes, -660, 0, NodeGroupInput)

        separate_color = create_node(nodes, -483, 121, ShaderNodeSeparateColor)
        separate_color.mode = "RGB"

        mix = create_node(nodes, 134, 39, ShaderNodeMix)
        mix.blend_type = "MIX"
        mix.clamp_factor = True
        mix.clamp_result = False
        mix.data_type = "FLOAT"
        mix.factor_mode = "UNIFORM"
        assign_value(mix, 2, 0.5)

        mix_002 = create_node(nodes, 323, 42, ShaderNodeMix)
        mix_002.blend_type = "MIX"
        mix_002.clamp_factor = True
        mix_002.clamp_result = False
        mix_002.data_type = "FLOAT"
        mix_002.factor_mode = "UNIFORM"

        mix_003 = create_node(nodes, 514, 26, ShaderNodeMix)
        mix_003.blend_type = "MIX"
        mix_003.clamp_factor = True
        mix_003.clamp_result = False
        mix_003.data_type = "FLOAT"
        mix_003.factor_mode = "UNIFORM"

        mix_004 = create_node(nodes, 703, 35, ShaderNodeMix)
        mix_004.blend_type = "MIX"
        mix_004.clamp_factor = True
        mix_004.clamp_result = False
        mix_004.data_type = "FLOAT"
        mix_004.factor_mode = "UNIFORM"

        mix_005 = create_node(nodes, 902, 35, ShaderNodeMix)
        mix_005.blend_type = "OVERLAY"
        mix_005.clamp_factor = True
        mix_005.clamp_result = False
        mix_005.data_type = "RGBA"
        assign_value(mix_005, 0, 1.0)

        mix_006 = create_node(nodes, 902, 35, ShaderNodeMix)
        mix_006.blend_type = "MIX"
        mix_006.clamp_factor = True
        mix_006.clamp_result = False
        mix_006.data_type = "RGBA"

        create_link(links, group_input, separate_color, 0, 0)
        create_link(links, group_input, mix, 4, 3)
        create_link(links, mix, mix_002, 0, 2)
        create_link(links, group_input, mix_002, 5, 3)
        create_link(links, mix_002, mix_003, 0, 2)
        create_link(links, group_input, mix_003, 6, 3)
        create_link(links, mix_003, mix_004, 0, 2)
        create_link(links, group_input, mix_004, 7, 3)
        create_link(links, separate_color, mix, 0, 0)
        create_link(links, separate_color, mix_002, 1, 0)
        create_link(links, separate_color, mix_003, 2, 0)
        create_link(links, group_input, mix_004, 1, 0)
        create_link(links, group_input, mix_005, 2, 6)
        create_link(links, mix_004, mix_005, 0, 7)
        create_link(links, group_input, mix_006, 3, 0)
        create_link(links, mix_004, mix_006, 0, 6)
        create_link(links, mix_005, mix_006, 2, 7)
        create_link(links, mix_006, group_output, 2, 0)
