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
    ShaderNodeMixRGB,
    ShaderNodeNormalMap,
    ShaderNodeSeparateColor,
    ShaderNodeTree,
)

from .norm_normalize import NormNormalize

from ..utils import assign_value, create_node, create_socket

__all__ = ["DiffuseShader"]


class DiffuseShader:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Diffuse Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Diffuse Shader")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        _ = create_socket(interface, "Color Texture", NodeSocketColor)
        control = create_socket(interface, "Control Texture", NodeSocketColor)
        control.default_value = (0.0, 1.0, 0.0, 0.0)
        _ = create_socket(interface, "Normal Texture", NodeSocketColor)
        rw = create_socket(interface, "Roughness White", NodeSocketFloat)
        rw.default_value = 0.0
        rb = create_socket(interface, "Roughness Black", NodeSocketFloat)
        rb.default_value = 1.0
        mw = create_socket(interface, "Metallic White", NodeSocketFloat)
        mw.default_value = 0.0
        mb = create_socket(interface, "Metallic Black", NodeSocketFloat)
        mb.default_value = 1.0
        _ = create_socket(interface, "Emission Tint", NodeSocketColor)
        _ = create_socket(interface, "Emission Amount", NodeSocketFloat)
        _ = create_socket(interface, "Emission Intensity", NodeSocketFloat)
        _ = create_socket(interface, "Color Tint", NodeSocketColor)
        _ = create_socket(interface, "Color Alpha", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes

        ao_multiply = create_node(nodes, 0, 0, ShaderNodeMixRGB)
        ao_multiply.blend_type = "MULTIPLY"
        assign_value(ao_multiply, 0, 1.0)

        input = create_node(nodes, 0, 0, NodeGroupInput)
        output = create_node(nodes, 0, 0, NodeGroupOutput)
        srgb = create_node(nodes, 0, 0, ShaderNodeSeparateColor)
        rough_mix = create_node(nodes, 0, 0, ShaderNodeMix)
        metal_mix = create_node(nodes, 0, 0, ShaderNodeMix)
        bsdf = create_node(nodes, 0, 0, ShaderNodeBsdfPrincipled)
        normal_map = create_node(nodes, 0, 0, ShaderNodeNormalMap)

        normalize = create_node(nodes, 0, 0, ShaderNodeGroup)
        normalize.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)
        assign_value(normalize, 1, 1.0)

        color_tint = create_node(nodes, 0, 0, ShaderNodeMix)
        color_tint.data_type = "RGBA"
        color_tint.blend_type = "COLOR"
        assign_value(color_tint, 0, 0.999)

        em_tint = create_node(nodes, 0, 0, ShaderNodeMix)
        em_tint.data_type = "RGBA"
        em_tint.blend_type = "COLOR"
        assign_value(em_tint, 0, 0.999)

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
