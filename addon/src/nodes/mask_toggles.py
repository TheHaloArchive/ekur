import bpy


def MaskToggles():
    node = bpy.data.node_groups.get("Mask Toggles")
    if node:
        return node

    mask_toggles = bpy.data.node_groups.new(type="ShaderNodeTree", name="Mask Toggles")

    # Sockets

    mask_0_socket_4 = mask_toggles.interface.new_socket(
        name="Mask_0", in_out="OUTPUT", socket_type="NodeSocketColor"
    )

    mask_1_socket_4 = mask_toggles.interface.new_socket(
        name="Mask_1", in_out="OUTPUT", socket_type="NodeSocketColor"
    )

    mask_0_socket_5 = mask_toggles.interface.new_socket(
        name="Mask_0", in_out="INPUT", socket_type="NodeSocketColor"
    )
    mask_0_socket_5.hide_value = True

    mask_1_socket_5 = mask_toggles.interface.new_socket(
        name="Mask_1", in_out="INPUT", socket_type="NodeSocketColor"
    )
    mask_1_socket_5.hide_value = True

    zone_2_toggle_socket = mask_toggles.interface.new_socket(
        name="Zone 2 Toggle", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    zone_2_toggle_socket.default_value = 1.0
    zone_2_toggle_socket.hide_value = True

    zone_3_toggle_socket = mask_toggles.interface.new_socket(
        name="Zone 3 Toggle", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    zone_3_toggle_socket.default_value = 1.0
    zone_3_toggle_socket.hide_value = True

    zone_4_toggle_socket = mask_toggles.interface.new_socket(
        name="Zone 4 Toggle", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    zone_4_toggle_socket.default_value = 1.0
    zone_4_toggle_socket.hide_value = True

    zone_5_toggle_socket = mask_toggles.interface.new_socket(
        name="Zone 5 Toggle", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    zone_5_toggle_socket.default_value = 1.0
    zone_5_toggle_socket.hide_value = True

    zone_6_toggle_socket = mask_toggles.interface.new_socket(
        name="Zone 6 Toggle", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    zone_6_toggle_socket.default_value = 1.0
    zone_6_toggle_socket.hide_value = True

    zone_7_toggle_socket = mask_toggles.interface.new_socket(
        name="Zone 7 Toggle", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    zone_7_toggle_socket.default_value = 1.0
    zone_7_toggle_socket.hide_value = True

    # Nodes
    combine_rgb_001 = mask_toggles.nodes.new("ShaderNodeCombineColor")
    combine_rgb_001.mode = "RGB"

    group_output_12 = mask_toggles.nodes.new("NodeGroupOutput")
    group_output_12.is_active_output = True

    math_004_2 = mask_toggles.nodes.new("ShaderNodeMath")
    math_004_2.operation = "SUBTRACT"
    math_004_2.use_clamp = False
    math_004_2.inputs[1].default_value = 1.0
    math_004_2.inputs[2].default_value = 0.5

    math_005_2 = mask_toggles.nodes.new("ShaderNodeMath")
    math_005_2.operation = "ADD"
    math_005_2.use_clamp = True
    math_005_2.inputs[2].default_value = 0.5

    math_003_1 = mask_toggles.nodes.new("ShaderNodeMath")
    math_003_1.operation = "SUBTRACT"
    math_003_1.use_clamp = False
    math_003_1.inputs[1].default_value = 1.0
    math_003_1.inputs[2].default_value = 0.5

    math_002_2 = mask_toggles.nodes.new("ShaderNodeMath")
    math_002_2.operation = "ADD"
    math_002_2.use_clamp = True
    math_002_2.inputs[2].default_value = 0.5

    combine_rgb_002 = mask_toggles.nodes.new("ShaderNodeCombineColor")
    combine_rgb_002.mode = "RGB"

    math_3 = mask_toggles.nodes.new("ShaderNodeMath")
    math_3.operation = "SUBTRACT"
    math_3.use_clamp = False
    math_3.inputs[1].default_value = 1.0
    math_3.inputs[2].default_value = 0.5

    separate_rgb_003_3 = mask_toggles.nodes.new("ShaderNodeSeparateColor")
    separate_rgb_003_3.mode = "RGB"

    math_010_1 = mask_toggles.nodes.new("ShaderNodeMath")
    math_010_1.operation = "SUBTRACT"
    math_010_1.use_clamp = False
    math_010_1.inputs[1].default_value = 1.0
    math_010_1.inputs[2].default_value = 0.5

    separate_rgb_004 = mask_toggles.nodes.new("ShaderNodeSeparateColor")
    separate_rgb_004.mode = "RGB"

    group_input_12 = mask_toggles.nodes.new("NodeGroupInput")

    math_007 = mask_toggles.nodes.new("ShaderNodeMath")
    math_007.operation = "ADD"
    math_007.use_clamp = True
    math_007.inputs[2].default_value = 0.5

    math_008 = mask_toggles.nodes.new("ShaderNodeMath")
    math_008.operation = "SUBTRACT"
    math_008.use_clamp = False
    math_008.inputs[1].default_value = 1.0
    math_008.inputs[2].default_value = 0.5

    math_009 = mask_toggles.nodes.new("ShaderNodeMath")
    math_009.operation = "ADD"
    math_009.use_clamp = True
    math_009.inputs[2].default_value = 0.5

    math_011_1 = mask_toggles.nodes.new("ShaderNodeMath")
    math_011_1.operation = "ADD"
    math_011_1.use_clamp = True
    math_011_1.inputs[2].default_value = 0.5

    math_006 = mask_toggles.nodes.new("ShaderNodeMath")
    math_006.operation = "SUBTRACT"
    math_006.use_clamp = False
    math_006.inputs[1].default_value = 1.0
    math_006.inputs[2].default_value = 0.5

    math_001_2 = mask_toggles.nodes.new("ShaderNodeMath")
    math_001_2.operation = "ADD"
    math_001_2.use_clamp = True
    math_001_2.inputs[2].default_value = 0.5

    combine_rgb_001.location = (574.973388671875, -6.1378173828125)
    group_output_12.location = (854.569580078125, -52.39923095703125)
    math_004_2.location = (135.48776245117188, -62.74334716796875)
    math_005_2.location = (321.2480773925781, -55.50457763671875)
    math_003_1.location = (139.00320434570312, -19.908966064453125)
    math_002_2.location = (321.8943176269531, -18.408966064453125)
    combine_rgb_002.location = (554.5843505859375, -273.8294982910156)
    math_3.location = (135.71482849121094, 19.672149658203125)
    separate_rgb_003_3.location = (-36.11372756958008, 96.54698944091797)
    math_010_1.location = (107.67276000976562, -419.98321533203125)
    separate_rgb_004.location = (-102.20046997070312, -288.08233642578125)
    group_input_12.location = (-366.1831970214844, -18.57741928100586)
    math_007.location = (317.5854187011719, -280.9073791503906)
    math_008.location = (123.69364929199219, -322.2621154785156)
    math_009.location = (335.5884094238281, -346.2477722167969)
    math_011_1.location = (335.8209533691406, -423.8923645019531)
    math_006.location = (118.5082015991211, -284.50140380859375)
    math_001_2.location = (318.03729248046875, 24.765289306640625)

    # Links

    mask_toggles.links.new(group_input_12.outputs[0], separate_rgb_003_3.inputs[0])
    mask_toggles.links.new(group_input_12.outputs[1], separate_rgb_004.inputs[0])
    mask_toggles.links.new(combine_rgb_001.outputs[0], group_output_12.inputs[0])
    mask_toggles.links.new(combine_rgb_002.outputs[0], group_output_12.inputs[1])
    mask_toggles.links.new(math_3.outputs[0], math_001_2.inputs[1])
    mask_toggles.links.new(group_input_12.outputs[2], math_3.inputs[0])
    mask_toggles.links.new(separate_rgb_003_3.outputs[0], math_001_2.inputs[0])
    mask_toggles.links.new(math_001_2.outputs[0], combine_rgb_001.inputs[0])
    mask_toggles.links.new(math_003_1.outputs[0], math_002_2.inputs[1])
    mask_toggles.links.new(separate_rgb_003_3.outputs[1], math_003_1.inputs[0])
    mask_toggles.links.new(group_input_12.outputs[3], math_002_2.inputs[0])
    mask_toggles.links.new(math_002_2.outputs[0], combine_rgb_001.inputs[1])
    mask_toggles.links.new(math_004_2.outputs[0], math_005_2.inputs[1])
    mask_toggles.links.new(separate_rgb_003_3.outputs[2], math_004_2.inputs[0])
    mask_toggles.links.new(group_input_12.outputs[4], math_005_2.inputs[0])
    mask_toggles.links.new(math_005_2.outputs[0], combine_rgb_001.inputs[2])
    mask_toggles.links.new(math_006.outputs[0], math_007.inputs[1])
    mask_toggles.links.new(separate_rgb_004.outputs[0], math_006.inputs[0])
    mask_toggles.links.new(math_007.outputs[0], combine_rgb_002.inputs[0])
    mask_toggles.links.new(group_input_12.outputs[5], math_007.inputs[0])
    mask_toggles.links.new(math_008.outputs[0], math_009.inputs[1])
    mask_toggles.links.new(group_input_12.outputs[6], math_008.inputs[0])
    mask_toggles.links.new(separate_rgb_004.outputs[1], math_009.inputs[0])
    mask_toggles.links.new(math_009.outputs[0], combine_rgb_002.inputs[1])
    mask_toggles.links.new(math_010_1.outputs[0], math_011_1.inputs[1])
    mask_toggles.links.new(group_input_12.outputs[7], math_010_1.inputs[0])
    mask_toggles.links.new(separate_rgb_004.outputs[2], math_011_1.inputs[0])
    mask_toggles.links.new(math_011_1.outputs[0], combine_rgb_002.inputs[2])
    return mask_toggles
