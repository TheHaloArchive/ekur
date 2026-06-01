# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
)

from ..utils import assign_value, create_node, create_socket

__all__ = ["OcclusionBlend"]


class OcclusionBlend:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Occlusion Blend")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Occlusion Blend")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Blended", NodeSocketFloat, False)
        _ = create_socket(interface, "l4_result", NodeSocketFloat, False)
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

        group_input = create_node(nodes, -660, 0, NodeGroupInput)
        group_output = create_node(nodes, 1250, 449, NodeGroupOutput)

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

        math = create_node(nodes, 52, 292, ShaderNodeMath)
        math.operation = "ADD"
        assign_value(math, 1, -1.0)

        math_001 = create_node(nodes, 321, 451, ShaderNodeMath)
        math_001.operation = "MULTIPLY"

        math_002 = create_node(nodes, 547, 474, ShaderNodeMath)
        math_002.operation = "ADD"
        assign_value(math_002, 1, 1.0)

        math_003 = create_node(nodes, 806, 448, ShaderNodeMath)
        math_003.operation = "MULTIPLY"

        _ = links.new(group_input.outputs[0], separate_color.inputs[0])
        _ = links.new(separate_color.outputs[0], mix.inputs[0])
        _ = links.new(separate_color.outputs[1], mix_002.inputs[0])
        _ = links.new(separate_color.outputs[2], mix_003.inputs[0])
        _ = links.new(group_input.outputs[1], mix_004.inputs[0])
        _ = links.new(group_input.outputs[4], mix.inputs[3])
        _ = links.new(mix.outputs[0], mix_002.inputs[2])
        _ = links.new(group_input.outputs[5], mix_002.inputs[3])
        _ = links.new(mix_002.outputs[0], mix_003.inputs[2])
        _ = links.new(group_input.outputs[6], mix_003.inputs[3])
        _ = links.new(mix_003.outputs[0], mix_004.inputs[2])
        _ = links.new(group_input.outputs[7], mix_004.inputs[3])
        _ = links.new(group_input.outputs[2], math.inputs[0])
        _ = links.new(group_input.outputs[3], math_001.inputs[0])
        _ = links.new(math.outputs[0], math_001.inputs[1])
        _ = links.new(math_001.outputs[0], math_002.inputs[0])
        _ = links.new(math_002.outputs[0], math_003.inputs[0])
        _ = links.new(mix_004.outputs[0], math_003.inputs[1])
        _ = links.new(math_003.outputs[0], group_output.inputs[0])
        _ = links.new(mix_004.outputs[0], group_output.inputs[1])
