# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketShader,
    ShaderNodeBsdfPrincipled,
    ShaderNodeGroup,
    ShaderNodeMix,
    ShaderNodeMixRGB,
    ShaderNodeNormalMap,
    ShaderNodeSeparateColor,
    ShaderNodeValToRGB,
)

from .norm_normalize import NormNormalize

from ..utils import create_node, create_socket


class Decal:
    def __init__(self) -> None:
        self.node_tree = bpy.data.node_groups.get("Decal Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Decal Shader",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
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
        nodes = self.node_tree.nodes
        input = create_node(nodes, 0, 0, NodeGroupInput)
        output = create_node(nodes, 0, 0, NodeGroupOutput)

        srgb = create_node(nodes, 0, 0, ShaderNodeSeparateColor)
        color_ramp = create_node(nodes, 0, 0, ShaderNodeValToRGB)
        color_ramp.color_ramp.elements[0].position = 0.5

        color_ramp2 = create_node(nodes, 0, 0, ShaderNodeValToRGB)
        color_ramp2.color_ramp.elements[1].position = 0.5

        mix = create_node(nodes, 0, 0, ShaderNodeMixRGB)
        mix2 = create_node(nodes, 0, 0, ShaderNodeMixRGB)

        rough_mix = create_node(nodes, 0, 0, ShaderNodeMix)
        bsdf = create_node(nodes, 0, 0, ShaderNodeBsdfPrincipled)

        normal_map = create_node(nodes, 0, 0, ShaderNodeNormalMap)
        normalize = create_node(nodes, 0, 0, ShaderNodeGroup)
        normalize.node_tree = NormNormalize().node_tree  # pyright: ignore[reportAttributeAccessIssue]
        invert: NodeSocketFloat = normalize.inputs[1]
        invert.default_value = 1.0

        _ = self.node_tree.links.new(input.outputs[0], srgb.inputs[0])
        _ = self.node_tree.links.new(srgb.outputs[0], color_ramp.inputs[0])
        _ = self.node_tree.links.new(srgb.outputs[0], color_ramp2.inputs[0])
        _ = self.node_tree.links.new(color_ramp2.outputs[0], mix.inputs[0])
        _ = self.node_tree.links.new(input.outputs[2], mix.inputs[1])
        _ = self.node_tree.links.new(input.outputs[3], mix.inputs[2])
        _ = self.node_tree.links.new(color_ramp.outputs[0], mix2.inputs[0])
        _ = self.node_tree.links.new(mix.outputs[0], mix2.inputs[1])
        _ = self.node_tree.links.new(input.outputs[4], mix2.inputs[2])
        _ = self.node_tree.links.new(mix2.outputs[0], bsdf.inputs[0])
        _ = self.node_tree.links.new(input.outputs[7], bsdf.inputs[1])
        _ = self.node_tree.links.new(srgb.outputs[2], rough_mix.inputs[0])
        _ = self.node_tree.links.new(input.outputs[5], rough_mix.inputs[2])
        _ = self.node_tree.links.new(input.outputs[6], rough_mix.inputs[3])
        _ = self.node_tree.links.new(srgb.outputs[1], bsdf.inputs[4])
        _ = self.node_tree.links.new(rough_mix.outputs[0], bsdf.inputs[2])
        _ = self.node_tree.links.new(input.outputs[1], normalize.inputs[0])
        _ = self.node_tree.links.new(normalize.outputs[0], normal_map.inputs[1])
        _ = self.node_tree.links.new(normal_map.outputs[0], bsdf.inputs[5])
        _ = self.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
