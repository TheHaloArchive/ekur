# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
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
    ShaderNodeNewGeometry,
)

from ..utils import create_node, create_socket

__all__ = ["ColorDecal"]


class ColorDecal:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Color Decal Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Color Decal Shader"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        _ = create_socket(interface, "Color Texture", NodeSocketColor)
        _ = create_socket(interface, "Alpha Map", NodeSocketFloat)
        _ = create_socket(interface, "Roughness", NodeSocketFloat)
        _ = create_socket(interface, "Opacity", NodeSocketFloat)
        _ = create_socket(interface, "Metallic", NodeSocketFloat)

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

        _ = self.node_tree.links.new(input.outputs[1], math.inputs[0])
        _ = self.node_tree.links.new(input.outputs[3], math.inputs[1])
        _ = self.node_tree.links.new(input.outputs[0], bsdf.inputs[0])
        _ = self.node_tree.links.new(math.outputs[0], bsdf.inputs[4])
        _ = self.node_tree.links.new(input.outputs[2], bsdf.inputs[2])
        _ = self.node_tree.links.new(input.outputs[4], bsdf.inputs[1])
        _ = self.node_tree.links.new(geometry.outputs[6], mix_shader.inputs[0])
        _ = self.node_tree.links.new(bsdf.outputs[0], mix_shader.inputs[1])
        _ = self.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[2])
        _ = self.node_tree.links.new(mix_shader.outputs[0], output.inputs[0])
