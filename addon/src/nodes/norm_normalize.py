import bpy


def NormNormalize():
    node = bpy.data.node_groups.get("Norm Normalize")
    if node:
        return node

    norm_normalize = bpy.data.node_groups.new(type="ShaderNodeTree", name="Norm Normalize")

    # Sockets

    normal_normalized_socket = norm_normalize.interface.new_socket(
        name="Normal Normalized", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    normal_normalized_socket.hide_value = True

    normal_socket = norm_normalize.interface.new_socket(
        name="Normal", in_out="INPUT", socket_type="NodeSocketVector"
    )
    normal_socket.default_value = (0.5, 0.5, 1.0)
    normal_socket.hide_value = True

    normal_flip_socket = norm_normalize.interface.new_socket(
        name="Normal Flip", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    normal_flip_socket.default_value = 1.0

    # Nodes

    frame = norm_normalize.nodes.new("NodeFrame")
    frame.label = "Normalizer"
    frame.name = "Frame"
    frame.use_custom_color = True
    frame.color = (0.5, 0.5, 1.0)
    frame.label_size = 64
    frame.shrink = True

    # node Group Output
    group_output = norm_normalize.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # node Group Input
    group_input = norm_normalize.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # node Math.107
    math_107 = norm_normalize.nodes.new("ShaderNodeMath")
    math_107.name = "Math.107"
    math_107.operation = "MULTIPLY_ADD"
    math_107.use_clamp = False
    # Value_001
    math_107.inputs[1].default_value = 2.0
    # Value_002
    math_107.inputs[2].default_value = -1.0

    # node Math.106
    math_106 = norm_normalize.nodes.new("ShaderNodeMath")
    math_106.name = "Math.106"
    math_106.operation = "SQRT"
    math_106.use_clamp = False
    # Value_001
    math_106.inputs[1].default_value = 0.5
    # Value_002
    math_106.inputs[2].default_value = 0.0

    # node Combine XYZ.004
    combine_xyz_004 = norm_normalize.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_004.name = "Combine XYZ.004"

    # node Vector Math
    vector_math = norm_normalize.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = "NORMALIZE"
    # Vector_001
    vector_math.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Vector_002
    vector_math.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    vector_math.inputs[3].default_value = 1.0

    # node Mix.028
    mix_028 = norm_normalize.nodes.new("ShaderNodeMix")
    mix_028.name = "Mix.028"
    mix_028.blend_type = "ADD"
    mix_028.clamp_factor = True
    mix_028.clamp_result = False
    mix_028.data_type = "RGBA"
    mix_028.factor_mode = "UNIFORM"
    # Factor_Float
    mix_028.inputs[0].default_value = 1.0
    # Factor_Vector
    mix_028.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_028.inputs[2].default_value = 0.0
    # B_Float
    mix_028.inputs[3].default_value = 0.0
    # A_Vector
    mix_028.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_028.inputs[5].default_value = (0.0, 0.0, 0.0)
    # B_Color
    mix_028.inputs[7].default_value = (1.0, 1.0, 1.0, 1.0)
    # A_Rotation
    mix_028.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix_028.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Math.035
    math_035 = norm_normalize.nodes.new("ShaderNodeMath")
    math_035.name = "Math.035"
    math_035.operation = "SUBTRACT"
    math_035.use_clamp = False
    # Value
    math_035.inputs[0].default_value = 1.0
    # Value_002
    math_035.inputs[2].default_value = 0.0

    # node Math.110
    math_110 = norm_normalize.nodes.new("ShaderNodeMath")
    math_110.name = "Math.110"
    math_110.operation = "MULTIPLY_ADD"
    math_110.use_clamp = True

    # node Math.109
    math_109 = norm_normalize.nodes.new("ShaderNodeMath")
    math_109.name = "Math.109"
    math_109.operation = "MULTIPLY"
    math_109.use_clamp = False
    # Value_002
    math_109.inputs[2].default_value = 0.0

    # node Mix.024
    mix_024 = norm_normalize.nodes.new("ShaderNodeMix")
    mix_024.name = "Mix.024"
    mix_024.blend_type = "DIVIDE"
    mix_024.clamp_factor = True
    mix_024.clamp_result = False
    mix_024.data_type = "RGBA"
    mix_024.factor_mode = "UNIFORM"
    # Factor_Float
    mix_024.inputs[0].default_value = 1.0
    # Factor_Vector
    mix_024.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_024.inputs[2].default_value = 0.0
    # B_Float
    mix_024.inputs[3].default_value = 0.0
    # A_Vector
    mix_024.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_024.inputs[5].default_value = (0.0, 0.0, 0.0)
    # B_Color
    mix_024.inputs[7].default_value = (2.0, 2.0, 2.0, 1.0)
    # A_Rotation
    mix_024.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix_024.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Separate XYZ.001
    separate_xyz_001 = norm_normalize.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_001.name = "Separate XYZ.001"

    # node Mix
    mix = norm_normalize.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = "FLOAT"
    mix.factor_mode = "UNIFORM"
    # Factor_Vector
    mix.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Vector
    mix.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix.inputs[5].default_value = (0.0, 0.0, 0.0)
    # A_Color
    mix.inputs[6].default_value = (0.5, 0.5, 0.5, 1.0)
    # B_Color
    mix.inputs[7].default_value = (0.5, 0.5, 0.5, 1.0)
    # A_Rotation
    mix.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Math.108
    math_108 = norm_normalize.nodes.new("ShaderNodeMath")
    math_108.name = "Math.108"
    math_108.operation = "MULTIPLY_ADD"
    math_108.use_clamp = False
    # Value_001
    math_108.inputs[1].default_value = 2.0
    # Value_002
    math_108.inputs[2].default_value = -1.0

    # node Math.111
    math_111 = norm_normalize.nodes.new("ShaderNodeMath")
    math_111.name = "Math.111"
    math_111.operation = "SUBTRACT"
    math_111.use_clamp = False
    # Value
    math_111.inputs[0].default_value = 1.0
    # Value_002
    math_111.inputs[2].default_value = -1.0

    # Set parents
    math_107.parent = frame
    math_106.parent = frame
    combine_xyz_004.parent = frame
    vector_math.parent = frame
    mix_028.parent = frame
    math_035.parent = frame
    math_110.parent = frame
    math_109.parent = frame
    mix_024.parent = frame
    separate_xyz_001.parent = frame
    mix.parent = frame
    math_108.parent = frame
    math_111.parent = frame

    # Set locations
    frame.location = (-796.8751220703125, 129.10098266601562)
    group_output.location = (1507.832275390625, -0.0)
    group_input.location = (-1067.2105712890625, 3.991671562194824)
    math_107.location = (220.0, 0.0)
    math_106.location = (1363.0, -100.0001220703125)
    combine_xyz_004.location = (1583.0, -140.0)
    vector_math.location = (1743.0, -140.0)
    mix_028.location = (1923.0, -140.0)
    math_035.location = (1183.0, -80.0)
    math_110.location = (1003.0, -80.0)
    math_109.location = (803.0, -180.0)
    mix_024.location = (2103.000244140625, -140.0)
    separate_xyz_001.location = (-40.0, -100.0001220703125)
    mix.location = (399.6340637207031, -350.3708190917969)
    math_108.location = (588.7058715820312, -198.44264221191406)
    math_111.location = (154.98382568359375, -413.8017883300781)

    # Set dimensions
    frame.width, frame.height = 2341.71435546875, 680.2857055664062
    group_output.width, group_output.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    math_107.width, math_107.height = 140.0, 100.0
    math_106.width, math_106.height = 140.0, 100.0
    combine_xyz_004.width, combine_xyz_004.height = 140.0, 100.0
    vector_math.width, vector_math.height = 140.0, 100.0
    mix_028.width, mix_028.height = 140.0, 100.0
    math_035.width, math_035.height = 140.0, 100.0
    math_110.width, math_110.height = 140.0, 100.0
    math_109.width, math_109.height = 140.0, 100.0
    mix_024.width, mix_024.height = 140.0, 100.0
    separate_xyz_001.width, separate_xyz_001.height = 140.0, 100.0
    mix.width, mix.height = 140.0, 100.0
    math_108.width, math_108.height = 140.0, 100.0
    math_111.width, math_111.height = 140.0, 100.0

    norm_normalize.links.new(group_input.outputs[0], separate_xyz_001.inputs[0])
    norm_normalize.links.new(mix_024.outputs[2], group_output.inputs[0])
    norm_normalize.links.new(combine_xyz_004.outputs[0], vector_math.inputs[0])
    norm_normalize.links.new(math_110.outputs[0], math_035.inputs[1])
    norm_normalize.links.new(math_035.outputs[0], math_106.inputs[0])
    norm_normalize.links.new(math_106.outputs[0], combine_xyz_004.inputs[2])
    norm_normalize.links.new(mix_028.outputs[2], mix_024.inputs[6])
    norm_normalize.links.new(vector_math.outputs[0], mix_028.inputs[6])
    norm_normalize.links.new(math_109.outputs[0], math_110.inputs[2])
    norm_normalize.links.new(math_107.outputs[0], math_110.inputs[0])
    norm_normalize.links.new(math_107.outputs[0], math_110.inputs[1])
    norm_normalize.links.new(math_108.outputs[0], math_109.inputs[1])
    norm_normalize.links.new(math_108.outputs[0], math_109.inputs[0])
    norm_normalize.links.new(math_107.outputs[0], combine_xyz_004.inputs[0])
    norm_normalize.links.new(separate_xyz_001.outputs[0], math_107.inputs[0])
    norm_normalize.links.new(group_input.outputs[1], mix.inputs[0])
    norm_normalize.links.new(separate_xyz_001.outputs[1], math_111.inputs[1])
    norm_normalize.links.new(math_111.outputs[0], mix.inputs[3])
    norm_normalize.links.new(separate_xyz_001.outputs[1], mix.inputs[2])
    norm_normalize.links.new(mix.outputs[0], math_108.inputs[0])
    norm_normalize.links.new(math_108.outputs[0], combine_xyz_004.inputs[1])
    return norm_normalize
