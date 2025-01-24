import bpy
from bpy.types import ShaderNodeVectorMath


def NormalMapCombineOrientation():
    node = bpy.data.node_groups.get("NormalMap_Combine-Orientation")
    if node:
        return node

    norm = bpy.data.node_groups.new(type="ShaderNodeTree", name="NormalMap_Combine-Orientation")

    _ = norm.interface.new_socket(
        name="Combined Normal Map", in_out="OUTPUT", socket_type="NodeSocketColor"
    )

    _ = norm.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    _ = norm.interface.new_socket(name="Base", in_out="INPUT", socket_type="NodeSocketColor")
    _ = norm.interface.new_socket(name="Detail", in_out="INPUT", socket_type="NodeSocketColor")

    group_input_14 = norm.nodes.new("NodeGroupInput")
    reroute_003 = norm.nodes.new("NodeReroute")
    reroute_002_3 = norm.nodes.new("NodeReroute")
    reroute_001_3 = norm.nodes.new("NodeReroute")
    reroute_004_3 = norm.nodes.new("NodeReroute")

    vectormult: ShaderNodeVectorMath = norm.nodes.new("ShaderNodeVectorMath")
    vectormult.operation = "MULTIPLY"
    vectormult.inputs[1].default_value = (-2.0, -2.0, 2.0)
    vectormult.inputs[2].default_value = (0.0, 0.0, 0.0)
    vectormult.inputs[3].default_value = 1.0

    vectorscale: ShaderNodeVectorMath = norm.nodes.new("ShaderNodeVectorMath")
    vectorscale.operation = "SCALE"
    vectorscale.inputs[1].default_value = (2.0, 2.0, 2.0)
    vectorscale.inputs[2].default_value = (0.0, 0.0, 0.0)
    vectorscale.inputs[3].default_value = 2.0

    vectoradd = norm.nodes.new("ShaderNodeVectorMath")
    vectoradd.operation = "ADD"
    vectoradd.inputs[1].default_value = (-1.0, -1.0, 0.0)
    vectoradd.inputs[2].default_value = (0.0, 0.0, 0.0)
    vectoradd.inputs[3].default_value = 1.0

    vectoradd2: ShaderNodeVectorMath = norm.nodes.new("ShaderNodeVectorMath")
    vectoradd2.operation = "ADD"
    vectoradd2.inputs[1].default_value = (1.0, 1.0, -1.0)
    vectoradd2.inputs[2].default_value = (0.0, 0.0, 0.0)
    vectoradd2.inputs[3].default_value = 1.0

    vectorscale2: ShaderNodeVectorMath = norm.nodes.new("ShaderNodeVectorMath")
    vectorscale2.operation = "SCALE"
    vectorscale2.inputs[1].default_value = (1.0, 1.0, -1.0)
    vectorscale2.inputs[2].default_value = (0.0, 0.0, 0.0)

    vectordot: ShaderNodeVectorMath = norm.nodes.new("ShaderNodeVectorMath")
    vectordot.operation = "DOT_PRODUCT"
    vectordot.inputs[2].default_value = (0.0, 0.0, 0.0)
    vectordot.inputs[3].default_value = 1.0

    separate_xyz = norm.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.outputs[0].hide = True
    separate_xyz.outputs[1].hide = True
    combinexyz = norm.nodes.new("ShaderNodeCombineXYZ")

    vector_math_010 = norm.nodes.new("ShaderNodeVectorMath")
    vector_math_010.operation = "DIVIDE"
    vector_math_010.inputs[2].default_value = (0.0, 0.0, 0.0)
    vector_math_010.inputs[3].default_value = 1.0

    vector_math_009 = norm.nodes.new("ShaderNodeVectorMath")
    vector_math_009.operation = "SUBTRACT"
    vector_math_009.inputs[2].default_value = (0.0, 0.0, 0.0)
    vector_math_009.inputs[3].default_value = 1.0

    vector_math_005 = norm.nodes.new("ShaderNodeVectorMath")
    vector_math_005.operation = "SCALE"
    vector_math_005.inputs[1].default_value = (0.5, 0.5, 0.5)
    vector_math_005.inputs[2].default_value = (0.0, 0.0, 0.0)
    vector_math_005.inputs[3].default_value = 0.5

    vector_math_004 = norm.nodes.new("ShaderNodeVectorMath")
    vector_math_004.operation = "NORMALIZE"
    vector_math_004.inputs[1].default_value = (0.0, 0.0, 0.0)
    vector_math_004.inputs[2].default_value = (0.0, 0.0, 0.0)
    vector_math_004.inputs[3].default_value = 1.0

    vector_math_006 = norm.nodes.new("ShaderNodeVectorMath")
    vector_math_006.operation = "ADD"
    vector_math_006.inputs[1].default_value = (0.5, 0.5, 0.5)
    vector_math_006.inputs[2].default_value = (0.0, 0.0, 0.0)
    vector_math_006.inputs[3].default_value = 1.0

    reroute = norm.nodes.new("NodeReroute")
    mix_8 = norm.nodes.new("ShaderNodeMix")
    mix_8.blend_type = "MIX"
    mix_8.clamp_factor = True
    mix_8.clamp_result = False
    mix_8.data_type = "RGBA"
    mix_8.factor_mode = "UNIFORM"
    mix_8.inputs[1].default_value = (0.5, 0.5, 0.5)
    mix_8.inputs[2].default_value = 0.0
    mix_8.inputs[3].default_value = 0.0
    mix_8.inputs[4].default_value = (0.0, 0.0, 0.0)
    mix_8.inputs[5].default_value = (0.0, 0.0, 0.0)
    mix_8.inputs[8].default_value = (0.0, 0.0, 0.0)
    mix_8.inputs[9].default_value = (0.0, 0.0, 0.0)

    reroute_005_3 = norm.nodes.new("NodeReroute")

    group_output_14 = norm.nodes.new("NodeGroupOutput")
    group_output_14.is_active_output = True

    group_input_14.location = (-680.1478271484375, -1.7763557434082031)
    reroute_003.location = (-473.7449645996094, -55.63496780395508)
    reroute_002_3.location = (-472.5776062011719, 236.6663818359375)
    reroute_001_3.location = (-442.8094177246094, -76.09606170654297)
    reroute_004_3.location = (-436.8861389160156, 164.55894470214844)
    vectormult.location = (-361.7262268066406, 166.41342163085938)
    vectorscale.location = (-352.0022277832031, 240.16766357421875)
    vectoradd.location = (-357.1380615234375, 205.62777709960938)
    vectoradd2.location = (-366.862060546875, 131.87353515625)
    vectorscale2.location = (-115.93279266357422, 165.04258728027344)
    vectordot.location = (-113.82295227050781, 200.9220733642578)
    separate_xyz.location = (-109.48788452148438, 241.37655639648438)
    combinexyz.location = (57.07867431640625, 209.7696075439453)
    vector_math_010.location = (55.63336181640625, 175.2928924560547)
    vector_math_009.location = (212.1328887939453, 148.53402709960938)
    vector_math_005.location = (214.83480834960938, 77.948974609375)
    vector_math_004.location = (213.77255249023438, 112.6468505859375)
    vector_math_006.location = (216.1195068359375, 43.219696044921875)
    reroute.location = (383.51739501953125, -64.48645782470703)
    mix_8.location = (415.302734375, 89.13896942138672)
    reroute_005_3.location = (383.51739501953125, 31.338207244873047)
    group_output_14.location = (613.7005615234375, 81.01988983154297)

    _ = norm.links.new(reroute_002_3.outputs[0], vectorscale.inputs[0])
    _ = norm.links.new(vectorscale.outputs[0], vectoradd.inputs[0])
    _ = norm.links.new(vectoradd.outputs[0], separate_xyz.inputs[0])
    _ = norm.links.new(vector_math_005.outputs[0], vector_math_006.inputs[0])
    _ = norm.links.new(vector_math_004.outputs[0], vector_math_005.inputs[0])
    _ = norm.links.new(mix_8.outputs[2], group_output_14.inputs[0])
    _ = norm.links.new(group_input_14.outputs[0], mix_8.inputs[0])
    _ = norm.links.new(reroute_003.outputs[0], mix_8.inputs[6])
    _ = norm.links.new(vectormult.outputs[0], vectoradd2.inputs[0])
    _ = norm.links.new(reroute_004_3.outputs[0], vectormult.inputs[0])
    _ = norm.links.new(vectoradd.outputs[0], vectordot.inputs[0])
    _ = norm.links.new(vectoradd2.outputs[0], vectordot.inputs[1])
    _ = norm.links.new(vectordot.outputs[1], vectorscale2.inputs[3])
    _ = norm.links.new(vectoradd.outputs[0], vectorscale2.inputs[0])
    _ = norm.links.new(vectoradd2.outputs[0], vector_math_009.inputs[1])
    _ = norm.links.new(vectorscale2.outputs[0], vector_math_010.inputs[0])
    _ = norm.links.new(vector_math_010.outputs[0], vector_math_009.inputs[0])
    _ = norm.links.new(separate_xyz.outputs[2], combinexyz.inputs[0])
    _ = norm.links.new(separate_xyz.outputs[2], combinexyz.inputs[1])
    _ = norm.links.new(separate_xyz.outputs[2], combinexyz.inputs[2])
    _ = norm.links.new(combinexyz.outputs[0], vector_math_010.inputs[1])
    _ = norm.links.new(vector_math_009.outputs[0], vector_math_004.inputs[0])
    _ = norm.links.new(reroute.outputs[0], mix_8.inputs[7])
    _ = norm.links.new(group_input_14.outputs[2], reroute_001_3.inputs[0])
    _ = norm.links.new(group_input_14.outputs[1], reroute_003.inputs[0])
    _ = norm.links.new(reroute_003.outputs[0], reroute_002_3.inputs[0])
    _ = norm.links.new(reroute_001_3.outputs[0], reroute_004_3.inputs[0])
    _ = norm.links.new(reroute_005_3.outputs[0], reroute.inputs[0])
    _ = norm.links.new(vector_math_006.outputs[0], reroute_005_3.inputs[0])
    return norm
