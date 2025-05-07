# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
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
    ShaderNodeSeparateXYZ,
    ShaderNodeVectorMath,
)

from ..utils import assign_value, create_node, create_socket

__all__ = ["NormNormalize"]


class NormNormalize:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Norm Normalize")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Norm Normalize")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if not self.node_tree:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Normal", NodeSocketVector)
        _ = create_socket(interface, "Normal Flip", NodeSocketFloat)
        _ = create_socket(interface, "Normal Normalized", NodeSocketColor, False)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes

        output = create_node(nodes, 1507, 0, NodeGroupOutput)
        input = create_node(nodes, -1067, 4, NodeGroupInput)
        combine_normal = create_node(nodes, 1583, -140, ShaderNodeCombineXYZ)
        separate_xyz = create_node(nodes, -40, -100, ShaderNodeSeparateXYZ)

        normal_remap = create_node(nodes, 220, 0, ShaderNodeMath)
        normal_remap.operation = "MULTIPLY_ADD"
        assign_value(normal_remap, 1, 2.0)
        assign_value(normal_remap, 2, -1.0)

        sqrt = create_node(nodes, 1363, -100, ShaderNodeMath)
        sqrt.operation = "SQRT"

        normalize = create_node(nodes, 1743, -140, ShaderNodeVectorMath)
        normalize.operation = "NORMALIZE"

        add = create_node(nodes, 1923, -140, ShaderNodeMix)
        add.blend_type = "ADD"
        add.data_type = "RGBA"
        assign_value(add, 0, 1.0)
        assign_value(add, 7, (1.0, 1.0, 1.0, 1.0))

        one_minus = create_node(nodes, 1183, -80, ShaderNodeMath)
        one_minus.operation = "SUBTRACT"
        assign_value(one_minus, 0, 1.0)

        clamp_mult = create_node(nodes, 1003, -80, ShaderNodeMath)
        clamp_mult.operation = "MULTIPLY_ADD"
        clamp_mult.use_clamp = True

        mult = create_node(nodes, 803, -180, ShaderNodeMath)
        mult.operation = "MULTIPLY"

        divide = create_node(nodes, 2103, -140, ShaderNodeMix)
        divide.blend_type = "DIVIDE"
        divide.data_type = "RGBA"
        assign_value(divide, 0, 1.0)
        assign_value(divide, 7, (2.0, 2.0, 2.0, 1.0))

        mix_flip = create_node(nodes, 399, -350, ShaderNodeMix)
        mix_flip.blend_type = "MIX"
        mix_flip.data_type = "FLOAT"

        mult_add = create_node(nodes, 588, -198, ShaderNodeMath)
        mult_add.operation = "MULTIPLY_ADD"
        assign_value(mult_add, 1, 2.0)
        assign_value(mult_add, 2, -1.0)

        one_minus_y = create_node(nodes, 154, -413, ShaderNodeMath)
        one_minus_y.operation = "SUBTRACT"
        assign_value(one_minus_y, 0, 1.0)

        links = self.node_tree.links
        _ = links.new(input.outputs[0], separate_xyz.inputs[0])
        _ = links.new(divide.outputs[2], output.inputs[0])
        _ = links.new(combine_normal.outputs[0], normalize.inputs[0])
        _ = links.new(clamp_mult.outputs[0], one_minus.inputs[1])
        _ = links.new(one_minus.outputs[0], sqrt.inputs[0])
        _ = links.new(sqrt.outputs[0], combine_normal.inputs[2])
        _ = links.new(add.outputs[2], divide.inputs[6])
        _ = links.new(normalize.outputs[0], add.inputs[6])
        _ = links.new(mult.outputs[0], clamp_mult.inputs[2])
        _ = links.new(normal_remap.outputs[0], clamp_mult.inputs[0])
        _ = links.new(normal_remap.outputs[0], clamp_mult.inputs[1])
        _ = links.new(mult_add.outputs[0], mult.inputs[1])
        _ = links.new(mult_add.outputs[0], mult.inputs[0])
        _ = links.new(normal_remap.outputs[0], combine_normal.inputs[0])
        _ = links.new(separate_xyz.outputs[0], normal_remap.inputs[0])
        _ = links.new(input.outputs[1], mix_flip.inputs[0])
        _ = links.new(separate_xyz.outputs[1], one_minus_y.inputs[1])
        _ = links.new(one_minus_y.outputs[0], mix_flip.inputs[3])
        _ = links.new(separate_xyz.outputs[1], mix_flip.inputs[2])
        _ = links.new(mix_flip.outputs[0], mult_add.inputs[0])
        _ = links.new(mult_add.outputs[0], combine_normal.inputs[1])
