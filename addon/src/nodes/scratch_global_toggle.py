# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import NodeGroupInput, NodeGroupOutput, NodeSocketFloat, NodeTree, ShaderNodeMix

from ..utils import create_node, create_socket, create_link

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
        create_link(links, zone2, output, 0, 0)
        create_link(links, zone3, output, 0, 1)
        create_link(links, mix, output, 0, 2)
        create_link(links, zone5, output, 0, 3)
        create_link(links, zone6, output, 0, 4)
        create_link(links, dust, output, 0, 5)
        create_link(links, input, zone2, 7, 0)
        create_link(links, input, zone3, 7, 0)
        create_link(links, input, mix, 7, 0)
        create_link(links, input, zone5, 7, 0)
        create_link(links, input, zone6, 7, 0)
        create_link(links, input, dust, 7, 0)
        create_link(links, input, zone2, 0, 3)
        create_link(links, input, zone3, 0, 3)
        create_link(links, input, mix, 0, 3)
        create_link(links, input, zone5, 0, 3)
        create_link(links, input, zone6, 0, 3)
        create_link(links, input, dust, 0, 3)
        create_link(links, input, zone2, 1, 2)
        create_link(links, input, zone3, 2, 2)
        create_link(links, input, mix, 3, 2)
        create_link(links, input, zone5, 4, 2)
        create_link(links, input, zone6, 5, 2)
        create_link(links, input, dust, 6, 2)
