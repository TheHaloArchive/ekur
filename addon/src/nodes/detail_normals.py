# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeGroup,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
)

from ..utils import assign_value, create_node, create_socket, create_link
from .norm_normalize import NormNormalize
from .normal_map_combine_orientation import NormalMapCombineOrientation

__all__ = ["DetailNormals"]


class DetailNormals:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Detail Normals")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Detail Normals")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Normal", NodeSocketColor, False)
        _ = create_socket(interface, "ASG", NodeSocketColor)
        _ = create_socket(interface, "Mask 0", NodeSocketColor)
        _ = create_socket(interface, "Mask 1", NodeSocketColor)
        _ = create_socket(interface, "Base Normal", NodeSocketColor)
        _ = create_socket(interface, "Slot 1", NodeSocketColor)
        _ = create_socket(interface, "Slot 2", NodeSocketColor)
        _ = create_socket(interface, "Slot 3", NodeSocketColor)
        _ = create_socket(interface, "Slot 4", NodeSocketColor)
        _ = create_socket(interface, "Slot 5", NodeSocketColor)
        _ = create_socket(interface, "Slot 6", NodeSocketColor)
        _ = create_socket(interface, "Slot 7", NodeSocketColor)
        _ = create_socket(interface, "Grime", NodeSocketColor)
        _ = create_socket(interface, "Scratch Amount", NodeSocketFloat)
        _ = create_socket(interface, "Grime Amount", NodeSocketFloat)
        _ = create_socket(interface, "Detail Normal Toggle", NodeSocketFloat)
        _ = create_socket(interface, "Normal Flip", NodeSocketFloat)
        _ = create_socket(interface, "Detail Normal Flip", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        subtract = create_node(self.node_tree.nodes, -400, 1083, ShaderNodeMath)
        subtract.operation = "SUBTRACT"
        assign_value(subtract, 1, 1.0)

        mix = create_node(self.node_tree.nodes, -670, 367, ShaderNodeMix)
        mix.data_type = "RGBA"
        mix2 = create_node(self.node_tree.nodes, -473, 367, ShaderNodeMix)
        mix2.data_type = "RGBA"
        mix3 = create_node(self.node_tree.nodes, -301, 367, ShaderNodeMix)
        mix3.data_type = "RGBA"
        mix4 = create_node(self.node_tree.nodes, -127, 367, ShaderNodeMix)
        mix4.data_type = "RGBA"
        mix5 = create_node(self.node_tree.nodes, -878, 367, ShaderNodeMix)
        mix5.data_type = "RGBA"
        grime = create_node(self.node_tree.nodes, 400, 367, ShaderNodeMix)
        grime.clamp_result = True
        grime.data_type = "RGBA"
        scratch = create_node(self.node_tree.nodes, 230, 370, ShaderNodeMix)
        scratch.data_type = "RGBA"
        dust = create_node(self.node_tree.nodes, 50, 370, ShaderNodeMix)
        dust.data_type = "RGBA"

        srgb = create_node(self.node_tree.nodes, -860, 380, ShaderNodeSeparateColor)
        srgb2 = create_node(self.node_tree.nodes, -895, 380, ShaderNodeSeparateColor)
        srgb3 = create_node(self.node_tree.nodes, -900, 760, ShaderNodeSeparateColor)
        output = create_node(self.node_tree.nodes, 1140, 350, NodeGroupOutput)
        input = create_node(self.node_tree.nodes, -1480, 490, NodeGroupInput)

        subtract2 = create_node(self.node_tree.nodes, -400, 1270, ShaderNodeMath)
        subtract2.operation = "SUBTRACT"
        assign_value(subtract2, 1, 1.0)

        grimemath = create_node(self.node_tree.nodes, 0, 1105, ShaderNodeMath)
        grimemath.label = "Grime"

        scratchmath = create_node(self.node_tree.nodes, 0, 1205, ShaderNodeMath)
        scratchmath.label = "Scratch"

        normalize = create_node(self.node_tree.nodes, 600, 480, ShaderNodeGroup)
        normalize.node_tree = NormNormalize().node_tree  # ty: ignore[invalid-assignment]

        normalize2 = create_node(self.node_tree.nodes, 600, 330, ShaderNodeGroup)
        normalize2.node_tree = NormNormalize().node_tree  # ty: ignore[invalid-assignment]

        normcombine = create_node(self.node_tree.nodes, 890, 480, ShaderNodeGroup)
        normcombine.node_tree = NormalMapCombineOrientation().node_tree  # ty: ignore[invalid-assignment]

        links = self.node_tree.links
        create_link(links, input, srgb2, 1, 0)
        create_link(links, input, srgb3, 2, 0)
        create_link(links, input, srgb, 0, 0)
        create_link(links, srgb, grimemath, 2, 0)
        create_link(links, subtract, grimemath, 0, 1)
        create_link(links, srgb, scratchmath, 1, 0)
        create_link(links, subtract2, scratchmath, 0, 1)
        create_link(links, input, subtract2, 12, 0)
        create_link(links, input, subtract, 13, 0)
        create_link(links, mix5, mix, 2, 6)
        create_link(links, input, mix, 6, 7)
        create_link(links, mix, mix2, 2, 6)
        create_link(links, input, mix2, 7, 7)
        create_link(links, mix2, mix3, 2, 6)
        create_link(links, input, mix3, 8, 7)
        create_link(links, mix3, mix4, 2, 6)
        create_link(links, input, mix4, 9, 7)
        create_link(links, mix4, dust, 2, 6)
        create_link(links, input, dust, 10, 7)
        create_link(links, dust, scratch, 2, 6)
        create_link(links, scratchmath, scratch, 0, 0)
        create_link(links, scratch, grime, 2, 6)
        create_link(links, grimemath, grime, 0, 0)
        create_link(links, input, grime, 11, 7)
        create_link(links, srgb2, mix5, 0, 0)
        create_link(links, srgb2, mix, 1, 0)
        create_link(links, srgb2, mix2, 2, 0)
        create_link(links, srgb3, mix3, 0, 0)
        create_link(links, srgb3, mix4, 1, 0)
        create_link(links, input, mix5, 4, 6)
        create_link(links, input, mix5, 5, 7)
        create_link(links, grime, normalize2, 2, 0)
        create_link(links, normalize, normcombine, 0, 1)
        create_link(links, normalize2, normcombine, 0, 2)
        create_link(links, normcombine, output, 0, 0)
        create_link(links, input, normalize, 3, 0)
        create_link(links, input, normcombine, 14, 0)
        create_link(links, srgb3, dust, 2, 0)
        create_link(links, input, normalize, 15, 1)
        create_link(links, input, normalize2, 16, 1)
