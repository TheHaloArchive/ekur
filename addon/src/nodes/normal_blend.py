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
    NodeSocketVector,
    NodeTree,
    ShaderNodeGroup,
    ShaderNodeNormalMap,
    ShaderNodeSeparateColor,
    ShaderNodeTree,
)

from ..utils import assign_value, create_node, create_socket, create_link
from .layer_overlay_bool_norm import LayerOverlayBoolNorm
from .norm_normalize import NormNormalize
from .normal_map_combine_orientation import NormalMapCombineOrientationNonNorm

__all__ = ["NormalBlend"]


class NormalBlend:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Normal Blend")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Normal Blend")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Result", NodeSocketVector, False)
        _ = create_socket(interface, "MacroMask Color", NodeSocketColor)
        _ = create_socket(interface, "MacroMask Alpha", NodeSocketFloat)
        _ = create_socket(interface, "Macro Normal", NodeSocketColor)
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

        group_input = create_node(nodes, -660, 0, NodeGroupInput)
        group_output = create_node(nodes, 1237, 128, NodeGroupOutput)

        separate_color = create_node(nodes, -483, 121, ShaderNodeSeparateColor)
        separate_color.mode = "RGB"

        layer_overlay_bool_col_003 = create_node(nodes, -112, 28, ShaderNodeGroup)
        layer_overlay_bool_col_003.node_tree = cast(
            ShaderNodeTree, LayerOverlayBoolNorm().node_tree
        )
        assign_value(layer_overlay_bool_col_003, 2, (0.5, 0.5, 1.0, 1.0))

        layer_overlay_bool_col = create_node(nodes, 82, 27, ShaderNodeGroup)
        layer_overlay_bool_col.node_tree = cast(ShaderNodeTree, LayerOverlayBoolNorm().node_tree)

        layer_overlay_bool_col_001 = create_node(nodes, 259, 26, ShaderNodeGroup)
        layer_overlay_bool_col_001.node_tree = cast(
            ShaderNodeTree, LayerOverlayBoolNorm().node_tree
        )

        layer_overlay_bool_col_002 = create_node(nodes, 433, 30, ShaderNodeGroup)
        layer_overlay_bool_col_002.node_tree = cast(
            ShaderNodeTree, LayerOverlayBoolNorm().node_tree
        )

        normal_map_combine_orientation = create_node(nodes, 793, 116, ShaderNodeGroup)
        normal_map_combine_orientation.node_tree = cast(
            ShaderNodeTree, NormalMapCombineOrientationNonNorm().node_tree
        )
        assign_value(normal_map_combine_orientation, 0, 1.0)

        normal_map = create_node(nodes, 1029, 174, ShaderNodeNormalMap)
        normal_map.space = "TANGENT"
        normal_map.uv_map = ""
        assign_value(normal_map, 0, 1.0)

        norm_normalize = create_node(nodes, 171, 339, ShaderNodeGroup)
        norm_normalize.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)
        assign_value(norm_normalize, 1, 1.0)

        norm_normalize_001 = create_node(nodes, 613, -1, ShaderNodeGroup)
        norm_normalize_001.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)
        assign_value(norm_normalize_001, 1, 1.0)

        create_link(links, group_input, separate_color, 0, 0)
        create_link(links, group_input, norm_normalize, 2, 0)
        create_link(links, group_input, layer_overlay_bool_col_003, 3, 3)
        create_link(links, group_input, layer_overlay_bool_col_003, 4, 0)
        create_link(links, group_input, layer_overlay_bool_col, 5, 3)
        create_link(links, group_input, layer_overlay_bool_col, 6, 0)
        create_link(links, group_input, layer_overlay_bool_col_001, 7, 3)
        create_link(links, group_input, layer_overlay_bool_col_001, 8, 0)
        create_link(links, group_input, layer_overlay_bool_col_002, 9, 3)
        create_link(links, group_input, layer_overlay_bool_col_002, 10, 0)
        create_link(links, group_input, layer_overlay_bool_col_002, 1, 1)
        create_link(links, separate_color, layer_overlay_bool_col_003, 0, 1)
        create_link(links, separate_color, layer_overlay_bool_col, 1, 1)
        create_link(links, separate_color, layer_overlay_bool_col_001, 2, 1)
        create_link(links, layer_overlay_bool_col_003, layer_overlay_bool_col, 0, 2)
        create_link(links, layer_overlay_bool_col, layer_overlay_bool_col_001, 0, 2)
        create_link(links, layer_overlay_bool_col_001, layer_overlay_bool_col_002, 0, 2)
        create_link(links, layer_overlay_bool_col_002, norm_normalize_001, 0, 0)
        create_link(links, norm_normalize, normal_map_combine_orientation, 0, 1)
        create_link(links, norm_normalize_001, normal_map_combine_orientation, 0, 2)
        create_link(links, normal_map_combine_orientation, normal_map, 0, 1)
        create_link(links, normal_map, group_output, 0, 0)
