# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeReroute,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeCombineXYZ,
    ShaderNodeMix,
    ShaderNodeSeparateXYZ,
    ShaderNodeVectorMath,
)

from ..utils import assign_value, create_node, create_socket

__all__ = ["NormalMapCombineOrientation"]


class NormalMapCombineOrientation:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Normal Map Combine-Orientation")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Normal Map Combine-Orientation",
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
        _ = links.new(reroute1.outputs[0], vectorscale.inputs[0])
        _ = links.new(vectorscale.outputs[0], vectoradd.inputs[0])
        _ = links.new(vectoradd.outputs[0], separate_xyz.inputs[0])
        _ = links.new(vectorscale3.outputs[0], vectoradd3.inputs[0])
        _ = links.new(vectornormz.outputs[0], vectorscale3.inputs[0])
        _ = links.new(mix.outputs[2], output.inputs[0])
        _ = links.new(input.outputs[0], mix.inputs[0])
        _ = links.new(reroute.outputs[0], mix.inputs[6])
        _ = links.new(vectormult.outputs[0], vectoradd2.inputs[0])
        _ = links.new(reroute3.outputs[0], vectormult.inputs[0])
        _ = links.new(vectoradd.outputs[0], vectordot.inputs[0])
        _ = links.new(vectoradd2.outputs[0], vectordot.inputs[1])
        _ = links.new(vectordot.outputs[1], vectorscale2.inputs[3])
        _ = links.new(vectoradd.outputs[0], vectorscale2.inputs[0])
        _ = links.new(vectoradd2.outputs[0], vectorsub.inputs[1])
        _ = links.new(vectorscale2.outputs[0], vectordiv.inputs[0])
        _ = links.new(vectordiv.outputs[0], vectorsub.inputs[0])
        _ = links.new(separate_xyz.outputs[2], combinexyz.inputs[0])
        _ = links.new(separate_xyz.outputs[2], combinexyz.inputs[1])
        _ = links.new(separate_xyz.outputs[2], combinexyz.inputs[2])
        _ = links.new(combinexyz.outputs[0], vectordiv.inputs[1])
        _ = links.new(vectorsub.outputs[0], vectornormz.inputs[0])
        _ = links.new(reroute4.outputs[0], mix.inputs[7])
        _ = links.new(input.outputs[2], reroute2.inputs[0])
        _ = links.new(input.outputs[1], reroute.inputs[0])
        _ = links.new(reroute.outputs[0], reroute1.inputs[0])
        _ = links.new(reroute2.outputs[0], reroute3.inputs[0])
        _ = links.new(reroute5.outputs[0], reroute4.inputs[0])
        _ = links.new(vectoradd3.outputs[0], reroute5.inputs[0])
