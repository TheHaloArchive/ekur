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
)

from .norm_normalize import NormNormalize

from ..utils import create_node, create_socket


class DiffuseShader:
    def __init__(self) -> None:
        self.node_tree = bpy.data.node_groups.get("Diffuse Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Diffuse Shader",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        _ = create_socket(interface, "Color Texture", NodeSocketColor)
        _ = create_socket(interface, "Control Texture", NodeSocketColor)
        _ = create_socket(interface, "Normal Texture", NodeSocketColor)
        _ = create_socket(interface, "Roughness White", NodeSocketFloat)
        _ = create_socket(interface, "Roughness Black", NodeSocketFloat)
        _ = create_socket(interface, "Metallic White", NodeSocketFloat)
        _ = create_socket(interface, "Metallic Black", NodeSocketFloat)
        _ = create_socket(interface, "Emission Tint", NodeSocketColor)
        _ = create_socket(interface, "Emission Amount", NodeSocketFloat)
        _ = create_socket(interface, "Emission Intensity", NodeSocketFloat)
        _ = create_socket(interface, "Color Tint", NodeSocketColor)
        _ = create_socket(interface, "Color Alpha", NodeSocketFloat)

    def create_nodes(self) -> None:
        nodes = self.node_tree.nodes

        ao_multiply = create_node(nodes, 0, 0, ShaderNodeMixRGB)
        ao_multiply.blend_type = "MULTIPLY"
        fac: NodeSocketFloat = ao_multiply.inputs[0]
        fac.default_value = 1.0

        input = create_node(nodes, 0, 0, NodeGroupInput)
        output = create_node(nodes, 0, 0, NodeGroupOutput)
        srgb = create_node(nodes, 0, 0, ShaderNodeSeparateColor)
        rough_mix = create_node(nodes, 0, 0, ShaderNodeMix)
        metal_mix = create_node(nodes, 0, 0, ShaderNodeMix)
        bsdf = create_node(nodes, 0, 0, ShaderNodeBsdfPrincipled)
        normal_map = create_node(nodes, 0, 0, ShaderNodeNormalMap)

        normalize = create_node(nodes, 0, 0, ShaderNodeGroup)
        normalize.node_tree = NormNormalize().node_tree  # pyright: ignore[reportAttributeAccessIssue]
        invert: NodeSocketFloat = normalize.inputs[1]
        invert.default_value = 1.0

        color_tint = create_node(nodes, 0, 0, ShaderNodeMix)
        color_tint.data_type = "RGBA"
        color_tint.blend_type = "COLOR"

        em_tint = create_node(nodes, 0, 0, ShaderNodeMix)
        em_tint.data_type = "RGBA"
        em_tint.blend_type = "COLOR"

        links = self.node_tree.links
        _ = links.new(input.outputs[0], color_tint.inputs[6])
        _ = links.new(input.outputs[10], color_tint.inputs[7])
        _ = links.new(color_tint.outputs[2], ao_multiply.inputs[1])
        _ = links.new(input.outputs[0], em_tint.inputs[6])
        _ = links.new(input.outputs[7], em_tint.inputs[7])
        _ = links.new(em_tint.outputs[2], bsdf.inputs[27])
        _ = links.new(input.outputs[8], bsdf.inputs[28])
        _ = links.new(color_tint.outputs[2], ao_multiply.inputs[1])
        _ = links.new(input.outputs[1], srgb.inputs[0])
        _ = links.new(srgb.outputs[1], ao_multiply.inputs[2])
        _ = links.new(ao_multiply.outputs[0], bsdf.inputs[0])
        _ = links.new(srgb.outputs[0], rough_mix.inputs[0])
        _ = links.new(input.outputs[3], rough_mix.inputs[2])
        _ = links.new(input.outputs[4], rough_mix.inputs[3])
        _ = links.new(rough_mix.outputs[0], bsdf.inputs[2])
        _ = links.new(srgb.outputs[2], metal_mix.inputs[0])
        _ = links.new(input.outputs[6], metal_mix.inputs[2])
        _ = links.new(input.outputs[5], metal_mix.inputs[3])
        _ = links.new(metal_mix.outputs[0], bsdf.inputs[1])
        _ = links.new(input.outputs[2], normalize.inputs[0])
        _ = links.new(normalize.outputs[0], normal_map.inputs[1])
        _ = links.new(normal_map.outputs[0], bsdf.inputs[5])
        _ = links.new(input.outputs[11], bsdf.inputs[4])
        _ = links.new(bsdf.outputs[0], output.inputs[0])
