import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketFloat,
    NodeSocketVector,
    ShaderNodeCombineXYZ,
    ShaderNodeMapping,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeUVMap,
)

from ..utils import create_node, create_socket


class BetterUVScaling:
    def __init__(self) -> None:
        self.node_tree = bpy.data.node_groups.get("BetterUVScaling")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="BetterUVScaling",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        interface = self.node_tree.interface
        _ = create_socket(interface, "Finalized Scale", NodeSocketVector, False)
        _ = create_socket(interface, "Base Scale X", NodeSocketFloat)
        _ = create_socket(interface, "Base Scale Y", NodeSocketFloat)
        _ = create_socket(interface, "Detail Scale X", NodeSocketFloat)
        _ = create_socket(interface, "Detail Scale Y", NodeSocketFloat)
        _ = create_socket(interface, "Alternative Transform X", NodeSocketFloat)
        _ = create_socket(interface, "Alternative Transform Y", NodeSocketFloat)

    def create_nodes(self) -> None:
        output = create_node(self.node_tree.nodes, 961, 158, NodeGroupOutput)
        mapping = create_node(self.node_tree.nodes, 796, 250, ShaderNodeMapping)
        combinexyz = create_node(self.node_tree.nodes, 208, 466, ShaderNodeCombineXYZ)
        combinexyz2 = create_node(self.node_tree.nodes, -392, -127, ShaderNodeCombineXYZ)
        uvmap = create_node(self.node_tree.nodes, 215, 134, ShaderNodeUVMap)
        input = create_node(self.node_tree.nodes, -972, 0, NodeGroupInput)
        mix = create_node(self.node_tree.nodes, -217, 212, ShaderNodeMix)
        mix2 = create_node(self.node_tree.nodes, 13, 205, ShaderNodeMix)
        add = create_node(self.node_tree.nodes, -15, -136, ShaderNodeMath)

        math_8 = create_node(self.node_tree.nodes, -393, -342, ShaderNodeMath)
        math_8.operation = "WRAP"
        _: NodeSocketFloat = math_8.inputs[1]
        _.default_value = 1.0
        _: NodeSocketFloat = math_8.inputs[2]
        _.default_value = 0.0

        subtract = create_node(self.node_tree.nodes, -214, -225, ShaderNodeMath)
        subtract.operation = "SUBTRACT"
        _: NodeSocketFloat = subtract.inputs[0]
        _.default_value = 1.0

        multiply = create_node(self.node_tree.nodes, -588, -428, ShaderNodeMath)
        multiply.operation = "MULTIPLY"

        multiply2 = create_node(self.node_tree.nodes, -606, -156, ShaderNodeMath)
        multiply2.operation = "MULTIPLY"

        subtract2 = create_node(self.node_tree.nodes, -424, 59, ShaderNodeMath)
        subtract2.operation = "SUBTRACT"
        _: NodeSocketFloat = subtract2.inputs[0]
        _.default_value = 1.0

        compare = create_node(self.node_tree.nodes, -402, 488, ShaderNodeMath)
        compare.operation = "COMPARE"
        _: NodeSocketFloat = compare.inputs[1]
        _.default_value = 0.5
        _: NodeSocketFloat = compare.inputs[2]
        _.default_value = 0.0

        compare2 = create_node(self.node_tree.nodes, -165, 522, ShaderNodeMath)
        compare2.operation = "COMPARE"
        _: NodeSocketFloat = compare2.inputs[1]
        _.default_value = 1.0
        _: NodeSocketFloat = compare2.inputs[2]
        _.default_value = 0.0

        links = self.node_tree.links
        _ = links.new(math_8.outputs[0], subtract.inputs[1])
        _ = links.new(uvmap.outputs[0], mapping.inputs[0])
        _ = links.new(combinexyz.outputs[0], mapping.inputs[1])
        _ = links.new(multiply.outputs[0], math_8.inputs[0])
        _ = links.new(multiply2.outputs[0], combinexyz2.inputs[0])
        _ = links.new(multiply.outputs[0], combinexyz2.inputs[1])
        _ = links.new(combinexyz2.outputs[0], mapping.inputs[3])
        _ = links.new(subtract.outputs[0], add.inputs[1])
        _ = links.new(compare.outputs[0], mix.inputs[0])
        _ = links.new(subtract2.outputs[0], mix.inputs[6])
        _ = links.new(mix.outputs[2], mix2.inputs[6])
        _ = links.new(compare2.outputs[0], mix2.inputs[0])
        _ = links.new(add.outputs[0], combinexyz.inputs[1])
        _ = links.new(input.outputs[0], multiply2.inputs[0])
        _ = links.new(input.outputs[4], combinexyz.inputs[0])
        _ = links.new(input.outputs[5], subtract2.inputs[1])
        _ = links.new(input.outputs[5], compare.inputs[0])
        _ = links.new(input.outputs[5], compare2.inputs[0])
        _ = links.new(mapping.outputs[0], output.inputs[0])
        _ = links.new(input.outputs[5], mix.inputs[7])
        _ = links.new(subtract2.outputs[0], mix.inputs[2])
        _ = links.new(input.outputs[5], mix.inputs[3])
        _ = links.new(mix.outputs[0], mix2.inputs[2])
        _ = links.new(input.outputs[5], mix2.inputs[3])
        _ = links.new(mix2.outputs[0], add.inputs[0])
        _ = links.new(input.outputs[2], multiply2.inputs[1])
        _ = links.new(input.outputs[3], multiply.inputs[1])
        _ = links.new(input.outputs[1], multiply.inputs[0])
