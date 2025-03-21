# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
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

from .better_uv_scaling import BetterUVScaling
from .roughness_math import RoughnessMath

from ..json_definitions import CommonLayer
from ..utils import create_node, create_socket, read_texture

__all__ = ["Layer"]


class Layer:
    def __init__(self, intention: CommonLayer, name: str) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get(name)
        self.intention: CommonLayer = intention
        self.name: str = name
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name=name,
            )
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
        uvscaling.node_tree = BetterUVScaling().node_tree  # pyright: ignore[reportAttributeAccessIssue]

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
        roughnode.node_tree = RoughnessMath().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        uvscaling2 = create_node(nodes, -372, 219, ShaderNodeGroup)
        uvscaling2.node_tree = BetterUVScaling().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        links = self.node_tree.links
        _ = links.new(normal.outputs[0], output.inputs[2])
        _ = links.new(input.outputs[9], reroute10.inputs[0])
        _ = links.new(input.outputs[10], reroute11.inputs[0])
        _ = links.new(reroute10.outputs[0], reroute8.inputs[0])
        _ = links.new(reroute11.outputs[0], reroute7.inputs[0])
        _ = links.new(input.outputs[8], reroute12.inputs[0])
        _ = links.new(reroute12.outputs[0], reroute9.inputs[0])
        _ = links.new(reroute35.outputs[0], gradient.inputs[0])
        _ = links.new(reroute3.outputs[0], normal.inputs[0])
        _ = links.new(reroute5.outputs[0], output.inputs[1])
        _ = links.new(gradient.outputs[0], reroute.inputs[0])
        _ = links.new(reroute.outputs[0], reroute4.inputs[0])
        _ = links.new(reroute4.outputs[0], srgb.inputs[0])
        _ = links.new(srgb.outputs[2], reroute6.inputs[0])
        _ = links.new(srgb.outputs[0], reroute1.inputs[0])
        _ = links.new(reroute1.outputs[0], reroute2.inputs[0])
        _ = links.new(reroute2.outputs[0], output.inputs[0])
        _ = links.new(reroute6.outputs[0], roughnode.inputs[0])
        _ = links.new(reroute9.outputs[0], roughnode.inputs[1])
        _ = links.new(reroute8.outputs[0], roughnode.inputs[2])
        _ = links.new(reroute7.outputs[0], roughnode.inputs[3])
        _ = links.new(roughnode.outputs[0], reroute5.inputs[0])
        _ = links.new(input.outputs[2], uvscaling2.inputs[2])
        _ = links.new(input.outputs[0], uvscaling2.inputs[0])
        _ = links.new(uvscaling2.outputs[0], reroute35.inputs[0])
        _ = links.new(uvscaling.outputs[0], reroute3.inputs[0])
        _ = links.new(input.outputs[0], uvscaling.inputs[0])
        _ = links.new(input.outputs[5], uvscaling.inputs[3])
        _ = links.new(input.outputs[7], uvscaling2.inputs[5])
        _ = links.new(input.outputs[6], uvscaling2.inputs[4])
        _ = links.new(input.outputs[1], uvscaling2.inputs[1])
        _ = links.new(input.outputs[3], uvscaling2.inputs[3])
        _ = links.new(input.outputs[4], uvscaling.inputs[2])
        _ = links.new(input.outputs[1], uvscaling.inputs[1])
        _ = links.new(input.outputs[6], uvscaling.inputs[4])
        _ = links.new(input.outputs[7], uvscaling.inputs[5])
        _ = links.new(input2.outputs[12], output.inputs[6])
        _ = links.new(input2.outputs[13], output.inputs[7])
        _ = links.new(input2.outputs[14], output.inputs[8])
        _ = links.new(input2.outputs[15], output.inputs[9])
        _ = links.new(input2.outputs[16], output.inputs[3])
        _ = links.new(input2.outputs[17], output.inputs[4])
        _ = links.new(input2.outputs[11], output.inputs[5])
