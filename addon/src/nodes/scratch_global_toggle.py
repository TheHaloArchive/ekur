# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy

from bpy.types import NodeGroupInput, NodeGroupOutput, NodeSocketFloat, NodeTree, ShaderNodeMix

from ..utils import create_node, create_socket

__all__ = ["ScratchGlobalToggle"]


class ScratchGlobalToggle:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Scratch Global Toggle")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="Scratch Global Toggle"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if not self.node_tree:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Zone 2", NodeSocketFloat, False)
        _ = create_socket(interface, "Zone 3", NodeSocketFloat, False)
        _ = create_socket(interface, "Zone 4", NodeSocketFloat, False)
        _ = create_socket(interface, "Zone 5", NodeSocketFloat, False)
        _ = create_socket(interface, "Zone 6", NodeSocketFloat, False)
        _ = create_socket(interface, "Zone 7", NodeSocketFloat, False)
        _ = create_socket(interface, "Zone 1", NodeSocketFloat)
        _ = create_socket(interface, "Zone 2", NodeSocketFloat)
        _ = create_socket(interface, "Zone 3", NodeSocketFloat)
        _ = create_socket(interface, "Zone 4", NodeSocketFloat)
        _ = create_socket(interface, "Zone 5", NodeSocketFloat)
        _ = create_socket(interface, "Zone 6", NodeSocketFloat)
        _ = create_socket(interface, "Zone 7", NodeSocketFloat)
        _ = create_socket(interface, "Scratch Global", NodeSocketFloat)

    def create_nodes(self) -> None:
        if not self.node_tree:
            return
        nodes = self.node_tree.nodes

        output = create_node(nodes, 312, 177, NodeGroupOutput)
        dust = create_node(nodes, -16, -450, ShaderNodeMix)
        zone6 = create_node(nodes, -16, -256, ShaderNodeMix)
        zone5 = create_node(nodes, -16, -61, ShaderNodeMix)
        mix = create_node(nodes, -16, 131, ShaderNodeMix)
        zone3 = create_node(nodes, -16, 326, ShaderNodeMix)
        zone2 = create_node(nodes, -16, 519, ShaderNodeMix)
        input = create_node(nodes, -341, 15, NodeGroupInput)

        links = self.node_tree.links
        _ = links.new(zone2.outputs[0], output.inputs[0])
        _ = links.new(zone3.outputs[0], output.inputs[1])
        _ = links.new(mix.outputs[0], output.inputs[2])
        _ = links.new(zone5.outputs[0], output.inputs[3])
        _ = links.new(zone6.outputs[0], output.inputs[4])
        _ = links.new(dust.outputs[0], output.inputs[5])
        _ = links.new(input.outputs[7], zone2.inputs[0])
        _ = links.new(input.outputs[7], zone3.inputs[0])
        _ = links.new(input.outputs[7], mix.inputs[0])
        _ = links.new(input.outputs[7], zone5.inputs[0])
        _ = links.new(input.outputs[7], zone6.inputs[0])
        _ = links.new(input.outputs[7], dust.inputs[0])
        _ = links.new(input.outputs[0], zone2.inputs[3])
        _ = links.new(input.outputs[0], zone3.inputs[3])
        _ = links.new(input.outputs[0], mix.inputs[3])
        _ = links.new(input.outputs[0], zone5.inputs[3])
        _ = links.new(input.outputs[0], zone6.inputs[3])
        _ = links.new(input.outputs[0], dust.inputs[3])
        _ = links.new(input.outputs[1], zone2.inputs[2])
        _ = links.new(input.outputs[2], zone3.inputs[2])
        _ = links.new(input.outputs[3], mix.inputs[2])
        _ = links.new(input.outputs[4], zone5.inputs[2])
        _ = links.new(input.outputs[5], zone6.inputs[2])
        _ = links.new(input.outputs[6], dust.inputs[2])
