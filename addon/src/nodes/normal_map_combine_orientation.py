# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import cast

import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeReroute,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeCombineXYZ,
    ShaderNodeGroup,
    ShaderNodeMix,
    ShaderNodeSeparateXYZ,
    ShaderNodeTree,
    ShaderNodeVectorMath,
)

from ..utils import assign_value, create_node, create_socket, create_link
from .norm_normalize import NormNormalize

__all__ = ["NormalMapCombineOrientation", "NormalMapCombineOrientationNonNorm"]


class NormalMapCombineOrientation:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Normal Map Combine-Orientation")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Normal Map Combine-Orientation"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if not self.node_tree:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Combined Normal Map", NodeSocketColor, False)
        _ = create_socket(interface, "Factor", NodeSocketFloat)
        _ = create_socket(interface, "Base", NodeSocketColor)
        _ = create_socket(interface, "Detail", NodeSocketColor)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        input = create_node(nodes, -680, 0, NodeGroupInput)
        reroute = create_node(nodes, -473, -55, NodeReroute)
        reroute1 = create_node(nodes, -472, 236, NodeReroute)
        reroute2 = create_node(nodes, -442, -76, NodeReroute)
        reroute3 = create_node(nodes, -436, 164, NodeReroute)

        vectormult = create_node(nodes, -361, 166, ShaderNodeVectorMath)
        vectormult.operation = "MULTIPLY"
        assign_value(vectormult, 1, (-2.0, -2.0, 2.0))

        vectorscale = create_node(nodes, -352, 240, ShaderNodeVectorMath)
        vectorscale.operation = "SCALE"
        assign_value(vectorscale, 3, 2.0)

        vectoradd = create_node(nodes, -357, 205, ShaderNodeVectorMath)
        vectoradd.operation = "ADD"
        assign_value(vectoradd, 1, (-1.0, -1.0, 0.0))

        vectoradd2 = create_node(nodes, -366, 131, ShaderNodeVectorMath)
        vectoradd2.operation = "ADD"
        assign_value(vectoradd2, 1, (1.0, 1.0, -1.0))

        vectorscale2 = create_node(nodes, -115, 165, ShaderNodeVectorMath)
        vectorscale2.operation = "SCALE"

        vectordot = create_node(nodes, -113, 200, ShaderNodeVectorMath)
        vectordot.operation = "DOT_PRODUCT"

        separate_xyz = create_node(nodes, -109, 241, ShaderNodeSeparateXYZ)
        combinexyz = create_node(nodes, 57, 209, ShaderNodeCombineXYZ)

        vectordiv = create_node(nodes, 55, 175, ShaderNodeVectorMath)
        vectordiv.operation = "DIVIDE"

        vectorsub = create_node(nodes, 212, 148, ShaderNodeVectorMath)
        vectorsub.operation = "SUBTRACT"

        vectorscale3 = create_node(nodes, 214, 77, ShaderNodeVectorMath)
        vectorscale3.operation = "SCALE"
        assign_value(vectorscale3, 3, 0.5)

        vectornormz = create_node(nodes, 213, 112, ShaderNodeVectorMath)
        vectornormz.operation = "NORMALIZE"

        vectoradd3 = create_node(nodes, 216, 43, ShaderNodeVectorMath)
        vectoradd3.operation = "ADD"
        assign_value(vectoradd3, 1, (0.5, 0.5, 0.5))

        reroute4 = create_node(nodes, 383, -64, NodeReroute)
        mix = create_node(nodes, 415, 89, ShaderNodeMix)
        mix.data_type = "RGBA"

        reroute5 = create_node(nodes, 383, 31, NodeReroute)
        output = create_node(nodes, 613, 81, NodeGroupOutput)

        links = self.node_tree.links
        create_link(links, reroute1, vectorscale, 0, 0)
        create_link(links, vectorscale, vectoradd, 0, 0)
        create_link(links, vectoradd, separate_xyz, 0, 0)
        create_link(links, vectorscale3, vectoradd3, 0, 0)
        create_link(links, vectornormz, vectorscale3, 0, 0)
        create_link(links, mix, output, 2, 0)
        create_link(links, input, mix, 0, 0)
        create_link(links, reroute, mix, 0, 6)
        create_link(links, vectormult, vectoradd2, 0, 0)
        create_link(links, reroute3, vectormult, 0, 0)
        create_link(links, vectoradd, vectordot, 0, 0)
        create_link(links, vectoradd2, vectordot, 0, 1)
        create_link(links, vectordot, vectorscale2, 1, 3)
        create_link(links, vectoradd, vectorscale2, 0, 0)
        create_link(links, vectoradd2, vectorsub, 0, 1)
        create_link(links, vectorscale2, vectordiv, 0, 0)
        create_link(links, vectordiv, vectorsub, 0, 0)
        create_link(links, separate_xyz, combinexyz, 2, 0)
        create_link(links, separate_xyz, combinexyz, 2, 1)
        create_link(links, separate_xyz, combinexyz, 2, 2)
        create_link(links, combinexyz, vectordiv, 0, 1)
        create_link(links, vectorsub, vectornormz, 0, 0)
        create_link(links, reroute4, mix, 0, 7)
        create_link(links, input, reroute2, 2, 0)
        create_link(links, input, reroute, 1, 0)
        create_link(links, reroute, reroute1, 0, 0)
        create_link(links, reroute2, reroute3, 0, 0)
        create_link(links, reroute5, reroute4, 0, 0)
        create_link(links, vectoradd3, reroute5, 0, 0)


class NormalMapCombineOrientationNonNorm:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get(
            "Normal Map Combine-Orientation Non-Norm"
        )
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Normal Map Combine-Orientation Non-Norm"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if not self.node_tree:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Combined Normal Map", NodeSocketColor, False)
        _ = create_socket(interface, "Factor", NodeSocketFloat)
        _ = create_socket(interface, "Base", NodeSocketColor)
        _ = create_socket(interface, "Detail", NodeSocketColor)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        input = create_node(nodes, -680, 0, NodeGroupInput)
        reroute = create_node(nodes, -473, -55, NodeReroute)
        reroute1 = create_node(nodes, -472, 236, NodeReroute)
        reroute2 = create_node(nodes, -442, -76, NodeReroute)
        reroute3 = create_node(nodes, -436, 164, NodeReroute)

        vectormult = create_node(nodes, -361, 166, ShaderNodeVectorMath)
        vectormult.operation = "MULTIPLY"
        assign_value(vectormult, 1, (-2.0, -2.0, 2.0))

        vectorscale = create_node(nodes, -352, 240, ShaderNodeVectorMath)
        vectorscale.operation = "SCALE"
        assign_value(vectorscale, 3, 2.0)

        vectoradd = create_node(nodes, -357, 205, ShaderNodeVectorMath)
        vectoradd.operation = "ADD"
        assign_value(vectoradd, 1, (-1.0, -1.0, 0.0))

        vectoradd2 = create_node(nodes, -366, 131, ShaderNodeVectorMath)
        vectoradd2.operation = "ADD"
        assign_value(vectoradd2, 1, (1.0, 1.0, -1.0))

        vectorscale2 = create_node(nodes, -115, 165, ShaderNodeVectorMath)
        vectorscale2.operation = "SCALE"

        vectordot = create_node(nodes, -113, 200, ShaderNodeVectorMath)
        vectordot.operation = "DOT_PRODUCT"

        separate_xyz = create_node(nodes, -109, 241, ShaderNodeSeparateXYZ)
        combinexyz = create_node(nodes, 57, 209, ShaderNodeCombineXYZ)

        vectordiv = create_node(nodes, 55, 175, ShaderNodeVectorMath)
        vectordiv.operation = "DIVIDE"

        vectorsub = create_node(nodes, 212, 148, ShaderNodeVectorMath)
        vectorsub.operation = "SUBTRACT"

        vectorscale3 = create_node(nodes, 214, 77, ShaderNodeVectorMath)
        vectorscale3.operation = "SCALE"
        assign_value(vectorscale3, 3, 0.5)

        vectornormz = create_node(nodes, 213, 112, ShaderNodeVectorMath)
        vectornormz.operation = "NORMALIZE"

        vectoradd3 = create_node(nodes, 216, 43, ShaderNodeVectorMath)
        vectoradd3.operation = "ADD"
        assign_value(vectoradd3, 1, (0.5, 0.5, 0.5))

        reroute4 = create_node(nodes, 383, -64, NodeReroute)
        mix = create_node(nodes, 415, 89, ShaderNodeMix)
        mix.data_type = "RGBA"

        reroute5 = create_node(nodes, 383, 31, NodeReroute)
        output = create_node(nodes, 613, 81, NodeGroupOutput)

        norm_normalize = create_node(nodes, 171, 339, ShaderNodeGroup)
        norm_normalize.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)

        norm_normalize2 = create_node(nodes, 171, 500, ShaderNodeGroup)
        norm_normalize2.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)

        links = self.node_tree.links
        create_link(links, reroute1, vectorscale, 0, 0)
        create_link(links, vectorscale, vectoradd, 0, 0)
        create_link(links, vectoradd, separate_xyz, 0, 0)
        create_link(links, vectorscale3, vectoradd3, 0, 0)
        create_link(links, vectornormz, vectorscale3, 0, 0)
        create_link(links, mix, output, 2, 0)
        create_link(links, input, mix, 0, 0)
        create_link(links, reroute, mix, 0, 6)
        create_link(links, vectormult, vectoradd2, 0, 0)
        create_link(links, reroute3, vectormult, 0, 0)
        create_link(links, vectoradd, vectordot, 0, 0)
        create_link(links, vectoradd2, vectordot, 0, 1)
        create_link(links, vectordot, vectorscale2, 1, 3)
        create_link(links, vectoradd, vectorscale2, 0, 0)
        create_link(links, vectoradd2, vectorsub, 0, 1)
        create_link(links, vectorscale2, vectordiv, 0, 0)
        create_link(links, vectordiv, vectorsub, 0, 0)
        create_link(links, separate_xyz, combinexyz, 2, 0)
        create_link(links, separate_xyz, combinexyz, 2, 1)
        create_link(links, separate_xyz, combinexyz, 2, 2)
        create_link(links, combinexyz, vectordiv, 0, 1)
        create_link(links, vectorsub, vectornormz, 0, 0)
        create_link(links, reroute4, mix, 0, 7)
        create_link(links, input, norm_normalize2, 2, 0)
        create_link(links, input, norm_normalize, 1, 0)
        create_link(links, norm_normalize2, reroute2, 0, 0)
        create_link(links, norm_normalize, reroute, 0, 0)
        create_link(links, reroute, reroute1, 0, 0)
        create_link(links, reroute2, reroute3, 0, 0)
        create_link(links, reroute5, reroute4, 0, 0)
        create_link(links, vectoradd3, reroute5, 0, 0)
