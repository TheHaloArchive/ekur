# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy

from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeGroup,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
)

from .norm_normalize import NormNormalize
from .normal_map_combine_orientation import NormalMapCombineOrientation
from ..utils import assign_value, create_node, create_socket

__all__ = ["DetailNormals"]


class DetailNormals:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Detail Normals")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Detail Normals")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Normal", NodeSocketColor, False)
        _ = create_socket(interface, "ASG", NodeSocketColor)
        _ = create_socket(interface, "Mask 0", NodeSocketColor)
        _ = create_socket(interface, "Mask 1", NodeSocketColor)
        _ = create_socket(interface, "Base Normal", NodeSocketColor)
        _ = create_socket(interface, "Slot 1", NodeSocketColor)
        _ = create_socket(interface, "Slot 2", NodeSocketColor)
        _ = create_socket(interface, "Slot 3", NodeSocketColor)
        _ = create_socket(interface, "Slot 4", NodeSocketColor)
        _ = create_socket(interface, "Slot 5", NodeSocketColor)
        _ = create_socket(interface, "Slot 6", NodeSocketColor)
        _ = create_socket(interface, "Slot 7", NodeSocketColor)
        _ = create_socket(interface, "Grime", NodeSocketColor)
        _ = create_socket(interface, "Scratch Amount", NodeSocketFloat)
        _ = create_socket(interface, "Grime Amount", NodeSocketFloat)
        _ = create_socket(interface, "Detail Normal Toggle", NodeSocketFloat)
        _ = create_socket(interface, "Normal Flip", NodeSocketFloat)
        _ = create_socket(interface, "Detail Normal Flip", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        subtract = create_node(self.node_tree.nodes, -400, 1083, ShaderNodeMath)
        subtract.operation = "SUBTRACT"
        assign_value(subtract, 1, 1.0)

        mix = create_node(self.node_tree.nodes, -670, 367, ShaderNodeMix)
        mix.data_type = "RGBA"
        mix2 = create_node(self.node_tree.nodes, -473, 367, ShaderNodeMix)
        mix2.data_type = "RGBA"
        mix3 = create_node(self.node_tree.nodes, -301, 367, ShaderNodeMix)
        mix3.data_type = "RGBA"
        mix4 = create_node(self.node_tree.nodes, -127, 367, ShaderNodeMix)
        mix4.data_type = "RGBA"
        mix5 = create_node(self.node_tree.nodes, -878, 367, ShaderNodeMix)
        mix5.data_type = "RGBA"
        grime = create_node(self.node_tree.nodes, 400, 367, ShaderNodeMix)
        grime.clamp_result = True
        grime.data_type = "RGBA"
        scratch = create_node(self.node_tree.nodes, 230, 370, ShaderNodeMix)
        scratch.data_type = "RGBA"
        dust = create_node(self.node_tree.nodes, 50, 370, ShaderNodeMix)
        dust.data_type = "RGBA"

        srgb = create_node(self.node_tree.nodes, -860, 380, ShaderNodeSeparateColor)
        srgb2 = create_node(self.node_tree.nodes, -895, 380, ShaderNodeSeparateColor)
        srgb3 = create_node(self.node_tree.nodes, -900, 760, ShaderNodeSeparateColor)
        output = create_node(self.node_tree.nodes, 1140, 350, NodeGroupOutput)
        input = create_node(self.node_tree.nodes, -1480, 490, NodeGroupInput)

        subtract2 = create_node(self.node_tree.nodes, -400, 1270, ShaderNodeMath)
        subtract2.operation = "SUBTRACT"
        assign_value(subtract2, 1, 1.0)

        grimemath = create_node(self.node_tree.nodes, 0, 1105, ShaderNodeMath)
        grimemath.label = "Grime"

        scratchmath = create_node(self.node_tree.nodes, 0, 1205, ShaderNodeMath)
        scratchmath.label = "Scratch"

        normalize = create_node(self.node_tree.nodes, 600, 480, ShaderNodeGroup)
        normalize.node_tree = NormNormalize().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        normalize2 = create_node(self.node_tree.nodes, 600, 330, ShaderNodeGroup)
        normalize2.node_tree = NormNormalize().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        normcombine = create_node(self.node_tree.nodes, 890, 480, ShaderNodeGroup)
        normcombine.node_tree = NormalMapCombineOrientation().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        links = self.node_tree.links
        _ = links.new(input.outputs[1], srgb2.inputs[0])
        _ = links.new(input.outputs[2], srgb3.inputs[0])
        _ = links.new(input.outputs[0], srgb.inputs[0])
        _ = links.new(srgb.outputs[2], grimemath.inputs[0])
        _ = links.new(subtract.outputs[0], grimemath.inputs[1])
        _ = links.new(srgb.outputs[1], scratchmath.inputs[0])
        _ = links.new(subtract2.outputs[0], scratchmath.inputs[1])
        _ = links.new(input.outputs[12], subtract2.inputs[0])
        _ = links.new(input.outputs[13], subtract.inputs[0])
        _ = links.new(mix5.outputs[2], mix.inputs[6])
        _ = links.new(input.outputs[6], mix.inputs[7])
        _ = links.new(mix.outputs[2], mix2.inputs[6])
        _ = links.new(input.outputs[7], mix2.inputs[7])
        _ = links.new(mix2.outputs[2], mix3.inputs[6])
        _ = links.new(input.outputs[8], mix3.inputs[7])
        _ = links.new(mix3.outputs[2], mix4.inputs[6])
        _ = links.new(input.outputs[9], mix4.inputs[7])
        _ = links.new(mix4.outputs[2], dust.inputs[6])
        _ = links.new(input.outputs[10], dust.inputs[7])
        _ = links.new(dust.outputs[2], scratch.inputs[6])
        _ = links.new(scratchmath.outputs[0], scratch.inputs[0])
        _ = links.new(scratch.outputs[2], grime.inputs[6])
        _ = links.new(grimemath.outputs[0], grime.inputs[0])
        _ = links.new(input.outputs[11], grime.inputs[7])
        _ = links.new(srgb2.outputs[0], mix5.inputs[0])
        _ = links.new(srgb2.outputs[1], mix.inputs[0])
        _ = links.new(srgb2.outputs[2], mix2.inputs[0])
        _ = links.new(srgb3.outputs[0], mix3.inputs[0])
        _ = links.new(srgb3.outputs[1], mix4.inputs[0])
        _ = links.new(input.outputs[4], mix5.inputs[6])
        _ = links.new(input.outputs[5], mix5.inputs[7])
        _ = links.new(grime.outputs[2], normalize2.inputs[0])
        _ = links.new(normalize.outputs[0], normcombine.inputs[1])
        _ = links.new(normalize2.outputs[0], normcombine.inputs[2])
        _ = links.new(normcombine.outputs[0], output.inputs[0])
        _ = links.new(input.outputs[3], normalize.inputs[0])
        _ = links.new(input.outputs[14], normcombine.inputs[0])
        _ = links.new(srgb3.outputs[2], dust.inputs[0])
        _ = links.new(input.outputs[15], normalize.inputs[1])
        _ = links.new(input.outputs[16], normalize2.inputs[1])
