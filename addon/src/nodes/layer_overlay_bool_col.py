# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketInt,
    NodeTree,
    ShaderNodeMix,
)

from ..utils import create_node, create_socket, create_link

__all__ = ["LayerOverlayBoolCol"]


class LayerOverlayBoolCol:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Layer Overlay Bool (Col)")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Layer Overlay Bool (Col)"
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

        group_output = create_node(nodes, 289, 0, NodeGroupOutput)
        group_input = create_node(nodes, -299, 0, NodeGroupInput)

        mix = create_node(nodes, -100, -121, ShaderNodeMix)
        mix.blend_type = "OVERLAY"
        mix.clamp_factor = True
        mix.clamp_result = False
        mix.data_type = "RGBA"
        mix.factor_mode = "UNIFORM"

        create_link(links, mix_007, mix_004, 2, 6)
        create_link(links, group_input, mix_007, 1, 0)
        create_link(links, group_input, mix_007, 3, 7)
        create_link(links, mix_004, group_output, 2, 0)
        create_link(links, group_input, mix_004, 0, 0)
        create_link(links, group_input, mix_007, 2, 6)
        create_link(links, group_input, mix, 2, 6)
        create_link(links, group_input, mix, 3, 7)
        create_link(links, group_input, mix, 1, 0)
        create_link(links, mix, mix_004, 2, 7)
