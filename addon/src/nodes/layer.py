# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeReroute,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeGroup,
    ShaderNodeSeparateColor,
    ShaderNodeTexImage,
)

from ..json_definitions import CommonLayer
from ..utils import create_node, create_socket, read_texture, create_link
from .better_uv_scaling import BetterUVScaling
from .roughness_math import RoughnessMath

__all__ = ["Layer"]


class Layer:
    def __init__(self, intention: CommonLayer, name: str) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get(name)
        self.intention: CommonLayer = intention
        self.name: str = name
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name=name)
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if not self.node_tree:
            return
        interface = self.node_tree.interface
        if not interface:
            return

        outputs = interface.new_panel("Outputs")
        _ = create_socket(interface, "Gradient Out", NodeSocketFloat, False, outputs)
        _ = create_socket(interface, "Rough Out", NodeSocketFloat, False, outputs)
        _ = create_socket(interface, "Norm Out", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Scratch Metallic", NodeSocketFloat, False, outputs)
        _ = create_socket(interface, "Scratch Roughness", NodeSocketFloat, False, outputs)
        _ = create_socket(interface, "Metallic", NodeSocketFloat, False, outputs)
        _ = create_socket(interface, "TopColor", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "MidColor", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "BotColor", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Scratch Color", NodeSocketColor, False, outputs)

        scaling = interface.new_panel("Scaling")
        _ = create_socket(interface, "Base-Scale_X", NodeSocketFloat, panel=scaling)
        _ = create_socket(interface, "Base-Scale_Y", NodeSocketFloat, panel=scaling)
        grad_x = create_socket(interface, "Gradient-Scale_X", NodeSocketFloat, panel=scaling)
        grad_x.default_value = self.intention["gradient_transform"][0]
        grad_y = create_socket(interface, "Gradient-Scale_Y", NodeSocketFloat, panel=scaling)
        grad_y.default_value = self.intention["gradient_transform"][1]
        norm_x = create_socket(interface, "Normal-Scale_X", NodeSocketFloat, panel=scaling)
        norm_x.default_value = self.intention["normal_transform"][0]
        norm_y = create_socket(interface, "Normal-Scale_Y", NodeSocketFloat, panel=scaling)
        norm_y.default_value = self.intention["normal_transform"][1]

        transforms = interface.new_panel("Transforms")
        _ = create_socket(interface, "Material Transform X", NodeSocketFloat, panel=transforms)
        _ = create_socket(interface, "Material Transform Y", NodeSocketFloat, panel=transforms)

        specular = interface.new_panel("Specular")
        rough = create_socket(interface, "Roughness", NodeSocketFloat, panel=specular)
        rough.default_value = self.intention["roughness"]
        rough_b = create_socket(interface, "Roughness Black", NodeSocketFloat, panel=specular)
        rough_b.default_value = self.intention["roughness_black"]
        rough_w = create_socket(interface, "Roughness White", NodeSocketFloat, panel=specular)
        rough_w.default_value = self.intention["roughness_white"]
        metal = create_socket(interface, "Metallic", NodeSocketFloat, panel=specular)
        metal.default_value = self.intention["metallic"]

        coloring = interface.new_panel("Coloring")
        top = create_socket(interface, "TopColor", NodeSocketColor, panel=coloring)
        top_color = self.intention["top_color"]
        top.default_value = (top_color[0], top_color[1], top_color[2], 1.0)
        mid = create_socket(interface, "MidColor", NodeSocketColor, panel=coloring)
        mid_color = self.intention["mid_color"]
        mid.default_value = (mid_color[0], mid_color[1], mid_color[2], 1.0)
        bot = create_socket(interface, "BotColor", NodeSocketColor, panel=coloring)
        bot_color = self.intention["bot_color"]
        bot.default_value = (bot_color[0], bot_color[1], bot_color[2], 1.0)

        scratch = interface.new_panel("Scratch Settings")
        col = create_socket(interface, "Scratch Color", NodeSocketColor, panel=scratch)
        scratch_col = self.intention["scratch_color"]
        col.default_value = (scratch_col[0], scratch_col[1], scratch_col[2], 1.0)
        metal = create_socket(interface, "Scratch Metallic", NodeSocketFloat, panel=scratch)
        metal.default_value = self.intention["scratch_metallic"]
        rough = create_socket(interface, "Scratch Roughness", NodeSocketFloat, panel=scratch)
        rough.default_value = self.intention["scratch_roughness"]

    def create_nodes(self) -> None:
        if not self.node_tree:
            return
        nodes = self.node_tree.nodes
        reroute = create_node(nodes, 392, 392, NodeReroute)
        reroute1 = create_node(nodes, 621, 259, NodeReroute)
        reroute2 = create_node(nodes, 621, 182, NodeReroute)
        reroute3 = create_node(nodes, 82, 191, NodeReroute)
        reroute35 = create_node(nodes, -77, -64, NodeReroute)
        reroute4 = create_node(nodes, 392, 190, NodeReroute)
        reroute5 = create_node(nodes, 1031, 160, NodeReroute)
        reroute6 = create_node(nodes, 587, 216, NodeReroute)
        reroute7 = create_node(nodes, -547, -345, NodeReroute)
        reroute8 = create_node(nodes, -527, -322, NodeReroute)
        reroute9 = create_node(nodes, -506, -277, NodeReroute)
        reroute10 = create_node(nodes, -528, -122, NodeReroute)
        reroute11 = create_node(nodes, -547, -144, NodeReroute)
        reroute12 = create_node(nodes, -506, -100, NodeReroute)
        srgb = create_node(nodes, 418, 294, ShaderNodeSeparateColor)
        output = create_node(nodes, 1072, 217, NodeGroupOutput)
        input = create_node(nodes, -745, 156, NodeGroupInput)

        normal = create_node(nodes, -45, 173, ShaderNodeTexImage)
        normal.label = "Normal Map"
        normal.image = read_texture(str(self.intention["normal_bitmap"]))

        uvscaling = create_node(nodes, -375, -9, ShaderNodeGroup)
        uvscaling.node_tree = BetterUVScaling().node_tree  # ty: ignore[invalid-assignment]

        gradient = create_node(nodes, 114, 427, ShaderNodeTexImage)
        gradient.label = "Gradient Map"
        gradient.image = read_texture(str(self.intention["gradient_bitmap"]))

        input2 = create_node(nodes, 755, 153, NodeGroupInput)
        input2.outputs[0].hide = True
        input2.outputs[1].hide = True
        input2.outputs[2].hide = True
        input2.outputs[3].hide = True
        input2.outputs[4].hide = True
        input2.outputs[5].hide = True
        input2.outputs[6].hide = True
        input2.outputs[7].hide = True
        input2.outputs[8].hide = True
        input2.outputs[9].hide = True
        input2.outputs[10].hide = True
        input2.outputs[18].hide = True

        roughnode = create_node(nodes, 772, -242, ShaderNodeGroup)
        roughnode.node_tree = RoughnessMath().node_tree  # ty: ignore[invalid-assignment]

        uvscaling2 = create_node(nodes, -372, 219, ShaderNodeGroup)
        uvscaling2.node_tree = BetterUVScaling().node_tree  # ty: ignore[invalid-assignment]

        links = self.node_tree.links
        create_link(links, normal, output, 0, 2)
        create_link(links, input, reroute10, 9, 0)
        create_link(links, input, reroute11, 10, 0)
        create_link(links, reroute10, reroute8, 0, 0)
        create_link(links, reroute11, reroute7, 0, 0)
        create_link(links, input, reroute12, 8, 0)
        create_link(links, reroute12, reroute9, 0, 0)
        create_link(links, reroute35, gradient, 0, 0)
        create_link(links, reroute3, normal, 0, 0)
        create_link(links, reroute5, output, 0, 1)
        create_link(links, gradient, reroute, 0, 0)
        create_link(links, reroute, reroute4, 0, 0)
        create_link(links, reroute4, srgb, 0, 0)
        create_link(links, srgb, reroute6, 2, 0)
        create_link(links, srgb, reroute1, 0, 0)
        create_link(links, reroute1, reroute2, 0, 0)
        create_link(links, reroute2, output, 0, 0)
        create_link(links, reroute6, roughnode, 0, 0)
        create_link(links, reroute9, roughnode, 0, 1)
        create_link(links, reroute8, roughnode, 0, 2)
        create_link(links, reroute7, roughnode, 0, 3)
        create_link(links, roughnode, reroute5, 0, 0)
        create_link(links, input, uvscaling2, 2, 2)
        create_link(links, input, uvscaling2, 0, 0)
        create_link(links, uvscaling2, reroute35, 0, 0)
        create_link(links, uvscaling, reroute3, 0, 0)
        create_link(links, input, uvscaling, 0, 0)
        create_link(links, input, uvscaling, 5, 3)
        create_link(links, input, uvscaling2, 7, 5)
        create_link(links, input, uvscaling2, 6, 4)
        create_link(links, input, uvscaling2, 1, 1)
        create_link(links, input, uvscaling2, 3, 3)
        create_link(links, input, uvscaling, 4, 2)
        create_link(links, input, uvscaling, 1, 1)
        create_link(links, input, uvscaling, 6, 4)
        create_link(links, input, uvscaling, 7, 5)
        create_link(links, input2, output, 12, 6)
        create_link(links, input2, output, 13, 7)
        create_link(links, input2, output, 14, 8)
        create_link(links, input2, output, 15, 9)
        create_link(links, input2, output, 16, 3)
        create_link(links, input2, output, 17, 4)
        create_link(links, input2, output, 11, 5)
