# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
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

from .norm_normalize import NormNormalize

from ..utils import assign_value, create_node, create_socket


__all__ = ["Hair"]


class Hair:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Hair Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Hair Shader",
            )
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
        _ = links.new(group_input.outputs[0], color_mix.inputs[6])
        _ = links.new(group_input.outputs[4], color_mix.inputs[7])

        ao_mix = create_node(nodes, 0, 0, ShaderNodeMix)
        ao_mix.data_type = "RGBA"
        ao_mix.blend_type = "MULTIPLY"
        assign_value(ao_mix, 0, 1.0)
        _ = links.new(color_mix.outputs[2], ao_mix.inputs[6])
        _ = links.new(group_input.outputs[6], ao_mix.inputs[7])
        _ = links.new(ao_mix.outputs[2], bsdf.inputs[0])

        norm_normalize = create_node(nodes, 0, 0, ShaderNodeGroup)
        norm_normalize.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)
        assign_value(norm_normalize, 1, 1.0)
        _ = links.new(group_input.outputs[3], norm_normalize.inputs[0])

        normal_map = create_node(nodes, 0, 0, ShaderNodeNormalMap)
        _ = links.new(norm_normalize.outputs[0], normal_map.inputs[1])
        _ = links.new(normal_map.outputs[0], bsdf.inputs[5])

        _ = links.new(group_input.outputs[1], bsdf.inputs[4])
        _ = links.new(group_input.outputs[2], bsdf.inputs[2])
        _ = links.new(bsdf.outputs[0], group_output.inputs[0])
