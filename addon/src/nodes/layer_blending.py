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

from ..utils import assign_value, create_node, create_socket
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
        cast(NodeSocketFloat, value_006.outputs[0]).default_value = 1.0

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

        _ = links.new(group_input.outputs[0], separate_xyz.inputs[0])
        _ = links.new(group_input.outputs[1], reroute.inputs[0])
        _ = links.new(group_input.outputs[2], separate_xyz_002.inputs[0])
        _ = links.new(group_input.outputs[4], separate_xyz_003.inputs[0])
        _ = links.new(group_input.outputs[5], separate_xyz_007.inputs[0])
        _ = links.new(group_input.outputs[6], separate_xyz_004.inputs[0])
        _ = links.new(group_input.outputs[7], separate_xyz_006.inputs[0])
        _ = links.new(group_input.outputs[8], separate_xyz_005.inputs[0])
        _ = links.new(group_input.outputs[9], separate_xyz_008.inputs[0])

        _ = links.new(separate_xyz.outputs[0], reroute_001.inputs[0])
        _ = links.new(separate_xyz.outputs[1], heightblend.inputs[2])
        _ = links.new(separate_xyz.outputs[2], heightblend_001.inputs[2])

        _ = links.new(separate_xyz_002.outputs[1], heightaccum.inputs[0])
        _ = links.new(separate_xyz_002.outputs[2], heightaccum.inputs[1])

        _ = links.new(separate_xyz_003.outputs[1], heightblend.inputs[0])
        _ = links.new(separate_xyz_003.outputs[2], heightblend.inputs[1])

        _ = links.new(separate_xyz_004.outputs[1], heightblend_001.inputs[0])
        _ = links.new(separate_xyz_004.outputs[2], heightblend_001.inputs[1])

        _ = links.new(separate_xyz_005.outputs[1], heightblend_002.inputs[0])
        _ = links.new(separate_xyz_005.outputs[2], heightblend_002.inputs[1])

        _ = links.new(separate_xyz_006.outputs[0], math_028.inputs[0])
        _ = links.new(separate_xyz_006.outputs[0], math_030.inputs[1])
        _ = links.new(separate_xyz_006.outputs[1], math_021.inputs[0])
        _ = links.new(separate_xyz_006.outputs[1], math_023.inputs[1])
        _ = links.new(separate_xyz_006.outputs[1], math_027.inputs[1])
        _ = links.new(separate_xyz_006.outputs[2], math_034.inputs[1])

        _ = links.new(separate_xyz_007.outputs[0], math_013.inputs[0])
        _ = links.new(separate_xyz_007.outputs[0], math_015.inputs[1])
        _ = links.new(separate_xyz_007.outputs[1], math_006.inputs[0])
        _ = links.new(separate_xyz_007.outputs[1], math_008.inputs[1])
        _ = links.new(separate_xyz_007.outputs[1], math_012.inputs[1])
        _ = links.new(separate_xyz_007.outputs[2], math_019.inputs[1])

        _ = links.new(separate_xyz_008.outputs[0], math_043.inputs[0])
        _ = links.new(separate_xyz_008.outputs[0], math_045.inputs[1])
        _ = links.new(separate_xyz_008.outputs[1], math_036.inputs[0])
        _ = links.new(separate_xyz_008.outputs[1], math_038.inputs[1])
        _ = links.new(separate_xyz_008.outputs[1], math_042.inputs[1])
        _ = links.new(separate_xyz_008.outputs[2], math_049.inputs[1])

        _ = links.new(reroute.outputs[0], heightblend_002.inputs[2])
        _ = links.new(reroute_001.outputs[0], heightaccum.inputs[2])

        _ = links.new(heightaccum.outputs[0], math_007.inputs[0])
        _ = links.new(heightaccum.outputs[0], math_017.inputs[0])
        _ = links.new(heightaccum.outputs[0], math_018.inputs[1])
        _ = links.new(heightaccum.outputs[0], math_020.inputs[1])

        _ = links.new(heightblend.outputs[0], math_010.inputs[0])
        _ = links.new(heightblend.outputs[0], math_011.inputs[0])
        _ = links.new(heightblend.outputs[0], math_017.inputs[1])

        _ = links.new(heightblend_001.outputs[0], math_025.inputs[0])
        _ = links.new(heightblend_001.outputs[0], math_026.inputs[0])
        _ = links.new(heightblend_001.outputs[0], math_032.inputs[1])

        _ = links.new(heightblend_002.outputs[0], math_040.inputs[0])
        _ = links.new(heightblend_002.outputs[0], math_041.inputs[0])
        _ = links.new(heightblend_002.outputs[0], math_047.inputs[1])

        _ = links.new(math_006.outputs[0], math_007.inputs[1])
        _ = links.new(math_007.outputs[0], math_008.inputs[0])
        _ = links.new(math_008.outputs[0], math_009.inputs[1])
        _ = links.new(math_009.outputs[0], math_010.inputs[1])
        _ = links.new(math_009.outputs[0], math_011.inputs[1])
        _ = links.new(math_011.outputs[0], math_012.inputs[0])
        _ = links.new(math_012.outputs[0], clamp.inputs[0])
        _ = links.new(math_013.outputs[0], mix_001.inputs[0])
        _ = links.new(clamp.outputs[0], math_014.inputs[1])
        _ = links.new(clamp.outputs[0], mix_001.inputs[2])
        _ = links.new(math_014.outputs[0], mix_001.inputs[3])
        _ = links.new(mix_001.outputs[0], math_015.inputs[0])
        _ = links.new(math_015.outputs[0], math_016.inputs[0])
        _ = links.new(math_016.outputs[0], combine_xyz.inputs[1])

        _ = links.new(math_017.outputs[0], math_018.inputs[0])
        _ = links.new(math_018.outputs[0], math_019.inputs[0])
        _ = links.new(math_019.outputs[0], math_020.inputs[0])
        _ = links.new(math_020.outputs[0], math_022.inputs[0])
        _ = links.new(math_020.outputs[0], math_032.inputs[0])
        _ = links.new(math_020.outputs[0], math_033.inputs[1])
        _ = links.new(math_020.outputs[0], math_035.inputs[1])

        _ = links.new(math_021.outputs[0], math_022.inputs[1])
        _ = links.new(math_022.outputs[0], math_023.inputs[0])
        _ = links.new(math_023.outputs[0], math_024.inputs[1])
        _ = links.new(math_024.outputs[0], math_025.inputs[1])
        _ = links.new(math_024.outputs[0], math_026.inputs[1])
        _ = links.new(math_026.outputs[0], math_027.inputs[0])
        _ = links.new(math_027.outputs[0], clamp_001.inputs[0])
        _ = links.new(math_028.outputs[0], mix_002.inputs[0])
        _ = links.new(clamp_001.outputs[0], math_029.inputs[1])
        _ = links.new(clamp_001.outputs[0], mix_002.inputs[2])
        _ = links.new(math_029.outputs[0], mix_002.inputs[3])
        _ = links.new(mix_002.outputs[0], math_030.inputs[0])
        _ = links.new(math_030.outputs[0], math_031.inputs[0])
        _ = links.new(math_031.outputs[0], combine_xyz.inputs[2])

        _ = links.new(math_032.outputs[0], math_033.inputs[0])
        _ = links.new(math_033.outputs[0], math_034.inputs[0])
        _ = links.new(math_034.outputs[0], math_035.inputs[0])
        _ = links.new(math_035.outputs[0], math_037.inputs[0])
        _ = links.new(math_035.outputs[0], math_047.inputs[0])
        _ = links.new(math_035.outputs[0], math_048.inputs[1])
        _ = links.new(math_035.outputs[0], math_050.inputs[1])

        _ = links.new(math_036.outputs[0], math_037.inputs[1])
        _ = links.new(math_037.outputs[0], math_038.inputs[0])
        _ = links.new(math_038.outputs[0], math_039.inputs[1])
        _ = links.new(math_039.outputs[0], math_040.inputs[1])
        _ = links.new(math_039.outputs[0], math_041.inputs[1])
        _ = links.new(math_041.outputs[0], math_042.inputs[0])
        _ = links.new(math_042.outputs[0], clamp_002.inputs[0])
        _ = links.new(math_043.outputs[0], mix_003.inputs[0])
        _ = links.new(clamp_002.outputs[0], math_044.inputs[1])
        _ = links.new(clamp_002.outputs[0], mix_003.inputs[2])
        _ = links.new(math_044.outputs[0], mix_003.inputs[3])
        _ = links.new(mix_003.outputs[0], math_045.inputs[0])
        _ = links.new(math_045.outputs[0], math_046.inputs[0])
        _ = links.new(math_046.outputs[0], group_output.inputs[1])

        _ = links.new(math_047.outputs[0], math_048.inputs[0])
        _ = links.new(math_048.outputs[0], math_049.inputs[0])
        _ = links.new(math_049.outputs[0], math_050.inputs[0])

        _ = links.new(combine_xyz.outputs[0], group_output.inputs[0])
