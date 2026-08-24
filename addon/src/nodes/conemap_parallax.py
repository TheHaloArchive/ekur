# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import bpy
from bpy.types import (
    GeometryNodeRepeatInput,
    GeometryNodeRepeatOutput,
    NodeEvaluateClosure,
    NodeFrame,
    NodeGroupInput,
    NodeGroupOutput,
    NodeReroute,
    NodeSocketClosure,
    NodeSocketFloat,
    NodeSocketVector,
    NodeTree,
    ShaderNodeCameraData,
    ShaderNodeCombineXYZ,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeNewGeometry,
    ShaderNodeSeparateXYZ,
    ShaderNodeTangent,
    ShaderNodeVectorMath,
)

from ..utils import assign_value, create_node, create_socket, create_link

__all__ = ["ConemapParallax"]


class ConemapParallax:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Cone Step Parallax")
        if self.node_tree:
            return
        self.node_tree = self._create_node_tree()

    def _create_node_tree(self) -> NodeTree:
        node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Cone Step Parallax")
        interface = node_tree.interface

        create_socket(interface, "UV", NodeSocketVector, False)
        create_socket(interface, "Fade", NodeSocketFloat, False)

        uv_in = create_socket(interface, "UV", NodeSocketVector)
        uv_in.description = "Detail UV, with your cone map scale/offset already applied"

        cone_map_in = create_socket(interface, "Cone Map", NodeSocketClosure)
        cone_map_in.description = "Closure: (Vector) -> (Height, Cone Ratio)"

        parallax_depth_in = create_socket(interface, "Parallax Depth", NodeSocketFloat)
        parallax_depth_in.default_value = 0.855
        parallax_depth_in.description = "Larger = deeper. Shrinks the Z divisor from 150 toward 10"

        parallax_height_offset_in = create_socket(
            interface, "Parallax Height Offset", NodeSocketFloat
        )
        parallax_height_offset_in.description = (
            "Pushes the ray start back below the top of the heightfield"
        )

        quality_in = create_socket(interface, "Quality", NodeSocketFloat)
        quality_in.default_value = 0.5
        quality_in.description = "floor(q*25) march steps, floor(q*9) refine steps. Must be a literal value -- no drivers or attributes"

        cone_step_fade_near_in = create_socket(interface, "Cone Step Fade Near", NodeSocketFloat)
        cone_step_fade_near_in.default_value = 8.0
        cone_step_fade_near_in.description = "Full strength at or below this camera distance"

        cone_step_fade_far_in = create_socket(interface, "Cone Step Fade Far", NodeSocketFloat)
        cone_step_fade_far_in.default_value = 11.0
        cone_step_fade_far_in.description = "Fully faded out at or beyond this camera distance"

        invert_handedness_in = create_socket(interface, "Invert Handedness", NodeSocketFloat)
        invert_handedness_in.description = (
            "0 = +1 handedness, 1 = -1. Flip if parallax slides the wrong way"
        )

        nodes = node_tree.nodes

        group_input = create_node(nodes, 30, -336, NodeGroupInput)
        group_input.label = "Inputs"

        group_output = create_node(nodes, 4322, -243, NodeGroupOutput)
        group_output.label = "Outputs"
        group_output.is_active_output = True

        frame = create_node(nodes, -7555, 718, NodeFrame)
        frame.label = "Tangent-Space View Ray"
        frame.use_custom_color = True
        frame.color = (0.22, 0.3, 0.38)
        frame.label_size = 22
        frame.shrink = True
        frame.width = 1381.1626
        frame.height = 933.0

        geometry = create_node(nodes, 30, -177, ShaderNodeNewGeometry)
        geometry.label = "Geometry"

        tangent = create_node(nodes, 181, -613, ShaderNodeTangent)
        tangent.label = "Tangent (UV)"
        tangent.axis = "Z"
        tangent.direction_type = "UV_MAP"
        tangent.uv_map = ""

        vector_math = create_node(nodes, 324, -272, ShaderNodeVectorMath)
        vector_math.label = "Normalize"
        vector_math.operation = "NORMALIZE"

        vector_math_001 = create_node(nodes, 483, -245, ShaderNodeVectorMath)
        vector_math_001.label = "V = camera -> surface"
        vector_math_001.operation = "SCALE"
        assign_value(vector_math_001, 3, -1.0)

        math = create_node(nodes, 379, -735, ShaderNodeMath)
        math.label = "handedness"
        math.operation = "MULTIPLY_ADD"
        math.use_clamp = False
        assign_value(math, 1, -2.0)
        assign_value(math, 2, 1.0)

        vector_math_002 = create_node(nodes, 407, -540, ShaderNodeVectorMath)
        vector_math_002.label = "Bitangent"
        vector_math_002.operation = "CROSS_PRODUCT"

        vector_math_003 = create_node(nodes, 662, -658, ShaderNodeVectorMath)
        vector_math_003.label = "Handedness"
        vector_math_003.operation = "SCALE"

        vector_math_004 = create_node(nodes, 953, -537, ShaderNodeVectorMath)
        vector_math_004.label = "ray.T"
        vector_math_004.operation = "DOT_PRODUCT"

        vector_math_005 = create_node(nodes, 955, -670, ShaderNodeVectorMath)
        vector_math_005.label = "ray.B"
        vector_math_005.operation = "DOT_PRODUCT"

        vector_math_006 = create_node(nodes, 617, -39, ShaderNodeVectorMath)
        vector_math_006.label = "N . V"
        vector_math_006.operation = "DOT_PRODUCT"

        frame_001 = create_node(nodes, -5935, 683, NodeFrame)
        frame_001.label = "Depth Scale  (150 - depth*140)"
        frame_001.use_custom_color = True
        frame_001.color = (0.22, 0.3, 0.38)
        frame_001.label_size = 22
        frame_001.shrink = True
        frame_001.width = 1997.0
        frame_001.height = 638.0

        math_001 = create_node(nodes, 205, -460, ShaderNodeMath)
        math_001.label = "Multiply"
        math_001.operation = "MULTIPLY"
        math_001.use_clamp = False
        assign_value(math_001, 1, 140.0)

        math_002 = create_node(nodes, 359, -459, ShaderNodeMath)
        math_002.label = "Divisor"
        math_002.operation = "SUBTRACT"
        math_002.use_clamp = False
        assign_value(math_002, 0, 150.0)

        math_003 = create_node(nodes, 542, -360, ShaderNodeMath)
        math_003.label = "rayZ"
        math_003.operation = "MULTIPLY"
        math_003.use_clamp = False

        math_004 = create_node(nodes, 714, -326, ShaderNodeMath)
        math_004.label = "Absolute"
        math_004.operation = "ABSOLUTE"
        math_004.use_clamp = False

        math_005 = create_node(nodes, 877, -307, ShaderNodeMath)
        math_005.label = "Maximum"
        math_005.operation = "MAXIMUM"
        math_005.use_clamp = False
        assign_value(math_005, 1, 1e-06)

        math_006 = create_node(nodes, 1068, -206, ShaderNodeMath)
        math_006.label = "1 / max(|rayZ|, eps)"
        math_006.operation = "DIVIDE"
        math_006.use_clamp = False
        assign_value(math_006, 0, 1.0)

        math_007 = create_node(nodes, 1397, -39, ShaderNodeMath)
        math_007.label = "d.x"
        math_007.operation = "MULTIPLY"
        math_007.use_clamp = False

        math_008 = create_node(nodes, 1387, -348, ShaderNodeMath)
        math_008.label = "d.y"
        math_008.operation = "MULTIPLY"
        math_008.use_clamp = False

        math_009 = create_node(nodes, 1392, -199, ShaderNodeMath)
        math_009.label = "dz = sign(N.V)"
        math_009.operation = "MULTIPLY"
        math_009.use_clamp = False

        combine_xyz = create_node(nodes, 1827, -231, ShaderNodeCombineXYZ)
        combine_xyz.label = "D = (d.xy, dz)"

        combine_xyz_001 = create_node(nodes, 1622, -73, ShaderNodeCombineXYZ)

        vector_math_007 = create_node(nodes, 1824, -75, ShaderNodeVectorMath)
        vector_math_007.label = "lateralSpeed"
        vector_math_007.operation = "LENGTH"

        frame_002 = create_node(nodes, -4895, -155, NodeFrame)
        frame_002.label = "Ray Start + Step Budget"
        frame_002.use_custom_color = True
        frame_002.color = (0.32, 0.28, 0.2)
        frame_002.label_size = 22
        frame_002.shrink = True
        frame_002.width = 1912.0
        frame_002.height = 738.0

        math_010 = create_node(nodes, 377, -319, ShaderNodeMath)
        math_010.label = "Maximum"
        math_010.operation = "MAXIMUM"
        math_010.use_clamp = False

        math_011 = create_node(nodes, 740, -256, ShaderNodeMath)
        math_011.label = "saturate(heightOffset)"
        math_011.operation = "MINIMUM"
        math_011.use_clamp = False
        assign_value(math_011, 1, 1.0)

        separate_xyz = create_node(nodes, 388, -142, ShaderNodeSeparateXYZ)
        separate_xyz.label = "UV"

        combine_xyz_002 = create_node(nodes, 1277, -370, ShaderNodeCombineXYZ)
        combine_xyz_002.label = "UV (flat)"

        combine_xyz_003 = create_node(nodes, 1272, -70, ShaderNodeCombineXYZ)
        combine_xyz_003.label = "(uv, 1)"
        assign_value(combine_xyz_003, 2, 1.0)

        vector_math_008 = create_node(nodes, 1281, -213, ShaderNodeVectorMath)
        vector_math_008.label = "Scale"
        vector_math_008.operation = "SCALE"

        vector_math_009 = create_node(nodes, 1503, -128, ShaderNodeVectorMath)
        vector_math_009.label = "start = (uv,1) - D*bias"
        vector_math_009.operation = "SUBTRACT"

        math_012 = create_node(nodes, 1286, -560, ShaderNodeMath)
        math_012.label = "Multiply"
        math_012.operation = "MULTIPLY"
        math_012.use_clamp = False
        assign_value(math_012, 1, 25.0)

        math_013 = create_node(nodes, 1742, -39, ShaderNodeMath)
        math_013.label = "floor(q*25)"
        math_013.operation = "FLOOR"
        math_013.use_clamp = False

        math_014 = create_node(nodes, 1525, -515, ShaderNodeMath)
        math_014.label = "Multiply"
        math_014.operation = "MULTIPLY"
        math_014.use_clamp = False
        assign_value(math_014, 1, 9.0)

        math_015 = create_node(nodes, 1742, -429, ShaderNodeMath)
        math_015.label = "floor(q*9)"
        math_015.operation = "FLOOR"
        math_015.use_clamp = False

        frame_003 = create_node(nodes, -2945, 783, NodeFrame)
        frame_003.label = "Cone March"
        frame_003.use_custom_color = True
        frame_003.color = (0.2, 0.32, 0.24)
        frame_003.label_size = 22
        frame_003.shrink = True
        frame_003.width = 2427.0
        frame_003.height = 530.0

        repeat_input = create_node(nodes, 215, -278, GeometryNodeRepeatInput)
        repeat_input.label = "March"

        repeat_output = create_node(nodes, 2257, -189, GeometryNodeRepeatOutput)
        repeat_output.label = "March End"
        repeat_output.repeat_items.clear()
        # Create item "P"
        repeat_output.repeat_items.new("VECTOR", "P")

        separate_xyz_001 = create_node(nodes, 452, -268, ShaderNodeSeparateXYZ)
        separate_xyz_001.label = "P"

        combine_xyz_004 = create_node(nodes, 709, -254, ShaderNodeCombineXYZ)
        combine_xyz_004.label = "Lookup UV"

        evaluate_closure = create_node(nodes, 874, -142, NodeEvaluateClosure)
        evaluate_closure.label = "Sample Cone Map"
        evaluate_closure.active_output_index = 1
        evaluate_closure.input_items.clear()
        evaluate_closure.input_items.new("VECTOR", "Vector")
        evaluate_closure.output_items.clear()
        evaluate_closure.output_items.new("FLOAT", "Height")
        evaluate_closure.output_items.new("FLOAT", "Cone Ratio")

        math_016 = create_node(nodes, 1090, -242, ShaderNodeMath)
        math_016.label = "guard cr = 0"
        math_016.operation = "MAXIMUM"
        math_016.use_clamp = False
        assign_value(math_016, 1, 0.03)

        math_017 = create_node(nodes, 861, -352, ShaderNodeMath)
        math_017.label = "Subtract"
        math_017.operation = "SUBTRACT"
        math_017.use_clamp = False

        math_018 = create_node(nodes, 1099, -73, ShaderNodeMath)
        math_018.label = "dh = saturate((z-bias) - h)"
        math_018.operation = "SUBTRACT"
        math_018.use_clamp = True

        math_019 = create_node(nodes, 1252, -229, ShaderNodeMath)
        math_019.label = "Add"
        math_019.operation = "ADD"
        math_019.use_clamp = False

        math_020 = create_node(nodes, 1491, -218, ShaderNodeMath)
        math_020.label = "cr + lateralSpeed"
        math_020.operation = "MAXIMUM"
        math_020.use_clamp = False
        assign_value(math_020, 1, 1e-06)

        math_021 = create_node(nodes, 1527, -39, ShaderNodeMath)
        math_021.label = "Multiply"
        math_021.operation = "MULTIPLY"
        math_021.use_clamp = False

        math_022 = create_node(nodes, 1783, -168, ShaderNodeMath)
        math_022.label = "step"
        math_022.operation = "DIVIDE"
        math_022.use_clamp = False

        vector_math_010 = create_node(nodes, 1932, -187, ShaderNodeVectorMath)
        vector_math_010.label = "Scale"
        vector_math_010.operation = "SCALE"

        vector_math_011 = create_node(nodes, 2077, -189, ShaderNodeVectorMath)
        vector_math_011.label = "P += D*step"
        vector_math_011.operation = "ADD"

        frame_004 = create_node(nodes, -157, 271, NodeFrame)
        frame_004.label = "Binary Search Refinement"
        frame_004.use_custom_color = True
        frame_004.color = (0.2, 0.32, 0.24)
        frame_004.label_size = 22
        frame_004.shrink = True
        frame_004.width = 1950.0
        frame_004.height = 832.0

        math_023 = create_node(nodes, 58, -355, ShaderNodeMath)
        math_023.label = "Add"
        math_023.operation = "ADD"
        math_023.use_clamp = False
        assign_value(math_023, 1, 1.0)

        separate_xyz_002 = create_node(nodes, 30, -229, ShaderNodeSeparateXYZ)
        separate_xyz_002.label = "P marched"

        math_024 = create_node(nodes, 231, -198, ShaderNodeMath)
        math_024.label = "Absolute"
        math_024.operation = "ABSOLUTE"
        math_024.use_clamp = False

        math_025 = create_node(nodes, 396, -171, ShaderNodeMath)
        math_025.label = "interval"
        math_025.operation = "SUBTRACT"
        math_025.use_clamp = False

        math_026 = create_node(nodes, 547, -165, ShaderNodeMath)
        math_026.label = "Multiply"
        math_026.operation = "MULTIPLY"
        math_026.use_clamp = False
        assign_value(math_026, 1, 0.5)

        vector_math_012 = create_node(nodes, 704, -39, ShaderNodeVectorMath)
        vector_math_012.label = "delta0"
        vector_math_012.operation = "SCALE"

        repeat_input_001 = create_node(nodes, 889, -92, GeometryNodeRepeatInput)
        repeat_input_001.label = "Refine"

        repeat_output_001 = create_node(nodes, 1780, -87, GeometryNodeRepeatOutput)
        repeat_output_001.label = "Refine End"
        repeat_output_001.active_index = 1
        repeat_output_001.repeat_items.clear()
        # Create item "P"
        repeat_output_001.repeat_items.new("VECTOR", "P")
        # Create item "Delta"
        repeat_output_001.repeat_items.new("VECTOR", "Delta")

        vector_math_013 = create_node(nodes, 706, -166, ShaderNodeVectorMath)
        vector_math_013.label = "start + delta0"
        vector_math_013.operation = "ADD"

        vector_math_014 = create_node(nodes, 1181, -278, ShaderNodeVectorMath)
        vector_math_014.label = "delta *= 0.5"
        vector_math_014.operation = "SCALE"
        assign_value(vector_math_014, 3, 0.5)

        separate_xyz_003 = create_node(nodes, 889, -229, ShaderNodeSeparateXYZ)
        separate_xyz_003.label = "P"

        combine_xyz_005 = create_node(nodes, 887, -350, ShaderNodeCombineXYZ)
        combine_xyz_005.label = "Lookup UV"

        evaluate_closure_001 = create_node(nodes, 886, -470, NodeEvaluateClosure)
        evaluate_closure_001.label = "Sample Height"
        evaluate_closure_001.active_output_index = 1
        evaluate_closure_001.input_items.clear()
        evaluate_closure_001.input_items.new("VECTOR", "Vector")
        evaluate_closure_001.output_items.clear()
        evaluate_closure_001.output_items.new("FLOAT", "Height")
        evaluate_closure_001.output_items.new("FLOAT", "Cone Ratio")

        math_027 = create_node(nodes, 886, -653, ShaderNodeMath)
        math_027.label = "Add"
        math_027.operation = "ADD"
        math_027.use_clamp = False

        math_028 = create_node(nodes, 1079, -654, ShaderNodeMath)
        math_028.label = "still above?"
        math_028.operation = "GREATER_THAN"
        math_028.use_clamp = False

        math_029 = create_node(nodes, 1276, -430, ShaderNodeMath)
        math_029.label = "above ? +1 : -1"
        math_029.operation = "MULTIPLY_ADD"
        math_029.use_clamp = False
        assign_value(math_029, 1, 2.0)
        assign_value(math_029, 2, -1.0)

        vector_math_015 = create_node(nodes, 1361, -211, ShaderNodeVectorMath)
        vector_math_015.label = "Scale"
        vector_math_015.operation = "SCALE"

        vector_math_016 = create_node(nodes, 1533, -91, ShaderNodeVectorMath)
        vector_math_016.label = "P +/- delta"
        vector_math_016.operation = "ADD"

        frame_005 = create_node(nodes, 1878, 247, NodeFrame)
        frame_005.label = "Distance Fade + Output"
        frame_005.use_custom_color = True
        frame_005.color = (0.32, 0.22, 0.28)
        frame_005.label_size = 22
        frame_005.shrink = True
        frame_005.width = 1961.0
        frame_005.height = 789.0

        math_030 = create_node(nodes, 506, -611, ShaderNodeMath)
        math_030.label = "Subtract"
        math_030.operation = "SUBTRACT"
        math_030.use_clamp = False

        math_031 = create_node(nodes, 854, -544, ShaderNodeMath)
        math_031.label = "far - near"
        math_031.operation = "MAXIMUM"
        math_031.use_clamp = False
        assign_value(math_031, 1, 1e-06)

        math_032 = create_node(nodes, 848, -368, ShaderNodeMath)
        math_032.label = "Subtract"
        math_032.operation = "SUBTRACT"
        math_032.use_clamp = False

        math_033 = create_node(nodes, 1079, -543, ShaderNodeMath)
        math_033.label = "Divide"
        math_033.operation = "DIVIDE"
        math_033.use_clamp = True

        math_034 = create_node(nodes, 1263, -532, ShaderNodeMath)
        math_034.label = "fade"
        math_034.operation = "SUBTRACT"
        math_034.use_clamp = False
        assign_value(math_034, 0, 1.0)

        math_035 = create_node(nodes, 1276, -248, ShaderNodeMath)
        math_035.label = "Greater_Than"
        math_035.operation = "GREATER_THAN"
        math_035.use_clamp = False
        assign_value(math_035, 1, 1e-05)

        math_036 = create_node(nodes, 1490, -136, ShaderNodeMath)
        math_036.label = "fade (gated)"
        math_036.operation = "MULTIPLY"
        math_036.use_clamp = True

        separate_xyz_004 = create_node(nodes, 1490, -331, ShaderNodeSeparateXYZ)
        separate_xyz_004.label = "P final"

        mix = create_node(nodes, 1791, -39, ShaderNodeMix)
        mix.label = "lerp(uv, hit, fade)"
        mix.blend_type = "MIX"
        mix.clamp_factor = True
        mix.clamp_result = False
        mix.data_type = "VECTOR"
        mix.factor_mode = "UNIFORM"

        combine_xyz_006 = create_node(nodes, 1665, -310, ShaderNodeCombineXYZ)
        combine_xyz_006.label = "hit UV"

        reroute = create_node(nodes, 1346, -150, NodeReroute)
        reroute.socket_idname = "NodeSocketFloat"
        reroute.width = 10.0

        camera_data_001 = create_node(nodes, 494, -443, ShaderNodeCameraData)

        group_input_001 = create_node(nodes, 145, -757, NodeGroupInput)
        group_input_001.label = "Inputs"
        group_input_001.outputs[0].hide = True
        group_input_001.outputs[1].hide = True
        group_input_001.outputs[2].hide = True
        group_input_001.outputs[3].hide = True
        group_input_001.outputs[4].hide = True
        group_input_001.outputs[5].hide = True
        group_input_001.outputs[6].hide = True
        group_input_001.outputs[8].hide = True

        group_input_002 = create_node(nodes, 30, -324, NodeGroupInput)
        group_input_002.label = "Inputs"

        group_input_003 = create_node(nodes, 910, -576, NodeGroupInput)
        group_input_003.label = "Inputs"
        group_input_003.outputs[0].hide = True
        group_input_003.outputs[1].hide = True
        group_input_003.outputs[2].hide = True
        group_input_003.outputs[3].hide = True
        group_input_003.outputs[5].hide = True
        group_input_003.outputs[6].hide = True
        group_input_003.outputs[7].hide = True
        group_input_003.outputs[8].hide = True

        group_input_004 = create_node(nodes, 484, -448, NodeGroupInput)

        group_input_005 = create_node(nodes, 30, -527, NodeGroupInput)
        group_input_005.label = "Inputs"
        group_input_005.outputs[0].hide = True
        group_input_005.outputs[1].hide = True
        group_input_005.outputs[3].hide = True
        group_input_005.outputs[4].hide = True
        group_input_005.outputs[5].hide = True
        group_input_005.outputs[6].hide = True
        group_input_005.outputs[7].hide = True
        group_input_005.outputs[8].hide = True

        group_input_006 = create_node(nodes, 30, -203, NodeGroupInput)

        repeat_input.pair_with_output(repeat_output)
        repeat_input_001.pair_with_output(repeat_output_001)

        group_input.parent = frame_005
        geometry.parent = frame
        tangent.parent = frame
        vector_math.parent = frame
        vector_math_001.parent = frame
        math.parent = frame
        vector_math_002.parent = frame
        vector_math_003.parent = frame
        vector_math_004.parent = frame
        vector_math_005.parent = frame
        vector_math_006.parent = frame
        math_001.parent = frame_001
        math_002.parent = frame_001
        math_003.parent = frame_001
        math_004.parent = frame_001
        math_005.parent = frame_001
        math_006.parent = frame_001
        math_007.parent = frame_001
        math_008.parent = frame_001
        math_009.parent = frame_001
        combine_xyz.parent = frame_001
        combine_xyz_001.parent = frame_001
        vector_math_007.parent = frame_001
        math_010.parent = frame_002
        math_011.parent = frame_002
        separate_xyz.parent = frame_002
        combine_xyz_002.parent = frame_002
        combine_xyz_003.parent = frame_002
        vector_math_008.parent = frame_002
        vector_math_009.parent = frame_002
        math_012.parent = frame_002
        math_013.parent = frame_002
        math_014.parent = frame_002
        math_015.parent = frame_002
        repeat_input.parent = frame_003
        repeat_output.parent = frame_003
        separate_xyz_001.parent = frame_003
        combine_xyz_004.parent = frame_003
        evaluate_closure.parent = frame_003
        math_016.parent = frame_003
        math_017.parent = frame_003
        math_018.parent = frame_003
        math_019.parent = frame_003
        math_020.parent = frame_003
        math_021.parent = frame_003
        math_022.parent = frame_003
        vector_math_010.parent = frame_003
        vector_math_011.parent = frame_003
        math_023.parent = frame_004
        separate_xyz_002.parent = frame_004
        math_024.parent = frame_004
        math_025.parent = frame_004
        math_026.parent = frame_004
        vector_math_012.parent = frame_004
        repeat_input_001.parent = frame_004
        repeat_output_001.parent = frame_004
        vector_math_013.parent = frame_004
        vector_math_014.parent = frame_004
        separate_xyz_003.parent = frame_004
        combine_xyz_005.parent = frame_004
        evaluate_closure_001.parent = frame_004
        math_027.parent = frame_004
        math_028.parent = frame_004
        math_029.parent = frame_004
        vector_math_015.parent = frame_004
        vector_math_016.parent = frame_004
        math_030.parent = frame_005
        math_031.parent = frame_005
        math_032.parent = frame_005
        math_033.parent = frame_005
        math_034.parent = frame_005
        math_035.parent = frame_005
        math_036.parent = frame_005
        separate_xyz_004.parent = frame_005
        mix.parent = frame_005
        combine_xyz_006.parent = frame_005
        reroute.parent = frame
        camera_data_001.parent = frame_005
        group_input_001.parent = frame
        group_input_002.parent = frame_002
        group_input_003.parent = frame_002
        group_input_004.parent = frame_004
        group_input_005.parent = frame_001
        group_input_006.parent = frame_003

        links = node_tree.links
        create_link(links, geometry, vector_math, 4, 0)
        create_link(links, vector_math, vector_math_001, 0, 0)
        create_link(links, geometry, vector_math_002, 1, 0)
        create_link(links, tangent, vector_math_002, 0, 1)
        create_link(links, vector_math_002, vector_math_003, 0, 0)
        create_link(links, math, vector_math_003, 0, 3)
        create_link(links, tangent, vector_math_004, 0, 0)
        create_link(links, vector_math_001, vector_math_004, 0, 1)
        create_link(links, vector_math_003, vector_math_005, 0, 0)
        create_link(links, vector_math_001, vector_math_005, 0, 1)
        create_link(links, geometry, vector_math_006, 1, 0)
        create_link(links, vector_math_001, vector_math_006, 0, 1)
        create_link(links, math_001, math_002, 0, 1)
        create_link(links, reroute, math_003, 0, 0)
        create_link(links, math_002, math_003, 0, 1)
        create_link(links, math_003, math_004, 0, 0)
        create_link(links, math_004, math_005, 0, 0)
        create_link(links, math_005, math_006, 0, 1)
        create_link(links, vector_math_004, math_007, 1, 0)
        create_link(links, math_006, math_007, 0, 1)
        create_link(links, vector_math_005, math_008, 1, 0)
        create_link(links, math_006, math_008, 0, 1)
        create_link(links, math_003, math_009, 0, 0)
        create_link(links, math_006, math_009, 0, 1)
        create_link(links, math_007, combine_xyz, 0, 0)
        create_link(links, math_008, combine_xyz, 0, 1)
        create_link(links, math_009, combine_xyz, 0, 2)
        create_link(links, math_007, combine_xyz_001, 0, 0)
        create_link(links, math_008, combine_xyz_001, 0, 1)
        create_link(links, combine_xyz_001, vector_math_007, 0, 0)
        create_link(links, math_010, math_011, 0, 0)
        create_link(links, separate_xyz, combine_xyz_002, 0, 0)
        create_link(links, separate_xyz, combine_xyz_002, 1, 1)
        create_link(links, separate_xyz, combine_xyz_003, 0, 0)
        create_link(links, separate_xyz, combine_xyz_003, 1, 1)
        create_link(links, combine_xyz, vector_math_008, 0, 0)
        create_link(links, math_011, vector_math_008, 0, 3)
        create_link(links, combine_xyz_003, vector_math_009, 0, 0)
        create_link(links, vector_math_008, vector_math_009, 0, 1)
        create_link(links, math_012, math_013, 0, 0)
        create_link(links, math_014, math_015, 0, 0)
        create_link(links, math_013, repeat_input, 0, 0)
        create_link(links, vector_math_009, repeat_input, 0, 1)
        create_link(links, repeat_input, separate_xyz_001, 1, 0)
        create_link(links, separate_xyz_001, combine_xyz_004, 0, 0)
        create_link(links, separate_xyz_001, combine_xyz_004, 1, 1)
        create_link(links, combine_xyz_004, evaluate_closure, 0, 1)
        create_link(links, evaluate_closure, math_016, 1, 0)
        create_link(links, separate_xyz_001, math_017, 2, 0)
        create_link(links, math_011, math_017, 0, 1)
        create_link(links, math_017, math_018, 0, 0)
        create_link(links, evaluate_closure, math_018, 0, 1)
        create_link(links, math_016, math_019, 0, 0)
        create_link(links, vector_math_007, math_019, 1, 1)
        create_link(links, math_019, math_020, 0, 0)
        create_link(links, math_016, math_021, 0, 0)
        create_link(links, math_018, math_021, 0, 1)
        create_link(links, math_021, math_022, 0, 0)
        create_link(links, math_020, math_022, 0, 1)
        create_link(links, combine_xyz, vector_math_010, 0, 0)
        create_link(links, math_022, vector_math_010, 0, 3)
        create_link(links, repeat_input, vector_math_011, 1, 0)
        create_link(links, vector_math_010, vector_math_011, 0, 1)
        create_link(links, vector_math_011, repeat_output, 0, 0)
        create_link(links, math_011, math_023, 0, 0)
        create_link(links, repeat_output, separate_xyz_002, 0, 0)
        create_link(links, separate_xyz_002, math_024, 2, 0)
        create_link(links, math_023, math_025, 0, 0)
        create_link(links, math_024, math_025, 0, 1)
        create_link(links, math_025, math_026, 0, 0)
        create_link(links, combine_xyz, vector_math_012, 0, 0)
        create_link(links, math_026, vector_math_012, 0, 3)
        create_link(links, math_015, repeat_input_001, 0, 0)
        create_link(links, vector_math_009, vector_math_013, 0, 0)
        create_link(links, vector_math_012, vector_math_013, 0, 1)
        create_link(links, vector_math_013, repeat_input_001, 0, 1)
        create_link(links, vector_math_012, repeat_input_001, 0, 2)
        create_link(links, repeat_input_001, vector_math_014, 2, 0)
        create_link(links, repeat_input_001, separate_xyz_003, 1, 0)
        create_link(links, separate_xyz_003, combine_xyz_005, 0, 0)
        create_link(links, separate_xyz_003, combine_xyz_005, 1, 1)
        create_link(links, combine_xyz_005, evaluate_closure_001, 0, 1)
        create_link(links, evaluate_closure_001, math_027, 0, 0)
        create_link(links, math_011, math_027, 0, 1)
        create_link(links, separate_xyz_003, math_028, 2, 0)
        create_link(links, math_027, math_028, 0, 1)
        create_link(links, math_028, math_029, 0, 0)
        create_link(links, vector_math_014, vector_math_015, 0, 0)
        create_link(links, math_029, vector_math_015, 0, 3)
        create_link(links, repeat_input_001, vector_math_016, 1, 0)
        create_link(links, vector_math_015, vector_math_016, 0, 1)
        create_link(links, vector_math_016, repeat_output_001, 0, 0)
        create_link(links, vector_math_014, repeat_output_001, 0, 1)
        create_link(links, group_input, math_030, 6, 0)
        create_link(links, group_input, math_030, 5, 1)
        create_link(links, math_030, math_031, 0, 0)
        create_link(links, group_input, math_032, 5, 1)
        create_link(links, math_032, math_033, 0, 0)
        create_link(links, math_031, math_033, 0, 1)
        create_link(links, math_033, math_034, 0, 1)
        create_link(links, group_input, math_035, 2, 0)
        create_link(links, math_034, math_036, 0, 0)
        create_link(links, math_035, math_036, 0, 1)
        create_link(links, repeat_output_001, separate_xyz_004, 0, 0)
        create_link(links, math_036, mix, 0, 0)
        create_link(links, combine_xyz_002, mix, 0, 4)
        create_link(links, separate_xyz_004, combine_xyz_006, 0, 0)
        create_link(links, separate_xyz_004, combine_xyz_006, 1, 1)
        create_link(links, combine_xyz_006, mix, 0, 5)
        create_link(links, mix, group_output, 1, 0)
        create_link(links, math_036, group_output, 0, 1)
        create_link(links, vector_math_006, reroute, 1, 0)
        create_link(links, camera_data_001, math_032, 2, 0)
        create_link(links, group_input_001, math, 7, 0)
        create_link(links, group_input_002, math_010, 3, 0)
        create_link(links, group_input_003, math_012, 4, 0)
        create_link(links, group_input_003, math_014, 4, 0)
        create_link(links, group_input_002, separate_xyz, 0, 0)
        create_link(links, group_input_004, evaluate_closure_001, 1, 0)
        create_link(links, group_input_005, math_001, 2, 0)
        create_link(links, group_input_006, evaluate_closure, 1, 0)

        return node_tree
