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
    ShaderNodeMath,
    ShaderNodeMixShader,
    ShaderNodeNewGeometry, ShaderNodeNormalMap, ShaderNodeGroup, ShaderNodeTree, ShaderNodeMix,
)

from .norm_normalize import NormNormalize
from ..utils import create_node, create_socket, create_link, assign_value

__all__ = ["ColorTintDecal"]


class ColorTintDecal:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Color Tint Decal Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Color Tint Decal Shader"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        _ = create_socket(interface, "Color Texture", NodeSocketColor)
        _ = create_socket(interface, "Color Alpha", NodeSocketFloat)
        _ = create_socket(interface, "Normal Map", NodeSocketColor)
        _ = create_socket(interface, "Roughness", NodeSocketFloat)
        _ = create_socket(interface, "Opacity", NodeSocketFloat)
        _ = create_socket(interface, "Metallic", NodeSocketFloat)
        _ = create_socket(interface, "Normal Intensity", NodeSocketFloat)
        _ = create_socket(interface, "Tint Color", NodeSocketColor)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        input = create_node(nodes, 0, 0, NodeGroupInput)
        output = create_node(nodes, 0, 0, NodeGroupOutput)

        bsdf = create_node(nodes, 0, 0, ShaderNodeBsdfPrincipled)

        math = create_node(nodes, 0, 0, ShaderNodeMath)
        math.operation = "MULTIPLY"

        geometry = create_node(nodes, 0, 0, ShaderNodeNewGeometry)
        mix_shader = create_node(nodes, 0, 0, ShaderNodeMixShader)
        transparent = create_node(nodes, 0, 0, ShaderNodeBsdfTransparent)

        normal_map = create_node(nodes, 0, 0, ShaderNodeNormalMap)

        normalize = create_node(nodes, 0, 0, ShaderNodeGroup)
        normalize.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)
        assign_value(normalize, 1, 1.0)

        mix = create_node(nodes, 0, 0, ShaderNodeMix)
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY" #TODO: Figure out blending logic
        assign_value(mix, 0, 1.0)

        links = self.node_tree.links
        create_link(links, input, mix, 0, 6)
        create_link(links, input, mix, 7, 7)
        create_link(links, input, normalize, 2, 0)
        create_link(links, normalize, normal_map, 0, 1)
        create_link(links, input, normal_map, 6, 0)
        create_link(links, normal_map, bsdf, 0, 6)
        create_link(links, input, math, 1, 0)
        create_link(links, input, math, 4, 1)
        create_link(links, mix, bsdf, 2, 0)
        create_link(links, math, bsdf, 0, 4)
        create_link(links, input, bsdf, 2, 2)
        create_link(links, input, bsdf, 3, 2)
        create_link(links, input, bsdf, 5, 1)
        create_link(links, geometry, mix_shader, 6, 0)
        create_link(links, bsdf, mix_shader, 0, 1)
        create_link(links, transparent, mix_shader, 0, 2)
        create_link(links, mix_shader, output, 0, 0)
