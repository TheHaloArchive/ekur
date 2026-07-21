# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import cast

import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketShader,
    NodeTree,
    ShaderNodeBsdfPrincipled,
    ShaderNodeGroup,
    ShaderNodeMix,
    ShaderNodeNormalMap,
    ShaderNodeTree,
)

from ..utils import assign_value, create_node, create_socket, create_link
from .norm_normalize import NormNormalize

__all__ = ["Hair"]


class Hair:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Hair Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Hair Shader")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        _ = create_socket(interface, "Color", NodeSocketColor)
        _ = create_socket(interface, "Color Alpha", NodeSocketFloat)
        _ = create_socket(interface, "Control", NodeSocketColor)
        _ = create_socket(interface, "Normal", NodeSocketColor)
        _ = create_socket(interface, "Tint Color", NodeSocketColor)
        _ = create_socket(interface, "IOR", NodeSocketFloat)
        _ = create_socket(interface, "AO", NodeSocketColor)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        links = self.node_tree.links
        group_input = create_node(nodes, 0, 0, NodeGroupInput)
        group_output = create_node(nodes, 0, 0, NodeGroupOutput)

        bsdf = create_node(nodes, 0, 0, ShaderNodeBsdfPrincipled)
        color_mix = create_node(nodes, 0, 0, ShaderNodeMix)
        color_mix.data_type = "RGBA"
        color_mix.blend_type = "MULTIPLY"
        assign_value(color_mix, 0, 1.0)
        create_link(links, group_input, color_mix, 0, 6)
        create_link(links, group_input, color_mix, 4, 7)

        ao_mix = create_node(nodes, 0, 0, ShaderNodeMix)
        ao_mix.data_type = "RGBA"
        ao_mix.blend_type = "MULTIPLY"
        assign_value(ao_mix, 0, 1.0)
        create_link(links, color_mix, ao_mix, 2, 6)
        create_link(links, group_input, ao_mix, 6, 7)
        create_link(links, ao_mix, bsdf, 2, 0)

        norm_normalize = create_node(nodes, 0, 0, ShaderNodeGroup)
        norm_normalize.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)
        assign_value(norm_normalize, 1, 1.0)
        create_link(links, group_input, norm_normalize, 3, 0)

        normal_map = create_node(nodes, 0, 0, ShaderNodeNormalMap)
        create_link(links, norm_normalize, normal_map, 0, 1)
        if bpy.app.version >= (5, 2, 0):
            create_link(links, normal_map, bsdf, 0, 6)
        else:
            create_link(links, normal_map, bsdf, 0, 5)

        create_link(links, group_input, bsdf, 1, 4)
        create_link(links, group_input, bsdf, 2, 2)
        create_link(links, bsdf, group_output, 0, 0)
