# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import cast

import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketVector,
    NodeTree,
    ShaderNodeCombineColor,
    ShaderNodeCombineXYZ,
    ShaderNodeGroup,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
    ShaderNodeTree,
)

from ..utils import assign_value, create_node, create_socket, create_link
from .color_mixer import ColorMixer

__all__ = ["NnhgShader"]


class NnhgShader:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("NNHG SHADER")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="NNHG SHADER")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Color", NodeSocketColor, False)
        _ = create_socket(interface, "Roughness", NodeSocketFloat, False)
        _ = create_socket(interface, "Metallic", NodeSocketFloat, False)
        _ = create_socket(interface, "Occlusion", NodeSocketFloat, False)
        _ = create_socket(interface, "Normal", NodeSocketVector, False)
        _ = create_socket(interface, "Height_Info", NodeSocketVector, False)
        _ = create_socket(interface, "Extra", NodeSocketVector, False)
        _ = create_socket(interface, "Socket", NodeSocketFloat)
        _ = create_socket(interface, "Control", NodeSocketColor)
        _ = create_socket(interface, "Control Alpha", NodeSocketFloat)
        _ = create_socket(interface, "Roughness Black", NodeSocketFloat)
        _ = create_socket(interface, "Roughness White", NodeSocketFloat)
        _ = create_socket(interface, "Metallic", NodeSocketFloat)
        _ = create_socket(interface, "Top", NodeSocketColor)
        _ = create_socket(interface, "Mid", NodeSocketColor)
        _ = create_socket(interface, "Bot", NodeSocketColor)
        _ = create_socket(interface, "Height Scale", NodeSocketFloat)
        _ = create_socket(interface, "Normal", NodeSocketColor)
        _ = create_socket(interface, "Normal Intensity", NodeSocketFloat)
        if interface is None:
            return
        extra_panel = interface.new_panel("Extra")
        _ = create_socket(interface, "Opacity", NodeSocketFloat, panel=extra_panel)
        _ = create_socket(interface, "Height_Blend_Range", NodeSocketFloat, panel=extra_panel)
        _ = create_socket(interface, "Height_Accumulation", NodeSocketFloat, panel=extra_panel)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        links = self.node_tree.links

        separate_color = create_node(nodes, -131, -11, ShaderNodeSeparateColor)
        separate_color.mode = "RGB"

        group_output = create_node(nodes, 540, 12, NodeGroupOutput)
        assign_value(group_output, 3, 1.0)
        group_input = create_node(nodes, -331, 0, NodeGroupInput)

        color_mixer = create_node(nodes, 128, 200, ShaderNodeGroup)
        color_mixer.node_tree = cast(ShaderNodeTree, ColorMixer().node_tree)

        mix_001 = create_node(nodes, 196, -274, ShaderNodeMix)
        mix_001.blend_type = "MIX"
        mix_001.clamp_factor = True
        mix_001.clamp_result = False
        mix_001.data_type = "RGBA"
        mix_001.factor_mode = "UNIFORM"
        assign_value(mix_001, 6, (0.5, 0.5, 1.0, 1.0))

        combine_xyz = create_node(nodes, 305, -157, ShaderNodeCombineXYZ)
        combine_xyz_001 = create_node(nodes, 37, -597, ShaderNodeCombineXYZ)

        math = create_node(nodes, 246, -4, ShaderNodeMath)
        math.operation = "MULTIPLY_ADD"
        math.use_clamp = False
        assign_value(math, 0, 0.5)

        combine_color = create_node(nodes, 41, -268, ShaderNodeCombineColor)
        combine_color.mode = "RGB"
        assign_value(combine_color, 2, 1.0)

        create_link(links, group_input, separate_color, 1, 0)
        create_link(links, group_input, color_mixer, 2, 0)
        create_link(links, group_input, color_mixer, 6, 1)
        create_link(links, group_input, color_mixer, 7, 2)
        create_link(links, group_input, color_mixer, 8, 3)
        create_link(links, group_input, group_output, 5, 2)
        create_link(links, group_input, mix_001, 11, 0)
        create_link(links, group_input, combine_xyz, 9, 1)
        create_link(links, combine_xyz, group_output, 0, 5)
        create_link(links, group_input, combine_xyz_001, 12, 0)
        create_link(links, group_input, combine_xyz_001, 13, 1)
        create_link(links, group_input, combine_xyz_001, 14, 2)
        create_link(links, combine_xyz_001, group_output, 0, 6)
        create_link(links, group_input, combine_xyz, 2, 0)
        create_link(links, color_mixer, group_output, 0, 0)
        create_link(links, mix_001, group_output, 2, 4)
        create_link(links, group_input, math, 3, 2)
        create_link(links, group_input, math, 4, 1)
        create_link(links, math, group_output, 0, 1)
        create_link(links, separate_color, combine_color, 0, 0)
        create_link(links, separate_color, combine_color, 1, 1)
        create_link(links, combine_color, mix_001, 0, 7)
        create_link(links, separate_color, combine_xyz, 2, 2)
