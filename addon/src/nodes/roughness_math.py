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


class RoughnessMath:
    def __init__(self) -> None:
        self.node_tree = bpy.data.node_groups.get("Roughness Math")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Roughness Math",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        interface = self.node_tree.interface
        _ = create_socket(interface, "Color", NodeSocketColor, False)
        _ = create_socket(interface, "Base", NodeSocketFloat)
        _ = create_socket(interface, "Exponent", NodeSocketFloat)
        _ = create_socket(interface, "Roughness Black", NodeSocketColor)
        _ = create_socket(interface, "Roughness White", NodeSocketColor)

    def create_nodes(self) -> None:
        nodes = self.node_tree.nodes
        output = create_node(nodes, 538, 0, NodeGroupOutput)
        input = create_node(nodes, -422, 0, NodeGroupInput)

        multiply = create_node(nodes, 57, 200, ShaderNodeMath)
        multiply.operation = "MULTIPLY"

        divide = create_node(nodes, -90, 15, ShaderNodeMath)
        divide.operation = "DIVIDE"
        _: NodeSocketFloat = divide.inputs[1]
        _.default_value = 4.0

        multiply2 = create_node(nodes, 73, -132, ShaderNodeMath)
        multiply2.operation = "MULTIPLY"

        mix = create_node(nodes, 272, 40, ShaderNodeMix)
        mix.data_type = "RGBA"

        _ = self.node_tree.links.new(input.outputs[1], divide.inputs[0])
        _ = self.node_tree.links.new(divide.outputs[0], multiply.inputs[1])
        _ = self.node_tree.links.new(input.outputs[2], multiply.inputs[0])
        _ = self.node_tree.links.new(multiply.outputs[0], mix.inputs[6])
        _ = self.node_tree.links.new(input.outputs[0], mix.inputs[0])
        _ = self.node_tree.links.new(multiply2.outputs[0], mix.inputs[7])
        _ = self.node_tree.links.new(input.outputs[3], multiply2.inputs[0])
        _ = self.node_tree.links.new(divide.outputs[0], multiply2.inputs[1])
        _ = self.node_tree.links.new(mix.outputs[2], output.inputs[0])
