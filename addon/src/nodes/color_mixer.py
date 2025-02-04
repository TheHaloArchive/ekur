import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    ShaderNodeMath,
    ShaderNodeMix,
)

from ..utils import create_node, create_socket


class ColorMixer:
    def __init__(self) -> None:
        self.node_tree = bpy.data.node_groups.get("Color Mixer")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Color Mixer",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        interface = self.node_tree.interface
        _ = create_socket(interface, "Color", NodeSocketColor, False)
        _ = create_socket(interface, "Gradient Out", NodeSocketFloat)
        _ = create_socket(interface, "Top", NodeSocketColor)
        _ = create_socket(interface, "Mid", NodeSocketColor)
        _ = create_socket(interface, "Bot", NodeSocketColor)

    def create_nodes(self) -> None:
        input = create_node(self.node_tree.nodes, -474, 0, NodeGroupInput)
        output = create_node(self.node_tree.nodes, 530, 4, NodeGroupOutput)

        madd = create_node(self.node_tree.nodes, -239, 316, ShaderNodeMath)
        madd.operation = "MULTIPLY_ADD"
        _: NodeSocketFloat = madd.inputs[1]
        _.default_value = 2.0
        _: NodeSocketFloat = madd.inputs[2]
        _.default_value = -1.0
        madd.location = (-239, 316)

        madd2 = create_node(self.node_tree.nodes, -240, 125, ShaderNodeMath)
        madd2.operation = "MULTIPLY_ADD"
        _: NodeSocketFloat = madd2.inputs[1]
        _.default_value = -2.0
        _: NodeSocketFloat = madd2.inputs[2]
        _.default_value = 1.0

        mix = create_node(self.node_tree.nodes, 300, 80, ShaderNodeMix)
        mix.clamp_factor = True
        mix.clamp_result = True
        mix.data_type = "RGBA"

        mix1 = create_node(self.node_tree.nodes, 79, 135, ShaderNodeMix)
        mix1.clamp_factor = True
        mix1.clamp_result = True
        mix1.data_type = "RGBA"

        links = self.node_tree.links
        _ = links.new(input.outputs[2], mix1.inputs[6])
        _ = links.new(mix1.outputs[2], mix.inputs[6])
        _ = links.new(input.outputs[3], mix.inputs[7])
        _ = links.new(mix.outputs[2], output.inputs[0])
        _ = links.new(input.outputs[1], mix1.inputs[7])
        _ = links.new(input.outputs[0], madd.inputs[0])
        _ = links.new(input.outputs[0], madd2.inputs[0])
        _ = links.new(madd.outputs[0], mix1.inputs[0])
        _ = links.new(madd2.outputs[0], mix.inputs[0])
