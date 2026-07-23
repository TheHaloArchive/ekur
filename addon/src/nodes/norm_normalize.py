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
    ShaderNodeSeparateXYZ,
    ShaderNodeVectorMath,
)

from ..utils import assign_value, create_node, create_socket, create_link

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
        create_link(links, input, separate_xyz, 0, 0)
        create_link(links, divide, output, 2, 0)
        create_link(links, combine_normal, normalize, 0, 0)
        create_link(links, clamp_mult, one_minus, 0, 1)
        create_link(links, one_minus, sqrt, 0, 0)
        create_link(links, sqrt, combine_normal, 0, 2)
        create_link(links, add, divide, 2, 6)
        create_link(links, normalize, add, 0, 6)
        create_link(links, mult, clamp_mult, 0, 2)
        create_link(links, normal_remap, clamp_mult, 0, 0)
        create_link(links, normal_remap, clamp_mult, 0, 1)
        create_link(links, mult_add, mult, 0, 1)
        create_link(links, mult_add, mult, 0, 0)
        create_link(links, normal_remap, combine_normal, 0, 0)
        create_link(links, separate_xyz, normal_remap, 0, 0)
        create_link(links, input, mix_flip, 1, 0)
        create_link(links, separate_xyz, one_minus_y, 1, 1)
        create_link(links, one_minus_y, mix_flip, 0, 3)
        create_link(links, separate_xyz, mix_flip, 1, 2)
        create_link(links, mix_flip, mult_add, 0, 0)
        create_link(links, mult_add, combine_normal, 0, 1)
