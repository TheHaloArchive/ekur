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
    ShaderNodeBsdfTransparent,
    ShaderNodeGroup,
    ShaderNodeMix,
    ShaderNodeMixRGB,
    ShaderNodeMixShader,
    ShaderNodeNewGeometry,
    ShaderNodeNormalMap,
    ShaderNodeSeparateColor,
    ShaderNodeTree,
    ShaderNodeValToRGB,
)

from ..utils import assign_value, create_node, create_socket, create_link
from .norm_normalize import NormNormalize

__all__ = ["Decal"]


class Decal:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Decal Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Decal Shader")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        _ = create_socket(interface, "Control Texture", NodeSocketColor)
        _ = create_socket(interface, "Normal Texture", NodeSocketColor)
        _ = create_socket(interface, "Top Color", NodeSocketColor)
        _ = create_socket(interface, "Mid Color", NodeSocketColor)
        _ = create_socket(interface, "Bottom Color", NodeSocketColor)
        _ = create_socket(interface, "Roughness White", NodeSocketFloat)
        _ = create_socket(interface, "Roughness Black", NodeSocketFloat)
        _ = create_socket(interface, "Metallic", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        input = create_node(nodes, 0, 0, NodeGroupInput)
        output = create_node(nodes, 0, 0, NodeGroupOutput)

        srgb = create_node(nodes, 0, 0, ShaderNodeSeparateColor)
        color_ramp = create_node(nodes, 0, 0, ShaderNodeValToRGB)
        if color_ramp.color_ramp:
            color_ramp.color_ramp.elements[0].position = 0.5

        color_ramp2 = create_node(nodes, 0, 0, ShaderNodeValToRGB)
        if color_ramp2.color_ramp:
            color_ramp2.color_ramp.elements[1].position = 0.5

        mix = create_node(nodes, 0, 0, ShaderNodeMixRGB)
        mix2 = create_node(nodes, 0, 0, ShaderNodeMixRGB)

        rough_mix = create_node(nodes, 0, 0, ShaderNodeMix)
        bsdf = create_node(nodes, 0, 0, ShaderNodeBsdfPrincipled)

        normal_map = create_node(nodes, 0, 0, ShaderNodeNormalMap)
        normalize = create_node(nodes, 0, 0, ShaderNodeGroup)
        normalize.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)
        assign_value(normalize, 1, 1.0)

        geometry = create_node(nodes, 0, 0, ShaderNodeNewGeometry)
        mix_shader = create_node(nodes, 0, 0, ShaderNodeMixShader)
        transparent = create_node(nodes, 0, 0, ShaderNodeBsdfTransparent)

        links = self.node_tree.links
        create_link(links, input, srgb, 0, 0)
        create_link(links, srgb, color_ramp, 0, 0)
        create_link(links, srgb, color_ramp2, 0, 0)
        create_link(links, color_ramp2, mix, 0, 0)
        create_link(links, input, mix, 2, 1)
        create_link(links, input, mix, 3, 2)
        create_link(links, color_ramp, mix2, 0, 0)
        create_link(links, mix, mix2, 0, 1)
        create_link(links, input, mix2, 4, 2)
        create_link(links, mix2, bsdf, 0, 0)
        create_link(links, input, bsdf, 7, 1)
        create_link(links, srgb, rough_mix, 2, 0)
        create_link(links, input, rough_mix, 5, 2)
        create_link(links, input, rough_mix, 6, 3)
        create_link(links, srgb, bsdf, 1, 4)
        create_link(links, rough_mix, bsdf, 0, 2)
        create_link(links, input, normalize, 1, 0)
        create_link(links, normalize, normal_map, 0, 1)
        if bpy.app.version >= (5, 2, 0):
            create_link(links, normal_map, bsdf, 0, 6)
        else:
            create_link(links, normal_map, bsdf, 0, 5)
        create_link(links, geometry, mix_shader, 6, 0)
        create_link(links, bsdf, mix_shader, 0, 1)
        create_link(links, transparent, mix_shader, 0, 2)
        create_link(links, mix_shader, output, 0, 0)
