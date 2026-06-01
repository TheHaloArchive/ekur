# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import cast

import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketInt,
    NodeTree,
    ShaderNodeGroup,
    ShaderNodeMix,
    ShaderNodeTree,
)

from ..utils import create_node, create_socket
from .normal_map_combine_orientation import NormalMapCombineOrientationNonNorm

__all__ = ["LayerOverlayBoolNorm"]


class LayerOverlayBoolNorm:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Layer Overlay Bool (Norm)")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Layer Overlay Bool (Norm)"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Out", NodeSocketColor, False)
        _ = create_socket(interface, "Blending Method", NodeSocketInt)
        _ = create_socket(interface, "Layer Mask", NodeSocketFloat)
        _ = create_socket(interface, "Prev.Layer", NodeSocketColor)
        _ = create_socket(interface, "Next Layer", NodeSocketColor)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        links = self.node_tree.links

        group_input = create_node(nodes, -299, 0, NodeGroupInput)
        group_output = create_node(nodes, 289, 0, NodeGroupOutput)

        mix_004 = create_node(nodes, 99, 37, ShaderNodeMix)
        mix_004.blend_type = "MIX"
        mix_004.clamp_factor = True
        mix_004.clamp_result = False
        mix_004.data_type = "RGBA"
        mix_004.factor_mode = "UNIFORM"

        mix_007 = create_node(nodes, -94, 118, ShaderNodeMix)
        mix_007.blend_type = "MIX"
        mix_007.clamp_factor = True
        mix_007.clamp_result = False
        mix_007.data_type = "RGBA"
        mix_007.factor_mode = "UNIFORM"

        normal_map_combine_orientation = create_node(nodes, -94, -155, ShaderNodeGroup)
        normal_map_combine_orientation.node_tree = cast(
            ShaderNodeTree, NormalMapCombineOrientationNonNorm().node_tree
        )

        _ = links.new(group_input.outputs[0], mix_004.inputs[0])
        _ = links.new(group_input.outputs[1], mix_007.inputs[0])
        _ = links.new(group_input.outputs[1], normal_map_combine_orientation.inputs[0])
        _ = links.new(group_input.outputs[2], mix_007.inputs[6])
        _ = links.new(group_input.outputs[2], normal_map_combine_orientation.inputs[1])
        _ = links.new(group_input.outputs[3], mix_007.inputs[7])
        _ = links.new(group_input.outputs[3], normal_map_combine_orientation.inputs[2])
        _ = links.new(mix_007.outputs[2], mix_004.inputs[6])
        _ = links.new(normal_map_combine_orientation.outputs[0], mix_004.inputs[7])
        _ = links.new(mix_004.outputs[2], group_output.inputs[0])
