# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import cast

import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketInt,
    NodeTree,
    ShaderNodeGroup,
    ShaderNodeSeparateColor,
    ShaderNodeTree,
)

from ..utils import assign_value, create_node, create_socket
from .layer_overlay_bool_col import LayerOverlayBoolCol

__all__ = ["ColorBlend"]


class ColorBlend:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Color Blend")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Color Blend")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Result", NodeSocketColor, False)
        _ = create_socket(interface, "MacroMask Color", NodeSocketColor)
        _ = create_socket(interface, "MacroMask Alpha", NodeSocketFloat)
        _ = create_socket(interface, "Layer 1 Color", NodeSocketColor)
        _ = create_socket(interface, "Layer 1 Blend", NodeSocketInt)
        _ = create_socket(interface, "Layer 2 Color", NodeSocketColor)
        _ = create_socket(interface, "Layer 2 Blend", NodeSocketInt)
        _ = create_socket(interface, "Layer 3 Color", NodeSocketColor)
        _ = create_socket(interface, "Layer 3 Blend", NodeSocketInt)
        _ = create_socket(interface, "Layer 4 Color", NodeSocketColor)
        _ = create_socket(interface, "Layer 4 Blend", NodeSocketInt)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        links = self.node_tree.links

        group_output = create_node(nodes, 1158, 34, NodeGroupOutput)
        group_input = create_node(nodes, -660, 0, NodeGroupInput)

        separate_color = create_node(nodes, -483, 121, ShaderNodeSeparateColor)
        separate_color.mode = "RGB"

        layer_overlay_bool_col = create_node(nodes, 82, 27, ShaderNodeGroup)
        layer_overlay_bool_col.node_tree = cast(ShaderNodeTree, LayerOverlayBoolCol().node_tree)

        layer_overlay_bool_col_001 = create_node(nodes, 259, 26, ShaderNodeGroup)
        layer_overlay_bool_col_001.node_tree = cast(ShaderNodeTree, LayerOverlayBoolCol().node_tree)

        layer_overlay_bool_col_002 = create_node(nodes, 433, 30, ShaderNodeGroup)
        layer_overlay_bool_col_002.node_tree = cast(ShaderNodeTree, LayerOverlayBoolCol().node_tree)

        layer_overlay_bool_col_003 = create_node(nodes, -112, 28, ShaderNodeGroup)
        layer_overlay_bool_col_003.node_tree = cast(ShaderNodeTree, LayerOverlayBoolCol().node_tree)
        assign_value(layer_overlay_bool_col_003, 2, (0.0, 0.0, 0.0, 1.0))

        _ = links.new(group_input.outputs[0], separate_color.inputs[0])
        _ = links.new(layer_overlay_bool_col_003.outputs[0], layer_overlay_bool_col.inputs[2])
        _ = links.new(group_input.outputs[4], layer_overlay_bool_col.inputs[3])
        _ = links.new(separate_color.outputs[1], layer_overlay_bool_col.inputs[1])
        _ = links.new(layer_overlay_bool_col.outputs[0], layer_overlay_bool_col_001.inputs[2])
        _ = links.new(separate_color.outputs[2], layer_overlay_bool_col_001.inputs[1])
        _ = links.new(group_input.outputs[6], layer_overlay_bool_col_001.inputs[3])
        _ = links.new(group_input.outputs[5], layer_overlay_bool_col.inputs[0])
        _ = links.new(group_input.outputs[7], layer_overlay_bool_col_001.inputs[0])
        _ = links.new(layer_overlay_bool_col_001.outputs[0], layer_overlay_bool_col_002.inputs[2])
        _ = links.new(group_input.outputs[2], layer_overlay_bool_col_003.inputs[3])
        _ = links.new(separate_color.outputs[0], layer_overlay_bool_col_003.inputs[1])
        _ = links.new(group_input.outputs[3], layer_overlay_bool_col_003.inputs[0])
        _ = links.new(group_input.outputs[9], layer_overlay_bool_col_002.inputs[0])
        _ = links.new(group_input.outputs[1], layer_overlay_bool_col_002.inputs[1])
        _ = links.new(group_input.outputs[8], layer_overlay_bool_col_002.inputs[3])
        _ = links.new(layer_overlay_bool_col_002.outputs[0], group_output.inputs[0])
