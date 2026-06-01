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
    ShaderNodeCombineXYZ,
    ShaderNodeGroup,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
    ShaderNodeTree,
)

from ..utils import assign_value, create_node, create_socket
from .color_mixer import ColorMixer

__all__ = ["RohgShader"]


class RohgShader:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("ROHG SHADER")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="ROHG SHADER")
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
        group_input = create_node(nodes, -331, 0, NodeGroupInput)

        color_mixer = create_node(nodes, 128, 200, ShaderNodeGroup)
        color_mixer.node_tree = cast(ShaderNodeTree, ColorMixer().node_tree)

        mix_001 = create_node(nodes, 38, -330, ShaderNodeMix)
        mix_001.blend_type = "MIX"
        mix_001.clamp_factor = True
        mix_001.clamp_result = False
        mix_001.data_type = "RGBA"
        mix_001.factor_mode = "UNIFORM"
        assign_value(mix_001, 6, (0.5, 0.5, 1.0, 1.0))

        combine_xyz = create_node(nodes, 311, -179, ShaderNodeCombineXYZ)
        combine_xyz_001 = create_node(nodes, 37, -597, ShaderNodeCombineXYZ)

        math = create_node(nodes, 246, -4, ShaderNodeMath)
        math.operation = "MULTIPLY_ADD"
        math.use_clamp = False

        _ = links.new(group_input.outputs[1], separate_color.inputs[0])
        _ = links.new(group_input.outputs[2], color_mixer.inputs[0])
        _ = links.new(group_input.outputs[6], color_mixer.inputs[1])
        _ = links.new(group_input.outputs[7], color_mixer.inputs[2])
        _ = links.new(group_input.outputs[8], color_mixer.inputs[3])
        _ = links.new(group_input.outputs[5], group_output.inputs[2])
        _ = links.new(group_input.outputs[11], mix_001.inputs[0])
        _ = links.new(group_input.outputs[10], mix_001.inputs[7])
        _ = links.new(separate_color.outputs[2], combine_xyz.inputs[2])
        _ = links.new(group_input.outputs[9], combine_xyz.inputs[1])
        _ = links.new(combine_xyz.outputs[0], group_output.inputs[5])
        _ = links.new(group_input.outputs[12], combine_xyz_001.inputs[0])
        _ = links.new(group_input.outputs[13], combine_xyz_001.inputs[1])
        _ = links.new(group_input.outputs[14], combine_xyz_001.inputs[2])
        _ = links.new(combine_xyz_001.outputs[0], group_output.inputs[6])
        _ = links.new(group_input.outputs[2], combine_xyz.inputs[0])
        _ = links.new(color_mixer.outputs[0], group_output.inputs[0])
        _ = links.new(separate_color.outputs[1], group_output.inputs[3])
        _ = links.new(mix_001.outputs[2], group_output.inputs[4])
        _ = links.new(separate_color.outputs[0], math.inputs[0])
        _ = links.new(group_input.outputs[3], math.inputs[2])
        _ = links.new(group_input.outputs[4], math.inputs[1])
        _ = links.new(math.outputs[0], group_output.inputs[1])
