# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import cast

import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeReroute,
    NodeSocketFloat,
    NodeSocketVector,
    NodeTree,
    ShaderNodeClamp,
    ShaderNodeCombineXYZ,
    ShaderNodeGroup,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateXYZ,
    ShaderNodeTree,
    ShaderNodeValue,
)

from ..utils import assign_value, create_node, create_socket, create_link
from .heightaccum_l1 import HeightAccumL1
from .heightblend import HeightBlend

__all__ = ["LayerBlending"]


class LayerBlending:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Layer Blending")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Layer Blending")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Vector", NodeSocketVector, False)
        _ = create_socket(interface, "Value", NodeSocketFloat, False)
        _ = create_socket(interface, "MacroMask", NodeSocketVector)
        _ = create_socket(interface, "Macro.a", NodeSocketFloat)
        _ = create_socket(interface, "L1.Control", NodeSocketVector)
        _ = create_socket(interface, "L1.Extra", NodeSocketVector)
        _ = create_socket(interface, "L2.Control", NodeSocketVector)
        _ = create_socket(interface, "L2.Extra", NodeSocketVector)
        _ = create_socket(interface, "L3.Control", NodeSocketVector)
        _ = create_socket(interface, "L3.Extra", NodeSocketVector)
        _ = create_socket(interface, "L4.Control", NodeSocketVector)
        _ = create_socket(interface, "L4.Extra", NodeSocketVector)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        links = self.node_tree.links

        group_input = create_node(nodes, -2181, 0, NodeGroupInput)
        group_output = create_node(nodes, 2416, -1656, NodeGroupOutput)

        separate_xyz = create_node(nodes, -1981, 546, ShaderNodeSeparateXYZ)
        separate_xyz_002 = create_node(nodes, -698, 1849, ShaderNodeSeparateXYZ)
        separate_xyz_003 = create_node(nodes, 30, -282, ShaderNodeSeparateXYZ)
        separate_xyz_004 = create_node(nodes, 30, -265, ShaderNodeSeparateXYZ)
        separate_xyz_005 = create_node(nodes, 30, -284, ShaderNodeSeparateXYZ)
        separate_xyz_006 = create_node(nodes, 299, -807, ShaderNodeSeparateXYZ)
        separate_xyz_007 = create_node(nodes, 36, -764, ShaderNodeSeparateXYZ)
        separate_xyz_008 = create_node(nodes, 237, -761, ShaderNodeSeparateXYZ)

        reroute = create_node(nodes, -1724, -388, NodeReroute)
        reroute_001 = create_node(nodes, -1096, 1735, NodeReroute)

        heightaccum = create_node(nodes, -302, 1869, ShaderNodeGroup)
        heightaccum.node_tree = cast(ShaderNodeTree, HeightAccumL1().node_tree)

        heightblend = create_node(nodes, 761, -248, ShaderNodeGroup)
        heightblend.node_tree = cast(ShaderNodeTree, HeightBlend().node_tree)
        assign_value(heightblend, 3, 1.0)

        heightblend_001 = create_node(nodes, 926, -340, ShaderNodeGroup)
        heightblend_001.node_tree = cast(ShaderNodeTree, HeightBlend().node_tree)
        assign_value(heightblend_001, 3, 2.0)

        heightblend_002 = create_node(nodes, 856, -277, ShaderNodeGroup)
        heightblend_002.node_tree = cast(ShaderNodeTree, HeightBlend().node_tree)
        assign_value(heightblend_002, 3, 3.0)

        value_006 = create_node(nodes, 336, -127, ShaderNodeValue)
        if value_006.outputs:
            value_006.outputs[0].default_value = 1.0

        combine_xyz = create_node(nodes, 1868, -1623, ShaderNodeCombineXYZ)
        assign_value(combine_xyz, 0, 1.0)

        math_006 = create_node(nodes, 30, -143, ShaderNodeMath)
        math_006.operation = "MULTIPLY"
        assign_value(math_006, 1, 0.5)

        math_007 = create_node(nodes, 207, -58, ShaderNodeMath)
        math_007.operation = "ADD"

        math_008 = create_node(nodes, 377, -74, ShaderNodeMath)
        math_008.operation = "SUBTRACT"

        math_009 = create_node(nodes, 576, -36, ShaderNodeMath)
        math_009.operation = "MINIMUM"
        assign_value(math_009, 0, 1.0)

        math_010 = create_node(nodes, 1843, -234, ShaderNodeMath)
        math_010.operation = "GREATER_THAN"

        math_011 = create_node(nodes, 30, -36, ShaderNodeMath)
        math_011.operation = "SUBTRACT"

        math_012 = create_node(nodes, 211, -55, ShaderNodeMath)
        math_012.operation = "DIVIDE"

        math_013 = create_node(nodes, 1141, -623, ShaderNodeMath)
        math_013.operation = "LESS_THAN"
        assign_value(math_013, 1, 0.0)

        clamp = create_node(nodes, 397, -65, ShaderNodeClamp)
        clamp.clamp_type = "MINMAX"
        assign_value(clamp, 1, 0.0)
        assign_value(clamp, 2, 1.0)

        mix_001 = create_node(nodes, 2217, -672, ShaderNodeMix)
        mix_001.blend_type = "MIX"
        mix_001.clamp_factor = False
        mix_001.clamp_result = False
        mix_001.data_type = "FLOAT"
        mix_001.factor_mode = "UNIFORM"

        math_014 = create_node(nodes, 2003, -811, ShaderNodeMath)
        math_014.operation = "SUBTRACT"
        assign_value(math_014, 0, 1.0)

        math_015 = create_node(nodes, 2409, -676, ShaderNodeMath)
        math_015.operation = "MULTIPLY"

        math_016 = create_node(nodes, 2589, -645, ShaderNodeMath)
        math_016.operation = "POWER"
        assign_value(math_016, 1, 1.0)

        math_017 = create_node(nodes, 30, -36, ShaderNodeMath)
        math_017.operation = "MAXIMUM"

        math_018 = create_node(nodes, 227, -50, ShaderNodeMath)
        math_018.operation = "SUBTRACT"

        math_019 = create_node(nodes, 414, -54, ShaderNodeMath)
        math_019.operation = "MULTIPLY"

        math_020 = create_node(nodes, 581, -57, ShaderNodeMath)
        math_020.operation = "ADD"

        math_021 = create_node(nodes, 30, -208, ShaderNodeMath)
        math_021.operation = "MULTIPLY"
        assign_value(math_021, 1, 0.5)

        math_022 = create_node(nodes, 197, -72, ShaderNodeMath)
        math_022.operation = "ADD"

        math_023 = create_node(nodes, 375, -82, ShaderNodeMath)
        math_023.operation = "SUBTRACT"

        math_024 = create_node(nodes, 572, -36, ShaderNodeMath)
        math_024.operation = "MINIMUM"
        assign_value(math_024, 0, 2.0)

        math_025 = create_node(nodes, 2019, -234, ShaderNodeMath)
        math_025.operation = "GREATER_THAN"

        math_026 = create_node(nodes, 30, -36, ShaderNodeMath)
        math_026.operation = "SUBTRACT"

        math_027 = create_node(nodes, 210, -54, ShaderNodeMath)
        math_027.operation = "DIVIDE"

        math_028 = create_node(nodes, 1294, -588, ShaderNodeMath)
        math_028.operation = "LESS_THAN"
        assign_value(math_028, 1, 0.0)

        clamp_001 = create_node(nodes, 396, -65, ShaderNodeClamp)
        clamp_001.clamp_type = "MINMAX"
        assign_value(clamp_001, 1, 0.0)
        assign_value(clamp_001, 2, 1.0)

        mix_002 = create_node(nodes, 2393, -671, ShaderNodeMix)
        mix_002.blend_type = "MIX"
        mix_002.clamp_factor = False
        mix_002.clamp_result = False
        mix_002.data_type = "FLOAT"
        mix_002.factor_mode = "UNIFORM"

        math_029 = create_node(nodes, 2179, -810, ShaderNodeMath)
        math_029.operation = "SUBTRACT"
        assign_value(math_029, 0, 1.0)

        math_030 = create_node(nodes, 2585, -676, ShaderNodeMath)
        math_030.operation = "MULTIPLY"

        math_031 = create_node(nodes, 2765, -645, ShaderNodeMath)
        math_031.operation = "POWER"
        assign_value(math_031, 1, 1.0)

        math_032 = create_node(nodes, 30, -36, ShaderNodeMath)
        math_032.operation = "MAXIMUM"

        math_033 = create_node(nodes, 227, -51, ShaderNodeMath)
        math_033.operation = "SUBTRACT"

        math_034 = create_node(nodes, 414, -55, ShaderNodeMath)
        math_034.operation = "MULTIPLY"

        math_035 = create_node(nodes, 582, -58, ShaderNodeMath)
        math_035.operation = "ADD"

        math_036 = create_node(nodes, 30, -172, ShaderNodeMath)
        math_036.operation = "MULTIPLY"
        assign_value(math_036, 1, 0.5)

        math_037 = create_node(nodes, 202, -64, ShaderNodeMath)
        math_037.operation = "ADD"

        math_038 = create_node(nodes, 395, -86, ShaderNodeMath)
        math_038.operation = "SUBTRACT"

        math_039 = create_node(nodes, 586, -36, ShaderNodeMath)
        math_039.operation = "MINIMUM"
        assign_value(math_039, 0, 3.0)

        math_040 = create_node(nodes, 1908, -225, ShaderNodeMath)
        math_040.operation = "GREATER_THAN"
        math_040.use_clamp = True

        math_041 = create_node(nodes, 30, -36, ShaderNodeMath)
        math_041.operation = "SUBTRACT"

        math_042 = create_node(nodes, 210, -54, ShaderNodeMath)
        math_042.operation = "DIVIDE"

        math_043 = create_node(nodes, 1190, -594, ShaderNodeMath)
        math_043.operation = "LESS_THAN"
        assign_value(math_043, 1, 0.0)

        clamp_002 = create_node(nodes, 396, -65, ShaderNodeClamp)
        clamp_002.clamp_type = "MINMAX"
        assign_value(clamp_002, 1, 0.0)
        assign_value(clamp_002, 2, 1.0)

        mix_003 = create_node(nodes, 2281, -663, ShaderNodeMix)
        mix_003.blend_type = "MIX"
        mix_003.clamp_factor = False
        mix_003.clamp_result = False
        mix_003.data_type = "FLOAT"
        mix_003.factor_mode = "UNIFORM"

        math_044 = create_node(nodes, 2067, -802, ShaderNodeMath)
        math_044.operation = "SUBTRACT"
        assign_value(math_044, 0, 1.0)

        math_045 = create_node(nodes, 2473, -667, ShaderNodeMath)
        math_045.operation = "MULTIPLY"

        math_046 = create_node(nodes, 2653, -636, ShaderNodeMath)
        math_046.operation = "POWER"
        assign_value(math_046, 1, 1.0)

        math_047 = create_node(nodes, 30, -36, ShaderNodeMath)
        math_047.operation = "MAXIMUM"

        math_048 = create_node(nodes, 227, -51, ShaderNodeMath)
        math_048.operation = "SUBTRACT"

        math_049 = create_node(nodes, 415, -55, ShaderNodeMath)
        math_049.operation = "MULTIPLY"

        math_050 = create_node(nodes, 582, -57, ShaderNodeMath)
        math_050.operation = "ADD"

        create_link(links, group_input, separate_xyz, 0, 0)
        create_link(links, group_input, reroute, 1, 0)
        create_link(links, group_input, separate_xyz_002, 2, 0)
        create_link(links, group_input, separate_xyz_003, 4, 0)
        create_link(links, group_input, separate_xyz_007, 5, 0)
        create_link(links, group_input, separate_xyz_004, 6, 0)
        create_link(links, group_input, separate_xyz_006, 7, 0)
        create_link(links, group_input, separate_xyz_005, 8, 0)
        create_link(links, group_input, separate_xyz_008, 9, 0)

        create_link(links, separate_xyz, reroute_001, 0, 0)
        create_link(links, separate_xyz, heightblend, 1, 2)
        create_link(links, separate_xyz, heightblend_001, 2, 2)

        create_link(links, separate_xyz_002, heightaccum, 1, 0)
        create_link(links, separate_xyz_002, heightaccum, 2, 1)

        create_link(links, separate_xyz_003, heightblend, 1, 0)
        create_link(links, separate_xyz_003, heightblend, 2, 1)

        create_link(links, separate_xyz_004, heightblend_001, 1, 0)
        create_link(links, separate_xyz_004, heightblend_001, 2, 1)

        create_link(links, separate_xyz_005, heightblend_002, 1, 0)
        create_link(links, separate_xyz_005, heightblend_002, 2, 1)

        create_link(links, separate_xyz_006, math_028, 0, 0)
        create_link(links, separate_xyz_006, math_030, 0, 1)
        create_link(links, separate_xyz_006, math_021, 1, 0)
        create_link(links, separate_xyz_006, math_023, 1, 1)
        create_link(links, separate_xyz_006, math_027, 1, 1)
        create_link(links, separate_xyz_006, math_034, 2, 1)

        create_link(links, separate_xyz_007, math_013, 0, 0)
        create_link(links, separate_xyz_007, math_015, 0, 1)
        create_link(links, separate_xyz_007, math_006, 1, 0)
        create_link(links, separate_xyz_007, math_008, 1, 1)
        create_link(links, separate_xyz_007, math_012, 1, 1)
        create_link(links, separate_xyz_007, math_019, 2, 1)

        create_link(links, separate_xyz_008, math_043, 0, 0)
        create_link(links, separate_xyz_008, math_045, 0, 1)
        create_link(links, separate_xyz_008, math_036, 1, 0)
        create_link(links, separate_xyz_008, math_038, 1, 1)
        create_link(links, separate_xyz_008, math_042, 1, 1)
        create_link(links, separate_xyz_008, math_049, 2, 1)

        create_link(links, reroute, heightblend_002, 0, 2)
        create_link(links, reroute_001, heightaccum, 0, 2)

        create_link(links, heightaccum, math_007, 0, 0)
        create_link(links, heightaccum, math_017, 0, 0)
        create_link(links, heightaccum, math_018, 0, 1)
        create_link(links, heightaccum, math_020, 0, 1)

        create_link(links, heightblend, math_010, 0, 0)
        create_link(links, heightblend, math_011, 0, 0)
        create_link(links, heightblend, math_017, 0, 1)

        create_link(links, heightblend_001, math_025, 0, 0)
        create_link(links, heightblend_001, math_026, 0, 0)
        create_link(links, heightblend_001, math_032, 0, 1)

        create_link(links, heightblend_002, math_040, 0, 0)
        create_link(links, heightblend_002, math_041, 0, 0)
        create_link(links, heightblend_002, math_047, 0, 1)

        create_link(links, math_006, math_007, 0, 1)
        create_link(links, math_007, math_008, 0, 0)
        create_link(links, math_008, math_009, 0, 1)
        create_link(links, math_009, math_010, 0, 1)
        create_link(links, math_009, math_011, 0, 1)
        create_link(links, math_011, math_012, 0, 0)
        create_link(links, math_012, clamp, 0, 0)
        create_link(links, math_013, mix_001, 0, 0)
        create_link(links, clamp, math_014, 0, 1)
        create_link(links, clamp, mix_001, 0, 2)
        create_link(links, math_014, mix_001, 0, 3)
        create_link(links, mix_001, math_015, 0, 0)
        create_link(links, math_015, math_016, 0, 0)
        create_link(links, math_016, combine_xyz, 0, 1)

        create_link(links, math_017, math_018, 0, 0)
        create_link(links, math_018, math_019, 0, 0)
        create_link(links, math_019, math_020, 0, 0)
        create_link(links, math_020, math_022, 0, 0)
        create_link(links, math_020, math_032, 0, 0)
        create_link(links, math_020, math_033, 0, 1)
        create_link(links, math_020, math_035, 0, 1)

        create_link(links, math_021, math_022, 0, 1)
        create_link(links, math_022, math_023, 0, 0)
        create_link(links, math_023, math_024, 0, 1)
        create_link(links, math_024, math_025, 0, 1)
        create_link(links, math_024, math_026, 0, 1)
        create_link(links, math_026, math_027, 0, 0)
        create_link(links, math_027, clamp_001, 0, 0)
        create_link(links, math_028, mix_002, 0, 0)
        create_link(links, clamp_001, math_029, 0, 1)
        create_link(links, clamp_001, mix_002, 0, 2)
        create_link(links, math_029, mix_002, 0, 3)
        create_link(links, mix_002, math_030, 0, 0)
        create_link(links, math_030, math_031, 0, 0)
        create_link(links, math_031, combine_xyz, 0, 2)

        create_link(links, math_032, math_033, 0, 0)
        create_link(links, math_033, math_034, 0, 0)
        create_link(links, math_034, math_035, 0, 0)
        create_link(links, math_035, math_037, 0, 0)
        create_link(links, math_035, math_047, 0, 0)
        create_link(links, math_035, math_048, 0, 1)
        create_link(links, math_035, math_050, 0, 1)

        create_link(links, math_036, math_037, 0, 1)
        create_link(links, math_037, math_038, 0, 0)
        create_link(links, math_038, math_039, 0, 1)
        create_link(links, math_039, math_040, 0, 1)
        create_link(links, math_039, math_041, 0, 1)
        create_link(links, math_041, math_042, 0, 0)
        create_link(links, math_042, clamp_002, 0, 0)
        create_link(links, math_043, mix_003, 0, 0)
        create_link(links, clamp_002, math_044, 0, 1)
        create_link(links, clamp_002, mix_003, 0, 2)
        create_link(links, math_044, mix_003, 0, 3)
        create_link(links, mix_003, math_045, 0, 0)
        create_link(links, math_045, math_046, 0, 0)
        create_link(links, math_046, group_output, 0, 1)

        create_link(links, math_047, math_048, 0, 0)
        create_link(links, math_048, math_049, 0, 0)
        create_link(links, math_049, math_050, 0, 0)

        create_link(links, combine_xyz, group_output, 0, 0)
