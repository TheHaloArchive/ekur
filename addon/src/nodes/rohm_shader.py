# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketVector,
    NodeTree,
    ShaderNodeCombineXYZ,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
)

from ..utils import assign_value, create_node, create_socket

__all__ = ["RohmShader"]


class RohmShader:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("ROHM SHADER")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="ROHM SHADER")
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
        _ = create_socket(interface, "Color", NodeSocketColor)
        _ = create_socket(interface, "Color Tint", NodeSocketColor)
        _ = create_socket(interface, "Control", NodeSocketColor)
        _ = create_socket(interface, "Control Alpha", NodeSocketFloat)
        _ = create_socket(interface, "Roughness Black", NodeSocketFloat)
        _ = create_socket(interface, "Roughness White", NodeSocketFloat)
        _ = create_socket(interface, "Metallic Black", NodeSocketFloat)
        _ = create_socket(interface, "Metallic White", NodeSocketFloat)
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

        separate_color = create_node(nodes, -168, 13, ShaderNodeSeparateColor)
        separate_color.mode = "RGB"

        group_output = create_node(nodes, 1523, 12, NodeGroupOutput)
        group_input = create_node(nodes, -521, 15, NodeGroupInput)

        math = create_node(nodes, 46, -184, ShaderNodeMath)
        math.operation = "DIVIDE"
        math.use_clamp = False
        assign_value(math, 1, 1000.0)

        mix_002 = create_node(nodes, -244, 260, ShaderNodeMix)
        mix_002.blend_type = "MULTIPLY"
        mix_002.clamp_factor = True
        mix_002.clamp_result = False
        mix_002.data_type = "RGBA"
        mix_002.factor_mode = "UNIFORM"
        assign_value(mix_002, 0, 1.0)

        mix_001 = create_node(nodes, 199, -377, ShaderNodeMix)
        mix_001.blend_type = "MIX"
        mix_001.clamp_factor = True
        mix_001.clamp_result = False
        mix_001.data_type = "RGBA"
        mix_001.factor_mode = "UNIFORM"
        assign_value(mix_001, 6, (0.5, 0.5, 1.0, 1.0))

        combine_xyz = create_node(nodes, 155, -847, ShaderNodeCombineXYZ)
        combine_xyz_001 = create_node(nodes, 157, -707, ShaderNodeCombineXYZ)

        math_001 = create_node(nodes, 150, 163, ShaderNodeMath)
        math_001.operation = "MULTIPLY_ADD"
        math_001.use_clamp = False

        math_002 = create_node(nodes, 316, -100, ShaderNodeMath)
        math_002.operation = "MULTIPLY_ADD"
        math_002.use_clamp = False

        _ = links.new(group_input.outputs[2], separate_color.inputs[0])
        _ = links.new(group_input.outputs[8], math.inputs[0])
        _ = links.new(group_input.outputs[0], mix_002.inputs[6])
        _ = links.new(group_input.outputs[1], mix_002.inputs[7])
        _ = links.new(mix_001.outputs[2], group_output.inputs[4])
        _ = links.new(group_input.outputs[10], mix_001.inputs[0])
        _ = links.new(group_input.outputs[11], combine_xyz.inputs[0])
        _ = links.new(group_input.outputs[13], combine_xyz.inputs[2])
        _ = links.new(combine_xyz.outputs[0], group_output.inputs[6])
        _ = links.new(separate_color.outputs[2], combine_xyz_001.inputs[2])
        _ = links.new(group_input.outputs[8], combine_xyz_001.inputs[1])
        _ = links.new(combine_xyz_001.outputs[0], group_output.inputs[5])
        _ = links.new(group_input.outputs[12], combine_xyz.inputs[1])
        _ = links.new(group_input.outputs[3], combine_xyz_001.inputs[0])
        _ = links.new(mix_002.outputs[2], group_output.inputs[0])
        _ = links.new(separate_color.outputs[1], group_output.inputs[3])
        _ = links.new(group_input.outputs[9], mix_001.inputs[7])
        _ = links.new(group_input.outputs[4], math_001.inputs[2])
        _ = links.new(group_input.outputs[5], math_001.inputs[1])
        _ = links.new(separate_color.outputs[0], math_001.inputs[0])
        _ = links.new(math_001.outputs[0], group_output.inputs[1])
        _ = links.new(math_002.outputs[0], group_output.inputs[2])
        _ = links.new(group_input.outputs[3], math_002.inputs[0])
        _ = links.new(group_input.outputs[6], math_002.inputs[2])
        _ = links.new(group_input.outputs[7], math_002.inputs[1])
