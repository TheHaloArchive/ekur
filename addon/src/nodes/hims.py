import bpy
from bpy.types import ShaderNodeGroup, ShaderNodeTree

from .detail_normals import DetailNormals
from .infinite_color import InfiniteColor
from .mask_toggles import MaskToggles
from .infinite_masking_sorter_nogrime_col import InfiniteMaskingSorterNoGrimeCol
from .infinite_matts import InfiniteMatts
from .emission import Emission
from .color_mixer import ColorMixer
from .scratch_global_toggle import ScratchGlobalToggle
from .infinite_masking_sorter import InfiniteMaskingSorter
from .infinite_masking_sorter_nogrime import InfiniteMaskingSorterNoGrime


def HIMS() -> ShaderNodeTree:
    shader: ShaderNodeTree | None = bpy.data.node_groups.get(
        "Halo Infinite Shader 3.0 by Chunch and ChromaCore"
    )
    if shader:
        return shader
    hims: ShaderNodeTree = bpy.data.node_groups.new(
        type="ShaderNodeTree", name="Halo Infinite Shader 3.0 by Chunch and ChromaCore"
    )

    outputs_panel_3 = hims.interface.new_panel("Outputs")
    _ = hims.interface.new_socket(
        name="BSDF",
        in_out="OUTPUT",
        socket_type="NodeSocketShader",
        parent=outputs_panel_3,
    )

    _ = hims.interface.new_socket(
        name="Bake_Color",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=outputs_panel_3,
    )

    _ = hims.interface.new_socket(
        name="Bake_Metallic",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=outputs_panel_3,
    )

    _ = hims.interface.new_socket(
        name="Bake_Roughness",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=outputs_panel_3,
    )

    _ = hims.interface.new_socket(
        name="Bake_Emissive",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=outputs_panel_3,
    )

    _ = hims.interface.new_socket(
        name="Bake_Spec",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=outputs_panel_3,
    )

    # Socket Bake_Color_SpecEdition
    bake_color_specedition_socket = hims.interface.new_socket(
        name="Bake_Color_SpecEdition",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=outputs_panel_3,
    )
    bake_color_specedition_socket.attribute_domain = "POINT"

    # Socket Bake_AO
    bake_ao_socket = hims.interface.new_socket(
        name="Bake_AO",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=outputs_panel_3,
    )
    bake_ao_socket.attribute_domain = "POINT"

    _ = hims.interface.new_socket(
        name="Normal",
        in_out="OUTPUT",
        socket_type="NodeSocketVector",
        parent=outputs_panel_3,
    )

    _ = hims.interface.new_socket(
        name="MaskMap <Unity>",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=outputs_panel_3,
    )
    _ = hims.interface.new_socket(
        name="SmoothnessMap <Unity>",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=outputs_panel_3,
    )

    # Socket Bake IDMask
    bake_idmask_socket = hims.interface.new_socket(
        name="Bake IDMask",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=outputs_panel_3,
    )
    bake_idmask_socket.attribute_domain = "POINT"

    # Panel Base Textures
    base_textures_panel = hims.interface.new_panel("Base Textures")
    # Socket ASG
    asg_socket_5 = hims.interface.new_socket(
        name="ASG",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=base_textures_panel,
    )
    asg_socket_5.attribute_domain = "POINT"
    asg_socket_5.hide_value = True

    # Socket Mask_0
    mask_0_socket_8 = hims.interface.new_socket(
        name="Mask_0",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=base_textures_panel,
    )
    mask_0_socket_8.attribute_domain = "POINT"
    mask_0_socket_8.hide_value = True

    # Socket Mask_1
    mask_1_socket_8 = hims.interface.new_socket(
        name="Mask_1",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=base_textures_panel,
    )
    mask_1_socket_8.attribute_domain = "POINT"
    mask_1_socket_8.hide_value = True

    # Socket Normal
    normal_socket_3 = hims.interface.new_socket(
        name="Normal",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=base_textures_panel,
    )
    normal_socket_3.attribute_domain = "POINT"
    normal_socket_3.hide_value = True

    # Panel Global Settings
    global_settings_panel = hims.interface.new_panel("Global Settings")
    # Socket Detail Norm Toggle
    detail_norm_toggle_socket = hims.interface.new_socket(
        name="Detail Norm Toggle",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=global_settings_panel,
    )
    detail_norm_toggle_socket.subtype = "NONE"
    detail_norm_toggle_socket.default_value = 1.0
    detail_norm_toggle_socket.min_value = 0.0
    detail_norm_toggle_socket.max_value = 1.0
    detail_norm_toggle_socket.attribute_domain = "POINT"

    # Socket Base Normal Flip
    base_normal_flip_socket = hims.interface.new_socket(
        name="Base Normal Flip",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=global_settings_panel,
    )
    base_normal_flip_socket.subtype = "NONE"
    base_normal_flip_socket.default_value = 1.0
    base_normal_flip_socket.min_value = -3.4028234663852886e38
    base_normal_flip_socket.max_value = 3.4028234663852886e38
    base_normal_flip_socket.attribute_domain = "POINT"

    # Socket Detail Normal Flip
    detail_normal_flip_socket_1 = hims.interface.new_socket(
        name="Detail Normal Flip",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=global_settings_panel,
    )
    detail_normal_flip_socket_1.subtype = "NONE"
    detail_normal_flip_socket_1.default_value = 1.0
    detail_normal_flip_socket_1.min_value = -3.4028234663852886e38
    detail_normal_flip_socket_1.max_value = 3.4028234663852886e38
    detail_normal_flip_socket_1.attribute_domain = "POINT"

    # Socket Grime Amount
    grime_amount_socket_6 = hims.interface.new_socket(
        name="Grime Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=global_settings_panel,
    )
    grime_amount_socket_6.subtype = "NONE"
    grime_amount_socket_6.default_value = 0.8500000238418579
    grime_amount_socket_6.min_value = 0.0
    grime_amount_socket_6.max_value = 2.0
    grime_amount_socket_6.attribute_domain = "POINT"

    # Socket Grime Height Toggle
    grime_height_toggle_socket = hims.interface.new_socket(
        name="Grime Height Toggle",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=global_settings_panel,
    )
    grime_height_toggle_socket.subtype = "NONE"
    grime_height_toggle_socket.default_value = 0.0
    grime_height_toggle_socket.min_value = 0.0
    grime_height_toggle_socket.max_value = 1.0
    grime_height_toggle_socket.attribute_domain = "POINT"

    # Socket Grime Height Scale
    grime_height_scale_socket = hims.interface.new_socket(
        name="Grime Height Scale",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=global_settings_panel,
    )
    grime_height_scale_socket.subtype = "NONE"
    grime_height_scale_socket.default_value = 100.0
    grime_height_scale_socket.min_value = 0.0
    grime_height_scale_socket.max_value = 100.0
    grime_height_scale_socket.attribute_domain = "POINT"

    # Socket AO Amount
    ao_amount_socket = hims.interface.new_socket(
        name="AO Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=global_settings_panel,
    )
    ao_amount_socket.subtype = "NONE"
    ao_amount_socket.default_value = 1.0
    ao_amount_socket.min_value = 0.0
    ao_amount_socket.max_value = 1.0
    ao_amount_socket.attribute_domain = "POINT"

    # Socket Scratch Height Amount
    scratch_height_amount_socket = hims.interface.new_socket(
        name="Scratch Height Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=global_settings_panel,
    )
    scratch_height_amount_socket.subtype = "NONE"
    scratch_height_amount_socket.default_value = 1.0
    scratch_height_amount_socket.min_value = 0.0
    scratch_height_amount_socket.max_value = 1.0
    scratch_height_amount_socket.attribute_domain = "POINT"

    # Socket Global Scratch Toggle (Uses Zone 1 Scratch Amount)
    global_scratch_toggle__uses_zone_1_scratch_amount__socket = hims.interface.new_socket(
        name="Global Scratch Toggle (Uses Zone 1 Scratch Amount)",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=global_settings_panel,
    )
    global_scratch_toggle__uses_zone_1_scratch_amount__socket.subtype = "NONE"
    global_scratch_toggle__uses_zone_1_scratch_amount__socket.default_value = 0.0
    global_scratch_toggle__uses_zone_1_scratch_amount__socket.min_value = 0.0
    global_scratch_toggle__uses_zone_1_scratch_amount__socket.max_value = 1.0
    global_scratch_toggle__uses_zone_1_scratch_amount__socket.attribute_domain = "POINT"

    # Panel Zone 1
    zone_1_panel = hims.interface.new_panel("Zone 1")
    # Socket Zone 1 Gradient Out
    zone_1_gradient_out_socket = hims.interface.new_socket(
        name="Zone 1 Gradient Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_1_panel,
    )
    zone_1_gradient_out_socket.subtype = "NONE"
    zone_1_gradient_out_socket.default_value = 0.0
    zone_1_gradient_out_socket.min_value = 0.0
    zone_1_gradient_out_socket.max_value = 1.0
    zone_1_gradient_out_socket.attribute_domain = "POINT"
    zone_1_gradient_out_socket.hide_value = True

    # Socket Zone 1 Rough Out
    zone_1_rough_out_socket = hims.interface.new_socket(
        name="Zone 1 Rough Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_1_panel,
    )
    zone_1_rough_out_socket.subtype = "NONE"
    zone_1_rough_out_socket.default_value = 0.5
    zone_1_rough_out_socket.min_value = 0.0
    zone_1_rough_out_socket.max_value = 1.0
    zone_1_rough_out_socket.attribute_domain = "POINT"
    zone_1_rough_out_socket.hide_value = True

    # Socket Zone 1 Norm Out
    zone_1_norm_out_socket = hims.interface.new_socket(
        name="Zone 1 Norm Out",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_1_panel,
    )
    zone_1_norm_out_socket.attribute_domain = "POINT"
    zone_1_norm_out_socket.hide_value = True

    # Socket Zone 1 Scratch Amount
    zone_1_scratch_amount_socket = hims.interface.new_socket(
        name="Zone 1 Scratch Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_1_panel,
    )
    zone_1_scratch_amount_socket.subtype = "NONE"
    zone_1_scratch_amount_socket.default_value = 0.800000011920929
    zone_1_scratch_amount_socket.min_value = 0.0
    zone_1_scratch_amount_socket.max_value = 2.0
    zone_1_scratch_amount_socket.attribute_domain = "POINT"

    # Socket Zone 1 Scratch Metallic
    zone_1_scratch_metallic_socket = hims.interface.new_socket(
        name="Zone 1 Scratch Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_1_panel,
    )
    zone_1_scratch_metallic_socket.subtype = "NONE"
    zone_1_scratch_metallic_socket.default_value = 1.0
    zone_1_scratch_metallic_socket.min_value = 0.0
    zone_1_scratch_metallic_socket.max_value = 1.0
    zone_1_scratch_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 1 Scratch Roughness
    zone_1_scratch_roughness_socket = hims.interface.new_socket(
        name="Zone 1 Scratch Roughness",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_1_panel,
    )
    zone_1_scratch_roughness_socket.subtype = "NONE"
    zone_1_scratch_roughness_socket.default_value = 0.4000000059604645
    zone_1_scratch_roughness_socket.min_value = 0.0
    zone_1_scratch_roughness_socket.max_value = 1.0
    zone_1_scratch_roughness_socket.attribute_domain = "POINT"

    # Socket Zone 1 Metallic
    zone_1_metallic_socket = hims.interface.new_socket(
        name="Zone 1 Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_1_panel,
    )
    zone_1_metallic_socket.subtype = "NONE"
    zone_1_metallic_socket.default_value = 0.0
    zone_1_metallic_socket.min_value = 0.0
    zone_1_metallic_socket.max_value = 1.0
    zone_1_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 1 SSS Amount
    zone_1_sss_amount_socket = hims.interface.new_socket(
        name="Zone 1 SSS Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_1_panel,
    )
    zone_1_sss_amount_socket.subtype = "NONE"
    zone_1_sss_amount_socket.default_value = 0.0
    zone_1_sss_amount_socket.min_value = 0.0
    zone_1_sss_amount_socket.max_value = 1.0
    zone_1_sss_amount_socket.attribute_domain = "POINT"

    # Socket Zone 1 Transparency Amount
    zone_1_transparency_amount_socket = hims.interface.new_socket(
        name="Zone 1 Transparency Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_1_panel,
    )
    zone_1_transparency_amount_socket.subtype = "NONE"
    zone_1_transparency_amount_socket.default_value = 0.0
    zone_1_transparency_amount_socket.min_value = 0.0
    zone_1_transparency_amount_socket.max_value = 1.0
    zone_1_transparency_amount_socket.attribute_domain = "POINT"

    # Socket Zone 1 Emmisive Amount
    zone_1_emmisive_amount_socket = hims.interface.new_socket(
        name="Zone 1 Emmisive Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_1_panel,
    )
    zone_1_emmisive_amount_socket.subtype = "NONE"
    zone_1_emmisive_amount_socket.default_value = 0.0
    zone_1_emmisive_amount_socket.min_value = 0.0
    zone_1_emmisive_amount_socket.max_value = 100.0
    zone_1_emmisive_amount_socket.attribute_domain = "POINT"

    # Socket Zone 1 TopColor
    zone_1_topcolor_socket = hims.interface.new_socket(
        name="Zone 1 TopColor",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_1_panel,
    )
    zone_1_topcolor_socket.attribute_domain = "POINT"

    # Socket Zone 1 MidColor
    zone_1_midcolor_socket = hims.interface.new_socket(
        name="Zone 1 MidColor",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_1_panel,
    )
    zone_1_midcolor_socket.attribute_domain = "POINT"

    # Socket Zone 1 BotColor
    zone_1_botcolor_socket = hims.interface.new_socket(
        name="Zone 1 BotColor",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_1_panel,
    )
    zone_1_botcolor_socket.attribute_domain = "POINT"

    # Socket Zone 1 ScratchColor
    zone_1_scratchcolor_socket = hims.interface.new_socket(
        name="Zone 1 ScratchColor",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_1_panel,
    )
    zone_1_scratchcolor_socket.attribute_domain = "POINT"

    # Panel Zone 2
    zone_2_panel = hims.interface.new_panel("Zone 2")
    # Socket Zone 2 Toggle
    zone_2_toggle_socket_1 = hims.interface.new_socket(
        name="Zone 2 Toggle",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_2_panel,
    )
    zone_2_toggle_socket_1.subtype = "NONE"
    zone_2_toggle_socket_1.default_value = 0.0
    zone_2_toggle_socket_1.min_value = 0.0
    zone_2_toggle_socket_1.max_value = 1.0
    zone_2_toggle_socket_1.attribute_domain = "POINT"

    # Socket Zone 2 Gradient Out
    zone_2_gradient_out_socket = hims.interface.new_socket(
        name="Zone 2 Gradient Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_2_panel,
    )
    zone_2_gradient_out_socket.subtype = "NONE"
    zone_2_gradient_out_socket.default_value = 0.0
    zone_2_gradient_out_socket.min_value = 0.0
    zone_2_gradient_out_socket.max_value = 1.0
    zone_2_gradient_out_socket.attribute_domain = "POINT"
    zone_2_gradient_out_socket.hide_value = True

    # Socket Zone 2 Rough Out
    zone_2_rough_out_socket = hims.interface.new_socket(
        name="Zone 2 Rough Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_2_panel,
    )
    zone_2_rough_out_socket.subtype = "NONE"
    zone_2_rough_out_socket.default_value = 0.5
    zone_2_rough_out_socket.min_value = 0.0
    zone_2_rough_out_socket.max_value = 1.0
    zone_2_rough_out_socket.attribute_domain = "POINT"
    zone_2_rough_out_socket.hide_value = True

    # Socket Zone 2 Norm Out
    zone_2_norm_out_socket = hims.interface.new_socket(
        name="Zone 2 Norm Out",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_2_panel,
    )
    zone_2_norm_out_socket.attribute_domain = "POINT"
    zone_2_norm_out_socket.hide_value = True

    # Socket Zone 2 Scratch Amount
    zone_2_scratch_amount_socket = hims.interface.new_socket(
        name="Zone 2 Scratch Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_2_panel,
    )
    zone_2_scratch_amount_socket.subtype = "NONE"
    zone_2_scratch_amount_socket.default_value = 0.800000011920929
    zone_2_scratch_amount_socket.min_value = 0.0
    zone_2_scratch_amount_socket.max_value = 2.0
    zone_2_scratch_amount_socket.attribute_domain = "POINT"

    # Socket Zone 2 Scratch Metallic
    zone_2_scratch_metallic_socket = hims.interface.new_socket(
        name="Zone 2 Scratch Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_2_panel,
    )
    zone_2_scratch_metallic_socket.subtype = "NONE"
    zone_2_scratch_metallic_socket.default_value = 1.0
    zone_2_scratch_metallic_socket.min_value = 0.0
    zone_2_scratch_metallic_socket.max_value = 1.0
    zone_2_scratch_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 2 Scratch Roughness
    zone_2_scratch_roughness_socket = hims.interface.new_socket(
        name="Zone 2 Scratch Roughness",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_2_panel,
    )
    zone_2_scratch_roughness_socket.subtype = "NONE"
    zone_2_scratch_roughness_socket.default_value = 0.4000000059604645
    zone_2_scratch_roughness_socket.min_value = 0.0
    zone_2_scratch_roughness_socket.max_value = 1.0
    zone_2_scratch_roughness_socket.attribute_domain = "POINT"

    # Socket Zone 2 Metallic
    zone_2_metallic_socket = hims.interface.new_socket(
        name="Zone 2 Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_2_panel,
    )
    zone_2_metallic_socket.subtype = "NONE"
    zone_2_metallic_socket.default_value = 0.0
    zone_2_metallic_socket.min_value = 0.0
    zone_2_metallic_socket.max_value = 1.0
    zone_2_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 2 SSS Amount
    zone_2_sss_amount_socket = hims.interface.new_socket(
        name="Zone 2 SSS Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_2_panel,
    )
    zone_2_sss_amount_socket.subtype = "NONE"
    zone_2_sss_amount_socket.default_value = 0.0
    zone_2_sss_amount_socket.min_value = 0.0
    zone_2_sss_amount_socket.max_value = 1.0
    zone_2_sss_amount_socket.attribute_domain = "POINT"

    # Socket Zone 2 Transparency Amount
    zone_2_transparency_amount_socket = hims.interface.new_socket(
        name="Zone 2 Transparency Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_2_panel,
    )
    zone_2_transparency_amount_socket.subtype = "NONE"
    zone_2_transparency_amount_socket.default_value = 0.0
    zone_2_transparency_amount_socket.min_value = 0.0
    zone_2_transparency_amount_socket.max_value = 1.0
    zone_2_transparency_amount_socket.attribute_domain = "POINT"

    # Socket Zone 2 Emmisive Amount
    zone_2_emmisive_amount_socket = hims.interface.new_socket(
        name="Zone 2 Emmisive Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_2_panel,
    )
    zone_2_emmisive_amount_socket.subtype = "NONE"
    zone_2_emmisive_amount_socket.default_value = 0.0
    zone_2_emmisive_amount_socket.min_value = 0.0
    zone_2_emmisive_amount_socket.max_value = 100.0
    zone_2_emmisive_amount_socket.attribute_domain = "POINT"

    # Socket Zone 2 Top
    zone_2_top_socket = hims.interface.new_socket(
        name="Zone 2 Top",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_2_panel,
    )
    zone_2_top_socket.attribute_domain = "POINT"

    # Socket Zone 2 Mid
    zone_2_mid_socket = hims.interface.new_socket(
        name="Zone 2 Mid",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_2_panel,
    )
    zone_2_mid_socket.attribute_domain = "POINT"

    # Socket Zone 2 Bot
    zone_2_bot_socket = hims.interface.new_socket(
        name="Zone 2 Bot",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_2_panel,
    )
    zone_2_bot_socket.attribute_domain = "POINT"

    # Socket Zone 2 ScratchColor
    zone_2_scratchcolor_socket = hims.interface.new_socket(
        name="Zone 2 ScratchColor",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_2_panel,
    )
    zone_2_scratchcolor_socket.attribute_domain = "POINT"

    # Panel Zone 3
    zone_3_panel = hims.interface.new_panel("Zone 3")
    # Socket Zone 3 Toggle
    zone_3_toggle_socket_1 = hims.interface.new_socket(
        name="Zone 3 Toggle",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_3_panel,
    )
    zone_3_toggle_socket_1.subtype = "NONE"
    zone_3_toggle_socket_1.default_value = 0.0
    zone_3_toggle_socket_1.min_value = 0.0
    zone_3_toggle_socket_1.max_value = 1.0
    zone_3_toggle_socket_1.attribute_domain = "POINT"

    # Socket Zone 3 Gradient Out
    zone_3_gradient_out_socket = hims.interface.new_socket(
        name="Zone 3 Gradient Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_3_panel,
    )
    zone_3_gradient_out_socket.subtype = "FACTOR"
    zone_3_gradient_out_socket.default_value = 0.0
    zone_3_gradient_out_socket.min_value = 0.0
    zone_3_gradient_out_socket.max_value = 1.0
    zone_3_gradient_out_socket.attribute_domain = "POINT"
    zone_3_gradient_out_socket.hide_value = True

    # Socket Zone 3 Rough Out
    zone_3_rough_out_socket = hims.interface.new_socket(
        name="Zone 3 Rough Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_3_panel,
    )
    zone_3_rough_out_socket.subtype = "FACTOR"
    zone_3_rough_out_socket.default_value = 0.5
    zone_3_rough_out_socket.min_value = 0.0
    zone_3_rough_out_socket.max_value = 1.0
    zone_3_rough_out_socket.attribute_domain = "POINT"
    zone_3_rough_out_socket.hide_value = True

    # Socket Zone 3 Norm Out
    zone_3_norm_out_socket = hims.interface.new_socket(
        name="Zone 3 Norm Out",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_3_panel,
    )
    zone_3_norm_out_socket.attribute_domain = "POINT"
    zone_3_norm_out_socket.hide_value = True

    # Socket Zone 3 Scratch Amount
    zone_3_scratch_amount_socket = hims.interface.new_socket(
        name="Zone 3 Scratch Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_3_panel,
    )
    zone_3_scratch_amount_socket.subtype = "NONE"
    zone_3_scratch_amount_socket.default_value = 0.800000011920929
    zone_3_scratch_amount_socket.min_value = 0.0
    zone_3_scratch_amount_socket.max_value = 2.0
    zone_3_scratch_amount_socket.attribute_domain = "POINT"

    # Socket Zone 3 Scratch Metallic
    zone_3_scratch_metallic_socket = hims.interface.new_socket(
        name="Zone 3 Scratch Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_3_panel,
    )
    zone_3_scratch_metallic_socket.subtype = "NONE"
    zone_3_scratch_metallic_socket.default_value = 1.0
    zone_3_scratch_metallic_socket.min_value = 0.0
    zone_3_scratch_metallic_socket.max_value = 1.0
    zone_3_scratch_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 3 Scratch Roughness
    zone_3_scratch_roughness_socket = hims.interface.new_socket(
        name="Zone 3 Scratch Roughness",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_3_panel,
    )
    zone_3_scratch_roughness_socket.subtype = "NONE"
    zone_3_scratch_roughness_socket.default_value = 0.4000000059604645
    zone_3_scratch_roughness_socket.min_value = 0.0
    zone_3_scratch_roughness_socket.max_value = 1.0
    zone_3_scratch_roughness_socket.attribute_domain = "POINT"

    # Socket Zone 3 Metallic
    zone_3_metallic_socket = hims.interface.new_socket(
        name="Zone 3 Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_3_panel,
    )
    zone_3_metallic_socket.subtype = "NONE"
    zone_3_metallic_socket.default_value = 0.0
    zone_3_metallic_socket.min_value = 0.0
    zone_3_metallic_socket.max_value = 1.0
    zone_3_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 3 SSS Amount
    zone_3_sss_amount_socket = hims.interface.new_socket(
        name="Zone 3 SSS Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_3_panel,
    )
    zone_3_sss_amount_socket.subtype = "NONE"
    zone_3_sss_amount_socket.default_value = 0.0
    zone_3_sss_amount_socket.min_value = 0.0
    zone_3_sss_amount_socket.max_value = 1.0
    zone_3_sss_amount_socket.attribute_domain = "POINT"

    # Socket Zone 3 Transparency Amount
    zone_3_transparency_amount_socket = hims.interface.new_socket(
        name="Zone 3 Transparency Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_3_panel,
    )
    zone_3_transparency_amount_socket.subtype = "NONE"
    zone_3_transparency_amount_socket.default_value = 0.0
    zone_3_transparency_amount_socket.min_value = 0.0
    zone_3_transparency_amount_socket.max_value = 1.0
    zone_3_transparency_amount_socket.attribute_domain = "POINT"

    # Socket Zone 3 Emmisive Amount
    zone_3_emmisive_amount_socket = hims.interface.new_socket(
        name="Zone 3 Emmisive Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_3_panel,
    )
    zone_3_emmisive_amount_socket.subtype = "NONE"
    zone_3_emmisive_amount_socket.default_value = 0.0
    zone_3_emmisive_amount_socket.min_value = 0.0
    zone_3_emmisive_amount_socket.max_value = 100.0
    zone_3_emmisive_amount_socket.attribute_domain = "POINT"

    # Socket Zone 3 Top
    zone_3_top_socket = hims.interface.new_socket(
        name="Zone 3 Top",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_3_panel,
    )
    zone_3_top_socket.attribute_domain = "POINT"

    # Socket Zone 3 Mid
    zone_3_mid_socket = hims.interface.new_socket(
        name="Zone 3 Mid",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_3_panel,
    )
    zone_3_mid_socket.attribute_domain = "POINT"

    # Socket Zone 3 Bot
    zone_3_bot_socket = hims.interface.new_socket(
        name="Zone 3 Bot",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_3_panel,
    )
    zone_3_bot_socket.attribute_domain = "POINT"

    # Socket Zone 3 ScratchColor
    zone_3_scratchcolor_socket = hims.interface.new_socket(
        name="Zone 3 ScratchColor",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_3_panel,
    )
    zone_3_scratchcolor_socket.attribute_domain = "POINT"

    # Socket Zone 3 SSS Color
    zone_3_sss_color_socket = hims.interface.new_socket(
        name="Zone 3 SSS Color",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_3_panel,
    )
    zone_3_sss_color_socket.attribute_domain = "POINT"

    # Panel Zone 4
    zone_4_panel = hims.interface.new_panel("Zone 4")
    # Socket Zone 4 Toggle
    zone_4_toggle_socket_1 = hims.interface.new_socket(
        name="Zone 4 Toggle",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_4_panel,
    )
    zone_4_toggle_socket_1.subtype = "NONE"
    zone_4_toggle_socket_1.default_value = 0.0
    zone_4_toggle_socket_1.min_value = 0.0
    zone_4_toggle_socket_1.max_value = 2.0
    zone_4_toggle_socket_1.attribute_domain = "POINT"

    # Socket Zone 4 Gradient Out
    zone_4_gradient_out_socket = hims.interface.new_socket(
        name="Zone 4 Gradient Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_4_panel,
    )
    zone_4_gradient_out_socket.subtype = "FACTOR"
    zone_4_gradient_out_socket.default_value = 0.0
    zone_4_gradient_out_socket.min_value = 0.0
    zone_4_gradient_out_socket.max_value = 1.0
    zone_4_gradient_out_socket.attribute_domain = "POINT"
    zone_4_gradient_out_socket.hide_value = True

    # Socket Zone 4 Rough Out
    zone_4_rough_out_socket = hims.interface.new_socket(
        name="Zone 4 Rough Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_4_panel,
    )
    zone_4_rough_out_socket.subtype = "FACTOR"
    zone_4_rough_out_socket.default_value = 0.5
    zone_4_rough_out_socket.min_value = 0.0
    zone_4_rough_out_socket.max_value = 1.0
    zone_4_rough_out_socket.attribute_domain = "POINT"
    zone_4_rough_out_socket.hide_value = True

    # Socket Zone 4 Norm Out
    zone_4_norm_out_socket = hims.interface.new_socket(
        name="Zone 4 Norm Out",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_4_panel,
    )
    zone_4_norm_out_socket.attribute_domain = "POINT"
    zone_4_norm_out_socket.hide_value = True

    # Socket Zone 4 Scratch Amount
    zone_4_scratch_amount_socket = hims.interface.new_socket(
        name="Zone 4 Scratch Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_4_panel,
    )
    zone_4_scratch_amount_socket.subtype = "NONE"
    zone_4_scratch_amount_socket.default_value = 0.800000011920929
    zone_4_scratch_amount_socket.min_value = 0.0
    zone_4_scratch_amount_socket.max_value = 2.0
    zone_4_scratch_amount_socket.attribute_domain = "POINT"

    # Socket Zone 4 Scratch Metallic
    zone_4_scratch_metallic_socket = hims.interface.new_socket(
        name="Zone 4 Scratch Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_4_panel,
    )
    zone_4_scratch_metallic_socket.subtype = "NONE"
    zone_4_scratch_metallic_socket.default_value = 1.0
    zone_4_scratch_metallic_socket.min_value = 0.0
    zone_4_scratch_metallic_socket.max_value = 1.0
    zone_4_scratch_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 4 Scratch Roughness
    zone_4_scratch_roughness_socket = hims.interface.new_socket(
        name="Zone 4 Scratch Roughness",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_4_panel,
    )
    zone_4_scratch_roughness_socket.subtype = "NONE"
    zone_4_scratch_roughness_socket.default_value = 0.4000000059604645
    zone_4_scratch_roughness_socket.min_value = 0.0
    zone_4_scratch_roughness_socket.max_value = 1.0
    zone_4_scratch_roughness_socket.attribute_domain = "POINT"

    # Socket Zone 4 Metallic
    zone_4_metallic_socket = hims.interface.new_socket(
        name="Zone 4 Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_4_panel,
    )
    zone_4_metallic_socket.subtype = "NONE"
    zone_4_metallic_socket.default_value = 0.0
    zone_4_metallic_socket.min_value = 0.0
    zone_4_metallic_socket.max_value = 1.0
    zone_4_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 4 SSS Amount
    zone_4_sss_amount_socket = hims.interface.new_socket(
        name="Zone 4 SSS Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_4_panel,
    )
    zone_4_sss_amount_socket.subtype = "NONE"
    zone_4_sss_amount_socket.default_value = 0.0
    zone_4_sss_amount_socket.min_value = 0.0
    zone_4_sss_amount_socket.max_value = 1.0
    zone_4_sss_amount_socket.attribute_domain = "POINT"

    # Socket Zone 4 Transparency Amount
    zone_4_transparency_amount_socket = hims.interface.new_socket(
        name="Zone 4 Transparency Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_4_panel,
    )
    zone_4_transparency_amount_socket.subtype = "NONE"
    zone_4_transparency_amount_socket.default_value = 0.0
    zone_4_transparency_amount_socket.min_value = 0.0
    zone_4_transparency_amount_socket.max_value = 1.0
    zone_4_transparency_amount_socket.attribute_domain = "POINT"

    # Socket Zone 4 Emmisive Amount
    zone_4_emmisive_amount_socket = hims.interface.new_socket(
        name="Zone 4 Emmisive Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_4_panel,
    )
    zone_4_emmisive_amount_socket.subtype = "NONE"
    zone_4_emmisive_amount_socket.default_value = 0.0
    zone_4_emmisive_amount_socket.min_value = 0.0
    zone_4_emmisive_amount_socket.max_value = 100.0
    zone_4_emmisive_amount_socket.attribute_domain = "POINT"

    # Socket Zone 4 Top
    zone_4_top_socket = hims.interface.new_socket(
        name="Zone 4 Top",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_4_panel,
    )
    zone_4_top_socket.attribute_domain = "POINT"

    # Socket Zone 4 Mid
    zone_4_mid_socket = hims.interface.new_socket(
        name="Zone 4 Mid",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_4_panel,
    )
    zone_4_mid_socket.attribute_domain = "POINT"

    # Socket Zone 4 Bot
    zone_4_bot_socket = hims.interface.new_socket(
        name="Zone 4 Bot",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_4_panel,
    )
    zone_4_bot_socket.attribute_domain = "POINT"

    # Socket Zone 4 Scratch Color
    zone_4_scratch_color_socket = hims.interface.new_socket(
        name="Zone 4 Scratch Color",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_4_panel,
    )
    zone_4_scratch_color_socket.attribute_domain = "POINT"

    # Socket Zone 4 SSS Color
    zone_4_sss_color_socket = hims.interface.new_socket(
        name="Zone 4 SSS Color",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_4_panel,
    )
    zone_4_sss_color_socket.attribute_domain = "POINT"

    # Panel Zone 5
    zone_5_panel = hims.interface.new_panel("Zone 5")
    # Socket Zone 5 Toggle
    zone_5_toggle_socket_1 = hims.interface.new_socket(
        name="Zone 5 Toggle",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_5_panel,
    )
    zone_5_toggle_socket_1.subtype = "NONE"
    zone_5_toggle_socket_1.default_value = 0.0
    zone_5_toggle_socket_1.min_value = 0.0
    zone_5_toggle_socket_1.max_value = 1.0
    zone_5_toggle_socket_1.attribute_domain = "POINT"

    # Socket Zone 5 Gradient Out
    zone_5_gradient_out_socket = hims.interface.new_socket(
        name="Zone 5 Gradient Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_5_panel,
    )
    zone_5_gradient_out_socket.subtype = "FACTOR"
    zone_5_gradient_out_socket.default_value = 0.0
    zone_5_gradient_out_socket.min_value = 0.0
    zone_5_gradient_out_socket.max_value = 1.0
    zone_5_gradient_out_socket.attribute_domain = "POINT"
    zone_5_gradient_out_socket.hide_value = True

    # Socket Zone 5 Rough Out
    zone_5_rough_out_socket = hims.interface.new_socket(
        name="Zone 5 Rough Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_5_panel,
    )
    zone_5_rough_out_socket.subtype = "NONE"
    zone_5_rough_out_socket.default_value = 0.5
    zone_5_rough_out_socket.min_value = 0.0
    zone_5_rough_out_socket.max_value = 1.0
    zone_5_rough_out_socket.attribute_domain = "POINT"
    zone_5_rough_out_socket.hide_value = True

    # Socket Zone 5 Norm Out
    zone_5_norm_out_socket = hims.interface.new_socket(
        name="Zone 5 Norm Out",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_5_panel,
    )
    zone_5_norm_out_socket.attribute_domain = "POINT"
    zone_5_norm_out_socket.hide_value = True

    # Socket Zone 5 Scratch Amount
    zone_5_scratch_amount_socket = hims.interface.new_socket(
        name="Zone 5 Scratch Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_5_panel,
    )
    zone_5_scratch_amount_socket.subtype = "NONE"
    zone_5_scratch_amount_socket.default_value = 0.800000011920929
    zone_5_scratch_amount_socket.min_value = 0.0
    zone_5_scratch_amount_socket.max_value = 2.0
    zone_5_scratch_amount_socket.attribute_domain = "POINT"

    # Socket Zone 5 Scratch Metallic
    zone_5_scratch_metallic_socket = hims.interface.new_socket(
        name="Zone 5 Scratch Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_5_panel,
    )
    zone_5_scratch_metallic_socket.subtype = "NONE"
    zone_5_scratch_metallic_socket.default_value = 1.0
    zone_5_scratch_metallic_socket.min_value = 0.0
    zone_5_scratch_metallic_socket.max_value = 1.0
    zone_5_scratch_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 5 Scratch Roughness
    zone_5_scratch_roughness_socket = hims.interface.new_socket(
        name="Zone 5 Scratch Roughness",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_5_panel,
    )
    zone_5_scratch_roughness_socket.subtype = "NONE"
    zone_5_scratch_roughness_socket.default_value = 0.4000000059604645
    zone_5_scratch_roughness_socket.min_value = 0.0
    zone_5_scratch_roughness_socket.max_value = 1.0
    zone_5_scratch_roughness_socket.attribute_domain = "POINT"

    # Socket Zone 5 Metallic
    zone_5_metallic_socket = hims.interface.new_socket(
        name="Zone 5 Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_5_panel,
    )
    zone_5_metallic_socket.subtype = "NONE"
    zone_5_metallic_socket.default_value = 0.0
    zone_5_metallic_socket.min_value = 0.0
    zone_5_metallic_socket.max_value = 1.0
    zone_5_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 5 SSS Amount
    zone_5_sss_amount_socket = hims.interface.new_socket(
        name="Zone 5 SSS Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_5_panel,
    )
    zone_5_sss_amount_socket.subtype = "NONE"
    zone_5_sss_amount_socket.default_value = 0.0
    zone_5_sss_amount_socket.min_value = 0.0
    zone_5_sss_amount_socket.max_value = 1.0
    zone_5_sss_amount_socket.attribute_domain = "POINT"

    # Socket Zone 5 Transparency Amount
    zone_5_transparency_amount_socket = hims.interface.new_socket(
        name="Zone 5 Transparency Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_5_panel,
    )
    zone_5_transparency_amount_socket.subtype = "NONE"
    zone_5_transparency_amount_socket.default_value = 0.0
    zone_5_transparency_amount_socket.min_value = 0.0
    zone_5_transparency_amount_socket.max_value = 1.0
    zone_5_transparency_amount_socket.attribute_domain = "POINT"

    # Socket Zone 5 Emmisive Amount
    zone_5_emmisive_amount_socket = hims.interface.new_socket(
        name="Zone 5 Emmisive Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_5_panel,
    )
    zone_5_emmisive_amount_socket.subtype = "NONE"
    zone_5_emmisive_amount_socket.default_value = 0.0
    zone_5_emmisive_amount_socket.min_value = 0.0
    zone_5_emmisive_amount_socket.max_value = 100.0
    zone_5_emmisive_amount_socket.attribute_domain = "POINT"

    # Socket Zone 5 Top
    zone_5_top_socket = hims.interface.new_socket(
        name="Zone 5 Top",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_5_panel,
    )
    zone_5_top_socket.attribute_domain = "POINT"

    # Socket Zone 5 Mid
    zone_5_mid_socket = hims.interface.new_socket(
        name="Zone 5 Mid",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_5_panel,
    )
    zone_5_mid_socket.attribute_domain = "POINT"

    # Socket Zone 5 Bot
    zone_5_bot_socket = hims.interface.new_socket(
        name="Zone 5 Bot",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_5_panel,
    )
    zone_5_bot_socket.attribute_domain = "POINT"

    # Socket Zone 5 Scratch Color
    zone_5_scratch_color_socket = hims.interface.new_socket(
        name="Zone 5 Scratch Color",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_5_panel,
    )
    zone_5_scratch_color_socket.attribute_domain = "POINT"

    # Socket Zone 5 SSS Color
    zone_5_sss_color_socket = hims.interface.new_socket(
        name="Zone 5 SSS Color",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_5_panel,
    )
    zone_5_sss_color_socket.attribute_domain = "POINT"

    # Panel Zone 6
    zone_6_panel = hims.interface.new_panel("Zone 6")
    # Socket Zone 6 Toggle
    zone_6_toggle_socket_1 = hims.interface.new_socket(
        name="Zone 6 Toggle",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_6_panel,
    )
    zone_6_toggle_socket_1.subtype = "NONE"
    zone_6_toggle_socket_1.default_value = 0.0
    zone_6_toggle_socket_1.min_value = 0.0
    zone_6_toggle_socket_1.max_value = 1.0
    zone_6_toggle_socket_1.attribute_domain = "POINT"

    # Socket Zone 6 Gradient Out
    zone_6_gradient_out_socket = hims.interface.new_socket(
        name="Zone 6 Gradient Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_6_panel,
    )
    zone_6_gradient_out_socket.subtype = "FACTOR"
    zone_6_gradient_out_socket.default_value = 0.0
    zone_6_gradient_out_socket.min_value = 0.0
    zone_6_gradient_out_socket.max_value = 1.0
    zone_6_gradient_out_socket.attribute_domain = "POINT"
    zone_6_gradient_out_socket.hide_value = True

    # Socket Zone 6 Rough Out
    zone_6_rough_out_socket = hims.interface.new_socket(
        name="Zone 6 Rough Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_6_panel,
    )
    zone_6_rough_out_socket.subtype = "FACTOR"
    zone_6_rough_out_socket.default_value = 0.5
    zone_6_rough_out_socket.min_value = 0.0
    zone_6_rough_out_socket.max_value = 1.0
    zone_6_rough_out_socket.attribute_domain = "POINT"
    zone_6_rough_out_socket.hide_value = True

    # Socket Zone 6 Norm Out
    zone_6_norm_out_socket = hims.interface.new_socket(
        name="Zone 6 Norm Out",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_6_panel,
    )
    zone_6_norm_out_socket.attribute_domain = "POINT"
    zone_6_norm_out_socket.hide_value = True

    # Socket Zone 6 Scratch Amount
    zone_6_scratch_amount_socket = hims.interface.new_socket(
        name="Zone 6 Scratch Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_6_panel,
    )
    zone_6_scratch_amount_socket.subtype = "NONE"
    zone_6_scratch_amount_socket.default_value = 0.800000011920929
    zone_6_scratch_amount_socket.min_value = 0.0
    zone_6_scratch_amount_socket.max_value = 2.0
    zone_6_scratch_amount_socket.attribute_domain = "POINT"

    # Socket Zone 6 Scratch Metallic
    zone_6_scratch_metallic_socket = hims.interface.new_socket(
        name="Zone 6 Scratch Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_6_panel,
    )
    zone_6_scratch_metallic_socket.subtype = "NONE"
    zone_6_scratch_metallic_socket.default_value = 1.0
    zone_6_scratch_metallic_socket.min_value = 0.0
    zone_6_scratch_metallic_socket.max_value = 1.0
    zone_6_scratch_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 6 Scratch Roughness
    zone_6_scratch_roughness_socket = hims.interface.new_socket(
        name="Zone 6 Scratch Roughness",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_6_panel,
    )
    zone_6_scratch_roughness_socket.subtype = "NONE"
    zone_6_scratch_roughness_socket.default_value = 0.4000000059604645
    zone_6_scratch_roughness_socket.min_value = 0.0
    zone_6_scratch_roughness_socket.max_value = 1.0
    zone_6_scratch_roughness_socket.attribute_domain = "POINT"

    # Socket Zone 6 Metallic
    zone_6_metallic_socket = hims.interface.new_socket(
        name="Zone 6 Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_6_panel,
    )
    zone_6_metallic_socket.subtype = "NONE"
    zone_6_metallic_socket.default_value = 0.0
    zone_6_metallic_socket.min_value = 0.0
    zone_6_metallic_socket.max_value = 1.0
    zone_6_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 6 SSS Amount
    zone_6_sss_amount_socket = hims.interface.new_socket(
        name="Zone 6 SSS Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_6_panel,
    )
    zone_6_sss_amount_socket.subtype = "NONE"
    zone_6_sss_amount_socket.default_value = 0.0
    zone_6_sss_amount_socket.min_value = 0.0
    zone_6_sss_amount_socket.max_value = 1.0
    zone_6_sss_amount_socket.attribute_domain = "POINT"

    # Socket Zone 6 Transparency Amount
    zone_6_transparency_amount_socket = hims.interface.new_socket(
        name="Zone 6 Transparency Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_6_panel,
    )
    zone_6_transparency_amount_socket.subtype = "NONE"
    zone_6_transparency_amount_socket.default_value = 0.0
    zone_6_transparency_amount_socket.min_value = 0.0
    zone_6_transparency_amount_socket.max_value = 1.0
    zone_6_transparency_amount_socket.attribute_domain = "POINT"

    # Socket Zone 6 Emmisive Amount
    zone_6_emmisive_amount_socket = hims.interface.new_socket(
        name="Zone 6 Emmisive Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_6_panel,
    )
    zone_6_emmisive_amount_socket.subtype = "NONE"
    zone_6_emmisive_amount_socket.default_value = 0.0
    zone_6_emmisive_amount_socket.min_value = 0.0
    zone_6_emmisive_amount_socket.max_value = 100.0
    zone_6_emmisive_amount_socket.attribute_domain = "POINT"

    # Socket Zone 6 Top
    zone_6_top_socket = hims.interface.new_socket(
        name="Zone 6 Top",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_6_panel,
    )
    zone_6_top_socket.attribute_domain = "POINT"

    # Socket Zone 6 Mid
    zone_6_mid_socket = hims.interface.new_socket(
        name="Zone 6 Mid",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_6_panel,
    )
    zone_6_mid_socket.attribute_domain = "POINT"

    # Socket Zone 6 Bot
    zone_6_bot_socket = hims.interface.new_socket(
        name="Zone 6 Bot",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_6_panel,
    )
    zone_6_bot_socket.attribute_domain = "POINT"

    # Socket Zone 6 Scratch Color
    zone_6_scratch_color_socket = hims.interface.new_socket(
        name="Zone 6 Scratch Color",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_6_panel,
    )
    zone_6_scratch_color_socket.attribute_domain = "POINT"

    # Socket Zone 6 SSS Color
    zone_6_sss_color_socket = hims.interface.new_socket(
        name="Zone 6 SSS Color",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_6_panel,
    )
    zone_6_sss_color_socket.attribute_domain = "POINT"

    # Panel Zone 7
    zone_7_panel = hims.interface.new_panel("Zone 7")
    # Socket Zone 7 Toggle
    zone_7_toggle_socket_1 = hims.interface.new_socket(
        name="Zone 7 Toggle",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_7_panel,
    )
    zone_7_toggle_socket_1.subtype = "NONE"
    zone_7_toggle_socket_1.default_value = 0.0
    zone_7_toggle_socket_1.min_value = 0.0
    zone_7_toggle_socket_1.max_value = 1.0
    zone_7_toggle_socket_1.attribute_domain = "POINT"

    # Socket Zone 7 Gradient Out
    zone_7_gradient_out_socket = hims.interface.new_socket(
        name="Zone 7 Gradient Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_7_panel,
    )
    zone_7_gradient_out_socket.subtype = "FACTOR"
    zone_7_gradient_out_socket.default_value = 0.0
    zone_7_gradient_out_socket.min_value = 0.0
    zone_7_gradient_out_socket.max_value = 1.0
    zone_7_gradient_out_socket.attribute_domain = "POINT"
    zone_7_gradient_out_socket.hide_value = True

    # Socket Zone 7 Rough Out
    zone_7_rough_out_socket = hims.interface.new_socket(
        name="Zone 7 Rough Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_7_panel,
    )
    zone_7_rough_out_socket.subtype = "FACTOR"
    zone_7_rough_out_socket.default_value = 0.800000011920929
    zone_7_rough_out_socket.min_value = 0.0
    zone_7_rough_out_socket.max_value = 1.0
    zone_7_rough_out_socket.attribute_domain = "POINT"
    zone_7_rough_out_socket.hide_value = True

    # Socket Zone 7 Norm Out
    zone_7_norm_out_socket = hims.interface.new_socket(
        name="Zone 7 Norm Out",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_7_panel,
    )
    zone_7_norm_out_socket.attribute_domain = "POINT"
    zone_7_norm_out_socket.hide_value = True

    # Socket Zone 7 Scratch Amount
    zone_7_scratch_amount_socket = hims.interface.new_socket(
        name="Zone 7 Scratch Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_7_panel,
    )
    zone_7_scratch_amount_socket.subtype = "NONE"
    zone_7_scratch_amount_socket.default_value = 0.800000011920929
    zone_7_scratch_amount_socket.min_value = 0.0
    zone_7_scratch_amount_socket.max_value = 2.0
    zone_7_scratch_amount_socket.attribute_domain = "POINT"

    # Socket Zone 7 Scratch Metallic
    zone_7_scratch_metallic_socket = hims.interface.new_socket(
        name="Zone 7 Scratch Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_7_panel,
    )
    zone_7_scratch_metallic_socket.subtype = "NONE"
    zone_7_scratch_metallic_socket.default_value = 0.0
    zone_7_scratch_metallic_socket.min_value = 0.0
    zone_7_scratch_metallic_socket.max_value = 1.0
    zone_7_scratch_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 7 Scratch Roughness
    zone_7_scratch_roughness_socket = hims.interface.new_socket(
        name="Zone 7 Scratch Roughness",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_7_panel,
    )
    zone_7_scratch_roughness_socket.subtype = "NONE"
    zone_7_scratch_roughness_socket.default_value = 0.8999999761581421
    zone_7_scratch_roughness_socket.min_value = 0.0
    zone_7_scratch_roughness_socket.max_value = 1.0
    zone_7_scratch_roughness_socket.attribute_domain = "POINT"

    # Socket Zone 7 Metallic
    zone_7_metallic_socket = hims.interface.new_socket(
        name="Zone 7 Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_7_panel,
    )
    zone_7_metallic_socket.subtype = "NONE"
    zone_7_metallic_socket.default_value = 0.0
    zone_7_metallic_socket.min_value = 0.0
    zone_7_metallic_socket.max_value = 1.0
    zone_7_metallic_socket.attribute_domain = "POINT"

    # Socket Zone 7 SSS Amount
    zone_7_sss_amount_socket = hims.interface.new_socket(
        name="Zone 7 SSS Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_7_panel,
    )
    zone_7_sss_amount_socket.subtype = "NONE"
    zone_7_sss_amount_socket.default_value = 0.0
    zone_7_sss_amount_socket.min_value = 0.0
    zone_7_sss_amount_socket.max_value = 1.0
    zone_7_sss_amount_socket.attribute_domain = "POINT"

    # Socket Zone 7 Transparency Amount
    zone_7_transparency_amount_socket = hims.interface.new_socket(
        name="Zone 7 Transparency Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_7_panel,
    )
    zone_7_transparency_amount_socket.subtype = "NONE"
    zone_7_transparency_amount_socket.default_value = 0.0
    zone_7_transparency_amount_socket.min_value = 0.0
    zone_7_transparency_amount_socket.max_value = 1.0
    zone_7_transparency_amount_socket.attribute_domain = "POINT"

    # Socket Zone 7 Emissive Amount
    zone_7_emissive_amount_socket = hims.interface.new_socket(
        name="Zone 7 Emissive Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=zone_7_panel,
    )
    zone_7_emissive_amount_socket.subtype = "NONE"
    zone_7_emissive_amount_socket.default_value = 0.0
    zone_7_emissive_amount_socket.min_value = 0.0
    zone_7_emissive_amount_socket.max_value = 100.0
    zone_7_emissive_amount_socket.attribute_domain = "POINT"

    # Socket Zone 7 Top
    zone_7_top_socket = hims.interface.new_socket(
        name="Zone 7 Top",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_7_panel,
    )
    zone_7_top_socket.attribute_domain = "POINT"

    # Socket Zone 7 Mid
    zone_7_mid_socket = hims.interface.new_socket(
        name="Zone 7 Mid",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_7_panel,
    )
    zone_7_mid_socket.attribute_domain = "POINT"

    # Socket Zone 7 Bot
    zone_7_bot_socket = hims.interface.new_socket(
        name="Zone 7 Bot",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_7_panel,
    )
    zone_7_bot_socket.attribute_domain = "POINT"

    # Socket Zone 7 Scratch Color
    zone_7_scratch_color_socket = hims.interface.new_socket(
        name="Zone 7 Scratch Color",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_7_panel,
    )
    zone_7_scratch_color_socket.attribute_domain = "POINT"

    # Socket Zone 7 SSS Color
    zone_7_sss_color_socket = hims.interface.new_socket(
        name="Zone 7 SSS Color",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=zone_7_panel,
    )
    zone_7_sss_color_socket.attribute_domain = "POINT"

    # Panel Grime
    grime_panel = hims.interface.new_panel("Grime")
    # Socket Grime Gradient Out
    grime_gradient_out_socket = hims.interface.new_socket(
        name="Grime Gradient Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=grime_panel,
    )
    grime_gradient_out_socket.subtype = "FACTOR"
    grime_gradient_out_socket.default_value = 0.0
    grime_gradient_out_socket.min_value = 0.0
    grime_gradient_out_socket.max_value = 1.0
    grime_gradient_out_socket.attribute_domain = "POINT"
    grime_gradient_out_socket.hide_value = True

    # Socket Grime Rough Out
    grime_rough_out_socket = hims.interface.new_socket(
        name="Grime Rough Out",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=grime_panel,
    )
    grime_rough_out_socket.subtype = "FACTOR"
    grime_rough_out_socket.default_value = 0.800000011920929
    grime_rough_out_socket.min_value = 0.0
    grime_rough_out_socket.max_value = 1.0
    grime_rough_out_socket.attribute_domain = "POINT"
    grime_rough_out_socket.hide_value = True

    # Socket Grime Norm Out
    grime_norm_out_socket = hims.interface.new_socket(
        name="Grime Norm Out",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=grime_panel,
    )
    grime_norm_out_socket.attribute_domain = "POINT"
    grime_norm_out_socket.hide_value = True

    # Socket Grime Metallic
    grime_metallic_socket = hims.interface.new_socket(
        name="Grime Metallic",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=grime_panel,
    )
    grime_metallic_socket.subtype = "NONE"
    grime_metallic_socket.default_value = 0.0
    grime_metallic_socket.min_value = 0.0
    grime_metallic_socket.max_value = 1.0
    grime_metallic_socket.attribute_domain = "POINT"

    # Socket Grime SSS Amount
    grime_sss_amount_socket = hims.interface.new_socket(
        name="Grime SSS Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=grime_panel,
    )
    grime_sss_amount_socket.subtype = "NONE"
    grime_sss_amount_socket.default_value = 0.0
    grime_sss_amount_socket.min_value = 0.0
    grime_sss_amount_socket.max_value = 1.0
    grime_sss_amount_socket.attribute_domain = "POINT"

    # Socket Grime Transparency Amount
    grime_transparency_amount_socket = hims.interface.new_socket(
        name="Grime Transparency Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=grime_panel,
    )
    grime_transparency_amount_socket.subtype = "NONE"
    grime_transparency_amount_socket.default_value = 0.0
    grime_transparency_amount_socket.min_value = 0.0
    grime_transparency_amount_socket.max_value = 1.0
    grime_transparency_amount_socket.attribute_domain = "POINT"

    # Socket Grime Emissive Amount
    grime_emissive_amount_socket = hims.interface.new_socket(
        name="Grime Emissive Amount",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=grime_panel,
    )
    grime_emissive_amount_socket.subtype = "NONE"
    grime_emissive_amount_socket.default_value = 0.0
    grime_emissive_amount_socket.min_value = 0.0
    grime_emissive_amount_socket.max_value = 100.0
    grime_emissive_amount_socket.attribute_domain = "POINT"

    # Socket Grime TopColor
    grime_topcolor_socket = hims.interface.new_socket(
        name="Grime TopColor",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=grime_panel,
    )
    grime_topcolor_socket.attribute_domain = "POINT"

    # Socket Grime MidColor
    grime_midcolor_socket = hims.interface.new_socket(
        name="Grime MidColor",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=grime_panel,
    )
    grime_midcolor_socket.attribute_domain = "POINT"

    # Socket Grime BotColor
    grime_botcolor_socket = hims.interface.new_socket(
        name="Grime BotColor",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=grime_panel,
    )
    grime_botcolor_socket.attribute_domain = "POINT"

    # Socket Grime SSS Color
    grime_sss_color_socket = hims.interface.new_socket(
        name="Grime SSS Color",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=grime_panel,
    )
    grime_sss_color_socket.attribute_domain = "POINT"

    # Panel Color Overrides
    color_overrides_panel = hims.interface.new_panel("Color Overrides")
    # Socket Color Override
    color_override_socket_1 = hims.interface.new_socket(
        name="Color Override",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=color_overrides_panel,
    )
    color_override_socket_1.attribute_domain = "POINT"

    # Socket Color Override Toggle
    color_override_toggle_socket_1 = hims.interface.new_socket(
        name="Color Override Toggle",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=color_overrides_panel,
    )
    color_override_toggle_socket_1.subtype = "NONE"
    color_override_toggle_socket_1.default_value = 0.0
    color_override_toggle_socket_1.min_value = 0.0
    color_override_toggle_socket_1.max_value = 1.0
    color_override_toggle_socket_1.attribute_domain = "POINT"
    color_override_toggle_socket_1.hide_value = True

    # initialize hims nodes
    # node Separate RGB
    separate_rgb_4 = hims.nodes.new("ShaderNodeSeparateColor")
    separate_rgb_4.name = "Separate RGB"
    separate_rgb_4.mode = "RGB"

    # node Math.002
    math_002_3 = hims.nodes.new("ShaderNodeMath")
    math_002_3.name = "Math.002"
    math_002_3.operation = "MULTIPLY"
    math_002_3.use_clamp = False
    math_002_3.inputs[2].hide = True
    # Value_002
    math_002_3.inputs[2].default_value = 0.5

    # node Math.004
    math_004_4 = hims.nodes.new("ShaderNodeMath")
    math_004_4.name = "Math.004"
    math_004_4.operation = "MULTIPLY"
    math_004_4.use_clamp = True
    math_004_4.inputs[2].hide = True
    # Value_002
    math_004_4.inputs[2].default_value = 0.5

    # node Math.005
    math_005_4 = hims.nodes.new("ShaderNodeMath")
    math_005_4.name = "Math.005"
    math_005_4.operation = "MULTIPLY"
    math_005_4.use_clamp = False
    math_005_4.inputs[2].hide = True
    # Value_002
    math_005_4.inputs[2].default_value = 0.5

    # node Math.003
    math_003_2 = hims.nodes.new("ShaderNodeMath")
    math_003_2.name = "Math.003"
    math_003_2.operation = "MULTIPLY"
    math_003_2.use_clamp = False
    math_003_2.inputs[2].hide = True
    # Value_002
    math_003_2.inputs[2].default_value = 0.5

    # node Normal Map
    normal_map = hims.nodes.new("ShaderNodeNormalMap")
    normal_map.name = "Normal Map"
    normal_map.space = "TANGENT"
    normal_map.uv_map = ""
    normal_map.inputs[0].hide = True
    # Strength
    normal_map.inputs[0].default_value = 1.0

    # node Reroute.002
    reroute_002_4 = hims.nodes.new("NodeReroute")
    reroute_002_4.name = "Reroute.002"
    # node Reroute.011
    reroute_011_3 = hims.nodes.new("NodeReroute")
    reroute_011_3.name = "Reroute.011"
    # node Reroute.010
    reroute_010_3 = hims.nodes.new("NodeReroute")
    reroute_010_3.name = "Reroute.010"
    # node Reroute.014
    reroute_014_3 = hims.nodes.new("NodeReroute")
    reroute_014_3.name = "Reroute.014"
    # node Reroute.015
    reroute_015_3 = hims.nodes.new("NodeReroute")
    reroute_015_3.name = "Reroute.015"
    # node Reroute.018
    reroute_018_3 = hims.nodes.new("NodeReroute")
    reroute_018_3.name = "Reroute.018"
    # node Reroute.003
    reroute_003_1 = hims.nodes.new("NodeReroute")
    reroute_003_1.name = "Reroute.003"
    # node Reroute.021
    reroute_021 = hims.nodes.new("NodeReroute")
    reroute_021.name = "Reroute.021"
    # node Invert
    invert = hims.nodes.new("ShaderNodeInvert")
    invert.name = "Invert"
    invert.inputs[0].hide = True
    # Fac
    invert.inputs[0].default_value = 1.0

    # node Reroute.023
    reroute_023 = hims.nodes.new("NodeReroute")
    reroute_023.name = "Reroute.023"
    # node Reroute.020
    reroute_020 = hims.nodes.new("NodeReroute")
    reroute_020.name = "Reroute.020"
    # node Reroute.026
    reroute_026 = hims.nodes.new("NodeReroute")
    reroute_026.name = "Reroute.026"
    # node Reroute.027
    reroute_027 = hims.nodes.new("NodeReroute")
    reroute_027.name = "Reroute.027"
    # node Reroute.028
    reroute_028 = hims.nodes.new("NodeReroute")
    reroute_028.name = "Reroute.028"
    # node Reroute.019
    reroute_019_3 = hims.nodes.new("NodeReroute")
    reroute_019_3.name = "Reroute.019"
    # node Reroute.025
    reroute_025 = hims.nodes.new("NodeReroute")
    reroute_025.name = "Reroute.025"
    # node Reroute.013
    reroute_013_3 = hims.nodes.new("NodeReroute")
    reroute_013_3.name = "Reroute.013"
    # node Reroute.022
    reroute_022 = hims.nodes.new("NodeReroute")
    reroute_022.name = "Reroute.022"
    # node Reroute.032
    reroute_032 = hims.nodes.new("NodeReroute")
    reroute_032.name = "Reroute.032"
    # node Reroute.033
    reroute_033 = hims.nodes.new("NodeReroute")
    reroute_033.name = "Reroute.033"
    # node Reroute.034
    reroute_034 = hims.nodes.new("NodeReroute")
    reroute_034.name = "Reroute.034"
    # node Reroute.035
    reroute_035 = hims.nodes.new("NodeReroute")
    reroute_035.name = "Reroute.035"
    # node Reroute.037
    reroute_037 = hims.nodes.new("NodeReroute")
    reroute_037.name = "Reroute.037"
    # node Reroute.016
    reroute_016_3 = hims.nodes.new("NodeReroute")
    reroute_016_3.name = "Reroute.016"
    # node Reroute.040
    reroute_040 = hims.nodes.new("NodeReroute")
    reroute_040.name = "Reroute.040"
    # node Reroute.045
    reroute_045 = hims.nodes.new("NodeReroute")
    reroute_045.name = "Reroute.045"
    # node Reroute.047
    reroute_047 = hims.nodes.new("NodeReroute")
    reroute_047.name = "Reroute.047"
    # node Reroute.050
    reroute_050 = hims.nodes.new("NodeReroute")
    reroute_050.name = "Reroute.050"
    # node Reroute.049
    reroute_049 = hims.nodes.new("NodeReroute")
    reroute_049.name = "Reroute.049"
    # node Reroute.012
    reroute_012 = hims.nodes.new("NodeReroute")
    reroute_012.name = "Reroute.012"
    # node Reroute.051
    reroute_051 = hims.nodes.new("NodeReroute")
    reroute_051.name = "Reroute.051"
    # node Reroute.053
    reroute_053 = hims.nodes.new("NodeReroute")
    reroute_053.name = "Reroute.053"
    # node Reroute.024
    reroute_024 = hims.nodes.new("NodeReroute")
    reroute_024.name = "Reroute.024"
    # node Reroute.029
    reroute_029 = hims.nodes.new("NodeReroute")
    reroute_029.name = "Reroute.029"
    # node Reroute.030
    reroute_030 = hims.nodes.new("NodeReroute")
    reroute_030.name = "Reroute.030"
    # node Reroute.054
    reroute_054 = hims.nodes.new("NodeReroute")
    reroute_054.name = "Reroute.054"
    # node Reroute.055
    reroute_055 = hims.nodes.new("NodeReroute")
    reroute_055.name = "Reroute.055"
    # node Reroute.057
    reroute_057 = hims.nodes.new("NodeReroute")
    reroute_057.name = "Reroute.057"
    # node Reroute.056
    reroute_056 = hims.nodes.new("NodeReroute")
    reroute_056.name = "Reroute.056"
    # node Reroute.060
    reroute_060 = hims.nodes.new("NodeReroute")
    reroute_060.name = "Reroute.060"
    # node Reroute.061
    reroute_061 = hims.nodes.new("NodeReroute")
    reroute_061.name = "Reroute.061"
    # node Reroute.059
    reroute_059 = hims.nodes.new("NodeReroute")
    reroute_059.name = "Reroute.059"
    # node Reroute.006
    reroute_006_3 = hims.nodes.new("NodeReroute")
    reroute_006_3.name = "Reroute.006"
    # node Reroute.063
    reroute_063 = hims.nodes.new("NodeReroute")
    reroute_063.name = "Reroute.063"
    # node Reroute.065
    reroute_065 = hims.nodes.new("NodeReroute")
    reroute_065.name = "Reroute.065"
    # node Reroute.064
    reroute_064 = hims.nodes.new("NodeReroute")
    reroute_064.name = "Reroute.064"
    # node Reroute.031
    reroute_031 = hims.nodes.new("NodeReroute")
    reroute_031.name = "Reroute.031"
    # node Reroute.004
    reroute_004_4 = hims.nodes.new("NodeReroute")
    reroute_004_4.name = "Reroute.004"
    # node Reroute.039
    reroute_039 = hims.nodes.new("NodeReroute")
    reroute_039.name = "Reroute.039"
    # node Reroute.042
    reroute_042 = hims.nodes.new("NodeReroute")
    reroute_042.name = "Reroute.042"
    # node Reroute
    reroute_1 = hims.nodes.new("NodeReroute")
    reroute_1.name = "Reroute"
    # node Reroute.001
    reroute_001_4 = hims.nodes.new("NodeReroute")
    reroute_001_4.name = "Reroute.001"
    # node Reroute.041
    reroute_041 = hims.nodes.new("NodeReroute")
    reroute_041.name = "Reroute.041"
    # node Reroute.043
    reroute_043 = hims.nodes.new("NodeReroute")
    reroute_043.name = "Reroute.043"
    # node Reroute.044
    reroute_044 = hims.nodes.new("NodeReroute")
    reroute_044.name = "Reroute.044"
    # node Reroute.062
    reroute_062 = hims.nodes.new("NodeReroute")
    reroute_062.name = "Reroute.062"
    # node Group.008
    group_008: ShaderNodeGroup = hims.nodes.new("ShaderNodeGroup")
    group_008.label = "Zone 3"
    group_008.name = "Group.008"
    group_008.node_tree = ColorMixer().node_tree

    # node Group Input.009
    group_input_009 = hims.nodes.new("NodeGroupInput")
    group_input_009.label = "Slot 3"
    group_input_009.name = "Group Input.009"
    group_input_009.use_custom_color = True
    group_input_009.color = (0.0, 0.5, 0.0)
    group_input_009.outputs[0].hide = True
    group_input_009.outputs[1].hide = True
    group_input_009.outputs[2].hide = True
    group_input_009.outputs[3].hide = True
    group_input_009.outputs[4].hide = True
    group_input_009.outputs[5].hide = True
    group_input_009.outputs[6].hide = True
    group_input_009.outputs[7].hide = True
    group_input_009.outputs[8].hide = True
    group_input_009.outputs[9].hide = True
    group_input_009.outputs[10].hide = True
    group_input_009.outputs[11].hide = True
    group_input_009.outputs[12].hide = True
    group_input_009.outputs[13].hide = True
    group_input_009.outputs[14].hide = True
    group_input_009.outputs[15].hide = True
    group_input_009.outputs[16].hide = True
    group_input_009.outputs[17].hide = True
    group_input_009.outputs[18].hide = True
    group_input_009.outputs[19].hide = True
    group_input_009.outputs[20].hide = True
    group_input_009.outputs[21].hide = True
    group_input_009.outputs[22].hide = True
    group_input_009.outputs[23].hide = True
    group_input_009.outputs[24].hide = True
    group_input_009.outputs[25].hide = True
    group_input_009.outputs[26].hide = True
    group_input_009.outputs[27].hide = True
    group_input_009.outputs[28].hide = True
    group_input_009.outputs[29].hide = True
    group_input_009.outputs[30].hide = True
    group_input_009.outputs[31].hide = True
    group_input_009.outputs[32].hide = True
    group_input_009.outputs[33].hide = True
    group_input_009.outputs[34].hide = True
    group_input_009.outputs[35].hide = True
    group_input_009.outputs[36].hide = True
    group_input_009.outputs[37].hide = True
    group_input_009.outputs[38].hide = True
    group_input_009.outputs[39].hide = True
    group_input_009.outputs[40].hide = True
    group_input_009.outputs[41].hide = True
    group_input_009.outputs[42].hide = True
    group_input_009.outputs[44].hide = True
    group_input_009.outputs[45].hide = True
    group_input_009.outputs[46].hide = True
    group_input_009.outputs[47].hide = True
    group_input_009.outputs[48].hide = True
    group_input_009.outputs[49].hide = True
    group_input_009.outputs[50].hide = True
    group_input_009.outputs[51].hide = True
    group_input_009.outputs[52].hide = True
    group_input_009.outputs[56].hide = True
    group_input_009.outputs[57].hide = True
    group_input_009.outputs[58].hide = True
    group_input_009.outputs[59].hide = True
    group_input_009.outputs[60].hide = True
    group_input_009.outputs[61].hide = True
    group_input_009.outputs[62].hide = True
    group_input_009.outputs[63].hide = True
    group_input_009.outputs[64].hide = True
    group_input_009.outputs[65].hide = True
    group_input_009.outputs[66].hide = True
    group_input_009.outputs[67].hide = True
    group_input_009.outputs[68].hide = True
    group_input_009.outputs[69].hide = True
    group_input_009.outputs[70].hide = True
    group_input_009.outputs[71].hide = True
    group_input_009.outputs[72].hide = True
    group_input_009.outputs[73].hide = True
    group_input_009.outputs[74].hide = True
    group_input_009.outputs[75].hide = True
    group_input_009.outputs[76].hide = True
    group_input_009.outputs[77].hide = True
    group_input_009.outputs[78].hide = True
    group_input_009.outputs[79].hide = True
    group_input_009.outputs[80].hide = True
    group_input_009.outputs[81].hide = True
    group_input_009.outputs[82].hide = True
    group_input_009.outputs[83].hide = True
    group_input_009.outputs[84].hide = True
    group_input_009.outputs[85].hide = True
    group_input_009.outputs[86].hide = True
    group_input_009.outputs[87].hide = True
    group_input_009.outputs[88].hide = True
    group_input_009.outputs[89].hide = True
    group_input_009.outputs[90].hide = True
    group_input_009.outputs[91].hide = True
    group_input_009.outputs[92].hide = True
    group_input_009.outputs[93].hide = True
    group_input_009.outputs[94].hide = True
    group_input_009.outputs[95].hide = True
    group_input_009.outputs[96].hide = True
    group_input_009.outputs[97].hide = True
    group_input_009.outputs[98].hide = True
    group_input_009.outputs[99].hide = True
    group_input_009.outputs[100].hide = True
    group_input_009.outputs[101].hide = True
    group_input_009.outputs[102].hide = True
    group_input_009.outputs[103].hide = True
    group_input_009.outputs[104].hide = True
    group_input_009.outputs[105].hide = True
    group_input_009.outputs[106].hide = True
    group_input_009.outputs[107].hide = True
    group_input_009.outputs[108].hide = True
    group_input_009.outputs[109].hide = True
    group_input_009.outputs[110].hide = True
    group_input_009.outputs[111].hide = True
    group_input_009.outputs[112].hide = True
    group_input_009.outputs[113].hide = True
    group_input_009.outputs[114].hide = True
    group_input_009.outputs[115].hide = True
    group_input_009.outputs[116].hide = True
    group_input_009.outputs[117].hide = True
    group_input_009.outputs[118].hide = True
    group_input_009.outputs[119].hide = True
    group_input_009.outputs[120].hide = True
    group_input_009.outputs[121].hide = True
    group_input_009.outputs[122].hide = True
    group_input_009.outputs[123].hide = True
    group_input_009.outputs[124].hide = True
    group_input_009.outputs[125].hide = True
    group_input_009.outputs[126].hide = True
    group_input_009.outputs[127].hide = True
    group_input_009.outputs[128].hide = True
    group_input_009.outputs[129].hide = True
    group_input_009.outputs[130].hide = True
    group_input_009.outputs[131].hide = True
    group_input_009.outputs[132].hide = True
    group_input_009.outputs[133].hide = True
    group_input_009.outputs[134].hide = True
    group_input_009.outputs[135].hide = True

    # node Group Input.004
    group_input_004 = hims.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.outputs[1].hide = True
    group_input_004.outputs[2].hide = True
    group_input_004.outputs[3].hide = True
    group_input_004.outputs[4].hide = True
    group_input_004.outputs[5].hide = True
    group_input_004.outputs[6].hide = True
    group_input_004.outputs[7].hide = True
    group_input_004.outputs[8].hide = True
    group_input_004.outputs[9].hide = True
    group_input_004.outputs[10].hide = True
    group_input_004.outputs[11].hide = True
    group_input_004.outputs[12].hide = True
    group_input_004.outputs[13].hide = True
    group_input_004.outputs[14].hide = True
    group_input_004.outputs[15].hide = True
    group_input_004.outputs[16].hide = True
    group_input_004.outputs[18].hide = True
    group_input_004.outputs[19].hide = True
    group_input_004.outputs[20].hide = True
    group_input_004.outputs[21].hide = True
    group_input_004.outputs[22].hide = True
    group_input_004.outputs[23].hide = True
    group_input_004.outputs[24].hide = True
    group_input_004.outputs[25].hide = True
    group_input_004.outputs[26].hide = True
    group_input_004.outputs[27].hide = True
    group_input_004.outputs[28].hide = True
    group_input_004.outputs[29].hide = True
    group_input_004.outputs[30].hide = True
    group_input_004.outputs[31].hide = True
    group_input_004.outputs[33].hide = True
    group_input_004.outputs[34].hide = True
    group_input_004.outputs[35].hide = True
    group_input_004.outputs[36].hide = True
    group_input_004.outputs[37].hide = True
    group_input_004.outputs[38].hide = True
    group_input_004.outputs[39].hide = True
    group_input_004.outputs[40].hide = True
    group_input_004.outputs[41].hide = True
    group_input_004.outputs[42].hide = True
    group_input_004.outputs[43].hide = True
    group_input_004.outputs[44].hide = True
    group_input_004.outputs[45].hide = True
    group_input_004.outputs[46].hide = True
    group_input_004.outputs[48].hide = True
    group_input_004.outputs[49].hide = True
    group_input_004.outputs[50].hide = True
    group_input_004.outputs[51].hide = True
    group_input_004.outputs[52].hide = True
    group_input_004.outputs[53].hide = True
    group_input_004.outputs[54].hide = True
    group_input_004.outputs[55].hide = True
    group_input_004.outputs[56].hide = True
    group_input_004.outputs[57].hide = True
    group_input_004.outputs[58].hide = True
    group_input_004.outputs[59].hide = True
    group_input_004.outputs[60].hide = True
    group_input_004.outputs[61].hide = True
    group_input_004.outputs[62].hide = True
    group_input_004.outputs[64].hide = True
    group_input_004.outputs[65].hide = True
    group_input_004.outputs[66].hide = True
    group_input_004.outputs[67].hide = True
    group_input_004.outputs[68].hide = True
    group_input_004.outputs[69].hide = True
    group_input_004.outputs[70].hide = True
    group_input_004.outputs[71].hide = True
    group_input_004.outputs[72].hide = True
    group_input_004.outputs[73].hide = True
    group_input_004.outputs[74].hide = True
    group_input_004.outputs[75].hide = True
    group_input_004.outputs[76].hide = True
    group_input_004.outputs[77].hide = True
    group_input_004.outputs[78].hide = True
    group_input_004.outputs[80].hide = True
    group_input_004.outputs[81].hide = True
    group_input_004.outputs[82].hide = True
    group_input_004.outputs[83].hide = True
    group_input_004.outputs[84].hide = True
    group_input_004.outputs[85].hide = True
    group_input_004.outputs[86].hide = True
    group_input_004.outputs[87].hide = True
    group_input_004.outputs[88].hide = True
    group_input_004.outputs[89].hide = True
    group_input_004.outputs[90].hide = True
    group_input_004.outputs[91].hide = True
    group_input_004.outputs[92].hide = True
    group_input_004.outputs[93].hide = True
    group_input_004.outputs[94].hide = True
    group_input_004.outputs[96].hide = True
    group_input_004.outputs[97].hide = True
    group_input_004.outputs[98].hide = True
    group_input_004.outputs[99].hide = True
    group_input_004.outputs[100].hide = True
    group_input_004.outputs[101].hide = True
    group_input_004.outputs[102].hide = True
    group_input_004.outputs[103].hide = True
    group_input_004.outputs[104].hide = True
    group_input_004.outputs[105].hide = True
    group_input_004.outputs[106].hide = True
    group_input_004.outputs[107].hide = True
    group_input_004.outputs[108].hide = True
    group_input_004.outputs[109].hide = True
    group_input_004.outputs[110].hide = True
    group_input_004.outputs[112].hide = True
    group_input_004.outputs[113].hide = True
    group_input_004.outputs[114].hide = True
    group_input_004.outputs[115].hide = True
    group_input_004.outputs[116].hide = True
    group_input_004.outputs[117].hide = True
    group_input_004.outputs[118].hide = True
    group_input_004.outputs[119].hide = True
    group_input_004.outputs[120].hide = True
    group_input_004.outputs[121].hide = True
    group_input_004.outputs[122].hide = True
    group_input_004.outputs[123].hide = True
    group_input_004.outputs[124].hide = True
    group_input_004.outputs[125].hide = True
    group_input_004.outputs[126].hide = True
    group_input_004.outputs[127].hide = True
    group_input_004.outputs[128].hide = True
    group_input_004.outputs[129].hide = True
    group_input_004.outputs[130].hide = True
    group_input_004.outputs[131].hide = True
    group_input_004.outputs[132].hide = True
    group_input_004.outputs[133].hide = True
    group_input_004.outputs[134].hide = True
    group_input_004.outputs[135].hide = True

    # node Group Input.019
    group_input_019 = hims.nodes.new("NodeGroupInput")
    group_input_019.name = "Group Input.019"
    group_input_019.outputs[1].hide = True
    group_input_019.outputs[2].hide = True
    group_input_019.outputs[3].hide = True
    group_input_019.outputs[4].hide = True
    group_input_019.outputs[5].hide = True
    group_input_019.outputs[6].hide = True
    group_input_019.outputs[7].hide = True
    group_input_019.outputs[8].hide = True
    group_input_019.outputs[9].hide = True
    group_input_019.outputs[10].hide = True
    group_input_019.outputs[11].hide = True
    group_input_019.outputs[13].hide = True
    group_input_019.outputs[14].hide = True
    group_input_019.outputs[15].hide = True
    group_input_019.outputs[17].hide = True
    group_input_019.outputs[18].hide = True
    group_input_019.outputs[19].hide = True
    group_input_019.outputs[20].hide = True
    group_input_019.outputs[21].hide = True
    group_input_019.outputs[22].hide = True
    group_input_019.outputs[23].hide = True
    group_input_019.outputs[24].hide = True
    group_input_019.outputs[25].hide = True
    group_input_019.outputs[26].hide = True
    group_input_019.outputs[27].hide = True
    group_input_019.outputs[28].hide = True
    group_input_019.outputs[29].hide = True
    group_input_019.outputs[30].hide = True
    group_input_019.outputs[32].hide = True
    group_input_019.outputs[33].hide = True
    group_input_019.outputs[34].hide = True
    group_input_019.outputs[35].hide = True
    group_input_019.outputs[36].hide = True
    group_input_019.outputs[37].hide = True
    group_input_019.outputs[38].hide = True
    group_input_019.outputs[39].hide = True
    group_input_019.outputs[40].hide = True
    group_input_019.outputs[41].hide = True
    group_input_019.outputs[42].hide = True
    group_input_019.outputs[43].hide = True
    group_input_019.outputs[44].hide = True
    group_input_019.outputs[45].hide = True
    group_input_019.outputs[47].hide = True
    group_input_019.outputs[48].hide = True
    group_input_019.outputs[49].hide = True
    group_input_019.outputs[50].hide = True
    group_input_019.outputs[51].hide = True
    group_input_019.outputs[52].hide = True
    group_input_019.outputs[53].hide = True
    group_input_019.outputs[54].hide = True
    group_input_019.outputs[55].hide = True
    group_input_019.outputs[56].hide = True
    group_input_019.outputs[57].hide = True
    group_input_019.outputs[58].hide = True
    group_input_019.outputs[59].hide = True
    group_input_019.outputs[60].hide = True
    group_input_019.outputs[61].hide = True
    group_input_019.outputs[63].hide = True
    group_input_019.outputs[64].hide = True
    group_input_019.outputs[65].hide = True
    group_input_019.outputs[66].hide = True
    group_input_019.outputs[67].hide = True
    group_input_019.outputs[68].hide = True
    group_input_019.outputs[69].hide = True
    group_input_019.outputs[70].hide = True
    group_input_019.outputs[71].hide = True
    group_input_019.outputs[72].hide = True
    group_input_019.outputs[73].hide = True
    group_input_019.outputs[74].hide = True
    group_input_019.outputs[75].hide = True
    group_input_019.outputs[76].hide = True
    group_input_019.outputs[77].hide = True
    group_input_019.outputs[79].hide = True
    group_input_019.outputs[80].hide = True
    group_input_019.outputs[81].hide = True
    group_input_019.outputs[82].hide = True
    group_input_019.outputs[83].hide = True
    group_input_019.outputs[84].hide = True
    group_input_019.outputs[85].hide = True
    group_input_019.outputs[86].hide = True
    group_input_019.outputs[87].hide = True
    group_input_019.outputs[88].hide = True
    group_input_019.outputs[89].hide = True
    group_input_019.outputs[90].hide = True
    group_input_019.outputs[91].hide = True
    group_input_019.outputs[92].hide = True
    group_input_019.outputs[93].hide = True
    group_input_019.outputs[95].hide = True
    group_input_019.outputs[96].hide = True
    group_input_019.outputs[97].hide = True
    group_input_019.outputs[98].hide = True
    group_input_019.outputs[99].hide = True
    group_input_019.outputs[100].hide = True
    group_input_019.outputs[101].hide = True
    group_input_019.outputs[102].hide = True
    group_input_019.outputs[103].hide = True
    group_input_019.outputs[104].hide = True
    group_input_019.outputs[105].hide = True
    group_input_019.outputs[106].hide = True
    group_input_019.outputs[107].hide = True
    group_input_019.outputs[108].hide = True
    group_input_019.outputs[109].hide = True
    group_input_019.outputs[111].hide = True
    group_input_019.outputs[112].hide = True
    group_input_019.outputs[113].hide = True
    group_input_019.outputs[114].hide = True
    group_input_019.outputs[115].hide = True
    group_input_019.outputs[116].hide = True
    group_input_019.outputs[117].hide = True
    group_input_019.outputs[118].hide = True
    group_input_019.outputs[119].hide = True
    group_input_019.outputs[120].hide = True
    group_input_019.outputs[121].hide = True
    group_input_019.outputs[122].hide = True
    group_input_019.outputs[123].hide = True
    group_input_019.outputs[124].hide = True
    group_input_019.outputs[125].hide = True
    group_input_019.outputs[126].hide = True
    group_input_019.outputs[127].hide = True
    group_input_019.outputs[128].hide = True
    group_input_019.outputs[129].hide = True
    group_input_019.outputs[130].hide = True
    group_input_019.outputs[131].hide = True
    group_input_019.outputs[132].hide = True
    group_input_019.outputs[133].hide = True
    group_input_019.outputs[134].hide = True
    group_input_019.outputs[135].hide = True

    # node Group Input.006
    group_input_006 = hims.nodes.new("NodeGroupInput")
    group_input_006.name = "Group Input.006"
    group_input_006.outputs[1].hide = True
    group_input_006.outputs[2].hide = True
    group_input_006.outputs[3].hide = True
    group_input_006.outputs[4].hide = True
    group_input_006.outputs[5].hide = True
    group_input_006.outputs[6].hide = True
    group_input_006.outputs[7].hide = True
    group_input_006.outputs[8].hide = True
    group_input_006.outputs[9].hide = True
    group_input_006.outputs[10].hide = True
    group_input_006.outputs[11].hide = True
    group_input_006.outputs[12].hide = True
    group_input_006.outputs[13].hide = True
    group_input_006.outputs[14].hide = True
    group_input_006.outputs[15].hide = True
    group_input_006.outputs[16].hide = True
    group_input_006.outputs[17].hide = True
    group_input_006.outputs[19].hide = True
    group_input_006.outputs[20].hide = True
    group_input_006.outputs[21].hide = True
    group_input_006.outputs[22].hide = True
    group_input_006.outputs[23].hide = True
    group_input_006.outputs[24].hide = True
    group_input_006.outputs[25].hide = True
    group_input_006.outputs[26].hide = True
    group_input_006.outputs[27].hide = True
    group_input_006.outputs[28].hide = True
    group_input_006.outputs[29].hide = True
    group_input_006.outputs[30].hide = True
    group_input_006.outputs[31].hide = True
    group_input_006.outputs[32].hide = True
    group_input_006.outputs[34].hide = True
    group_input_006.outputs[35].hide = True
    group_input_006.outputs[36].hide = True
    group_input_006.outputs[37].hide = True
    group_input_006.outputs[38].hide = True
    group_input_006.outputs[39].hide = True
    group_input_006.outputs[40].hide = True
    group_input_006.outputs[41].hide = True
    group_input_006.outputs[42].hide = True
    group_input_006.outputs[43].hide = True
    group_input_006.outputs[44].hide = True
    group_input_006.outputs[45].hide = True
    group_input_006.outputs[46].hide = True
    group_input_006.outputs[47].hide = True
    group_input_006.outputs[49].hide = True
    group_input_006.outputs[50].hide = True
    group_input_006.outputs[51].hide = True
    group_input_006.outputs[52].hide = True
    group_input_006.outputs[53].hide = True
    group_input_006.outputs[54].hide = True
    group_input_006.outputs[55].hide = True
    group_input_006.outputs[56].hide = True
    group_input_006.outputs[57].hide = True
    group_input_006.outputs[58].hide = True
    group_input_006.outputs[59].hide = True
    group_input_006.outputs[60].hide = True
    group_input_006.outputs[61].hide = True
    group_input_006.outputs[62].hide = True
    group_input_006.outputs[63].hide = True
    group_input_006.outputs[65].hide = True
    group_input_006.outputs[66].hide = True
    group_input_006.outputs[67].hide = True
    group_input_006.outputs[68].hide = True
    group_input_006.outputs[69].hide = True
    group_input_006.outputs[70].hide = True
    group_input_006.outputs[71].hide = True
    group_input_006.outputs[72].hide = True
    group_input_006.outputs[73].hide = True
    group_input_006.outputs[74].hide = True
    group_input_006.outputs[75].hide = True
    group_input_006.outputs[76].hide = True
    group_input_006.outputs[77].hide = True
    group_input_006.outputs[78].hide = True
    group_input_006.outputs[79].hide = True
    group_input_006.outputs[81].hide = True
    group_input_006.outputs[82].hide = True
    group_input_006.outputs[83].hide = True
    group_input_006.outputs[84].hide = True
    group_input_006.outputs[85].hide = True
    group_input_006.outputs[86].hide = True
    group_input_006.outputs[87].hide = True
    group_input_006.outputs[88].hide = True
    group_input_006.outputs[89].hide = True
    group_input_006.outputs[90].hide = True
    group_input_006.outputs[91].hide = True
    group_input_006.outputs[92].hide = True
    group_input_006.outputs[93].hide = True
    group_input_006.outputs[94].hide = True
    group_input_006.outputs[95].hide = True
    group_input_006.outputs[97].hide = True
    group_input_006.outputs[98].hide = True
    group_input_006.outputs[99].hide = True
    group_input_006.outputs[100].hide = True
    group_input_006.outputs[101].hide = True
    group_input_006.outputs[102].hide = True
    group_input_006.outputs[103].hide = True
    group_input_006.outputs[104].hide = True
    group_input_006.outputs[105].hide = True
    group_input_006.outputs[106].hide = True
    group_input_006.outputs[107].hide = True
    group_input_006.outputs[108].hide = True
    group_input_006.outputs[109].hide = True
    group_input_006.outputs[110].hide = True
    group_input_006.outputs[111].hide = True
    group_input_006.outputs[113].hide = True
    group_input_006.outputs[114].hide = True
    group_input_006.outputs[115].hide = True
    group_input_006.outputs[116].hide = True
    group_input_006.outputs[117].hide = True
    group_input_006.outputs[118].hide = True
    group_input_006.outputs[119].hide = True
    group_input_006.outputs[120].hide = True
    group_input_006.outputs[121].hide = True
    group_input_006.outputs[122].hide = True
    group_input_006.outputs[123].hide = True
    group_input_006.outputs[124].hide = True
    group_input_006.outputs[125].hide = True
    group_input_006.outputs[126].hide = True
    group_input_006.outputs[127].hide = True
    group_input_006.outputs[128].hide = True
    group_input_006.outputs[129].hide = True
    group_input_006.outputs[130].hide = True
    group_input_006.outputs[131].hide = True
    group_input_006.outputs[132].hide = True
    group_input_006.outputs[133].hide = True
    group_input_006.outputs[134].hide = True
    group_input_006.outputs[135].hide = True

    # node Group Input.025
    group_input_025 = hims.nodes.new("NodeGroupInput")
    group_input_025.name = "Group Input.025"
    group_input_025.outputs[1].hide = True
    group_input_025.outputs[2].hide = True
    group_input_025.outputs[3].hide = True
    group_input_025.outputs[4].hide = True
    group_input_025.outputs[5].hide = True
    group_input_025.outputs[6].hide = True
    group_input_025.outputs[8].hide = True
    group_input_025.outputs[9].hide = True
    group_input_025.outputs[10].hide = True
    group_input_025.outputs[11].hide = True
    group_input_025.outputs[12].hide = True
    group_input_025.outputs[13].hide = True
    group_input_025.outputs[14].hide = True
    group_input_025.outputs[15].hide = True
    group_input_025.outputs[16].hide = True
    group_input_025.outputs[17].hide = True
    group_input_025.outputs[18].hide = True
    group_input_025.outputs[19].hide = True
    group_input_025.outputs[21].hide = True
    group_input_025.outputs[22].hide = True
    group_input_025.outputs[23].hide = True
    group_input_025.outputs[24].hide = True
    group_input_025.outputs[25].hide = True
    group_input_025.outputs[26].hide = True
    group_input_025.outputs[27].hide = True
    group_input_025.outputs[28].hide = True
    group_input_025.outputs[29].hide = True
    group_input_025.outputs[30].hide = True
    group_input_025.outputs[31].hide = True
    group_input_025.outputs[32].hide = True
    group_input_025.outputs[33].hide = True
    group_input_025.outputs[34].hide = True
    group_input_025.outputs[36].hide = True
    group_input_025.outputs[37].hide = True
    group_input_025.outputs[38].hide = True
    group_input_025.outputs[39].hide = True
    group_input_025.outputs[40].hide = True
    group_input_025.outputs[41].hide = True
    group_input_025.outputs[42].hide = True
    group_input_025.outputs[43].hide = True
    group_input_025.outputs[44].hide = True
    group_input_025.outputs[45].hide = True
    group_input_025.outputs[46].hide = True
    group_input_025.outputs[47].hide = True
    group_input_025.outputs[48].hide = True
    group_input_025.outputs[49].hide = True
    group_input_025.outputs[51].hide = True
    group_input_025.outputs[52].hide = True
    group_input_025.outputs[53].hide = True
    group_input_025.outputs[54].hide = True
    group_input_025.outputs[55].hide = True
    group_input_025.outputs[56].hide = True
    group_input_025.outputs[57].hide = True
    group_input_025.outputs[58].hide = True
    group_input_025.outputs[59].hide = True
    group_input_025.outputs[60].hide = True
    group_input_025.outputs[61].hide = True
    group_input_025.outputs[62].hide = True
    group_input_025.outputs[63].hide = True
    group_input_025.outputs[64].hide = True
    group_input_025.outputs[65].hide = True
    group_input_025.outputs[67].hide = True
    group_input_025.outputs[68].hide = True
    group_input_025.outputs[69].hide = True
    group_input_025.outputs[70].hide = True
    group_input_025.outputs[71].hide = True
    group_input_025.outputs[72].hide = True
    group_input_025.outputs[73].hide = True
    group_input_025.outputs[74].hide = True
    group_input_025.outputs[75].hide = True
    group_input_025.outputs[76].hide = True
    group_input_025.outputs[77].hide = True
    group_input_025.outputs[78].hide = True
    group_input_025.outputs[79].hide = True
    group_input_025.outputs[80].hide = True
    group_input_025.outputs[81].hide = True
    group_input_025.outputs[83].hide = True
    group_input_025.outputs[84].hide = True
    group_input_025.outputs[85].hide = True
    group_input_025.outputs[86].hide = True
    group_input_025.outputs[87].hide = True
    group_input_025.outputs[88].hide = True
    group_input_025.outputs[89].hide = True
    group_input_025.outputs[90].hide = True
    group_input_025.outputs[91].hide = True
    group_input_025.outputs[92].hide = True
    group_input_025.outputs[93].hide = True
    group_input_025.outputs[94].hide = True
    group_input_025.outputs[95].hide = True
    group_input_025.outputs[96].hide = True
    group_input_025.outputs[97].hide = True
    group_input_025.outputs[99].hide = True
    group_input_025.outputs[100].hide = True
    group_input_025.outputs[101].hide = True
    group_input_025.outputs[102].hide = True
    group_input_025.outputs[103].hide = True
    group_input_025.outputs[104].hide = True
    group_input_025.outputs[105].hide = True
    group_input_025.outputs[106].hide = True
    group_input_025.outputs[107].hide = True
    group_input_025.outputs[108].hide = True
    group_input_025.outputs[109].hide = True
    group_input_025.outputs[110].hide = True
    group_input_025.outputs[111].hide = True
    group_input_025.outputs[112].hide = True
    group_input_025.outputs[113].hide = True
    group_input_025.outputs[115].hide = True
    group_input_025.outputs[116].hide = True
    group_input_025.outputs[117].hide = True
    group_input_025.outputs[118].hide = True
    group_input_025.outputs[119].hide = True
    group_input_025.outputs[120].hide = True
    group_input_025.outputs[121].hide = True
    group_input_025.outputs[122].hide = True
    group_input_025.outputs[123].hide = True
    group_input_025.outputs[124].hide = True
    group_input_025.outputs[125].hide = True
    group_input_025.outputs[127].hide = True
    group_input_025.outputs[128].hide = True
    group_input_025.outputs[129].hide = True
    group_input_025.outputs[130].hide = True
    group_input_025.outputs[131].hide = True
    group_input_025.outputs[132].hide = True
    group_input_025.outputs[133].hide = True
    group_input_025.outputs[134].hide = True
    group_input_025.outputs[135].hide = True

    # node Group.016
    group_016 = hims.nodes.new("ShaderNodeGroup")
    group_016.label = "Grime"
    group_016.name = "Group.016"
    group_016.node_tree = ColorMixer().node_tree

    # node Group.017
    group_017 = hims.nodes.new("ShaderNodeGroup")
    group_017.label = "Scratch Metallic"
    group_017.name = "Group.017"
    group_017.node_tree = InfiniteMaskingSorterNoGrime().node_tree

    # node Group.020
    group_020 = hims.nodes.new("ShaderNodeGroup")
    group_020.label = "Scratch Amount"
    group_020.name = "Group.020"
    group_020.node_tree = InfiniteMaskingSorterNoGrime().node_tree

    # node Clamp
    clamp_1 = hims.nodes.new("ShaderNodeClamp")
    clamp_1.name = "Clamp"
    clamp_1.clamp_type = "MINMAX"
    clamp_1.inputs[1].hide = True
    clamp_1.inputs[2].hide = True
    # Min
    clamp_1.inputs[1].default_value = 0.0
    # Max
    clamp_1.inputs[2].default_value = 1.0

    # node Clamp.001
    clamp_001 = hims.nodes.new("ShaderNodeClamp")
    clamp_001.name = "Clamp.001"
    clamp_001.clamp_type = "MINMAX"
    clamp_001.inputs[1].hide = True
    clamp_001.inputs[2].hide = True
    # Min
    clamp_001.inputs[1].default_value = 0.0
    # Max
    clamp_001.inputs[2].default_value = 1.0

    # node Clamp.002
    clamp_002 = hims.nodes.new("ShaderNodeClamp")
    clamp_002.name = "Clamp.002"
    clamp_002.clamp_type = "MINMAX"
    clamp_002.inputs[1].hide = True
    clamp_002.inputs[2].hide = True
    # Min
    clamp_002.inputs[1].default_value = 0.0
    # Max
    clamp_002.inputs[2].default_value = 1.0

    # node Clamp.003
    clamp_003 = hims.nodes.new("ShaderNodeClamp")
    clamp_003.name = "Clamp.003"
    clamp_003.clamp_type = "MINMAX"
    clamp_003.inputs[1].hide = True
    clamp_003.inputs[2].hide = True
    # Min
    clamp_003.inputs[1].default_value = 0.0
    # Max
    clamp_003.inputs[2].default_value = 1.0

    # node Clamp.004
    clamp_004 = hims.nodes.new("ShaderNodeClamp")
    clamp_004.name = "Clamp.004"
    clamp_004.clamp_type = "MINMAX"
    clamp_004.inputs[1].hide = True
    clamp_004.inputs[2].hide = True
    # Min
    clamp_004.inputs[1].default_value = 0.0
    # Max
    clamp_004.inputs[2].default_value = 1.0

    # node Clamp.005
    clamp_005 = hims.nodes.new("ShaderNodeClamp")
    clamp_005.name = "Clamp.005"
    clamp_005.clamp_type = "MINMAX"
    clamp_005.inputs[1].hide = True
    clamp_005.inputs[2].hide = True
    # Min
    clamp_005.inputs[1].default_value = 0.0
    # Max
    clamp_005.inputs[2].default_value = 1.0

    # node Clamp.006
    clamp_006 = hims.nodes.new("ShaderNodeClamp")
    clamp_006.name = "Clamp.006"
    clamp_006.clamp_type = "MINMAX"
    clamp_006.inputs[1].hide = True
    clamp_006.inputs[2].hide = True
    # Min
    clamp_006.inputs[1].default_value = 0.0
    # Max
    clamp_006.inputs[2].default_value = 1.0

    # node Clamp.007
    clamp_007 = hims.nodes.new("ShaderNodeClamp")
    clamp_007.name = "Clamp.007"
    clamp_007.clamp_type = "MINMAX"
    clamp_007.inputs[1].hide = True
    clamp_007.inputs[2].hide = True
    # Min
    clamp_007.inputs[1].default_value = 0.0
    # Max
    clamp_007.inputs[2].default_value = 1.0

    # node Group Input
    group_input_17 = hims.nodes.new("NodeGroupInput")
    group_input_17.name = "Group Input"
    group_input_17.outputs[1].hide = True
    group_input_17.outputs[2].hide = True
    group_input_17.outputs[3].hide = True
    group_input_17.outputs[4].hide = True
    group_input_17.outputs[5].hide = True
    group_input_17.outputs[6].hide = True
    group_input_17.outputs[8].hide = True
    group_input_17.outputs[9].hide = True
    group_input_17.outputs[10].hide = True
    group_input_17.outputs[11].hide = True
    group_input_17.outputs[12].hide = True
    group_input_17.outputs[13].hide = True
    group_input_17.outputs[14].hide = True
    group_input_17.outputs[15].hide = True
    group_input_17.outputs[16].hide = True
    group_input_17.outputs[17].hide = True
    group_input_17.outputs[18].hide = True
    group_input_17.outputs[19].hide = True
    group_input_17.outputs[20].hide = True
    group_input_17.outputs[21].hide = True
    group_input_17.outputs[23].hide = True
    group_input_17.outputs[24].hide = True
    group_input_17.outputs[25].hide = True
    group_input_17.outputs[26].hide = True
    group_input_17.outputs[27].hide = True
    group_input_17.outputs[28].hide = True
    group_input_17.outputs[29].hide = True
    group_input_17.outputs[30].hide = True
    group_input_17.outputs[31].hide = True
    group_input_17.outputs[32].hide = True
    group_input_17.outputs[33].hide = True
    group_input_17.outputs[34].hide = True
    group_input_17.outputs[35].hide = True
    group_input_17.outputs[36].hide = True
    group_input_17.outputs[38].hide = True
    group_input_17.outputs[39].hide = True
    group_input_17.outputs[40].hide = True
    group_input_17.outputs[41].hide = True
    group_input_17.outputs[42].hide = True
    group_input_17.outputs[43].hide = True
    group_input_17.outputs[44].hide = True
    group_input_17.outputs[45].hide = True
    group_input_17.outputs[46].hide = True
    group_input_17.outputs[47].hide = True
    group_input_17.outputs[48].hide = True
    group_input_17.outputs[49].hide = True
    group_input_17.outputs[50].hide = True
    group_input_17.outputs[51].hide = True
    group_input_17.outputs[53].hide = True
    group_input_17.outputs[54].hide = True
    group_input_17.outputs[55].hide = True
    group_input_17.outputs[56].hide = True
    group_input_17.outputs[57].hide = True
    group_input_17.outputs[58].hide = True
    group_input_17.outputs[59].hide = True
    group_input_17.outputs[60].hide = True
    group_input_17.outputs[61].hide = True
    group_input_17.outputs[62].hide = True
    group_input_17.outputs[63].hide = True
    group_input_17.outputs[64].hide = True
    group_input_17.outputs[65].hide = True
    group_input_17.outputs[66].hide = True
    group_input_17.outputs[67].hide = True
    group_input_17.outputs[69].hide = True
    group_input_17.outputs[70].hide = True
    group_input_17.outputs[71].hide = True
    group_input_17.outputs[72].hide = True
    group_input_17.outputs[73].hide = True
    group_input_17.outputs[74].hide = True
    group_input_17.outputs[75].hide = True
    group_input_17.outputs[76].hide = True
    group_input_17.outputs[77].hide = True
    group_input_17.outputs[78].hide = True
    group_input_17.outputs[79].hide = True
    group_input_17.outputs[80].hide = True
    group_input_17.outputs[81].hide = True
    group_input_17.outputs[82].hide = True
    group_input_17.outputs[83].hide = True
    group_input_17.outputs[85].hide = True
    group_input_17.outputs[86].hide = True
    group_input_17.outputs[87].hide = True
    group_input_17.outputs[88].hide = True
    group_input_17.outputs[89].hide = True
    group_input_17.outputs[90].hide = True
    group_input_17.outputs[91].hide = True
    group_input_17.outputs[92].hide = True
    group_input_17.outputs[93].hide = True
    group_input_17.outputs[94].hide = True
    group_input_17.outputs[95].hide = True
    group_input_17.outputs[96].hide = True
    group_input_17.outputs[97].hide = True
    group_input_17.outputs[98].hide = True
    group_input_17.outputs[99].hide = True
    group_input_17.outputs[101].hide = True
    group_input_17.outputs[102].hide = True
    group_input_17.outputs[103].hide = True
    group_input_17.outputs[104].hide = True
    group_input_17.outputs[105].hide = True
    group_input_17.outputs[106].hide = True
    group_input_17.outputs[107].hide = True
    group_input_17.outputs[108].hide = True
    group_input_17.outputs[109].hide = True
    group_input_17.outputs[110].hide = True
    group_input_17.outputs[111].hide = True
    group_input_17.outputs[112].hide = True
    group_input_17.outputs[113].hide = True
    group_input_17.outputs[114].hide = True
    group_input_17.outputs[115].hide = True
    group_input_17.outputs[117].hide = True
    group_input_17.outputs[118].hide = True
    group_input_17.outputs[119].hide = True
    group_input_17.outputs[120].hide = True
    group_input_17.outputs[121].hide = True
    group_input_17.outputs[122].hide = True
    group_input_17.outputs[123].hide = True
    group_input_17.outputs[124].hide = True
    group_input_17.outputs[125].hide = True
    group_input_17.outputs[126].hide = True
    group_input_17.outputs[127].hide = True
    group_input_17.outputs[129].hide = True
    group_input_17.outputs[130].hide = True
    group_input_17.outputs[131].hide = True
    group_input_17.outputs[132].hide = True
    group_input_17.outputs[133].hide = True
    group_input_17.outputs[134].hide = True
    group_input_17.outputs[135].hide = True

    # node Mix.005
    mix_005_6 = hims.nodes.new("ShaderNodeMix")
    mix_005_6.name = "Mix.005"
    mix_005_6.blend_type = "MULTIPLY"
    mix_005_6.clamp_factor = True
    mix_005_6.clamp_result = True
    mix_005_6.data_type = "RGBA"
    mix_005_6.factor_mode = "UNIFORM"
    mix_005_6.inputs[0].hide = True
    mix_005_6.inputs[1].hide = True
    mix_005_6.inputs[2].hide = True
    mix_005_6.inputs[3].hide = True
    mix_005_6.inputs[4].hide = True
    mix_005_6.inputs[5].hide = True
    mix_005_6.outputs[0].hide = True
    mix_005_6.outputs[1].hide = True
    # Factor_Float
    mix_005_6.inputs[0].default_value = 1.0
    # Factor_Vector
    mix_005_6.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_005_6.inputs[2].default_value = 0.0
    # B_Float
    mix_005_6.inputs[3].default_value = 0.0
    # A_Vector
    mix_005_6.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_005_6.inputs[5].default_value = (0.0, 0.0, 0.0)
    # A_Rotation
    mix_005_6.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix_005_6.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Gamma
    gamma = hims.nodes.new("ShaderNodeGamma")
    gamma.name = "Gamma"
    gamma.inputs[1].hide = True
    # Gamma
    gamma.inputs[1].default_value = 2.200000047683716

    # node Math.006
    math_006_1 = hims.nodes.new("ShaderNodeMath")
    math_006_1.name = "Math.006"
    math_006_1.operation = "SUBTRACT"
    math_006_1.use_clamp = True
    math_006_1.inputs[0].hide = True
    math_006_1.inputs[2].hide = True
    # Value
    math_006_1.inputs[0].default_value = 1.0
    # Value_002
    math_006_1.inputs[2].default_value = 0.5

    # node Group Input.021
    group_input_021 = hims.nodes.new("NodeGroupInput")
    group_input_021.name = "Group Input.021"
    group_input_021.outputs[0].hide = True
    group_input_021.outputs[1].hide = True
    group_input_021.outputs[2].hide = True
    group_input_021.outputs[3].hide = True
    group_input_021.outputs[4].hide = True
    group_input_021.outputs[5].hide = True
    group_input_021.outputs[6].hide = True
    group_input_021.outputs[9].hide = True
    group_input_021.outputs[10].hide = True
    group_input_021.outputs[11].hide = True
    group_input_021.outputs[12].hide = True
    group_input_021.outputs[13].hide = True
    group_input_021.outputs[14].hide = True
    group_input_021.outputs[15].hide = True
    group_input_021.outputs[16].hide = True
    group_input_021.outputs[17].hide = True
    group_input_021.outputs[18].hide = True
    group_input_021.outputs[19].hide = True
    group_input_021.outputs[20].hide = True
    group_input_021.outputs[21].hide = True
    group_input_021.outputs[22].hide = True
    group_input_021.outputs[23].hide = True
    group_input_021.outputs[24].hide = True
    group_input_021.outputs[25].hide = True
    group_input_021.outputs[26].hide = True
    group_input_021.outputs[27].hide = True
    group_input_021.outputs[28].hide = True
    group_input_021.outputs[29].hide = True
    group_input_021.outputs[30].hide = True
    group_input_021.outputs[31].hide = True
    group_input_021.outputs[32].hide = True
    group_input_021.outputs[33].hide = True
    group_input_021.outputs[34].hide = True
    group_input_021.outputs[35].hide = True
    group_input_021.outputs[36].hide = True
    group_input_021.outputs[37].hide = True
    group_input_021.outputs[38].hide = True
    group_input_021.outputs[39].hide = True
    group_input_021.outputs[40].hide = True
    group_input_021.outputs[41].hide = True
    group_input_021.outputs[42].hide = True
    group_input_021.outputs[43].hide = True
    group_input_021.outputs[44].hide = True
    group_input_021.outputs[45].hide = True
    group_input_021.outputs[46].hide = True
    group_input_021.outputs[47].hide = True
    group_input_021.outputs[48].hide = True
    group_input_021.outputs[49].hide = True
    group_input_021.outputs[50].hide = True
    group_input_021.outputs[51].hide = True
    group_input_021.outputs[52].hide = True
    group_input_021.outputs[53].hide = True
    group_input_021.outputs[54].hide = True
    group_input_021.outputs[55].hide = True
    group_input_021.outputs[56].hide = True
    group_input_021.outputs[57].hide = True
    group_input_021.outputs[58].hide = True
    group_input_021.outputs[59].hide = True
    group_input_021.outputs[60].hide = True
    group_input_021.outputs[61].hide = True
    group_input_021.outputs[62].hide = True
    group_input_021.outputs[63].hide = True
    group_input_021.outputs[64].hide = True
    group_input_021.outputs[65].hide = True
    group_input_021.outputs[66].hide = True
    group_input_021.outputs[67].hide = True
    group_input_021.outputs[68].hide = True
    group_input_021.outputs[69].hide = True
    group_input_021.outputs[70].hide = True
    group_input_021.outputs[71].hide = True
    group_input_021.outputs[72].hide = True
    group_input_021.outputs[73].hide = True
    group_input_021.outputs[74].hide = True
    group_input_021.outputs[75].hide = True
    group_input_021.outputs[76].hide = True
    group_input_021.outputs[77].hide = True
    group_input_021.outputs[78].hide = True
    group_input_021.outputs[79].hide = True
    group_input_021.outputs[80].hide = True
    group_input_021.outputs[81].hide = True
    group_input_021.outputs[82].hide = True
    group_input_021.outputs[83].hide = True
    group_input_021.outputs[84].hide = True
    group_input_021.outputs[85].hide = True
    group_input_021.outputs[86].hide = True
    group_input_021.outputs[87].hide = True
    group_input_021.outputs[88].hide = True
    group_input_021.outputs[89].hide = True
    group_input_021.outputs[90].hide = True
    group_input_021.outputs[91].hide = True
    group_input_021.outputs[92].hide = True
    group_input_021.outputs[93].hide = True
    group_input_021.outputs[94].hide = True
    group_input_021.outputs[95].hide = True
    group_input_021.outputs[96].hide = True
    group_input_021.outputs[97].hide = True
    group_input_021.outputs[98].hide = True
    group_input_021.outputs[99].hide = True
    group_input_021.outputs[100].hide = True
    group_input_021.outputs[101].hide = True
    group_input_021.outputs[102].hide = True
    group_input_021.outputs[103].hide = True
    group_input_021.outputs[104].hide = True
    group_input_021.outputs[105].hide = True
    group_input_021.outputs[106].hide = True
    group_input_021.outputs[107].hide = True
    group_input_021.outputs[108].hide = True
    group_input_021.outputs[109].hide = True
    group_input_021.outputs[110].hide = True
    group_input_021.outputs[111].hide = True
    group_input_021.outputs[112].hide = True
    group_input_021.outputs[113].hide = True
    group_input_021.outputs[114].hide = True
    group_input_021.outputs[115].hide = True
    group_input_021.outputs[116].hide = True
    group_input_021.outputs[117].hide = True
    group_input_021.outputs[118].hide = True
    group_input_021.outputs[119].hide = True
    group_input_021.outputs[120].hide = True
    group_input_021.outputs[121].hide = True
    group_input_021.outputs[122].hide = True
    group_input_021.outputs[123].hide = True
    group_input_021.outputs[124].hide = True
    group_input_021.outputs[125].hide = True
    group_input_021.outputs[126].hide = True
    group_input_021.outputs[127].hide = True
    group_input_021.outputs[128].hide = True
    group_input_021.outputs[129].hide = True
    group_input_021.outputs[130].hide = True
    group_input_021.outputs[131].hide = True
    group_input_021.outputs[132].hide = True
    group_input_021.outputs[133].hide = True
    group_input_021.outputs[134].hide = True
    group_input_021.outputs[135].hide = True

    # node Group Input.023
    group_input_023 = hims.nodes.new("NodeGroupInput")
    group_input_023.name = "Group Input.023"
    group_input_023.outputs[0].hide = True
    group_input_023.outputs[1].hide = True
    group_input_023.outputs[2].hide = True
    group_input_023.outputs[3].hide = True
    group_input_023.outputs[4].hide = True
    group_input_023.outputs[5].hide = True
    group_input_023.outputs[6].hide = True
    group_input_023.outputs[7].hide = True
    group_input_023.outputs[8].hide = True
    group_input_023.outputs[9].hide = True
    group_input_023.outputs[10].hide = True
    group_input_023.outputs[12].hide = True
    group_input_023.outputs[13].hide = True
    group_input_023.outputs[14].hide = True
    group_input_023.outputs[15].hide = True
    group_input_023.outputs[16].hide = True
    group_input_023.outputs[17].hide = True
    group_input_023.outputs[18].hide = True
    group_input_023.outputs[19].hide = True
    group_input_023.outputs[20].hide = True
    group_input_023.outputs[21].hide = True
    group_input_023.outputs[22].hide = True
    group_input_023.outputs[23].hide = True
    group_input_023.outputs[24].hide = True
    group_input_023.outputs[25].hide = True
    group_input_023.outputs[26].hide = True
    group_input_023.outputs[27].hide = True
    group_input_023.outputs[28].hide = True
    group_input_023.outputs[29].hide = True
    group_input_023.outputs[30].hide = True
    group_input_023.outputs[31].hide = True
    group_input_023.outputs[32].hide = True
    group_input_023.outputs[33].hide = True
    group_input_023.outputs[34].hide = True
    group_input_023.outputs[35].hide = True
    group_input_023.outputs[36].hide = True
    group_input_023.outputs[37].hide = True
    group_input_023.outputs[38].hide = True
    group_input_023.outputs[39].hide = True
    group_input_023.outputs[40].hide = True
    group_input_023.outputs[41].hide = True
    group_input_023.outputs[42].hide = True
    group_input_023.outputs[43].hide = True
    group_input_023.outputs[44].hide = True
    group_input_023.outputs[45].hide = True
    group_input_023.outputs[46].hide = True
    group_input_023.outputs[47].hide = True
    group_input_023.outputs[48].hide = True
    group_input_023.outputs[49].hide = True
    group_input_023.outputs[50].hide = True
    group_input_023.outputs[51].hide = True
    group_input_023.outputs[52].hide = True
    group_input_023.outputs[53].hide = True
    group_input_023.outputs[54].hide = True
    group_input_023.outputs[55].hide = True
    group_input_023.outputs[56].hide = True
    group_input_023.outputs[57].hide = True
    group_input_023.outputs[58].hide = True
    group_input_023.outputs[59].hide = True
    group_input_023.outputs[60].hide = True
    group_input_023.outputs[61].hide = True
    group_input_023.outputs[62].hide = True
    group_input_023.outputs[63].hide = True
    group_input_023.outputs[64].hide = True
    group_input_023.outputs[65].hide = True
    group_input_023.outputs[66].hide = True
    group_input_023.outputs[67].hide = True
    group_input_023.outputs[68].hide = True
    group_input_023.outputs[69].hide = True
    group_input_023.outputs[70].hide = True
    group_input_023.outputs[71].hide = True
    group_input_023.outputs[72].hide = True
    group_input_023.outputs[73].hide = True
    group_input_023.outputs[74].hide = True
    group_input_023.outputs[75].hide = True
    group_input_023.outputs[76].hide = True
    group_input_023.outputs[77].hide = True
    group_input_023.outputs[78].hide = True
    group_input_023.outputs[79].hide = True
    group_input_023.outputs[80].hide = True
    group_input_023.outputs[81].hide = True
    group_input_023.outputs[82].hide = True
    group_input_023.outputs[83].hide = True
    group_input_023.outputs[84].hide = True
    group_input_023.outputs[85].hide = True
    group_input_023.outputs[86].hide = True
    group_input_023.outputs[87].hide = True
    group_input_023.outputs[88].hide = True
    group_input_023.outputs[89].hide = True
    group_input_023.outputs[90].hide = True
    group_input_023.outputs[91].hide = True
    group_input_023.outputs[92].hide = True
    group_input_023.outputs[93].hide = True
    group_input_023.outputs[94].hide = True
    group_input_023.outputs[95].hide = True
    group_input_023.outputs[96].hide = True
    group_input_023.outputs[97].hide = True
    group_input_023.outputs[98].hide = True
    group_input_023.outputs[99].hide = True
    group_input_023.outputs[100].hide = True
    group_input_023.outputs[101].hide = True
    group_input_023.outputs[102].hide = True
    group_input_023.outputs[103].hide = True
    group_input_023.outputs[104].hide = True
    group_input_023.outputs[105].hide = True
    group_input_023.outputs[106].hide = True
    group_input_023.outputs[107].hide = True
    group_input_023.outputs[108].hide = True
    group_input_023.outputs[109].hide = True
    group_input_023.outputs[110].hide = True
    group_input_023.outputs[111].hide = True
    group_input_023.outputs[112].hide = True
    group_input_023.outputs[113].hide = True
    group_input_023.outputs[114].hide = True
    group_input_023.outputs[115].hide = True
    group_input_023.outputs[116].hide = True
    group_input_023.outputs[117].hide = True
    group_input_023.outputs[118].hide = True
    group_input_023.outputs[119].hide = True
    group_input_023.outputs[120].hide = True
    group_input_023.outputs[121].hide = True
    group_input_023.outputs[122].hide = True
    group_input_023.outputs[123].hide = True
    group_input_023.outputs[124].hide = True
    group_input_023.outputs[125].hide = True
    group_input_023.outputs[126].hide = True
    group_input_023.outputs[127].hide = True
    group_input_023.outputs[128].hide = True
    group_input_023.outputs[129].hide = True
    group_input_023.outputs[130].hide = True
    group_input_023.outputs[131].hide = True
    group_input_023.outputs[132].hide = True
    group_input_023.outputs[133].hide = True
    group_input_023.outputs[134].hide = True
    group_input_023.outputs[135].hide = True

    # node Group Input.022
    group_input_022 = hims.nodes.new("NodeGroupInput")
    group_input_022.name = "Group Input.022"
    group_input_022.outputs[0].hide = True
    group_input_022.outputs[1].hide = True
    group_input_022.outputs[2].hide = True
    group_input_022.outputs[3].hide = True
    group_input_022.outputs[4].hide = True
    group_input_022.outputs[5].hide = True
    group_input_022.outputs[6].hide = True
    group_input_022.outputs[7].hide = True
    group_input_022.outputs[8].hide = True
    group_input_022.outputs[9].hide = True
    group_input_022.outputs[11].hide = True
    group_input_022.outputs[12].hide = True
    group_input_022.outputs[13].hide = True
    group_input_022.outputs[14].hide = True
    group_input_022.outputs[15].hide = True
    group_input_022.outputs[16].hide = True
    group_input_022.outputs[17].hide = True
    group_input_022.outputs[18].hide = True
    group_input_022.outputs[19].hide = True
    group_input_022.outputs[20].hide = True
    group_input_022.outputs[21].hide = True
    group_input_022.outputs[22].hide = True
    group_input_022.outputs[23].hide = True
    group_input_022.outputs[24].hide = True
    group_input_022.outputs[25].hide = True
    group_input_022.outputs[26].hide = True
    group_input_022.outputs[27].hide = True
    group_input_022.outputs[28].hide = True
    group_input_022.outputs[29].hide = True
    group_input_022.outputs[30].hide = True
    group_input_022.outputs[31].hide = True
    group_input_022.outputs[32].hide = True
    group_input_022.outputs[33].hide = True
    group_input_022.outputs[34].hide = True
    group_input_022.outputs[35].hide = True
    group_input_022.outputs[36].hide = True
    group_input_022.outputs[37].hide = True
    group_input_022.outputs[38].hide = True
    group_input_022.outputs[39].hide = True
    group_input_022.outputs[40].hide = True
    group_input_022.outputs[41].hide = True
    group_input_022.outputs[42].hide = True
    group_input_022.outputs[43].hide = True
    group_input_022.outputs[44].hide = True
    group_input_022.outputs[45].hide = True
    group_input_022.outputs[46].hide = True
    group_input_022.outputs[47].hide = True
    group_input_022.outputs[48].hide = True
    group_input_022.outputs[49].hide = True
    group_input_022.outputs[50].hide = True
    group_input_022.outputs[51].hide = True
    group_input_022.outputs[52].hide = True
    group_input_022.outputs[53].hide = True
    group_input_022.outputs[54].hide = True
    group_input_022.outputs[55].hide = True
    group_input_022.outputs[56].hide = True
    group_input_022.outputs[57].hide = True
    group_input_022.outputs[58].hide = True
    group_input_022.outputs[59].hide = True
    group_input_022.outputs[60].hide = True
    group_input_022.outputs[61].hide = True
    group_input_022.outputs[62].hide = True
    group_input_022.outputs[63].hide = True
    group_input_022.outputs[64].hide = True
    group_input_022.outputs[65].hide = True
    group_input_022.outputs[66].hide = True
    group_input_022.outputs[67].hide = True
    group_input_022.outputs[68].hide = True
    group_input_022.outputs[69].hide = True
    group_input_022.outputs[70].hide = True
    group_input_022.outputs[71].hide = True
    group_input_022.outputs[72].hide = True
    group_input_022.outputs[73].hide = True
    group_input_022.outputs[74].hide = True
    group_input_022.outputs[75].hide = True
    group_input_022.outputs[76].hide = True
    group_input_022.outputs[77].hide = True
    group_input_022.outputs[78].hide = True
    group_input_022.outputs[79].hide = True
    group_input_022.outputs[80].hide = True
    group_input_022.outputs[81].hide = True
    group_input_022.outputs[82].hide = True
    group_input_022.outputs[83].hide = True
    group_input_022.outputs[84].hide = True
    group_input_022.outputs[85].hide = True
    group_input_022.outputs[86].hide = True
    group_input_022.outputs[87].hide = True
    group_input_022.outputs[88].hide = True
    group_input_022.outputs[89].hide = True
    group_input_022.outputs[90].hide = True
    group_input_022.outputs[91].hide = True
    group_input_022.outputs[92].hide = True
    group_input_022.outputs[93].hide = True
    group_input_022.outputs[94].hide = True
    group_input_022.outputs[95].hide = True
    group_input_022.outputs[96].hide = True
    group_input_022.outputs[97].hide = True
    group_input_022.outputs[98].hide = True
    group_input_022.outputs[99].hide = True
    group_input_022.outputs[100].hide = True
    group_input_022.outputs[101].hide = True
    group_input_022.outputs[102].hide = True
    group_input_022.outputs[103].hide = True
    group_input_022.outputs[104].hide = True
    group_input_022.outputs[105].hide = True
    group_input_022.outputs[106].hide = True
    group_input_022.outputs[107].hide = True
    group_input_022.outputs[108].hide = True
    group_input_022.outputs[109].hide = True
    group_input_022.outputs[110].hide = True
    group_input_022.outputs[111].hide = True
    group_input_022.outputs[112].hide = True
    group_input_022.outputs[113].hide = True
    group_input_022.outputs[114].hide = True
    group_input_022.outputs[115].hide = True
    group_input_022.outputs[116].hide = True
    group_input_022.outputs[117].hide = True
    group_input_022.outputs[118].hide = True
    group_input_022.outputs[119].hide = True
    group_input_022.outputs[120].hide = True
    group_input_022.outputs[121].hide = True
    group_input_022.outputs[122].hide = True
    group_input_022.outputs[123].hide = True
    group_input_022.outputs[124].hide = True
    group_input_022.outputs[125].hide = True
    group_input_022.outputs[126].hide = True
    group_input_022.outputs[127].hide = True
    group_input_022.outputs[128].hide = True
    group_input_022.outputs[129].hide = True
    group_input_022.outputs[130].hide = True
    group_input_022.outputs[131].hide = True
    group_input_022.outputs[132].hide = True
    group_input_022.outputs[133].hide = True
    group_input_022.outputs[134].hide = True
    group_input_022.outputs[135].hide = True

    # node Texture Coordinate
    texture_coordinate = hims.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False
    texture_coordinate.outputs[0].hide = True
    texture_coordinate.outputs[1].hide = True
    texture_coordinate.outputs[3].hide = True
    texture_coordinate.outputs[4].hide = True
    texture_coordinate.outputs[5].hide = True
    texture_coordinate.outputs[6].hide = True

    # node Mapping
    mapping_1 = hims.nodes.new("ShaderNodeMapping")
    mapping_1.name = "Mapping"
    mapping_1.vector_type = "POINT"
    mapping_1.inputs[1].hide = True
    mapping_1.inputs[2].hide = True
    # Location
    mapping_1.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    mapping_1.inputs[2].default_value = (0.0, 0.0, 0.0)

    # node Musgrave Texture
    musgrave_texture = hims.nodes.new("ShaderNodeTexNoise")
    musgrave_texture.name = "Musgrave Texture"
    musgrave_texture.noise_dimensions = "2D"
    musgrave_texture.normalize = False
    musgrave_texture.inputs[1].hide = True
    musgrave_texture.inputs[2].hide = True
    musgrave_texture.inputs[3].hide = True
    musgrave_texture.inputs[4].hide = True
    musgrave_texture.inputs[5].hide = True
    musgrave_texture.inputs[6].hide = True
    musgrave_texture.inputs[7].hide = True
    # W
    musgrave_texture.inputs[1].default_value = 0.0
    # Scale
    musgrave_texture.inputs[2].default_value = 3.0
    # Detail
    musgrave_texture.inputs[3].default_value = 0.0
    # Roughness
    musgrave_texture.inputs[4].default_value = 0.6944444179534912
    # Lacunarity
    musgrave_texture.inputs[5].default_value = 1.2000000476837158
    # Offset
    musgrave_texture.inputs[6].default_value = 0.0
    # Gain
    musgrave_texture.inputs[7].default_value = 1.0
    # Distortion
    musgrave_texture.inputs[8].default_value = 0.0

    # node ColorRamp.001
    colorramp_001 = hims.nodes.new("ShaderNodeValToRGB")
    colorramp_001.name = "ColorRamp.001"
    colorramp_001.color_ramp.color_mode = "RGB"
    colorramp_001.color_ramp.hue_interpolation = "NEAR"
    colorramp_001.color_ramp.interpolation = "LINEAR"

    # initialize color ramp elements
    colorramp_001.color_ramp.elements.remove(colorramp_001.color_ramp.elements[0])
    colorramp_001_cre_0 = colorramp_001.color_ramp.elements[0]
    colorramp_001_cre_0.position = 0.5
    colorramp_001_cre_0.alpha = 1.0
    colorramp_001_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    colorramp_001_cre_1 = colorramp_001.color_ramp.elements.new(0.6424239277839661)
    colorramp_001_cre_1.alpha = 1.0
    colorramp_001_cre_1.color = (
        0.004999999888241291,
        0.004999999888241291,
        0.004999999888241291,
        1.0,
    )

    colorramp_001_cre_2 = colorramp_001.color_ramp.elements.new(0.884848415851593)
    colorramp_001_cre_2.alpha = 1.0
    colorramp_001_cre_2.color = (
        0.022307951003313065,
        0.022307951003313065,
        0.022307951003313065,
        1.0,
    )

    colorramp_001.outputs[1].hide = True

    # node Bump
    bump = hims.nodes.new("ShaderNodeBump")
    bump.name = "Bump"
    bump.invert = True
    bump.inputs[1].hide = True
    # Distance
    bump.inputs[1].default_value = 0.004000000189989805

    # node ColorRamp
    colorramp = hims.nodes.new("ShaderNodeValToRGB")
    colorramp.name = "ColorRamp"
    colorramp.color_ramp.color_mode = "RGB"
    colorramp.color_ramp.hue_interpolation = "NEAR"
    colorramp.color_ramp.interpolation = "LINEAR"

    # initialize color ramp elements
    colorramp.color_ramp.elements.remove(colorramp.color_ramp.elements[0])
    colorramp_cre_0 = colorramp.color_ramp.elements[0]
    colorramp_cre_0.position = 0.13939400017261505
    colorramp_cre_0.alpha = 1.0
    colorramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    colorramp_cre_1 = colorramp.color_ramp.elements.new(0.7379999756813049)
    colorramp_cre_1.alpha = 1.0
    colorramp_cre_1.color = (
        0.0122859887778759,
        0.01228599064052105,
        0.012285999953746796,
        1.0,
    )

    colorramp_cre_2 = colorramp.color_ramp.elements.new(1.0)
    colorramp_cre_2.alpha = 1.0
    colorramp_cre_2.color = (
        0.01520898099988699,
        0.015208990313112736,
        0.015208999626338482,
        1.0,
    )

    colorramp.outputs[1].hide = True

    # node Group.006
    group_006 = hims.nodes.new("ShaderNodeGroup")
    group_006.name = "Group.006"
    group_006.node_tree = ScratchGlobalToggle().node_tree

    # node Group.012
    group_012 = hims.nodes.new("ShaderNodeGroup")
    group_012.label = "Zone 6"
    group_012.name = "Group.012"
    group_012.node_tree = ColorMixer().node_tree

    # node Group.018
    group_018 = hims.nodes.new("ShaderNodeGroup")
    group_018.label = "Scratch Roughness"
    group_018.name = "Group.018"
    group_018.node_tree = InfiniteMaskingSorterNoGrime().node_tree

    # node Group.023
    group_023 = hims.nodes.new("ShaderNodeGroup")
    group_023.label = "Transparency Amount"
    group_023.name = "Group.023"
    group_023.node_tree = InfiniteMaskingSorter().node_tree

    # node Group.019
    group_019 = hims.nodes.new("ShaderNodeGroup")
    group_019.label = "SSS Amount"
    group_019.name = "Group.019"
    group_019.node_tree = InfiniteMaskingSorter().node_tree

    # node Group.004
    group_004 = hims.nodes.new("ShaderNodeGroup")
    group_004.label = "Zone 2"
    group_004.name = "Group.004"
    group_004.node_tree = ColorMixer().node_tree

    # node Group Input.020
    group_input_020 = hims.nodes.new("NodeGroupInput")
    group_input_020.name = "Group Input.020"
    group_input_020.outputs[0].hide = True
    group_input_020.outputs[1].hide = True
    group_input_020.outputs[2].hide = True
    group_input_020.outputs[3].hide = True
    group_input_020.outputs[4].hide = True
    group_input_020.outputs[5].hide = True
    group_input_020.outputs[6].hide = True
    group_input_020.outputs[7].hide = True
    group_input_020.outputs[8].hide = True
    group_input_020.outputs[10].hide = True
    group_input_020.outputs[11].hide = True
    group_input_020.outputs[12].hide = True
    group_input_020.outputs[13].hide = True
    group_input_020.outputs[14].hide = True
    group_input_020.outputs[15].hide = True
    group_input_020.outputs[16].hide = True
    group_input_020.outputs[17].hide = True
    group_input_020.outputs[18].hide = True
    group_input_020.outputs[19].hide = True
    group_input_020.outputs[20].hide = True
    group_input_020.outputs[21].hide = True
    group_input_020.outputs[22].hide = True
    group_input_020.outputs[23].hide = True
    group_input_020.outputs[24].hide = True
    group_input_020.outputs[25].hide = True
    group_input_020.outputs[26].hide = True
    group_input_020.outputs[27].hide = True
    group_input_020.outputs[28].hide = True
    group_input_020.outputs[29].hide = True
    group_input_020.outputs[30].hide = True
    group_input_020.outputs[31].hide = True
    group_input_020.outputs[32].hide = True
    group_input_020.outputs[33].hide = True
    group_input_020.outputs[34].hide = True
    group_input_020.outputs[35].hide = True
    group_input_020.outputs[36].hide = True
    group_input_020.outputs[37].hide = True
    group_input_020.outputs[38].hide = True
    group_input_020.outputs[39].hide = True
    group_input_020.outputs[40].hide = True
    group_input_020.outputs[41].hide = True
    group_input_020.outputs[42].hide = True
    group_input_020.outputs[43].hide = True
    group_input_020.outputs[44].hide = True
    group_input_020.outputs[45].hide = True
    group_input_020.outputs[46].hide = True
    group_input_020.outputs[47].hide = True
    group_input_020.outputs[48].hide = True
    group_input_020.outputs[49].hide = True
    group_input_020.outputs[50].hide = True
    group_input_020.outputs[51].hide = True
    group_input_020.outputs[52].hide = True
    group_input_020.outputs[53].hide = True
    group_input_020.outputs[54].hide = True
    group_input_020.outputs[55].hide = True
    group_input_020.outputs[56].hide = True
    group_input_020.outputs[57].hide = True
    group_input_020.outputs[58].hide = True
    group_input_020.outputs[59].hide = True
    group_input_020.outputs[60].hide = True
    group_input_020.outputs[61].hide = True
    group_input_020.outputs[62].hide = True
    group_input_020.outputs[63].hide = True
    group_input_020.outputs[64].hide = True
    group_input_020.outputs[65].hide = True
    group_input_020.outputs[66].hide = True
    group_input_020.outputs[67].hide = True
    group_input_020.outputs[68].hide = True
    group_input_020.outputs[69].hide = True
    group_input_020.outputs[70].hide = True
    group_input_020.outputs[71].hide = True
    group_input_020.outputs[72].hide = True
    group_input_020.outputs[73].hide = True
    group_input_020.outputs[74].hide = True
    group_input_020.outputs[75].hide = True
    group_input_020.outputs[76].hide = True
    group_input_020.outputs[77].hide = True
    group_input_020.outputs[78].hide = True
    group_input_020.outputs[79].hide = True
    group_input_020.outputs[80].hide = True
    group_input_020.outputs[81].hide = True
    group_input_020.outputs[82].hide = True
    group_input_020.outputs[83].hide = True
    group_input_020.outputs[84].hide = True
    group_input_020.outputs[85].hide = True
    group_input_020.outputs[86].hide = True
    group_input_020.outputs[87].hide = True
    group_input_020.outputs[88].hide = True
    group_input_020.outputs[89].hide = True
    group_input_020.outputs[90].hide = True
    group_input_020.outputs[91].hide = True
    group_input_020.outputs[92].hide = True
    group_input_020.outputs[93].hide = True
    group_input_020.outputs[94].hide = True
    group_input_020.outputs[95].hide = True
    group_input_020.outputs[96].hide = True
    group_input_020.outputs[97].hide = True
    group_input_020.outputs[98].hide = True
    group_input_020.outputs[99].hide = True
    group_input_020.outputs[100].hide = True
    group_input_020.outputs[101].hide = True
    group_input_020.outputs[102].hide = True
    group_input_020.outputs[103].hide = True
    group_input_020.outputs[104].hide = True
    group_input_020.outputs[105].hide = True
    group_input_020.outputs[106].hide = True
    group_input_020.outputs[107].hide = True
    group_input_020.outputs[108].hide = True
    group_input_020.outputs[109].hide = True
    group_input_020.outputs[110].hide = True
    group_input_020.outputs[111].hide = True
    group_input_020.outputs[112].hide = True
    group_input_020.outputs[113].hide = True
    group_input_020.outputs[114].hide = True
    group_input_020.outputs[115].hide = True
    group_input_020.outputs[116].hide = True
    group_input_020.outputs[117].hide = True
    group_input_020.outputs[118].hide = True
    group_input_020.outputs[119].hide = True
    group_input_020.outputs[120].hide = True
    group_input_020.outputs[121].hide = True
    group_input_020.outputs[122].hide = True
    group_input_020.outputs[123].hide = True
    group_input_020.outputs[124].hide = True
    group_input_020.outputs[125].hide = True
    group_input_020.outputs[126].hide = True
    group_input_020.outputs[127].hide = True
    group_input_020.outputs[128].hide = True
    group_input_020.outputs[129].hide = True
    group_input_020.outputs[130].hide = True
    group_input_020.outputs[131].hide = True
    group_input_020.outputs[132].hide = True
    group_input_020.outputs[133].hide = True
    group_input_020.outputs[134].hide = True
    group_input_020.outputs[135].hide = True

    # node Group Input.017
    group_input_017 = hims.nodes.new("NodeGroupInput")
    group_input_017.name = "Group Input.017"
    group_input_017.outputs[1].hide = True
    group_input_017.outputs[2].hide = True
    group_input_017.outputs[3].hide = True
    group_input_017.outputs[4].hide = True
    group_input_017.outputs[5].hide = True
    group_input_017.outputs[6].hide = True
    group_input_017.outputs[8].hide = True
    group_input_017.outputs[9].hide = True
    group_input_017.outputs[10].hide = True
    group_input_017.outputs[11].hide = True
    group_input_017.outputs[12].hide = True
    group_input_017.outputs[13].hide = True
    group_input_017.outputs[14].hide = True
    group_input_017.outputs[15].hide = True
    group_input_017.outputs[16].hide = True
    group_input_017.outputs[17].hide = True
    group_input_017.outputs[18].hide = True
    group_input_017.outputs[19].hide = True
    group_input_017.outputs[20].hide = True
    group_input_017.outputs[21].hide = True
    group_input_017.outputs[22].hide = True
    group_input_017.outputs[23].hide = True
    group_input_017.outputs[24].hide = True
    group_input_017.outputs[25].hide = True
    group_input_017.outputs[26].hide = True
    group_input_017.outputs[27].hide = True
    group_input_017.outputs[28].hide = True
    group_input_017.outputs[29].hide = True
    group_input_017.outputs[30].hide = True
    group_input_017.outputs[31].hide = True
    group_input_017.outputs[32].hide = True
    group_input_017.outputs[33].hide = True
    group_input_017.outputs[34].hide = True
    group_input_017.outputs[35].hide = True
    group_input_017.outputs[36].hide = True
    group_input_017.outputs[37].hide = True
    group_input_017.outputs[38].hide = True
    group_input_017.outputs[39].hide = True
    group_input_017.outputs[40].hide = True
    group_input_017.outputs[41].hide = True
    group_input_017.outputs[42].hide = True
    group_input_017.outputs[43].hide = True
    group_input_017.outputs[44].hide = True
    group_input_017.outputs[45].hide = True
    group_input_017.outputs[46].hide = True
    group_input_017.outputs[47].hide = True
    group_input_017.outputs[48].hide = True
    group_input_017.outputs[49].hide = True
    group_input_017.outputs[50].hide = True
    group_input_017.outputs[51].hide = True
    group_input_017.outputs[52].hide = True
    group_input_017.outputs[53].hide = True
    group_input_017.outputs[54].hide = True
    group_input_017.outputs[55].hide = True
    group_input_017.outputs[56].hide = True
    group_input_017.outputs[57].hide = True
    group_input_017.outputs[58].hide = True
    group_input_017.outputs[59].hide = True
    group_input_017.outputs[60].hide = True
    group_input_017.outputs[61].hide = True
    group_input_017.outputs[62].hide = True
    group_input_017.outputs[63].hide = True
    group_input_017.outputs[64].hide = True
    group_input_017.outputs[65].hide = True
    group_input_017.outputs[66].hide = True
    group_input_017.outputs[67].hide = True
    group_input_017.outputs[68].hide = True
    group_input_017.outputs[69].hide = True
    group_input_017.outputs[70].hide = True
    group_input_017.outputs[71].hide = True
    group_input_017.outputs[72].hide = True
    group_input_017.outputs[73].hide = True
    group_input_017.outputs[74].hide = True
    group_input_017.outputs[75].hide = True
    group_input_017.outputs[76].hide = True
    group_input_017.outputs[77].hide = True
    group_input_017.outputs[78].hide = True
    group_input_017.outputs[79].hide = True
    group_input_017.outputs[80].hide = True
    group_input_017.outputs[81].hide = True
    group_input_017.outputs[82].hide = True
    group_input_017.outputs[83].hide = True
    group_input_017.outputs[84].hide = True
    group_input_017.outputs[85].hide = True
    group_input_017.outputs[86].hide = True
    group_input_017.outputs[87].hide = True
    group_input_017.outputs[88].hide = True
    group_input_017.outputs[89].hide = True
    group_input_017.outputs[90].hide = True
    group_input_017.outputs[91].hide = True
    group_input_017.outputs[92].hide = True
    group_input_017.outputs[93].hide = True
    group_input_017.outputs[94].hide = True
    group_input_017.outputs[95].hide = True
    group_input_017.outputs[96].hide = True
    group_input_017.outputs[97].hide = True
    group_input_017.outputs[98].hide = True
    group_input_017.outputs[99].hide = True
    group_input_017.outputs[100].hide = True
    group_input_017.outputs[101].hide = True
    group_input_017.outputs[102].hide = True
    group_input_017.outputs[103].hide = True
    group_input_017.outputs[104].hide = True
    group_input_017.outputs[105].hide = True
    group_input_017.outputs[106].hide = True
    group_input_017.outputs[107].hide = True
    group_input_017.outputs[108].hide = True
    group_input_017.outputs[109].hide = True
    group_input_017.outputs[110].hide = True
    group_input_017.outputs[111].hide = True
    group_input_017.outputs[112].hide = True
    group_input_017.outputs[113].hide = True
    group_input_017.outputs[114].hide = True
    group_input_017.outputs[115].hide = True
    group_input_017.outputs[116].hide = True
    group_input_017.outputs[117].hide = True
    group_input_017.outputs[118].hide = True
    group_input_017.outputs[119].hide = True
    group_input_017.outputs[120].hide = True
    group_input_017.outputs[121].hide = True
    group_input_017.outputs[122].hide = True
    group_input_017.outputs[123].hide = True
    group_input_017.outputs[124].hide = True
    group_input_017.outputs[125].hide = True
    group_input_017.outputs[126].hide = True
    group_input_017.outputs[127].hide = True
    group_input_017.outputs[128].hide = True
    group_input_017.outputs[129].hide = True
    group_input_017.outputs[130].hide = True
    group_input_017.outputs[131].hide = True
    group_input_017.outputs[132].hide = True
    group_input_017.outputs[135].hide = True

    # node Group.013
    group_013 = hims.nodes.new("ShaderNodeGroup")
    group_013.name = "Group.013"
    group_013.node_tree = Emission().node_tree

    # node Group.022
    group_022 = hims.nodes.new("ShaderNodeGroup")
    group_022.label = "Emission Baker"
    group_022.name = "Group.022"
    group_022.node_tree = Emission().node_tree

    # node Gamma.004
    gamma_004 = hims.nodes.new("ShaderNodeGamma")
    gamma_004.name = "Gamma.004"
    gamma_004.inputs[1].hide = True
    # Gamma
    gamma_004.inputs[1].default_value = 2.200000047683716

    # node Group Input.008
    group_input_008 = hims.nodes.new("NodeGroupInput")
    group_input_008.label = "Slot 2"
    group_input_008.name = "Group Input.008"
    group_input_008.use_custom_color = True
    group_input_008.color = (0.5, 0.5, 0.0)
    group_input_008.outputs[0].hide = True
    group_input_008.outputs[1].hide = True
    group_input_008.outputs[2].hide = True
    group_input_008.outputs[3].hide = True
    group_input_008.outputs[4].hide = True
    group_input_008.outputs[5].hide = True
    group_input_008.outputs[6].hide = True
    group_input_008.outputs[7].hide = True
    group_input_008.outputs[8].hide = True
    group_input_008.outputs[9].hide = True
    group_input_008.outputs[10].hide = True
    group_input_008.outputs[11].hide = True
    group_input_008.outputs[12].hide = True
    group_input_008.outputs[13].hide = True
    group_input_008.outputs[14].hide = True
    group_input_008.outputs[15].hide = True
    group_input_008.outputs[16].hide = True
    group_input_008.outputs[17].hide = True
    group_input_008.outputs[18].hide = True
    group_input_008.outputs[19].hide = True
    group_input_008.outputs[20].hide = True
    group_input_008.outputs[21].hide = True
    group_input_008.outputs[22].hide = True
    group_input_008.outputs[23].hide = True
    group_input_008.outputs[24].hide = True
    group_input_008.outputs[25].hide = True
    group_input_008.outputs[26].hide = True
    group_input_008.outputs[27].hide = True
    group_input_008.outputs[29].hide = True
    group_input_008.outputs[30].hide = True
    group_input_008.outputs[31].hide = True
    group_input_008.outputs[32].hide = True
    group_input_008.outputs[33].hide = True
    group_input_008.outputs[34].hide = True
    group_input_008.outputs[35].hide = True
    group_input_008.outputs[36].hide = True
    group_input_008.outputs[37].hide = True
    group_input_008.outputs[41].hide = True
    group_input_008.outputs[42].hide = True
    group_input_008.outputs[43].hide = True
    group_input_008.outputs[44].hide = True
    group_input_008.outputs[45].hide = True
    group_input_008.outputs[46].hide = True
    group_input_008.outputs[47].hide = True
    group_input_008.outputs[48].hide = True
    group_input_008.outputs[49].hide = True
    group_input_008.outputs[50].hide = True
    group_input_008.outputs[51].hide = True
    group_input_008.outputs[52].hide = True
    group_input_008.outputs[53].hide = True
    group_input_008.outputs[54].hide = True
    group_input_008.outputs[55].hide = True
    group_input_008.outputs[56].hide = True
    group_input_008.outputs[57].hide = True
    group_input_008.outputs[58].hide = True
    group_input_008.outputs[59].hide = True
    group_input_008.outputs[60].hide = True
    group_input_008.outputs[61].hide = True
    group_input_008.outputs[62].hide = True
    group_input_008.outputs[63].hide = True
    group_input_008.outputs[64].hide = True
    group_input_008.outputs[65].hide = True
    group_input_008.outputs[66].hide = True
    group_input_008.outputs[67].hide = True
    group_input_008.outputs[68].hide = True
    group_input_008.outputs[69].hide = True
    group_input_008.outputs[70].hide = True
    group_input_008.outputs[71].hide = True
    group_input_008.outputs[72].hide = True
    group_input_008.outputs[73].hide = True
    group_input_008.outputs[74].hide = True
    group_input_008.outputs[75].hide = True
    group_input_008.outputs[76].hide = True
    group_input_008.outputs[77].hide = True
    group_input_008.outputs[78].hide = True
    group_input_008.outputs[79].hide = True
    group_input_008.outputs[80].hide = True
    group_input_008.outputs[81].hide = True
    group_input_008.outputs[82].hide = True
    group_input_008.outputs[83].hide = True
    group_input_008.outputs[84].hide = True
    group_input_008.outputs[85].hide = True
    group_input_008.outputs[86].hide = True
    group_input_008.outputs[87].hide = True
    group_input_008.outputs[88].hide = True
    group_input_008.outputs[89].hide = True
    group_input_008.outputs[90].hide = True
    group_input_008.outputs[91].hide = True
    group_input_008.outputs[92].hide = True
    group_input_008.outputs[93].hide = True
    group_input_008.outputs[94].hide = True
    group_input_008.outputs[95].hide = True
    group_input_008.outputs[96].hide = True
    group_input_008.outputs[97].hide = True
    group_input_008.outputs[98].hide = True
    group_input_008.outputs[99].hide = True
    group_input_008.outputs[100].hide = True
    group_input_008.outputs[101].hide = True
    group_input_008.outputs[102].hide = True
    group_input_008.outputs[103].hide = True
    group_input_008.outputs[104].hide = True
    group_input_008.outputs[105].hide = True
    group_input_008.outputs[106].hide = True
    group_input_008.outputs[107].hide = True
    group_input_008.outputs[108].hide = True
    group_input_008.outputs[109].hide = True
    group_input_008.outputs[110].hide = True
    group_input_008.outputs[111].hide = True
    group_input_008.outputs[112].hide = True
    group_input_008.outputs[113].hide = True
    group_input_008.outputs[114].hide = True
    group_input_008.outputs[115].hide = True
    group_input_008.outputs[116].hide = True
    group_input_008.outputs[117].hide = True
    group_input_008.outputs[118].hide = True
    group_input_008.outputs[119].hide = True
    group_input_008.outputs[120].hide = True
    group_input_008.outputs[121].hide = True
    group_input_008.outputs[122].hide = True
    group_input_008.outputs[123].hide = True
    group_input_008.outputs[124].hide = True
    group_input_008.outputs[125].hide = True
    group_input_008.outputs[126].hide = True
    group_input_008.outputs[127].hide = True
    group_input_008.outputs[128].hide = True
    group_input_008.outputs[129].hide = True
    group_input_008.outputs[130].hide = True
    group_input_008.outputs[131].hide = True
    group_input_008.outputs[132].hide = True
    group_input_008.outputs[133].hide = True
    group_input_008.outputs[134].hide = True
    group_input_008.outputs[135].hide = True

    # node Mix.004
    mix_004_7 = hims.nodes.new("ShaderNodeMix")
    mix_004_7.name = "Mix.004"
    mix_004_7.blend_type = "MIX"
    mix_004_7.clamp_factor = True
    mix_004_7.clamp_result = True
    mix_004_7.data_type = "RGBA"
    mix_004_7.factor_mode = "UNIFORM"
    mix_004_7.inputs[1].hide = True
    mix_004_7.inputs[2].hide = True
    mix_004_7.inputs[3].hide = True
    mix_004_7.inputs[4].hide = True
    mix_004_7.inputs[5].hide = True
    mix_004_7.inputs[7].hide = True
    mix_004_7.outputs[0].hide = True
    mix_004_7.outputs[1].hide = True
    # Factor_Vector
    mix_004_7.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_004_7.inputs[2].default_value = 0.0
    # B_Float
    mix_004_7.inputs[3].default_value = 0.0
    # A_Vector
    mix_004_7.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_004_7.inputs[5].default_value = (0.0, 0.0, 0.0)
    # B_Color
    mix_004_7.inputs[7].default_value = (
        0.24701076745986938,
        0.24701084196567535,
        0.24701106548309326,
        1.0,
    )
    # A_Rotation
    mix_004_7.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix_004_7.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Mix.006
    mix_006_7 = hims.nodes.new("ShaderNodeMix")
    mix_006_7.name = "Mix.006"
    mix_006_7.blend_type = "MULTIPLY"
    mix_006_7.clamp_factor = True
    mix_006_7.clamp_result = True
    mix_006_7.data_type = "RGBA"
    mix_006_7.factor_mode = "UNIFORM"
    mix_006_7.inputs[1].hide = True
    mix_006_7.inputs[2].hide = True
    mix_006_7.inputs[3].hide = True
    mix_006_7.inputs[4].hide = True
    mix_006_7.inputs[5].hide = True
    mix_006_7.inputs[7].hide = True
    mix_006_7.outputs[0].hide = True
    mix_006_7.outputs[1].hide = True
    # Factor_Vector
    mix_006_7.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_006_7.inputs[2].default_value = 0.0
    # B_Float
    mix_006_7.inputs[3].default_value = 0.0
    # A_Vector
    mix_006_7.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_006_7.inputs[5].default_value = (0.0, 0.0, 0.0)
    # B_Color
    mix_006_7.inputs[7].default_value = (0.0, 0.0, 0.0, 1.0)
    # A_Rotation
    mix_006_7.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix_006_7.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Gamma.002
    gamma_002 = hims.nodes.new("ShaderNodeGamma")
    gamma_002.name = "Gamma.002"
    gamma_002.inputs[1].hide = True
    # Gamma
    gamma_002.inputs[1].default_value = 2.200000047683716

    # node Reroute.009
    reroute_009 = hims.nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    # node Reroute.066
    reroute_066 = hims.nodes.new("NodeReroute")
    reroute_066.name = "Reroute.066"
    # node Reroute.068
    reroute_068 = hims.nodes.new("NodeReroute")
    reroute_068.name = "Reroute.068"
    # node Reroute.067
    reroute_067 = hims.nodes.new("NodeReroute")
    reroute_067.name = "Reroute.067"
    # node Reroute.069
    reroute_069 = hims.nodes.new("NodeReroute")
    reroute_069.name = "Reroute.069"
    # node Reroute.070
    reroute_070 = hims.nodes.new("NodeReroute")
    reroute_070.name = "Reroute.070"
    # node Reroute.071
    reroute_071 = hims.nodes.new("NodeReroute")
    reroute_071.name = "Reroute.071"
    # node Reroute.072
    reroute_072 = hims.nodes.new("NodeReroute")
    reroute_072.name = "Reroute.072"
    # node Reroute.074
    reroute_074 = hims.nodes.new("NodeReroute")
    reroute_074.name = "Reroute.074"
    # node Reroute.073
    reroute_073 = hims.nodes.new("NodeReroute")
    reroute_073.name = "Reroute.073"
    # node Group.011
    group_011 = hims.nodes.new("ShaderNodeGroup")
    group_011.label = "Zone 5"
    group_011.name = "Group.011"
    group_011.node_tree = ColorMixer().node_tree

    # node Group Input.011
    group_input_011 = hims.nodes.new("NodeGroupInput")
    group_input_011.label = "Slot 5"
    group_input_011.name = "Group Input.011"
    group_input_011.use_custom_color = True
    group_input_011.color = (0.0, 0.5, 0.5)
    group_input_011.outputs[0].hide = True
    group_input_011.outputs[1].hide = True
    group_input_011.outputs[2].hide = True
    group_input_011.outputs[3].hide = True
    group_input_011.outputs[4].hide = True
    group_input_011.outputs[5].hide = True
    group_input_011.outputs[6].hide = True
    group_input_011.outputs[7].hide = True
    group_input_011.outputs[8].hide = True
    group_input_011.outputs[9].hide = True
    group_input_011.outputs[10].hide = True
    group_input_011.outputs[11].hide = True
    group_input_011.outputs[12].hide = True
    group_input_011.outputs[13].hide = True
    group_input_011.outputs[14].hide = True
    group_input_011.outputs[15].hide = True
    group_input_011.outputs[16].hide = True
    group_input_011.outputs[17].hide = True
    group_input_011.outputs[18].hide = True
    group_input_011.outputs[19].hide = True
    group_input_011.outputs[20].hide = True
    group_input_011.outputs[21].hide = True
    group_input_011.outputs[22].hide = True
    group_input_011.outputs[23].hide = True
    group_input_011.outputs[24].hide = True
    group_input_011.outputs[25].hide = True
    group_input_011.outputs[26].hide = True
    group_input_011.outputs[27].hide = True
    group_input_011.outputs[28].hide = True
    group_input_011.outputs[29].hide = True
    group_input_011.outputs[30].hide = True
    group_input_011.outputs[31].hide = True
    group_input_011.outputs[32].hide = True
    group_input_011.outputs[33].hide = True
    group_input_011.outputs[34].hide = True
    group_input_011.outputs[35].hide = True
    group_input_011.outputs[36].hide = True
    group_input_011.outputs[37].hide = True
    group_input_011.outputs[38].hide = True
    group_input_011.outputs[39].hide = True
    group_input_011.outputs[40].hide = True
    group_input_011.outputs[41].hide = True
    group_input_011.outputs[42].hide = True
    group_input_011.outputs[43].hide = True
    group_input_011.outputs[44].hide = True
    group_input_011.outputs[45].hide = True
    group_input_011.outputs[46].hide = True
    group_input_011.outputs[47].hide = True
    group_input_011.outputs[48].hide = True
    group_input_011.outputs[49].hide = True
    group_input_011.outputs[50].hide = True
    group_input_011.outputs[51].hide = True
    group_input_011.outputs[52].hide = True
    group_input_011.outputs[53].hide = True
    group_input_011.outputs[54].hide = True
    group_input_011.outputs[55].hide = True
    group_input_011.outputs[56].hide = True
    group_input_011.outputs[57].hide = True
    group_input_011.outputs[58].hide = True
    group_input_011.outputs[59].hide = True
    group_input_011.outputs[60].hide = True
    group_input_011.outputs[61].hide = True
    group_input_011.outputs[62].hide = True
    group_input_011.outputs[63].hide = True
    group_input_011.outputs[64].hide = True
    group_input_011.outputs[65].hide = True
    group_input_011.outputs[66].hide = True
    group_input_011.outputs[67].hide = True
    group_input_011.outputs[68].hide = True
    group_input_011.outputs[69].hide = True
    group_input_011.outputs[70].hide = True
    group_input_011.outputs[71].hide = True
    group_input_011.outputs[72].hide = True
    group_input_011.outputs[73].hide = True
    group_input_011.outputs[74].hide = True
    group_input_011.outputs[76].hide = True
    group_input_011.outputs[77].hide = True
    group_input_011.outputs[78].hide = True
    group_input_011.outputs[79].hide = True
    group_input_011.outputs[80].hide = True
    group_input_011.outputs[81].hide = True
    group_input_011.outputs[82].hide = True
    group_input_011.outputs[83].hide = True
    group_input_011.outputs[84].hide = True
    group_input_011.outputs[88].hide = True
    group_input_011.outputs[89].hide = True
    group_input_011.outputs[90].hide = True
    group_input_011.outputs[91].hide = True
    group_input_011.outputs[92].hide = True
    group_input_011.outputs[93].hide = True
    group_input_011.outputs[94].hide = True
    group_input_011.outputs[95].hide = True
    group_input_011.outputs[96].hide = True
    group_input_011.outputs[97].hide = True
    group_input_011.outputs[98].hide = True
    group_input_011.outputs[99].hide = True
    group_input_011.outputs[100].hide = True
    group_input_011.outputs[101].hide = True
    group_input_011.outputs[102].hide = True
    group_input_011.outputs[103].hide = True
    group_input_011.outputs[104].hide = True
    group_input_011.outputs[105].hide = True
    group_input_011.outputs[106].hide = True
    group_input_011.outputs[107].hide = True
    group_input_011.outputs[108].hide = True
    group_input_011.outputs[109].hide = True
    group_input_011.outputs[110].hide = True
    group_input_011.outputs[111].hide = True
    group_input_011.outputs[112].hide = True
    group_input_011.outputs[113].hide = True
    group_input_011.outputs[114].hide = True
    group_input_011.outputs[115].hide = True
    group_input_011.outputs[116].hide = True
    group_input_011.outputs[117].hide = True
    group_input_011.outputs[118].hide = True
    group_input_011.outputs[119].hide = True
    group_input_011.outputs[120].hide = True
    group_input_011.outputs[121].hide = True
    group_input_011.outputs[122].hide = True
    group_input_011.outputs[123].hide = True
    group_input_011.outputs[124].hide = True
    group_input_011.outputs[125].hide = True
    group_input_011.outputs[126].hide = True
    group_input_011.outputs[127].hide = True
    group_input_011.outputs[128].hide = True
    group_input_011.outputs[129].hide = True
    group_input_011.outputs[130].hide = True
    group_input_011.outputs[131].hide = True
    group_input_011.outputs[132].hide = True
    group_input_011.outputs[133].hide = True
    group_input_011.outputs[134].hide = True
    group_input_011.outputs[135].hide = True

    # node Group.010
    group_010 = hims.nodes.new("ShaderNodeGroup")
    group_010.label = "Zone 4"
    group_010.name = "Group.010"
    group_010.node_tree = ColorMixer().node_tree

    # node Group Input.010
    group_input_010 = hims.nodes.new("NodeGroupInput")
    group_input_010.label = "Slot 4"
    group_input_010.name = "Group Input.010"
    group_input_010.use_custom_color = True
    group_input_010.color = (0.0, 0.0, 1.0)
    group_input_010.outputs[0].hide = True
    group_input_010.outputs[1].hide = True
    group_input_010.outputs[2].hide = True
    group_input_010.outputs[3].hide = True
    group_input_010.outputs[4].hide = True
    group_input_010.outputs[5].hide = True
    group_input_010.outputs[6].hide = True
    group_input_010.outputs[7].hide = True
    group_input_010.outputs[8].hide = True
    group_input_010.outputs[9].hide = True
    group_input_010.outputs[10].hide = True
    group_input_010.outputs[11].hide = True
    group_input_010.outputs[12].hide = True
    group_input_010.outputs[13].hide = True
    group_input_010.outputs[14].hide = True
    group_input_010.outputs[15].hide = True
    group_input_010.outputs[16].hide = True
    group_input_010.outputs[17].hide = True
    group_input_010.outputs[18].hide = True
    group_input_010.outputs[19].hide = True
    group_input_010.outputs[20].hide = True
    group_input_010.outputs[21].hide = True
    group_input_010.outputs[22].hide = True
    group_input_010.outputs[23].hide = True
    group_input_010.outputs[24].hide = True
    group_input_010.outputs[25].hide = True
    group_input_010.outputs[26].hide = True
    group_input_010.outputs[27].hide = True
    group_input_010.outputs[28].hide = True
    group_input_010.outputs[29].hide = True
    group_input_010.outputs[30].hide = True
    group_input_010.outputs[31].hide = True
    group_input_010.outputs[32].hide = True
    group_input_010.outputs[33].hide = True
    group_input_010.outputs[34].hide = True
    group_input_010.outputs[35].hide = True
    group_input_010.outputs[36].hide = True
    group_input_010.outputs[37].hide = True
    group_input_010.outputs[38].hide = True
    group_input_010.outputs[39].hide = True
    group_input_010.outputs[40].hide = True
    group_input_010.outputs[41].hide = True
    group_input_010.outputs[42].hide = True
    group_input_010.outputs[43].hide = True
    group_input_010.outputs[44].hide = True
    group_input_010.outputs[45].hide = True
    group_input_010.outputs[46].hide = True
    group_input_010.outputs[47].hide = True
    group_input_010.outputs[48].hide = True
    group_input_010.outputs[49].hide = True
    group_input_010.outputs[50].hide = True
    group_input_010.outputs[51].hide = True
    group_input_010.outputs[52].hide = True
    group_input_010.outputs[53].hide = True
    group_input_010.outputs[54].hide = True
    group_input_010.outputs[55].hide = True
    group_input_010.outputs[56].hide = True
    group_input_010.outputs[57].hide = True
    group_input_010.outputs[58].hide = True
    group_input_010.outputs[60].hide = True
    group_input_010.outputs[61].hide = True
    group_input_010.outputs[62].hide = True
    group_input_010.outputs[63].hide = True
    group_input_010.outputs[64].hide = True
    group_input_010.outputs[65].hide = True
    group_input_010.outputs[66].hide = True
    group_input_010.outputs[67].hide = True
    group_input_010.outputs[68].hide = True
    group_input_010.outputs[72].hide = True
    group_input_010.outputs[73].hide = True
    group_input_010.outputs[74].hide = True
    group_input_010.outputs[75].hide = True
    group_input_010.outputs[76].hide = True
    group_input_010.outputs[77].hide = True
    group_input_010.outputs[78].hide = True
    group_input_010.outputs[79].hide = True
    group_input_010.outputs[80].hide = True
    group_input_010.outputs[81].hide = True
    group_input_010.outputs[82].hide = True
    group_input_010.outputs[83].hide = True
    group_input_010.outputs[84].hide = True
    group_input_010.outputs[85].hide = True
    group_input_010.outputs[86].hide = True
    group_input_010.outputs[87].hide = True
    group_input_010.outputs[88].hide = True
    group_input_010.outputs[89].hide = True
    group_input_010.outputs[90].hide = True
    group_input_010.outputs[91].hide = True
    group_input_010.outputs[92].hide = True
    group_input_010.outputs[93].hide = True
    group_input_010.outputs[94].hide = True
    group_input_010.outputs[95].hide = True
    group_input_010.outputs[96].hide = True
    group_input_010.outputs[97].hide = True
    group_input_010.outputs[98].hide = True
    group_input_010.outputs[99].hide = True
    group_input_010.outputs[100].hide = True
    group_input_010.outputs[101].hide = True
    group_input_010.outputs[102].hide = True
    group_input_010.outputs[103].hide = True
    group_input_010.outputs[104].hide = True
    group_input_010.outputs[105].hide = True
    group_input_010.outputs[106].hide = True
    group_input_010.outputs[107].hide = True
    group_input_010.outputs[108].hide = True
    group_input_010.outputs[109].hide = True
    group_input_010.outputs[110].hide = True
    group_input_010.outputs[111].hide = True
    group_input_010.outputs[112].hide = True
    group_input_010.outputs[113].hide = True
    group_input_010.outputs[114].hide = True
    group_input_010.outputs[115].hide = True
    group_input_010.outputs[116].hide = True
    group_input_010.outputs[117].hide = True
    group_input_010.outputs[118].hide = True
    group_input_010.outputs[119].hide = True
    group_input_010.outputs[120].hide = True
    group_input_010.outputs[121].hide = True
    group_input_010.outputs[122].hide = True
    group_input_010.outputs[123].hide = True
    group_input_010.outputs[124].hide = True
    group_input_010.outputs[125].hide = True
    group_input_010.outputs[126].hide = True
    group_input_010.outputs[127].hide = True
    group_input_010.outputs[128].hide = True
    group_input_010.outputs[129].hide = True
    group_input_010.outputs[130].hide = True
    group_input_010.outputs[131].hide = True
    group_input_010.outputs[132].hide = True
    group_input_010.outputs[133].hide = True
    group_input_010.outputs[134].hide = True
    group_input_010.outputs[135].hide = True

    # node Reroute.058
    reroute_058 = hims.nodes.new("NodeReroute")
    reroute_058.name = "Reroute.058"
    # node Bump.001
    bump_001 = hims.nodes.new("ShaderNodeBump")
    bump_001.name = "Bump.001"
    bump_001.invert = False
    bump_001.inputs[0].hide = True
    bump_001.inputs[1].hide = True
    # Strength
    bump_001.inputs[0].default_value = 1.0
    # Distance
    bump_001.inputs[1].default_value = 0.007499999832361937

    # node Group Output
    group_output_17 = hims.nodes.new("NodeGroupOutput")
    group_output_17.name = "Group Output"
    group_output_17.is_active_output = True
    group_output_17.inputs[12].hide = True

    # node Group Input.026
    group_input_026 = hims.nodes.new("NodeGroupInput")
    group_input_026.name = "Group Input.026"
    group_input_026.outputs[1].hide = True
    group_input_026.outputs[2].hide = True
    group_input_026.outputs[3].hide = True
    group_input_026.outputs[4].hide = True
    group_input_026.outputs[5].hide = True
    group_input_026.outputs[6].hide = True
    group_input_026.outputs[8].hide = True
    group_input_026.outputs[9].hide = True
    group_input_026.outputs[10].hide = True
    group_input_026.outputs[11].hide = True
    group_input_026.outputs[12].hide = True
    group_input_026.outputs[13].hide = True
    group_input_026.outputs[14].hide = True
    group_input_026.outputs[15].hide = True
    group_input_026.outputs[16].hide = True
    group_input_026.outputs[17].hide = True
    group_input_026.outputs[18].hide = True
    group_input_026.outputs[19].hide = True
    group_input_026.outputs[20].hide = True
    group_input_026.outputs[22].hide = True
    group_input_026.outputs[23].hide = True
    group_input_026.outputs[24].hide = True
    group_input_026.outputs[25].hide = True
    group_input_026.outputs[26].hide = True
    group_input_026.outputs[27].hide = True
    group_input_026.outputs[28].hide = True
    group_input_026.outputs[29].hide = True
    group_input_026.outputs[30].hide = True
    group_input_026.outputs[31].hide = True
    group_input_026.outputs[32].hide = True
    group_input_026.outputs[33].hide = True
    group_input_026.outputs[34].hide = True
    group_input_026.outputs[35].hide = True
    group_input_026.outputs[37].hide = True
    group_input_026.outputs[38].hide = True
    group_input_026.outputs[39].hide = True
    group_input_026.outputs[40].hide = True
    group_input_026.outputs[41].hide = True
    group_input_026.outputs[42].hide = True
    group_input_026.outputs[43].hide = True
    group_input_026.outputs[44].hide = True
    group_input_026.outputs[45].hide = True
    group_input_026.outputs[46].hide = True
    group_input_026.outputs[47].hide = True
    group_input_026.outputs[48].hide = True
    group_input_026.outputs[49].hide = True
    group_input_026.outputs[50].hide = True
    group_input_026.outputs[52].hide = True
    group_input_026.outputs[53].hide = True
    group_input_026.outputs[54].hide = True
    group_input_026.outputs[55].hide = True
    group_input_026.outputs[56].hide = True
    group_input_026.outputs[57].hide = True
    group_input_026.outputs[58].hide = True
    group_input_026.outputs[59].hide = True
    group_input_026.outputs[60].hide = True
    group_input_026.outputs[61].hide = True
    group_input_026.outputs[62].hide = True
    group_input_026.outputs[63].hide = True
    group_input_026.outputs[64].hide = True
    group_input_026.outputs[65].hide = True
    group_input_026.outputs[66].hide = True
    group_input_026.outputs[68].hide = True
    group_input_026.outputs[69].hide = True
    group_input_026.outputs[70].hide = True
    group_input_026.outputs[71].hide = True
    group_input_026.outputs[72].hide = True
    group_input_026.outputs[73].hide = True
    group_input_026.outputs[74].hide = True
    group_input_026.outputs[75].hide = True
    group_input_026.outputs[76].hide = True
    group_input_026.outputs[77].hide = True
    group_input_026.outputs[78].hide = True
    group_input_026.outputs[79].hide = True
    group_input_026.outputs[80].hide = True
    group_input_026.outputs[81].hide = True
    group_input_026.outputs[82].hide = True
    group_input_026.outputs[84].hide = True
    group_input_026.outputs[85].hide = True
    group_input_026.outputs[86].hide = True
    group_input_026.outputs[87].hide = True
    group_input_026.outputs[88].hide = True
    group_input_026.outputs[89].hide = True
    group_input_026.outputs[90].hide = True
    group_input_026.outputs[91].hide = True
    group_input_026.outputs[92].hide = True
    group_input_026.outputs[93].hide = True
    group_input_026.outputs[94].hide = True
    group_input_026.outputs[95].hide = True
    group_input_026.outputs[96].hide = True
    group_input_026.outputs[97].hide = True
    group_input_026.outputs[98].hide = True
    group_input_026.outputs[100].hide = True
    group_input_026.outputs[101].hide = True
    group_input_026.outputs[102].hide = True
    group_input_026.outputs[103].hide = True
    group_input_026.outputs[104].hide = True
    group_input_026.outputs[105].hide = True
    group_input_026.outputs[106].hide = True
    group_input_026.outputs[107].hide = True
    group_input_026.outputs[108].hide = True
    group_input_026.outputs[109].hide = True
    group_input_026.outputs[110].hide = True
    group_input_026.outputs[111].hide = True
    group_input_026.outputs[112].hide = True
    group_input_026.outputs[113].hide = True
    group_input_026.outputs[114].hide = True
    group_input_026.outputs[116].hide = True
    group_input_026.outputs[117].hide = True
    group_input_026.outputs[118].hide = True
    group_input_026.outputs[119].hide = True
    group_input_026.outputs[120].hide = True
    group_input_026.outputs[121].hide = True
    group_input_026.outputs[122].hide = True
    group_input_026.outputs[123].hide = True
    group_input_026.outputs[124].hide = True
    group_input_026.outputs[125].hide = True
    group_input_026.outputs[126].hide = True
    group_input_026.outputs[128].hide = True
    group_input_026.outputs[129].hide = True
    group_input_026.outputs[130].hide = True
    group_input_026.outputs[131].hide = True
    group_input_026.outputs[132].hide = True
    group_input_026.outputs[133].hide = True
    group_input_026.outputs[134].hide = True
    group_input_026.outputs[135].hide = True

    # node Reroute.075
    reroute_075 = hims.nodes.new("NodeReroute")
    reroute_075.name = "Reroute.075"
    # node Reroute.007
    reroute_007_3 = hims.nodes.new("NodeReroute")
    reroute_007_3.name = "Reroute.007"
    # node Reroute.076
    reroute_076 = hims.nodes.new("NodeReroute")
    reroute_076.name = "Reroute.076"
    # node Reroute.077
    reroute_077 = hims.nodes.new("NodeReroute")
    reroute_077.name = "Reroute.077"
    # node Reroute.078
    reroute_078 = hims.nodes.new("NodeReroute")
    reroute_078.name = "Reroute.078"
    # node Reroute.005
    reroute_005_4 = hims.nodes.new("NodeReroute")
    reroute_005_4.name = "Reroute.005"
    # node Reroute.079
    reroute_079 = hims.nodes.new("NodeReroute")
    reroute_079.name = "Reroute.079"
    # node Reroute.008
    reroute_008 = hims.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    # node Reroute.052
    reroute_052 = hims.nodes.new("NodeReroute")
    reroute_052.name = "Reroute.052"
    # node Gamma.003
    gamma_003 = hims.nodes.new("ShaderNodeGamma")
    gamma_003.name = "Gamma.003"
    gamma_003.inputs[1].hide = True
    # Gamma
    gamma_003.inputs[1].default_value = 2.200000047683716

    # node Reroute.048
    reroute_048 = hims.nodes.new("NodeReroute")
    reroute_048.name = "Reroute.048"
    # node Reroute.046
    reroute_046 = hims.nodes.new("NodeReroute")
    reroute_046.name = "Reroute.046"
    # node Mix
    mix_11 = hims.nodes.new("ShaderNodeMix")
    mix_11.name = "Mix"
    mix_11.blend_type = "MULTIPLY"
    mix_11.clamp_factor = True
    mix_11.clamp_result = False
    mix_11.data_type = "RGBA"
    mix_11.factor_mode = "UNIFORM"
    mix_11.inputs[0].hide = True
    mix_11.inputs[1].hide = True
    mix_11.inputs[2].hide = True
    mix_11.inputs[3].hide = True
    mix_11.inputs[4].hide = True
    mix_11.inputs[5].hide = True
    mix_11.outputs[0].hide = True
    mix_11.outputs[1].hide = True
    # Factor_Float
    mix_11.inputs[0].default_value = 1.0
    # Factor_Vector
    mix_11.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_11.inputs[2].default_value = 0.0
    # B_Float
    mix_11.inputs[3].default_value = 0.0
    # A_Vector
    mix_11.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_11.inputs[5].default_value = (0.0, 0.0, 0.0)
    # A_Rotation
    mix_11.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix_11.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Math.001
    math_001_4 = hims.nodes.new("ShaderNodeMath")
    math_001_4.name = "Math.001"
    math_001_4.operation = "POWER"
    math_001_4.use_clamp = False
    math_001_4.inputs[2].hide = True
    # Value_002
    math_001_4.inputs[2].default_value = 0.5

    # node Reroute.080
    reroute_080 = hims.nodes.new("NodeReroute")
    reroute_080.name = "Reroute.080"
    # node Reroute.083
    reroute_083 = hims.nodes.new("NodeReroute")
    reroute_083.name = "Reroute.083"
    # node Reroute.084
    reroute_084 = hims.nodes.new("NodeReroute")
    reroute_084.name = "Reroute.084"
    # node Reroute.081
    reroute_081 = hims.nodes.new("NodeReroute")
    reroute_081.name = "Reroute.081"
    # node Reroute.017
    reroute_017 = hims.nodes.new("NodeReroute")
    reroute_017.name = "Reroute.017"
    # node Math.007
    math_007_1 = hims.nodes.new("ShaderNodeMath")
    math_007_1.name = "Math.007"
    math_007_1.operation = "SUBTRACT"
    math_007_1.use_clamp = False
    math_007_1.inputs[0].hide = True
    math_007_1.inputs[2].hide = True
    # Value
    math_007_1.inputs[0].default_value = 1.0
    # Value_002
    math_007_1.inputs[2].default_value = 0.5

    # node Gamma.001
    gamma_001 = hims.nodes.new("ShaderNodeGamma")
    gamma_001.name = "Gamma.001"
    gamma_001.inputs[1].hide = True
    # Gamma
    gamma_001.inputs[1].default_value = 2.200000047683716

    # node Combine Color
    combine_color = hims.nodes.new("ShaderNodeCombineColor")
    combine_color.name = "Combine Color"
    combine_color.mode = "RGB"
    combine_color.inputs[2].hide = True
    # Blue
    combine_color.inputs[2].default_value = 0.0

    # node Group Input.005
    group_input_005 = hims.nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.outputs[1].hide = True
    group_input_005.outputs[2].hide = True
    group_input_005.outputs[3].hide = True
    group_input_005.outputs[4].hide = True
    group_input_005.outputs[5].hide = True
    group_input_005.outputs[6].hide = True
    group_input_005.outputs[8].hide = True
    group_input_005.outputs[9].hide = True
    group_input_005.outputs[10].hide = True
    group_input_005.outputs[11].hide = True
    group_input_005.outputs[12].hide = True
    group_input_005.outputs[13].hide = True
    group_input_005.outputs[14].hide = True
    group_input_005.outputs[15].hide = True
    group_input_005.outputs[16].hide = True
    group_input_005.outputs[17].hide = True
    group_input_005.outputs[18].hide = True
    group_input_005.outputs[19].hide = True
    group_input_005.outputs[20].hide = True
    group_input_005.outputs[21].hide = True
    group_input_005.outputs[22].hide = True
    group_input_005.outputs[23].hide = True
    group_input_005.outputs[24].hide = True
    group_input_005.outputs[25].hide = True
    group_input_005.outputs[27].hide = True
    group_input_005.outputs[28].hide = True
    group_input_005.outputs[29].hide = True
    group_input_005.outputs[30].hide = True
    group_input_005.outputs[31].hide = True
    group_input_005.outputs[32].hide = True
    group_input_005.outputs[33].hide = True
    group_input_005.outputs[34].hide = True
    group_input_005.outputs[35].hide = True
    group_input_005.outputs[36].hide = True
    group_input_005.outputs[37].hide = True
    group_input_005.outputs[38].hide = True
    group_input_005.outputs[39].hide = True
    group_input_005.outputs[40].hide = True
    group_input_005.outputs[42].hide = True
    group_input_005.outputs[43].hide = True
    group_input_005.outputs[44].hide = True
    group_input_005.outputs[45].hide = True
    group_input_005.outputs[46].hide = True
    group_input_005.outputs[47].hide = True
    group_input_005.outputs[48].hide = True
    group_input_005.outputs[49].hide = True
    group_input_005.outputs[50].hide = True
    group_input_005.outputs[51].hide = True
    group_input_005.outputs[52].hide = True
    group_input_005.outputs[53].hide = True
    group_input_005.outputs[54].hide = True
    group_input_005.outputs[55].hide = True
    group_input_005.outputs[57].hide = True
    group_input_005.outputs[58].hide = True
    group_input_005.outputs[59].hide = True
    group_input_005.outputs[60].hide = True
    group_input_005.outputs[61].hide = True
    group_input_005.outputs[62].hide = True
    group_input_005.outputs[63].hide = True
    group_input_005.outputs[64].hide = True
    group_input_005.outputs[65].hide = True
    group_input_005.outputs[66].hide = True
    group_input_005.outputs[67].hide = True
    group_input_005.outputs[68].hide = True
    group_input_005.outputs[69].hide = True
    group_input_005.outputs[70].hide = True
    group_input_005.outputs[71].hide = True
    group_input_005.outputs[73].hide = True
    group_input_005.outputs[74].hide = True
    group_input_005.outputs[75].hide = True
    group_input_005.outputs[76].hide = True
    group_input_005.outputs[77].hide = True
    group_input_005.outputs[78].hide = True
    group_input_005.outputs[79].hide = True
    group_input_005.outputs[80].hide = True
    group_input_005.outputs[81].hide = True
    group_input_005.outputs[82].hide = True
    group_input_005.outputs[83].hide = True
    group_input_005.outputs[84].hide = True
    group_input_005.outputs[85].hide = True
    group_input_005.outputs[86].hide = True
    group_input_005.outputs[87].hide = True
    group_input_005.outputs[89].hide = True
    group_input_005.outputs[90].hide = True
    group_input_005.outputs[91].hide = True
    group_input_005.outputs[92].hide = True
    group_input_005.outputs[93].hide = True
    group_input_005.outputs[94].hide = True
    group_input_005.outputs[95].hide = True
    group_input_005.outputs[96].hide = True
    group_input_005.outputs[97].hide = True
    group_input_005.outputs[98].hide = True
    group_input_005.outputs[99].hide = True
    group_input_005.outputs[100].hide = True
    group_input_005.outputs[101].hide = True
    group_input_005.outputs[102].hide = True
    group_input_005.outputs[103].hide = True
    group_input_005.outputs[105].hide = True
    group_input_005.outputs[106].hide = True
    group_input_005.outputs[107].hide = True
    group_input_005.outputs[108].hide = True
    group_input_005.outputs[109].hide = True
    group_input_005.outputs[110].hide = True
    group_input_005.outputs[111].hide = True
    group_input_005.outputs[112].hide = True
    group_input_005.outputs[113].hide = True
    group_input_005.outputs[114].hide = True
    group_input_005.outputs[115].hide = True
    group_input_005.outputs[116].hide = True
    group_input_005.outputs[117].hide = True
    group_input_005.outputs[118].hide = True
    group_input_005.outputs[119].hide = True
    group_input_005.outputs[121].hide = True
    group_input_005.outputs[122].hide = True
    group_input_005.outputs[123].hide = True
    group_input_005.outputs[124].hide = True
    group_input_005.outputs[125].hide = True
    group_input_005.outputs[126].hide = True
    group_input_005.outputs[127].hide = True
    group_input_005.outputs[128].hide = True
    group_input_005.outputs[129].hide = True
    group_input_005.outputs[130].hide = True
    group_input_005.outputs[131].hide = True
    group_input_005.outputs[132].hide = True
    group_input_005.outputs[133].hide = True
    group_input_005.outputs[134].hide = True
    group_input_005.outputs[135].hide = True

    # node Group.009
    group_009 = hims.nodes.new("ShaderNodeGroup")
    group_009.label = "Roughness"
    group_009.name = "Group.009"
    group_009.node_tree = InfiniteMatts().node_tree

    # node Group.001
    group_001_4 = hims.nodes.new("ShaderNodeGroup")
    group_001_4.label = "Metalness"
    group_001_4.name = "Group.001"
    group_001_4.node_tree = InfiniteMatts().node_tree

    # node Group.014
    group_014 = hims.nodes.new("ShaderNodeGroup")
    group_014.label = "Scratch Color"
    group_014.name = "Group.014"
    group_014.node_tree = InfiniteMaskingSorterNoGrimeCol().node_tree
    # node Group.003
    group_003 = hims.nodes.new("ShaderNodeGroup")
    group_003.name = "Group.003"
    group_003.node_tree = MaskToggles()

    # node Group Input.016
    group_input_016 = hims.nodes.new("NodeGroupInput")
    group_input_016.name = "Group Input.016"
    group_input_016.outputs[1].hide = True
    group_input_016.outputs[2].hide = True
    group_input_016.outputs[3].hide = True
    group_input_016.outputs[4].hide = True
    group_input_016.outputs[5].hide = True
    group_input_016.outputs[6].hide = True
    group_input_016.outputs[8].hide = True
    group_input_016.outputs[9].hide = True
    group_input_016.outputs[10].hide = True
    group_input_016.outputs[11].hide = True
    group_input_016.outputs[12].hide = True
    group_input_016.outputs[13].hide = True
    group_input_016.outputs[14].hide = True
    group_input_016.outputs[15].hide = True
    group_input_016.outputs[16].hide = True
    group_input_016.outputs[17].hide = True
    group_input_016.outputs[18].hide = True
    group_input_016.outputs[20].hide = True
    group_input_016.outputs[21].hide = True
    group_input_016.outputs[22].hide = True
    group_input_016.outputs[23].hide = True
    group_input_016.outputs[24].hide = True
    group_input_016.outputs[25].hide = True
    group_input_016.outputs[26].hide = True
    group_input_016.outputs[27].hide = True
    group_input_016.outputs[28].hide = True
    group_input_016.outputs[29].hide = True
    group_input_016.outputs[30].hide = True
    group_input_016.outputs[31].hide = True
    group_input_016.outputs[32].hide = True
    group_input_016.outputs[33].hide = True
    group_input_016.outputs[35].hide = True
    group_input_016.outputs[36].hide = True
    group_input_016.outputs[37].hide = True
    group_input_016.outputs[38].hide = True
    group_input_016.outputs[39].hide = True
    group_input_016.outputs[40].hide = True
    group_input_016.outputs[41].hide = True
    group_input_016.outputs[42].hide = True
    group_input_016.outputs[43].hide = True
    group_input_016.outputs[44].hide = True
    group_input_016.outputs[45].hide = True
    group_input_016.outputs[46].hide = True
    group_input_016.outputs[47].hide = True
    group_input_016.outputs[48].hide = True
    group_input_016.outputs[50].hide = True
    group_input_016.outputs[51].hide = True
    group_input_016.outputs[52].hide = True
    group_input_016.outputs[53].hide = True
    group_input_016.outputs[54].hide = True
    group_input_016.outputs[55].hide = True
    group_input_016.outputs[56].hide = True
    group_input_016.outputs[57].hide = True
    group_input_016.outputs[58].hide = True
    group_input_016.outputs[59].hide = True
    group_input_016.outputs[60].hide = True
    group_input_016.outputs[61].hide = True
    group_input_016.outputs[62].hide = True
    group_input_016.outputs[63].hide = True
    group_input_016.outputs[64].hide = True
    group_input_016.outputs[66].hide = True
    group_input_016.outputs[67].hide = True
    group_input_016.outputs[68].hide = True
    group_input_016.outputs[69].hide = True
    group_input_016.outputs[70].hide = True
    group_input_016.outputs[71].hide = True
    group_input_016.outputs[72].hide = True
    group_input_016.outputs[73].hide = True
    group_input_016.outputs[74].hide = True
    group_input_016.outputs[75].hide = True
    group_input_016.outputs[76].hide = True
    group_input_016.outputs[77].hide = True
    group_input_016.outputs[78].hide = True
    group_input_016.outputs[79].hide = True
    group_input_016.outputs[80].hide = True
    group_input_016.outputs[82].hide = True
    group_input_016.outputs[83].hide = True
    group_input_016.outputs[84].hide = True
    group_input_016.outputs[85].hide = True
    group_input_016.outputs[86].hide = True
    group_input_016.outputs[87].hide = True
    group_input_016.outputs[88].hide = True
    group_input_016.outputs[89].hide = True
    group_input_016.outputs[90].hide = True
    group_input_016.outputs[91].hide = True
    group_input_016.outputs[92].hide = True
    group_input_016.outputs[93].hide = True
    group_input_016.outputs[94].hide = True
    group_input_016.outputs[95].hide = True
    group_input_016.outputs[96].hide = True
    group_input_016.outputs[98].hide = True
    group_input_016.outputs[99].hide = True
    group_input_016.outputs[100].hide = True
    group_input_016.outputs[101].hide = True
    group_input_016.outputs[102].hide = True
    group_input_016.outputs[103].hide = True
    group_input_016.outputs[104].hide = True
    group_input_016.outputs[105].hide = True
    group_input_016.outputs[106].hide = True
    group_input_016.outputs[107].hide = True
    group_input_016.outputs[108].hide = True
    group_input_016.outputs[109].hide = True
    group_input_016.outputs[110].hide = True
    group_input_016.outputs[111].hide = True
    group_input_016.outputs[112].hide = True
    group_input_016.outputs[114].hide = True
    group_input_016.outputs[115].hide = True
    group_input_016.outputs[116].hide = True
    group_input_016.outputs[117].hide = True
    group_input_016.outputs[118].hide = True
    group_input_016.outputs[119].hide = True
    group_input_016.outputs[120].hide = True
    group_input_016.outputs[121].hide = True
    group_input_016.outputs[122].hide = True
    group_input_016.outputs[123].hide = True
    group_input_016.outputs[124].hide = True
    group_input_016.outputs[126].hide = True
    group_input_016.outputs[127].hide = True
    group_input_016.outputs[128].hide = True
    group_input_016.outputs[129].hide = True
    group_input_016.outputs[130].hide = True
    group_input_016.outputs[131].hide = True
    group_input_016.outputs[132].hide = True
    group_input_016.outputs[133].hide = True
    group_input_016.outputs[134].hide = True
    group_input_016.outputs[135].hide = True

    # node Group Input.012
    group_input_012 = hims.nodes.new("NodeGroupInput")
    group_input_012.label = "Slot 6"
    group_input_012.name = "Group Input.012"
    group_input_012.use_custom_color = True
    group_input_012.color = (0.5, 0.5, 0.5)
    group_input_012.outputs[0].hide = True
    group_input_012.outputs[1].hide = True
    group_input_012.outputs[2].hide = True
    group_input_012.outputs[3].hide = True
    group_input_012.outputs[4].hide = True
    group_input_012.outputs[5].hide = True
    group_input_012.outputs[6].hide = True
    group_input_012.outputs[7].hide = True
    group_input_012.outputs[8].hide = True
    group_input_012.outputs[9].hide = True
    group_input_012.outputs[10].hide = True
    group_input_012.outputs[11].hide = True
    group_input_012.outputs[12].hide = True
    group_input_012.outputs[13].hide = True
    group_input_012.outputs[14].hide = True
    group_input_012.outputs[15].hide = True
    group_input_012.outputs[16].hide = True
    group_input_012.outputs[17].hide = True
    group_input_012.outputs[18].hide = True
    group_input_012.outputs[19].hide = True
    group_input_012.outputs[20].hide = True
    group_input_012.outputs[21].hide = True
    group_input_012.outputs[22].hide = True
    group_input_012.outputs[23].hide = True
    group_input_012.outputs[24].hide = True
    group_input_012.outputs[25].hide = True
    group_input_012.outputs[26].hide = True
    group_input_012.outputs[27].hide = True
    group_input_012.outputs[28].hide = True
    group_input_012.outputs[29].hide = True
    group_input_012.outputs[30].hide = True
    group_input_012.outputs[31].hide = True
    group_input_012.outputs[32].hide = True
    group_input_012.outputs[33].hide = True
    group_input_012.outputs[34].hide = True
    group_input_012.outputs[35].hide = True
    group_input_012.outputs[36].hide = True
    group_input_012.outputs[37].hide = True
    group_input_012.outputs[38].hide = True
    group_input_012.outputs[39].hide = True
    group_input_012.outputs[40].hide = True
    group_input_012.outputs[41].hide = True
    group_input_012.outputs[42].hide = True
    group_input_012.outputs[43].hide = True
    group_input_012.outputs[44].hide = True
    group_input_012.outputs[45].hide = True
    group_input_012.outputs[46].hide = True
    group_input_012.outputs[47].hide = True
    group_input_012.outputs[48].hide = True
    group_input_012.outputs[49].hide = True
    group_input_012.outputs[50].hide = True
    group_input_012.outputs[51].hide = True
    group_input_012.outputs[52].hide = True
    group_input_012.outputs[53].hide = True
    group_input_012.outputs[54].hide = True
    group_input_012.outputs[55].hide = True
    group_input_012.outputs[56].hide = True
    group_input_012.outputs[57].hide = True
    group_input_012.outputs[58].hide = True
    group_input_012.outputs[59].hide = True
    group_input_012.outputs[60].hide = True
    group_input_012.outputs[61].hide = True
    group_input_012.outputs[62].hide = True
    group_input_012.outputs[63].hide = True
    group_input_012.outputs[64].hide = True
    group_input_012.outputs[65].hide = True
    group_input_012.outputs[66].hide = True
    group_input_012.outputs[67].hide = True
    group_input_012.outputs[68].hide = True
    group_input_012.outputs[69].hide = True
    group_input_012.outputs[70].hide = True
    group_input_012.outputs[71].hide = True
    group_input_012.outputs[72].hide = True
    group_input_012.outputs[73].hide = True
    group_input_012.outputs[74].hide = True
    group_input_012.outputs[75].hide = True
    group_input_012.outputs[76].hide = True
    group_input_012.outputs[77].hide = True
    group_input_012.outputs[78].hide = True
    group_input_012.outputs[79].hide = True
    group_input_012.outputs[80].hide = True
    group_input_012.outputs[81].hide = True
    group_input_012.outputs[82].hide = True
    group_input_012.outputs[83].hide = True
    group_input_012.outputs[84].hide = True
    group_input_012.outputs[85].hide = True
    group_input_012.outputs[86].hide = True
    group_input_012.outputs[87].hide = True
    group_input_012.outputs[88].hide = True
    group_input_012.outputs[89].hide = True
    group_input_012.outputs[90].hide = True
    group_input_012.outputs[92].hide = True
    group_input_012.outputs[93].hide = True
    group_input_012.outputs[94].hide = True
    group_input_012.outputs[95].hide = True
    group_input_012.outputs[96].hide = True
    group_input_012.outputs[97].hide = True
    group_input_012.outputs[98].hide = True
    group_input_012.outputs[99].hide = True
    group_input_012.outputs[100].hide = True
    group_input_012.outputs[104].hide = True
    group_input_012.outputs[105].hide = True
    group_input_012.outputs[106].hide = True
    group_input_012.outputs[107].hide = True
    group_input_012.outputs[108].hide = True
    group_input_012.outputs[109].hide = True
    group_input_012.outputs[110].hide = True
    group_input_012.outputs[111].hide = True
    group_input_012.outputs[112].hide = True
    group_input_012.outputs[113].hide = True
    group_input_012.outputs[114].hide = True
    group_input_012.outputs[115].hide = True
    group_input_012.outputs[116].hide = True
    group_input_012.outputs[117].hide = True
    group_input_012.outputs[118].hide = True
    group_input_012.outputs[119].hide = True
    group_input_012.outputs[120].hide = True
    group_input_012.outputs[121].hide = True
    group_input_012.outputs[122].hide = True
    group_input_012.outputs[123].hide = True
    group_input_012.outputs[124].hide = True
    group_input_012.outputs[125].hide = True
    group_input_012.outputs[126].hide = True
    group_input_012.outputs[127].hide = True
    group_input_012.outputs[128].hide = True
    group_input_012.outputs[129].hide = True
    group_input_012.outputs[130].hide = True
    group_input_012.outputs[131].hide = True
    group_input_012.outputs[132].hide = True
    group_input_012.outputs[133].hide = True
    group_input_012.outputs[134].hide = True
    group_input_012.outputs[135].hide = True

    # node Group.015
    group_015 = hims.nodes.new("ShaderNodeGroup")
    group_015.label = "Zone 7"
    group_015.name = "Group.015"
    group_015.node_tree = ColorMixer().node_tree

    # node Group Input.014
    group_input_014 = hims.nodes.new("NodeGroupInput")
    group_input_014.label = "Grime"
    group_input_014.name = "Group Input.014"
    group_input_014.use_custom_color = True
    group_input_014.color = (
        0.2265840768814087,
        0.14695684611797333,
        0.09751491248607635,
    )
    group_input_014.outputs[0].hide = True
    group_input_014.outputs[1].hide = True
    group_input_014.outputs[2].hide = True
    group_input_014.outputs[3].hide = True
    group_input_014.outputs[4].hide = True
    group_input_014.outputs[5].hide = True
    group_input_014.outputs[6].hide = True
    group_input_014.outputs[7].hide = True
    group_input_014.outputs[8].hide = True
    group_input_014.outputs[9].hide = True
    group_input_014.outputs[10].hide = True
    group_input_014.outputs[11].hide = True
    group_input_014.outputs[12].hide = True
    group_input_014.outputs[13].hide = True
    group_input_014.outputs[14].hide = True
    group_input_014.outputs[15].hide = True
    group_input_014.outputs[16].hide = True
    group_input_014.outputs[17].hide = True
    group_input_014.outputs[18].hide = True
    group_input_014.outputs[19].hide = True
    group_input_014.outputs[20].hide = True
    group_input_014.outputs[21].hide = True
    group_input_014.outputs[22].hide = True
    group_input_014.outputs[23].hide = True
    group_input_014.outputs[24].hide = True
    group_input_014.outputs[25].hide = True
    group_input_014.outputs[26].hide = True
    group_input_014.outputs[27].hide = True
    group_input_014.outputs[28].hide = True
    group_input_014.outputs[29].hide = True
    group_input_014.outputs[30].hide = True
    group_input_014.outputs[31].hide = True
    group_input_014.outputs[32].hide = True
    group_input_014.outputs[33].hide = True
    group_input_014.outputs[34].hide = True
    group_input_014.outputs[35].hide = True
    group_input_014.outputs[36].hide = True
    group_input_014.outputs[37].hide = True
    group_input_014.outputs[38].hide = True
    group_input_014.outputs[39].hide = True
    group_input_014.outputs[40].hide = True
    group_input_014.outputs[41].hide = True
    group_input_014.outputs[42].hide = True
    group_input_014.outputs[43].hide = True
    group_input_014.outputs[44].hide = True
    group_input_014.outputs[45].hide = True
    group_input_014.outputs[46].hide = True
    group_input_014.outputs[47].hide = True
    group_input_014.outputs[48].hide = True
    group_input_014.outputs[49].hide = True
    group_input_014.outputs[50].hide = True
    group_input_014.outputs[51].hide = True
    group_input_014.outputs[52].hide = True
    group_input_014.outputs[53].hide = True
    group_input_014.outputs[54].hide = True
    group_input_014.outputs[55].hide = True
    group_input_014.outputs[56].hide = True
    group_input_014.outputs[57].hide = True
    group_input_014.outputs[58].hide = True
    group_input_014.outputs[59].hide = True
    group_input_014.outputs[60].hide = True
    group_input_014.outputs[61].hide = True
    group_input_014.outputs[62].hide = True
    group_input_014.outputs[63].hide = True
    group_input_014.outputs[64].hide = True
    group_input_014.outputs[65].hide = True
    group_input_014.outputs[66].hide = True
    group_input_014.outputs[67].hide = True
    group_input_014.outputs[68].hide = True
    group_input_014.outputs[69].hide = True
    group_input_014.outputs[70].hide = True
    group_input_014.outputs[71].hide = True
    group_input_014.outputs[72].hide = True
    group_input_014.outputs[73].hide = True
    group_input_014.outputs[74].hide = True
    group_input_014.outputs[75].hide = True
    group_input_014.outputs[76].hide = True
    group_input_014.outputs[77].hide = True
    group_input_014.outputs[78].hide = True
    group_input_014.outputs[79].hide = True
    group_input_014.outputs[80].hide = True
    group_input_014.outputs[81].hide = True
    group_input_014.outputs[82].hide = True
    group_input_014.outputs[83].hide = True
    group_input_014.outputs[84].hide = True
    group_input_014.outputs[85].hide = True
    group_input_014.outputs[86].hide = True
    group_input_014.outputs[87].hide = True
    group_input_014.outputs[88].hide = True
    group_input_014.outputs[89].hide = True
    group_input_014.outputs[90].hide = True
    group_input_014.outputs[91].hide = True
    group_input_014.outputs[92].hide = True
    group_input_014.outputs[93].hide = True
    group_input_014.outputs[94].hide = True
    group_input_014.outputs[95].hide = True
    group_input_014.outputs[96].hide = True
    group_input_014.outputs[97].hide = True
    group_input_014.outputs[98].hide = True
    group_input_014.outputs[99].hide = True
    group_input_014.outputs[100].hide = True
    group_input_014.outputs[101].hide = True
    group_input_014.outputs[102].hide = True
    group_input_014.outputs[103].hide = True
    group_input_014.outputs[104].hide = True
    group_input_014.outputs[105].hide = True
    group_input_014.outputs[106].hide = True
    group_input_014.outputs[107].hide = True
    group_input_014.outputs[108].hide = True
    group_input_014.outputs[109].hide = True
    group_input_014.outputs[110].hide = True
    group_input_014.outputs[111].hide = True
    group_input_014.outputs[112].hide = True
    group_input_014.outputs[113].hide = True
    group_input_014.outputs[114].hide = True
    group_input_014.outputs[115].hide = True
    group_input_014.outputs[116].hide = True
    group_input_014.outputs[117].hide = True
    group_input_014.outputs[118].hide = True
    group_input_014.outputs[119].hide = True
    group_input_014.outputs[120].hide = True
    group_input_014.outputs[121].hide = True
    group_input_014.outputs[123].hide = True
    group_input_014.outputs[124].hide = True
    group_input_014.outputs[125].hide = True
    group_input_014.outputs[126].hide = True
    group_input_014.outputs[127].hide = True
    group_input_014.outputs[128].hide = True
    group_input_014.outputs[132].hide = True
    group_input_014.outputs[133].hide = True
    group_input_014.outputs[134].hide = True
    group_input_014.outputs[135].hide = True

    # node Group Input.013
    group_input_013 = hims.nodes.new("NodeGroupInput")
    group_input_013.label = "Slot 6"
    group_input_013.name = "Group Input.013"
    group_input_013.use_custom_color = True
    group_input_013.color = (
        0.20665998756885529,
        0.20665998756885529,
        0.20665998756885529,
    )
    group_input_013.outputs[0].hide = True
    group_input_013.outputs[1].hide = True
    group_input_013.outputs[2].hide = True
    group_input_013.outputs[3].hide = True
    group_input_013.outputs[4].hide = True
    group_input_013.outputs[5].hide = True
    group_input_013.outputs[6].hide = True
    group_input_013.outputs[7].hide = True
    group_input_013.outputs[8].hide = True
    group_input_013.outputs[9].hide = True
    group_input_013.outputs[10].hide = True
    group_input_013.outputs[11].hide = True
    group_input_013.outputs[12].hide = True
    group_input_013.outputs[13].hide = True
    group_input_013.outputs[14].hide = True
    group_input_013.outputs[15].hide = True
    group_input_013.outputs[16].hide = True
    group_input_013.outputs[17].hide = True
    group_input_013.outputs[18].hide = True
    group_input_013.outputs[19].hide = True
    group_input_013.outputs[20].hide = True
    group_input_013.outputs[21].hide = True
    group_input_013.outputs[22].hide = True
    group_input_013.outputs[23].hide = True
    group_input_013.outputs[24].hide = True
    group_input_013.outputs[25].hide = True
    group_input_013.outputs[26].hide = True
    group_input_013.outputs[27].hide = True
    group_input_013.outputs[28].hide = True
    group_input_013.outputs[29].hide = True
    group_input_013.outputs[30].hide = True
    group_input_013.outputs[31].hide = True
    group_input_013.outputs[32].hide = True
    group_input_013.outputs[33].hide = True
    group_input_013.outputs[34].hide = True
    group_input_013.outputs[35].hide = True
    group_input_013.outputs[36].hide = True
    group_input_013.outputs[37].hide = True
    group_input_013.outputs[38].hide = True
    group_input_013.outputs[39].hide = True
    group_input_013.outputs[40].hide = True
    group_input_013.outputs[41].hide = True
    group_input_013.outputs[42].hide = True
    group_input_013.outputs[43].hide = True
    group_input_013.outputs[44].hide = True
    group_input_013.outputs[45].hide = True
    group_input_013.outputs[46].hide = True
    group_input_013.outputs[47].hide = True
    group_input_013.outputs[48].hide = True
    group_input_013.outputs[49].hide = True
    group_input_013.outputs[50].hide = True
    group_input_013.outputs[51].hide = True
    group_input_013.outputs[52].hide = True
    group_input_013.outputs[53].hide = True
    group_input_013.outputs[54].hide = True
    group_input_013.outputs[55].hide = True
    group_input_013.outputs[56].hide = True
    group_input_013.outputs[57].hide = True
    group_input_013.outputs[58].hide = True
    group_input_013.outputs[59].hide = True
    group_input_013.outputs[60].hide = True
    group_input_013.outputs[61].hide = True
    group_input_013.outputs[62].hide = True
    group_input_013.outputs[63].hide = True
    group_input_013.outputs[64].hide = True
    group_input_013.outputs[65].hide = True
    group_input_013.outputs[66].hide = True
    group_input_013.outputs[67].hide = True
    group_input_013.outputs[68].hide = True
    group_input_013.outputs[69].hide = True
    group_input_013.outputs[70].hide = True
    group_input_013.outputs[71].hide = True
    group_input_013.outputs[72].hide = True
    group_input_013.outputs[73].hide = True
    group_input_013.outputs[74].hide = True
    group_input_013.outputs[75].hide = True
    group_input_013.outputs[76].hide = True
    group_input_013.outputs[77].hide = True
    group_input_013.outputs[78].hide = True
    group_input_013.outputs[79].hide = True
    group_input_013.outputs[80].hide = True
    group_input_013.outputs[81].hide = True
    group_input_013.outputs[82].hide = True
    group_input_013.outputs[83].hide = True
    group_input_013.outputs[84].hide = True
    group_input_013.outputs[85].hide = True
    group_input_013.outputs[86].hide = True
    group_input_013.outputs[87].hide = True
    group_input_013.outputs[88].hide = True
    group_input_013.outputs[89].hide = True
    group_input_013.outputs[90].hide = True
    group_input_013.outputs[91].hide = True
    group_input_013.outputs[92].hide = True
    group_input_013.outputs[93].hide = True
    group_input_013.outputs[94].hide = True
    group_input_013.outputs[95].hide = True
    group_input_013.outputs[96].hide = True
    group_input_013.outputs[97].hide = True
    group_input_013.outputs[98].hide = True
    group_input_013.outputs[99].hide = True
    group_input_013.outputs[100].hide = True
    group_input_013.outputs[101].hide = True
    group_input_013.outputs[102].hide = True
    group_input_013.outputs[103].hide = True
    group_input_013.outputs[104].hide = True
    group_input_013.outputs[105].hide = True
    group_input_013.outputs[106].hide = True
    group_input_013.outputs[108].hide = True
    group_input_013.outputs[109].hide = True
    group_input_013.outputs[110].hide = True
    group_input_013.outputs[111].hide = True
    group_input_013.outputs[112].hide = True
    group_input_013.outputs[113].hide = True
    group_input_013.outputs[114].hide = True
    group_input_013.outputs[115].hide = True
    group_input_013.outputs[116].hide = True
    group_input_013.outputs[120].hide = True
    group_input_013.outputs[121].hide = True
    group_input_013.outputs[122].hide = True
    group_input_013.outputs[123].hide = True
    group_input_013.outputs[124].hide = True
    group_input_013.outputs[125].hide = True
    group_input_013.outputs[126].hide = True
    group_input_013.outputs[127].hide = True
    group_input_013.outputs[128].hide = True
    group_input_013.outputs[129].hide = True
    group_input_013.outputs[130].hide = True
    group_input_013.outputs[131].hide = True
    group_input_013.outputs[132].hide = True
    group_input_013.outputs[133].hide = True
    group_input_013.outputs[134].hide = True
    group_input_013.outputs[135].hide = True

    # node Separate Color.001
    separate_color_001 = hims.nodes.new("ShaderNodeSeparateColor")
    separate_color_001.name = "Separate Color.001"
    separate_color_001.mode = "RGB"

    # node Mix.001
    mix_001_9 = hims.nodes.new("ShaderNodeMix")
    mix_001_9.name = "Mix.001"
    mix_001_9.blend_type = "MIX"
    mix_001_9.clamp_factor = True
    mix_001_9.clamp_result = False
    mix_001_9.data_type = "RGBA"
    mix_001_9.factor_mode = "UNIFORM"
    mix_001_9.inputs[1].hide = True
    mix_001_9.inputs[2].hide = True
    mix_001_9.inputs[3].hide = True
    mix_001_9.inputs[4].hide = True
    mix_001_9.inputs[5].hide = True
    mix_001_9.inputs[7].hide = True
    mix_001_9.outputs[0].hide = True
    mix_001_9.outputs[1].hide = True
    # Factor_Vector
    mix_001_9.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_001_9.inputs[2].default_value = 0.0
    # B_Float
    mix_001_9.inputs[3].default_value = 0.0
    # A_Vector
    mix_001_9.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_001_9.inputs[5].default_value = (0.0, 0.0, 0.0)
    # B_Color
    mix_001_9.inputs[7].default_value = (0.0, 1.0, 1.0, 1.0)
    # A_Rotation
    mix_001_9.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix_001_9.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Mix.003
    mix_003_7 = hims.nodes.new("ShaderNodeMix")
    mix_003_7.name = "Mix.003"
    mix_003_7.blend_type = "MIX"
    mix_003_7.clamp_factor = True
    mix_003_7.clamp_result = False
    mix_003_7.data_type = "RGBA"
    mix_003_7.factor_mode = "UNIFORM"
    mix_003_7.inputs[1].hide = True
    mix_003_7.inputs[2].hide = True
    mix_003_7.inputs[3].hide = True
    mix_003_7.inputs[4].hide = True
    mix_003_7.inputs[5].hide = True
    mix_003_7.inputs[7].hide = True
    mix_003_7.outputs[0].hide = True
    mix_003_7.outputs[1].hide = True
    # Factor_Vector
    mix_003_7.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_003_7.inputs[2].default_value = 0.0
    # B_Float
    mix_003_7.inputs[3].default_value = 0.0
    # A_Vector
    mix_003_7.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_003_7.inputs[5].default_value = (0.0, 0.0, 0.0)
    # B_Color
    mix_003_7.inputs[7].default_value = (1.0, 0.01103365421295166, 1.0, 1.0)
    # A_Rotation
    mix_003_7.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix_003_7.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Mix.002
    mix_002_7 = hims.nodes.new("ShaderNodeMix")
    mix_002_7.name = "Mix.002"
    mix_002_7.blend_type = "MIX"
    mix_002_7.clamp_factor = True
    mix_002_7.clamp_result = False
    mix_002_7.data_type = "RGBA"
    mix_002_7.factor_mode = "UNIFORM"
    mix_002_7.inputs[1].hide = True
    mix_002_7.inputs[2].hide = True
    mix_002_7.inputs[3].hide = True
    mix_002_7.inputs[4].hide = True
    mix_002_7.inputs[5].hide = True
    mix_002_7.inputs[7].hide = True
    mix_002_7.outputs[0].hide = True
    mix_002_7.outputs[1].hide = True
    # Factor_Vector
    mix_002_7.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_002_7.inputs[2].default_value = 0.0
    # B_Float
    mix_002_7.inputs[3].default_value = 0.0
    # A_Vector
    mix_002_7.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_002_7.inputs[5].default_value = (0.0, 0.0, 0.0)
    # B_Color
    mix_002_7.inputs[7].default_value = (1.0, 1.0, 0.0, 1.0)
    # A_Rotation
    mix_002_7.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix_002_7.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Group Input.015
    group_input_015 = hims.nodes.new("NodeGroupInput")
    group_input_015.name = "Group Input.015"
    group_input_015.outputs[1].hide = True
    group_input_015.outputs[2].hide = True
    group_input_015.outputs[3].hide = True
    group_input_015.outputs[4].hide = True
    group_input_015.outputs[5].hide = True
    group_input_015.outputs[6].hide = True
    group_input_015.outputs[8].hide = True
    group_input_015.outputs[9].hide = True
    group_input_015.outputs[10].hide = True
    group_input_015.outputs[11].hide = True
    group_input_015.outputs[12].hide = True
    group_input_015.outputs[13].hide = True
    group_input_015.outputs[15].hide = True
    group_input_015.outputs[16].hide = True
    group_input_015.outputs[17].hide = True
    group_input_015.outputs[18].hide = True
    group_input_015.outputs[19].hide = True
    group_input_015.outputs[20].hide = True
    group_input_015.outputs[21].hide = True
    group_input_015.outputs[22].hide = True
    group_input_015.outputs[23].hide = True
    group_input_015.outputs[24].hide = True
    group_input_015.outputs[25].hide = True
    group_input_015.outputs[26].hide = True
    group_input_015.outputs[27].hide = True
    group_input_015.outputs[28].hide = True
    group_input_015.outputs[30].hide = True
    group_input_015.outputs[31].hide = True
    group_input_015.outputs[32].hide = True
    group_input_015.outputs[33].hide = True
    group_input_015.outputs[34].hide = True
    group_input_015.outputs[35].hide = True
    group_input_015.outputs[36].hide = True
    group_input_015.outputs[37].hide = True
    group_input_015.outputs[38].hide = True
    group_input_015.outputs[39].hide = True
    group_input_015.outputs[40].hide = True
    group_input_015.outputs[41].hide = True
    group_input_015.outputs[42].hide = True
    group_input_015.outputs[43].hide = True
    group_input_015.outputs[45].hide = True
    group_input_015.outputs[46].hide = True
    group_input_015.outputs[47].hide = True
    group_input_015.outputs[48].hide = True
    group_input_015.outputs[49].hide = True
    group_input_015.outputs[50].hide = True
    group_input_015.outputs[51].hide = True
    group_input_015.outputs[52].hide = True
    group_input_015.outputs[53].hide = True
    group_input_015.outputs[54].hide = True
    group_input_015.outputs[55].hide = True
    group_input_015.outputs[56].hide = True
    group_input_015.outputs[57].hide = True
    group_input_015.outputs[58].hide = True
    group_input_015.outputs[59].hide = True
    group_input_015.outputs[61].hide = True
    group_input_015.outputs[62].hide = True
    group_input_015.outputs[63].hide = True
    group_input_015.outputs[64].hide = True
    group_input_015.outputs[65].hide = True
    group_input_015.outputs[66].hide = True
    group_input_015.outputs[67].hide = True
    group_input_015.outputs[68].hide = True
    group_input_015.outputs[69].hide = True
    group_input_015.outputs[70].hide = True
    group_input_015.outputs[71].hide = True
    group_input_015.outputs[72].hide = True
    group_input_015.outputs[73].hide = True
    group_input_015.outputs[74].hide = True
    group_input_015.outputs[75].hide = True
    group_input_015.outputs[77].hide = True
    group_input_015.outputs[78].hide = True
    group_input_015.outputs[79].hide = True
    group_input_015.outputs[80].hide = True
    group_input_015.outputs[81].hide = True
    group_input_015.outputs[82].hide = True
    group_input_015.outputs[83].hide = True
    group_input_015.outputs[84].hide = True
    group_input_015.outputs[85].hide = True
    group_input_015.outputs[86].hide = True
    group_input_015.outputs[87].hide = True
    group_input_015.outputs[88].hide = True
    group_input_015.outputs[89].hide = True
    group_input_015.outputs[90].hide = True
    group_input_015.outputs[91].hide = True
    group_input_015.outputs[93].hide = True
    group_input_015.outputs[94].hide = True
    group_input_015.outputs[95].hide = True
    group_input_015.outputs[96].hide = True
    group_input_015.outputs[97].hide = True
    group_input_015.outputs[98].hide = True
    group_input_015.outputs[99].hide = True
    group_input_015.outputs[100].hide = True
    group_input_015.outputs[101].hide = True
    group_input_015.outputs[102].hide = True
    group_input_015.outputs[103].hide = True
    group_input_015.outputs[104].hide = True
    group_input_015.outputs[105].hide = True
    group_input_015.outputs[106].hide = True
    group_input_015.outputs[107].hide = True
    group_input_015.outputs[109].hide = True
    group_input_015.outputs[110].hide = True
    group_input_015.outputs[111].hide = True
    group_input_015.outputs[112].hide = True
    group_input_015.outputs[113].hide = True
    group_input_015.outputs[114].hide = True
    group_input_015.outputs[115].hide = True
    group_input_015.outputs[116].hide = True
    group_input_015.outputs[117].hide = True
    group_input_015.outputs[118].hide = True
    group_input_015.outputs[119].hide = True
    group_input_015.outputs[120].hide = True
    group_input_015.outputs[121].hide = True
    group_input_015.outputs[122].hide = True
    group_input_015.outputs[124].hide = True
    group_input_015.outputs[125].hide = True
    group_input_015.outputs[126].hide = True
    group_input_015.outputs[127].hide = True
    group_input_015.outputs[128].hide = True
    group_input_015.outputs[129].hide = True
    group_input_015.outputs[130].hide = True
    group_input_015.outputs[131].hide = True
    group_input_015.outputs[132].hide = True
    group_input_015.outputs[133].hide = True
    group_input_015.outputs[134].hide = True
    group_input_015.outputs[135].hide = True

    # node Math
    math_5 = hims.nodes.new("ShaderNodeMath")
    math_5.label = "Finalize Base Spec"
    math_5.name = "Math"
    math_5.operation = "MULTIPLY"
    math_5.use_clamp = False
    # Value
    math_5.inputs[0].default_value = 0.5
    # Value_002
    math_5.inputs[2].default_value = 0.5

    # node Group.005
    group_005: ShaderNodeGroup = hims.nodes.new("ShaderNodeGroup")
    group_005.name = "Group.005"
    group_005.node_tree = DetailNormals().node_tree

    # node Group Input.018
    group_input_018 = hims.nodes.new("NodeGroupInput")
    group_input_018.name = "Group Input.018"
    group_input_018.outputs[1].hide = True
    group_input_018.outputs[2].hide = True
    group_input_018.outputs[8].hide = True
    group_input_018.outputs[9].hide = True
    group_input_018.outputs[10].hide = True
    group_input_018.outputs[11].hide = True
    group_input_018.outputs[12].hide = True
    group_input_018.outputs[13].hide = True
    group_input_018.outputs[14].hide = True
    group_input_018.outputs[16].hide = True
    group_input_018.outputs[17].hide = True
    group_input_018.outputs[18].hide = True
    group_input_018.outputs[19].hide = True
    group_input_018.outputs[20].hide = True
    group_input_018.outputs[21].hide = True
    group_input_018.outputs[22].hide = True
    group_input_018.outputs[23].hide = True
    group_input_018.outputs[24].hide = True
    group_input_018.outputs[25].hide = True
    group_input_018.outputs[26].hide = True
    group_input_018.outputs[27].hide = True
    group_input_018.outputs[28].hide = True
    group_input_018.outputs[29].hide = True
    group_input_018.outputs[31].hide = True
    group_input_018.outputs[32].hide = True
    group_input_018.outputs[33].hide = True
    group_input_018.outputs[34].hide = True
    group_input_018.outputs[35].hide = True
    group_input_018.outputs[36].hide = True
    group_input_018.outputs[37].hide = True
    group_input_018.outputs[38].hide = True
    group_input_018.outputs[39].hide = True
    group_input_018.outputs[40].hide = True
    group_input_018.outputs[41].hide = True
    group_input_018.outputs[42].hide = True
    group_input_018.outputs[43].hide = True
    group_input_018.outputs[44].hide = True
    group_input_018.outputs[46].hide = True
    group_input_018.outputs[47].hide = True
    group_input_018.outputs[48].hide = True
    group_input_018.outputs[49].hide = True
    group_input_018.outputs[50].hide = True
    group_input_018.outputs[51].hide = True
    group_input_018.outputs[52].hide = True
    group_input_018.outputs[53].hide = True
    group_input_018.outputs[54].hide = True
    group_input_018.outputs[55].hide = True
    group_input_018.outputs[56].hide = True
    group_input_018.outputs[57].hide = True
    group_input_018.outputs[58].hide = True
    group_input_018.outputs[59].hide = True
    group_input_018.outputs[60].hide = True
    group_input_018.outputs[62].hide = True
    group_input_018.outputs[63].hide = True
    group_input_018.outputs[64].hide = True
    group_input_018.outputs[65].hide = True
    group_input_018.outputs[66].hide = True
    group_input_018.outputs[67].hide = True
    group_input_018.outputs[68].hide = True
    group_input_018.outputs[69].hide = True
    group_input_018.outputs[70].hide = True
    group_input_018.outputs[71].hide = True
    group_input_018.outputs[72].hide = True
    group_input_018.outputs[73].hide = True
    group_input_018.outputs[74].hide = True
    group_input_018.outputs[75].hide = True
    group_input_018.outputs[76].hide = True
    group_input_018.outputs[78].hide = True
    group_input_018.outputs[79].hide = True
    group_input_018.outputs[80].hide = True
    group_input_018.outputs[81].hide = True
    group_input_018.outputs[82].hide = True
    group_input_018.outputs[83].hide = True
    group_input_018.outputs[84].hide = True
    group_input_018.outputs[85].hide = True
    group_input_018.outputs[86].hide = True
    group_input_018.outputs[87].hide = True
    group_input_018.outputs[88].hide = True
    group_input_018.outputs[89].hide = True
    group_input_018.outputs[90].hide = True
    group_input_018.outputs[91].hide = True
    group_input_018.outputs[92].hide = True
    group_input_018.outputs[94].hide = True
    group_input_018.outputs[95].hide = True
    group_input_018.outputs[96].hide = True
    group_input_018.outputs[97].hide = True
    group_input_018.outputs[98].hide = True
    group_input_018.outputs[99].hide = True
    group_input_018.outputs[100].hide = True
    group_input_018.outputs[101].hide = True
    group_input_018.outputs[102].hide = True
    group_input_018.outputs[103].hide = True
    group_input_018.outputs[104].hide = True
    group_input_018.outputs[105].hide = True
    group_input_018.outputs[106].hide = True
    group_input_018.outputs[107].hide = True
    group_input_018.outputs[108].hide = True
    group_input_018.outputs[110].hide = True
    group_input_018.outputs[111].hide = True
    group_input_018.outputs[112].hide = True
    group_input_018.outputs[113].hide = True
    group_input_018.outputs[114].hide = True
    group_input_018.outputs[115].hide = True
    group_input_018.outputs[116].hide = True
    group_input_018.outputs[117].hide = True
    group_input_018.outputs[118].hide = True
    group_input_018.outputs[119].hide = True
    group_input_018.outputs[120].hide = True
    group_input_018.outputs[121].hide = True
    group_input_018.outputs[122].hide = True
    group_input_018.outputs[123].hide = True
    group_input_018.outputs[125].hide = True
    group_input_018.outputs[126].hide = True
    group_input_018.outputs[127].hide = True
    group_input_018.outputs[128].hide = True
    group_input_018.outputs[129].hide = True
    group_input_018.outputs[130].hide = True
    group_input_018.outputs[131].hide = True
    group_input_018.outputs[132].hide = True
    group_input_018.outputs[133].hide = True
    group_input_018.outputs[134].hide = True
    group_input_018.outputs[135].hide = True

    # node Group.002
    group_002_4 = hims.nodes.new("ShaderNodeGroup")
    group_002_4.label = "Zone 1"
    group_002_4.name = "Group.002"
    group_002_4.node_tree = ColorMixer().node_tree

    # node Group Input.007
    group_input_007 = hims.nodes.new("NodeGroupInput")
    group_input_007.label = "Slot 1"
    group_input_007.name = "Group Input.007"
    group_input_007.use_custom_color = True
    group_input_007.color = (0.42922577261924744, 0.0, 0.0)
    group_input_007.outputs[0].hide = True
    group_input_007.outputs[1].hide = True
    group_input_007.outputs[2].hide = True
    group_input_007.outputs[3].hide = True
    group_input_007.outputs[4].hide = True
    group_input_007.outputs[5].hide = True
    group_input_007.outputs[6].hide = True
    group_input_007.outputs[7].hide = True
    group_input_007.outputs[8].hide = True
    group_input_007.outputs[9].hide = True
    group_input_007.outputs[10].hide = True
    group_input_007.outputs[11].hide = True
    group_input_007.outputs[12].hide = True
    group_input_007.outputs[14].hide = True
    group_input_007.outputs[15].hide = True
    group_input_007.outputs[16].hide = True
    group_input_007.outputs[17].hide = True
    group_input_007.outputs[18].hide = True
    group_input_007.outputs[19].hide = True
    group_input_007.outputs[20].hide = True
    group_input_007.outputs[21].hide = True
    group_input_007.outputs[22].hide = True
    group_input_007.outputs[26].hide = True
    group_input_007.outputs[27].hide = True
    group_input_007.outputs[28].hide = True
    group_input_007.outputs[29].hide = True
    group_input_007.outputs[30].hide = True
    group_input_007.outputs[31].hide = True
    group_input_007.outputs[32].hide = True
    group_input_007.outputs[33].hide = True
    group_input_007.outputs[34].hide = True
    group_input_007.outputs[35].hide = True
    group_input_007.outputs[36].hide = True
    group_input_007.outputs[37].hide = True
    group_input_007.outputs[38].hide = True
    group_input_007.outputs[39].hide = True
    group_input_007.outputs[40].hide = True
    group_input_007.outputs[41].hide = True
    group_input_007.outputs[42].hide = True
    group_input_007.outputs[43].hide = True
    group_input_007.outputs[44].hide = True
    group_input_007.outputs[45].hide = True
    group_input_007.outputs[46].hide = True
    group_input_007.outputs[47].hide = True
    group_input_007.outputs[48].hide = True
    group_input_007.outputs[49].hide = True
    group_input_007.outputs[50].hide = True
    group_input_007.outputs[51].hide = True
    group_input_007.outputs[52].hide = True
    group_input_007.outputs[53].hide = True
    group_input_007.outputs[54].hide = True
    group_input_007.outputs[55].hide = True
    group_input_007.outputs[56].hide = True
    group_input_007.outputs[57].hide = True
    group_input_007.outputs[58].hide = True
    group_input_007.outputs[59].hide = True
    group_input_007.outputs[60].hide = True
    group_input_007.outputs[61].hide = True
    group_input_007.outputs[62].hide = True
    group_input_007.outputs[63].hide = True
    group_input_007.outputs[64].hide = True
    group_input_007.outputs[65].hide = True
    group_input_007.outputs[66].hide = True
    group_input_007.outputs[67].hide = True
    group_input_007.outputs[68].hide = True
    group_input_007.outputs[69].hide = True
    group_input_007.outputs[70].hide = True
    group_input_007.outputs[71].hide = True
    group_input_007.outputs[72].hide = True
    group_input_007.outputs[73].hide = True
    group_input_007.outputs[74].hide = True
    group_input_007.outputs[75].hide = True
    group_input_007.outputs[76].hide = True
    group_input_007.outputs[77].hide = True
    group_input_007.outputs[78].hide = True
    group_input_007.outputs[79].hide = True
    group_input_007.outputs[80].hide = True
    group_input_007.outputs[81].hide = True
    group_input_007.outputs[82].hide = True
    group_input_007.outputs[83].hide = True
    group_input_007.outputs[84].hide = True
    group_input_007.outputs[85].hide = True
    group_input_007.outputs[86].hide = True
    group_input_007.outputs[87].hide = True
    group_input_007.outputs[88].hide = True
    group_input_007.outputs[89].hide = True
    group_input_007.outputs[90].hide = True
    group_input_007.outputs[91].hide = True
    group_input_007.outputs[92].hide = True
    group_input_007.outputs[93].hide = True
    group_input_007.outputs[94].hide = True
    group_input_007.outputs[95].hide = True
    group_input_007.outputs[96].hide = True
    group_input_007.outputs[97].hide = True
    group_input_007.outputs[98].hide = True
    group_input_007.outputs[99].hide = True
    group_input_007.outputs[100].hide = True
    group_input_007.outputs[101].hide = True
    group_input_007.outputs[102].hide = True
    group_input_007.outputs[103].hide = True
    group_input_007.outputs[104].hide = True
    group_input_007.outputs[105].hide = True
    group_input_007.outputs[106].hide = True
    group_input_007.outputs[107].hide = True
    group_input_007.outputs[108].hide = True
    group_input_007.outputs[109].hide = True
    group_input_007.outputs[110].hide = True
    group_input_007.outputs[111].hide = True
    group_input_007.outputs[112].hide = True
    group_input_007.outputs[113].hide = True
    group_input_007.outputs[114].hide = True
    group_input_007.outputs[115].hide = True
    group_input_007.outputs[116].hide = True
    group_input_007.outputs[117].hide = True
    group_input_007.outputs[118].hide = True
    group_input_007.outputs[119].hide = True
    group_input_007.outputs[120].hide = True
    group_input_007.outputs[121].hide = True
    group_input_007.outputs[122].hide = True
    group_input_007.outputs[123].hide = True
    group_input_007.outputs[124].hide = True
    group_input_007.outputs[125].hide = True
    group_input_007.outputs[126].hide = True
    group_input_007.outputs[127].hide = True
    group_input_007.outputs[128].hide = True
    group_input_007.outputs[129].hide = True
    group_input_007.outputs[130].hide = True
    group_input_007.outputs[131].hide = True
    group_input_007.outputs[132].hide = True
    group_input_007.outputs[133].hide = True
    group_input_007.outputs[134].hide = True
    group_input_007.outputs[135].hide = True

    # node Principled BSDF
    principled_bsdf = hims.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = "GGX"
    principled_bsdf.subsurface_method = "RANDOM_WALK_SKIN"

    # node Mix.007
    mix_007_4 = hims.nodes.new("ShaderNodeMix")
    mix_007_4.name = "Mix.007"
    mix_007_4.blend_type = "MIX"
    mix_007_4.clamp_factor = True
    mix_007_4.clamp_result = False
    mix_007_4.data_type = "RGBA"
    mix_007_4.factor_mode = "UNIFORM"
    # Factor_Vector
    mix_007_4.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_007_4.inputs[2].default_value = 0.0
    # B_Float
    mix_007_4.inputs[3].default_value = 0.0
    # A_Vector
    mix_007_4.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_007_4.inputs[5].default_value = (0.0, 0.0, 0.0)
    # A_Rotation
    mix_007_4.inputs[8].default_value = (0.0, 0.0, 0.0)
    # B_Rotation
    mix_007_4.inputs[9].default_value = (0.0, 0.0, 0.0)

    # node Group
    group_4 = hims.nodes.new("ShaderNodeGroup")
    group_4.label = "Color"
    group_4.name = "Group"
    group_4.node_tree = InfiniteColor().node_tree

    # node Group Input.027
    group_input_027 = hims.nodes.new("NodeGroupInput")
    group_input_027.name = "Group Input.027"
    group_input_027.outputs[0].hide = True
    group_input_027.outputs[3].hide = True
    group_input_027.outputs[4].hide = True
    group_input_027.outputs[5].hide = True
    group_input_027.outputs[6].hide = True
    group_input_027.outputs[7].hide = True
    group_input_027.outputs[8].hide = True
    group_input_027.outputs[9].hide = True
    group_input_027.outputs[10].hide = True
    group_input_027.outputs[11].hide = True
    group_input_027.outputs[12].hide = True
    group_input_027.outputs[13].hide = True
    group_input_027.outputs[14].hide = True
    group_input_027.outputs[15].hide = True
    group_input_027.outputs[16].hide = True
    group_input_027.outputs[17].hide = True
    group_input_027.outputs[18].hide = True
    group_input_027.outputs[19].hide = True
    group_input_027.outputs[20].hide = True
    group_input_027.outputs[21].hide = True
    group_input_027.outputs[22].hide = True
    group_input_027.outputs[23].hide = True
    group_input_027.outputs[24].hide = True
    group_input_027.outputs[25].hide = True
    group_input_027.outputs[26].hide = True
    group_input_027.outputs[28].hide = True
    group_input_027.outputs[29].hide = True
    group_input_027.outputs[30].hide = True
    group_input_027.outputs[31].hide = True
    group_input_027.outputs[32].hide = True
    group_input_027.outputs[33].hide = True
    group_input_027.outputs[34].hide = True
    group_input_027.outputs[35].hide = True
    group_input_027.outputs[36].hide = True
    group_input_027.outputs[37].hide = True
    group_input_027.outputs[38].hide = True
    group_input_027.outputs[39].hide = True
    group_input_027.outputs[40].hide = True
    group_input_027.outputs[41].hide = True
    group_input_027.outputs[43].hide = True
    group_input_027.outputs[44].hide = True
    group_input_027.outputs[45].hide = True
    group_input_027.outputs[46].hide = True
    group_input_027.outputs[47].hide = True
    group_input_027.outputs[48].hide = True
    group_input_027.outputs[49].hide = True
    group_input_027.outputs[50].hide = True
    group_input_027.outputs[51].hide = True
    group_input_027.outputs[52].hide = True
    group_input_027.outputs[53].hide = True
    group_input_027.outputs[54].hide = True
    group_input_027.outputs[55].hide = True
    group_input_027.outputs[56].hide = True
    group_input_027.outputs[57].hide = True
    group_input_027.outputs[59].hide = True
    group_input_027.outputs[60].hide = True
    group_input_027.outputs[61].hide = True
    group_input_027.outputs[62].hide = True
    group_input_027.outputs[63].hide = True
    group_input_027.outputs[64].hide = True
    group_input_027.outputs[65].hide = True
    group_input_027.outputs[66].hide = True
    group_input_027.outputs[67].hide = True
    group_input_027.outputs[68].hide = True
    group_input_027.outputs[69].hide = True
    group_input_027.outputs[70].hide = True
    group_input_027.outputs[71].hide = True
    group_input_027.outputs[72].hide = True
    group_input_027.outputs[73].hide = True
    group_input_027.outputs[75].hide = True
    group_input_027.outputs[76].hide = True
    group_input_027.outputs[77].hide = True
    group_input_027.outputs[78].hide = True
    group_input_027.outputs[79].hide = True
    group_input_027.outputs[80].hide = True
    group_input_027.outputs[81].hide = True
    group_input_027.outputs[82].hide = True
    group_input_027.outputs[83].hide = True
    group_input_027.outputs[84].hide = True
    group_input_027.outputs[85].hide = True
    group_input_027.outputs[86].hide = True
    group_input_027.outputs[87].hide = True
    group_input_027.outputs[88].hide = True
    group_input_027.outputs[89].hide = True
    group_input_027.outputs[91].hide = True
    group_input_027.outputs[92].hide = True
    group_input_027.outputs[93].hide = True
    group_input_027.outputs[94].hide = True
    group_input_027.outputs[95].hide = True
    group_input_027.outputs[96].hide = True
    group_input_027.outputs[97].hide = True
    group_input_027.outputs[98].hide = True
    group_input_027.outputs[99].hide = True
    group_input_027.outputs[100].hide = True
    group_input_027.outputs[101].hide = True
    group_input_027.outputs[102].hide = True
    group_input_027.outputs[103].hide = True
    group_input_027.outputs[104].hide = True
    group_input_027.outputs[105].hide = True
    group_input_027.outputs[107].hide = True
    group_input_027.outputs[108].hide = True
    group_input_027.outputs[109].hide = True
    group_input_027.outputs[110].hide = True
    group_input_027.outputs[111].hide = True
    group_input_027.outputs[112].hide = True
    group_input_027.outputs[113].hide = True
    group_input_027.outputs[114].hide = True
    group_input_027.outputs[115].hide = True
    group_input_027.outputs[116].hide = True
    group_input_027.outputs[117].hide = True
    group_input_027.outputs[118].hide = True
    group_input_027.outputs[119].hide = True
    group_input_027.outputs[120].hide = True
    group_input_027.outputs[121].hide = True
    group_input_027.outputs[122].hide = True
    group_input_027.outputs[123].hide = True
    group_input_027.outputs[124].hide = True
    group_input_027.outputs[125].hide = True
    group_input_027.outputs[126].hide = True
    group_input_027.outputs[127].hide = True
    group_input_027.outputs[128].hide = True
    group_input_027.outputs[129].hide = True
    group_input_027.outputs[130].hide = True
    group_input_027.outputs[131].hide = True
    group_input_027.outputs[132].hide = True
    group_input_027.outputs[133].hide = True
    group_input_027.outputs[134].hide = True
    group_input_027.outputs[135].hide = True

    # node Math.008
    math_008_2 = hims.nodes.new("ShaderNodeMath")
    math_008_2.name = "Math.008"
    math_008_2.operation = "MULTIPLY"
    math_008_2.use_clamp = False
    # Value_001
    math_008_2.inputs[1].default_value = 0.4399999976158142
    # Value_002
    math_008_2.inputs[2].default_value = 0.5

    # node Math.009
    math_009_2 = hims.nodes.new("ShaderNodeMath")
    math_009_2.name = "Math.009"
    math_009_2.operation = "ADD"
    math_009_2.use_clamp = False
    # Value_001
    math_009_2.inputs[1].default_value = 0.5600000023841858
    # Value_002
    math_009_2.inputs[2].default_value = 0.5

    # Set locations
    separate_rgb_4.location = (1210.0343017578125, 366.75048828125)
    math_002_3.location = (2175.57666015625, 167.1549072265625)
    math_004_4.location = (2615.739501953125, -140.130126953125)
    math_005_4.location = (2167.04150390625, -286.380126953125)
    math_003_2.location = (2395.739501953125, 17.44978904724121)
    normal_map.location = (1758.1846923828125, -640.986328125)
    reroute_002_4.location = (361.5635681152344, 835.6195678710938)
    reroute_011_3.location = (2218.1455078125, -762.0377197265625)
    reroute_010_3.location = (1439.04150390625, 308.13250732421875)
    reroute_014_3.location = (1446.7025146484375, -185.32423400878906)
    reroute_015_3.location = (1417.68017578125, 287.316162109375)
    reroute_018_3.location = (3071.028564453125, 375.3570556640625)
    reroute_003_1.location = (1828.097900390625, 620.0368041992188)
    reroute_021.location = (2982.773193359375, 604.2268676757812)
    invert.location = (3316.08837890625, 712.96875)
    reroute_023.location = (3855.60595703125, 470.8802490234375)
    reroute_020.location = (3949.81396484375, 372.5987854003906)
    reroute_026.location = (3950.721435546875, -177.6341552734375)
    reroute_027.location = (3950.953857421875, 201.0716094970703)
    reroute_028.location = (4545.17333984375, 687.51171875)
    reroute_019_3.location = (3070.8603515625, 117.38058471679688)
    reroute_025.location = (2983.163330078125, 72.54264831542969)
    reroute_013_3.location = (2819.94677734375, 50.750732421875)
    reroute_022.location = (2982.773193359375, 480.6976318359375)
    reroute_032.location = (3398.82421875, 200.83401489257812)
    reroute_033.location = (3289.7529296875, 182.54298400878906)
    reroute_034.location = (3290.66015625, 163.137451171875)
    reroute_035.location = (762.3345947265625, 195.68263244628906)
    reroute_037.location = (756.5297241210938, -768.2499389648438)
    reroute_016_3.location = (1422.8017578125, 63.79310607910156)
    reroute_040.location = (3071.32373046875, 657.0897827148438)
    reroute_045.location = (3876.27001953125, -69.84181213378906)
    reroute_047.location = (2706.80322265625, 101.36702728271484)
    reroute_050.location = (4107.5087890625, -274.68988037109375)
    reroute_049.location = (4105.80126953125, 353.3472900390625)
    reroute_012.location = (2807.00244140625, -764.1935424804688)
    reroute_051.location = (4211.27197265625, -861.2295532226562)
    reroute_053.location = (4170.30322265625, 285.1639404296875)
    reroute_024.location = (3855.120361328125, 226.1242218017578)
    reroute_029.location = (4549.212890625, 262.6029357910156)
    reroute_030.location = (4170.251953125, 495.5069274902344)
    reroute_054.location = (2106.01318359375, 1319.4393310546875)
    reroute_055.location = (2100.0087890625, 33.32284927368164)
    reroute_057.location = (2359.9833984375, -546.9471435546875)
    reroute_056.location = (2361.30322265625, -325.0791931152344)
    reroute_060.location = (4691.818359375, -462.3729248046875)
    reroute_061.location = (4692.388671875, 189.62496948242188)
    reroute_059.location = (3328.998291015625, 3.341456413269043)
    reroute_006_3.location = (-1098.9185791015625, -23.31800079345703)
    reroute_063.location = (167.50445556640625, -157.35601806640625)
    reroute_065.location = (2980.8671875, 26.75341796875)
    reroute_064.location = (2969.083740234375, -1519.6937255859375)
    reroute_031.location = (3395.428955078125, 550.6635131835938)
    reroute_004_4.location = (1830.6190185546875, 465.7493591308594)
    reroute_039.location = (3071.32373046875, 743.0167236328125)
    reroute_042.location = (3085.290283203125, 146.49276733398438)
    reroute_1.location = (1823.316162109375, 821.5437622070312)
    reroute_001_4.location = (358.541748046875, 1388.126953125)
    reroute_041.location = (3076.5791015625, 445.67071533203125)
    reroute_043.location = (3871.645751953125, 442.1236572265625)
    reroute_044.location = (3898.373779296875, 442.1236267089844)
    reroute_062.location = (-1098.9185791015625, -146.46742248535156)
    group_008.location = (-1609.9658203125, 1866.7508544921875)
    group_input_009.location = (-2009.9654541015625, 1826.75048828125)
    group_input_004.location = (-2069.9658203125, 306.7505798339844)
    group_input_019.location = (-2266.87890625, -50.833553314208984)
    group_input_006.location = (-2116.717529296875, -385.7625732421875)
    group_input_025.location = (-2120.583740234375, -731.9295654296875)
    group_016.location = (-1609.9658203125, 966.75048828125)
    group_017.location = (-1689.9661865234375, 366.7505798339844)
    group_020.location = (-1689.9661865234375, 14.793144226074219)
    clamp_1.location = (-250.19227600097656, -1363.5765380859375)
    clamp_001.location = (-247.9335174560547, -1403.0809326171875)
    clamp_002.location = (-247.93353271484375, -1447.10009765625)
    clamp_003.location = (-245.67474365234375, -1488.862060546875)
    clamp_004.location = (-245.6747283935547, -1526.1090087890625)
    clamp_005.location = (-243.41595458984375, -1563.35595703125)
    clamp_006.location = (-243.41595458984375, -1596.0882568359375)
    clamp_007.location = (-243.41595458984375, -1629.94921875)
    group_input_17.location = (-781.9807739257812, -1074.4022216796875)
    mix_005_6.location = (2505.625244140625, -803.4283447265625)
    gamma.location = (4112.35986328125, -12.653839111328125)
    math_006_1.location = (4489.9873046875, -158.54791259765625)
    group_input_021.location = (2096.2841796875, -61.13663864135742)
    group_input_023.location = (1638.611328125, -400.6353454589844)
    group_input_022.location = (1506.5400390625, 315.4192810058594)
    texture_coordinate.location = (778.5026245117188, 1611.7574462890625)
    mapping_1.location = (1015.56884765625, 1526.8017578125)
    musgrave_texture.location = (1321.500244140625, 1533.3026123046875)
    colorramp_001.location = (1818.0628662109375, 237.72613525390625)
    bump.location = (2522.285400390625, -434.7271423339844)
    colorramp.location = (1622.6456298828125, -8.753049850463867)
    group_006.location = (-1989.093994140625, 55.962345123291016)
    group_012.location = (-1609.9658203125, 1326.75048828125)
    group_018.location = (-1736.718017578125, -325.762451171875)
    group_023.location = (-1749.1181640625, -1459.643798828125)
    group_019.location = (-1740.583740234375, -693.3277587890625)
    group_004.location = (-1609.9658203125, 2046.75048828125)
    group_input_020.location = (745.5018920898438, 1469.8060302734375)
    group_input_017.location = (-682.7652587890625, 1142.9691162109375)
    group_013.location = (-42.23020935058594, -901.8160400390625)
    group_022.location = (-36.950374603271484, -1272.497802734375)
    gamma_004.location = (4798.55859375, 358.29608154296875)
    group_input_008.location = (-2009.9654541015625, 2006.75048828125)
    mix_004_7.location = (3559.901123046875, 732.34619140625)
    mix_006_7.location = (3899.473388671875, 242.8136444091797)
    gamma_002.location = (4820.5517578125, 227.38999938964844)
    reroute_009.location = (-2781.629638671875, -264.4286804199219)
    reroute_066.location = (-2804.859619140625, -292.05706787109375)
    reroute_068.location = (-2801.541015625, -2135.2001953125)
    reroute_067.location = (-2778.31103515625, -2100.95556640625)
    reroute_069.location = (4009.56689453125, -2105.42919921875)
    reroute_070.location = (4026.65576171875, -2131.844970703125)
    reroute_071.location = (4020.26123046875, -977.706787109375)
    reroute_072.location = (4037.35009765625, -1004.12255859375)
    reroute_074.location = (4185.7041015625, -1005.98046875)
    reroute_073.location = (4179.81494140625, -978.4462280273438)
    group_011.location = (-1609.9658203125, 1506.75048828125)
    group_input_011.location = (-2009.9654541015625, 1466.75048828125)
    group_010.location = (-1609.9658203125, 1686.7501220703125)
    group_input_010.location = (-2009.9654541015625, 1646.7503662109375)
    reroute_058.location = (3324.754638671875, -448.6982116699219)
    bump_001.location = (3108.949462890625, -414.1265563964844)
    group_output_17.location = (5216.7314453125, 406.7503967285156)
    group_input_026.location = (-2136.499267578125, -1540.68310546875)
    reroute_075.location = (1247.4300537109375, -161.6805419921875)
    reroute_007_3.location = (1249.0855712890625, -533.1724853515625)
    reroute_076.location = (1093.282470703125, -754.285400390625)
    reroute_077.location = (1088.766357421875, -181.19677734375)
    reroute_078.location = (1786.76904296875, -1316.533935546875)
    reroute_005_4.location = (1848.6778564453125, -969.0878295898438)
    reroute_079.location = (1792.28369140625, -989.9581909179688)
    reroute_008.location = (2216.890625, -937.55029296875)
    reroute_052.location = (4212.53271484375, 285.9776306152344)
    gamma_003.location = (4796.31982421875, 313.47723388671875)
    reroute_048.location = (2705.419677734375, 347.8983154296875)
    reroute_046.location = (2704.7900390625, 251.45082092285156)
    mix_11.location = (2478.24169921875, 560.5236206054688)
    math_001_4.location = (1747.0526123046875, 329.03521728515625)
    reroute_080.location = (2073.84619140625, 321.6976013183594)
    reroute_083.location = (1975.389892578125, 463.18780517578125)
    reroute_084.location = (1974.360107421875, 561.1426391601562)
    reroute_081.location = (2079.392578125, 542.44677734375)
    reroute_017.location = (2075.392333984375, 368.93499755859375)
    math_007_1.location = (3092.0634765625, 35.17744445800781)
    gamma_001.location = (4111.2919921875, -118.42040252685547)
    combine_color.location = (4491.5263671875, -5.611602783203125)
    group_input_005.location = (-2069.9658203125, 646.75048828125)
    group_009.location = (-49.96565628051758, 306.75048828125)
    group_001_4.location = (-49.96565628051758, 806.75048828125)
    group_014.location = (-1688.847900390625, 753.6773681640625)
    group_003.location = (-3035.89697265625, -233.072265625)
    group_input_016.location = (-556.974365234375, 723.9324340820312)
    group_input_012.location = (-2009.9654541015625, 1286.75048828125)
    group_015.location = (-1609.9658203125, 1146.75048828125)
    group_input_014.location = (-2021.33056640625, 913.5067138671875)
    group_input_013.location = (-2018.759033203125, 1091.77294921875)
    separate_color_001.location = (4255.1904296875, -999.6777954101562)
    mix_001_9.location = (4436.95654296875, -965.3305053710938)
    mix_003_7.location = (4877.5087890625, -961.576171875)
    mix_002_7.location = (4649.0185546875, -963.38232421875)
    group_input_015.location = (-599.45849609375, 230.6046600341797)
    math_5.location = (3287.00830078125, 127.77780151367188)
    group_005.location = (-30.266983032226562, -142.71868896484375)
    group_input_018.location = (-564.484375, -195.13954162597656)
    group_002_4.location = (-1609.9658203125, 2226.75048828125)
    group_input_007.location = (-2009.9654541015625, 2186.75048828125)
    principled_bsdf.location = (3693.52001953125, 316.2340087890625)
    mix_007_4.location = (3494.010498046875, 196.2340087890625)
    group_4.location = (-53.98965072631836, 1419.260498046875)
    group_input_027.location = (-3481.869140625, -308.447509765625)
    math_008_2.location = (1321.500244140625, 1573.3026123046875)
    math_009_2.location = (1321.500244140625, 1613.3026123046875)

    # Set dimensions
    separate_rgb_4.width, separate_rgb_4.height = 140.0, 100.0
    math_002_3.width, math_002_3.height = 140.0, 100.0
    math_004_4.width, math_004_4.height = 140.0, 100.0
    math_005_4.width, math_005_4.height = 140.0, 100.0
    math_003_2.width, math_003_2.height = 140.0, 100.0
    normal_map.width, normal_map.height = 150.0, 100.0
    reroute_002_4.width, reroute_002_4.height = 16.0, 100.0
    reroute_011_3.width, reroute_011_3.height = 16.0, 100.0
    reroute_010_3.width, reroute_010_3.height = 16.0, 100.0
    reroute_014_3.width, reroute_014_3.height = 16.0, 100.0
    reroute_015_3.width, reroute_015_3.height = 16.0, 100.0
    reroute_018_3.width, reroute_018_3.height = 16.0, 100.0
    reroute_003_1.width, reroute_003_1.height = 16.0, 100.0
    reroute_021.width, reroute_021.height = 16.0, 100.0
    invert.width, invert.height = 140.0, 100.0
    reroute_023.width, reroute_023.height = 16.0, 100.0
    reroute_020.width, reroute_020.height = 16.0, 100.0
    reroute_026.width, reroute_026.height = 16.0, 100.0
    reroute_027.width, reroute_027.height = 16.0, 100.0
    reroute_028.width, reroute_028.height = 16.0, 100.0
    reroute_019_3.width, reroute_019_3.height = 16.0, 100.0
    reroute_025.width, reroute_025.height = 16.0, 100.0
    reroute_013_3.width, reroute_013_3.height = 16.0, 100.0
    reroute_022.width, reroute_022.height = 16.0, 100.0
    reroute_032.width, reroute_032.height = 16.0, 100.0
    reroute_033.width, reroute_033.height = 16.0, 100.0
    reroute_034.width, reroute_034.height = 16.0, 100.0
    reroute_035.width, reroute_035.height = 16.0, 100.0
    reroute_037.width, reroute_037.height = 16.0, 100.0
    reroute_016_3.width, reroute_016_3.height = 16.0, 100.0
    reroute_040.width, reroute_040.height = 16.0, 100.0
    reroute_045.width, reroute_045.height = 16.0, 100.0
    reroute_047.width, reroute_047.height = 16.0, 100.0
    reroute_050.width, reroute_050.height = 16.0, 100.0
    reroute_049.width, reroute_049.height = 16.0, 100.0
    reroute_012.width, reroute_012.height = 16.0, 100.0
    reroute_051.width, reroute_051.height = 16.0, 100.0
    reroute_053.width, reroute_053.height = 16.0, 100.0
    reroute_024.width, reroute_024.height = 16.0, 100.0
    reroute_029.width, reroute_029.height = 16.0, 100.0
    reroute_030.width, reroute_030.height = 16.0, 100.0
    reroute_054.width, reroute_054.height = 16.0, 100.0
    reroute_055.width, reroute_055.height = 16.0, 100.0
    reroute_057.width, reroute_057.height = 16.0, 100.0
    reroute_056.width, reroute_056.height = 16.0, 100.0
    reroute_060.width, reroute_060.height = 16.0, 100.0
    reroute_061.width, reroute_061.height = 16.0, 100.0
    reroute_059.width, reroute_059.height = 16.0, 100.0
    reroute_006_3.width, reroute_006_3.height = 16.0, 100.0
    reroute_063.width, reroute_063.height = 16.0, 100.0
    reroute_065.width, reroute_065.height = 16.0, 100.0
    reroute_064.width, reroute_064.height = 16.0, 100.0
    reroute_031.width, reroute_031.height = 16.0, 100.0
    reroute_004_4.width, reroute_004_4.height = 16.0, 100.0
    reroute_039.width, reroute_039.height = 16.0, 100.0
    reroute_042.width, reroute_042.height = 16.0, 100.0
    reroute_1.width, reroute_1.height = 16.0, 100.0
    reroute_001_4.width, reroute_001_4.height = 16.0, 100.0
    reroute_041.width, reroute_041.height = 16.0, 100.0
    reroute_043.width, reroute_043.height = 16.0, 100.0
    reroute_044.width, reroute_044.height = 16.0, 100.0
    reroute_062.width, reroute_062.height = 16.0, 100.0
    group_008.width, group_008.height = 140.0, 100.0
    group_input_009.width, group_input_009.height = 179.714111328125, 100.0
    group_input_004.width, group_input_004.height = 200.9415283203125, 100.0
    group_input_019.width, group_input_019.height = 200.9415283203125, 100.0
    group_input_006.width, group_input_006.height = 200.9415283203125, 100.0
    group_input_025.width, group_input_025.height = 205.6479034423828, 100.0
    group_016.width, group_016.height = 140.0, 100.0
    group_017.width, group_017.height = 239.53497314453125, 100.0
    group_020.width, group_020.height = 239.4532470703125, 100.0
    clamp_1.width, clamp_1.height = 140.0, 100.0
    clamp_001.width, clamp_001.height = 140.0, 100.0
    clamp_002.width, clamp_002.height = 140.0, 100.0
    clamp_003.width, clamp_003.height = 140.0, 100.0
    clamp_004.width, clamp_004.height = 140.0, 100.0
    clamp_005.width, clamp_005.height = 140.0, 100.0
    clamp_006.width, clamp_006.height = 140.0, 100.0
    clamp_007.width, clamp_007.height = 140.0, 100.0
    group_input_17.width, group_input_17.height = 400.0, 100.0
    mix_005_6.width, mix_005_6.height = 140.0, 100.0
    gamma.width, gamma.height = 140.0, 100.0
    math_006_1.width, math_006_1.height = 141.0074920654297, 100.0
    group_input_021.width, group_input_021.height = 106.337158203125, 100.0
    group_input_023.width, group_input_023.height = 200.9415283203125, 100.0
    group_input_022.width, group_input_022.height = 163.4935302734375, 100.0
    texture_coordinate.width, texture_coordinate.height = 140.0, 100.0
    mapping_1.width, mapping_1.height = 231.29718017578125, 100.0
    musgrave_texture.width, musgrave_texture.height = 150.0, 100.0
    colorramp_001.width, colorramp_001.height = 240.0, 100.0
    bump.width, bump.height = 140.0, 100.0
    colorramp.width, colorramp.height = 240.0, 100.0
    group_006.width, group_006.height = 140.0, 100.0
    group_012.width, group_012.height = 140.0, 100.0
    group_018.width, group_018.height = 239.4532470703125, 100.0
    group_023.width, group_023.height = 241.806396484375, 100.0
    group_019.width, group_019.height = 241.806396484375, 100.0
    group_004.width, group_004.height = 140.0, 100.0
    group_input_020.width, group_input_020.height = 200.9415283203125, 100.0
    group_input_017.width, group_input_017.height = 400.0, 100.0
    group_013.width, group_013.height = 212.21826171875, 100.0
    group_022.width, group_022.height = 212.21826171875, 100.0
    gamma_004.width, gamma_004.height = 140.0, 100.0
    group_input_008.width, group_input_008.height = 179.714111328125, 100.0
    mix_004_7.width, mix_004_7.height = 140.0, 100.0
    mix_006_7.width, mix_006_7.height = 140.0, 100.0
    gamma_002.width, gamma_002.height = 140.0, 100.0
    reroute_009.width, reroute_009.height = 16.0, 100.0
    reroute_066.width, reroute_066.height = 16.0, 100.0
    reroute_068.width, reroute_068.height = 16.0, 100.0
    reroute_067.width, reroute_067.height = 16.0, 100.0
    reroute_069.width, reroute_069.height = 16.0, 100.0
    reroute_070.width, reroute_070.height = 16.0, 100.0
    reroute_071.width, reroute_071.height = 16.0, 100.0
    reroute_072.width, reroute_072.height = 16.0, 100.0
    reroute_074.width, reroute_074.height = 16.0, 100.0
    reroute_073.width, reroute_073.height = 16.0, 100.0
    group_011.width, group_011.height = 140.0, 100.0
    group_input_011.width, group_input_011.height = 179.714111328125, 100.0
    group_010.width, group_010.height = 140.0, 100.0
    group_input_010.width, group_input_010.height = 179.714111328125, 100.0
    reroute_058.width, reroute_058.height = 16.0, 100.0
    bump_001.width, bump_001.height = 140.0, 100.0
    group_output_17.width, group_output_17.height = 140.0, 100.0
    group_input_026.width, group_input_026.height = 205.6479034423828, 100.0
    reroute_075.width, reroute_075.height = 16.0, 100.0
    reroute_007_3.width, reroute_007_3.height = 16.0, 100.0
    reroute_076.width, reroute_076.height = 16.0, 100.0
    reroute_077.width, reroute_077.height = 16.0, 100.0
    reroute_078.width, reroute_078.height = 16.0, 100.0
    reroute_005_4.width, reroute_005_4.height = 16.0, 100.0
    reroute_079.width, reroute_079.height = 16.0, 100.0
    reroute_008.width, reroute_008.height = 16.0, 100.0
    reroute_052.width, reroute_052.height = 16.0, 100.0
    gamma_003.width, gamma_003.height = 140.0, 100.0
    reroute_048.width, reroute_048.height = 16.0, 100.0
    reroute_046.width, reroute_046.height = 16.0, 100.0
    mix_11.width, mix_11.height = 140.0, 100.0
    math_001_4.width, math_001_4.height = 140.0, 100.0
    reroute_080.width, reroute_080.height = 16.0, 100.0
    reroute_083.width, reroute_083.height = 16.0, 100.0
    reroute_084.width, reroute_084.height = 16.0, 100.0
    reroute_081.width, reroute_081.height = 16.0, 100.0
    reroute_017.width, reroute_017.height = 16.0, 100.0
    math_007_1.width, math_007_1.height = 140.0, 100.0
    gamma_001.width, gamma_001.height = 140.0, 100.0
    combine_color.width, combine_color.height = 140.0, 100.0
    group_input_005.width, group_input_005.height = 200.9415283203125, 100.0
    group_009.width, group_009.height = 216.826904296875, 100.0
    group_001_4.width, group_001_4.height = 216.826904296875, 100.0
    group_014.width, group_014.height = 240.0601806640625, 100.0
    group_003.width, group_003.height = 140.0, 100.0
    group_input_016.width, group_input_016.height = 395.70654296875, 100.0
    group_input_012.width, group_input_012.height = 179.714111328125, 100.0
    group_015.width, group_015.height = 140.0, 100.0
    group_input_014.width, group_input_014.height = 179.714111328125, 100.0
    group_input_013.width, group_input_013.height = 179.714111328125, 100.0
    separate_color_001.width, separate_color_001.height = 140.0, 100.0
    mix_001_9.width, mix_001_9.height = 140.0, 100.0
    mix_003_7.width, mix_003_7.height = 140.0, 100.0
    mix_002_7.width, mix_002_7.height = 140.0, 100.0
    group_input_015.width, group_input_015.height = 400.0, 100.0
    math_5.width, math_5.height = 140.0, 100.0
    group_005.width, group_005.height = 216.25881958007812, 100.0
    group_input_018.width, group_input_018.height = 400.0, 100.0
    group_002_4.width, group_002_4.height = 140.0, 100.0
    group_input_007.width, group_input_007.height = 179.714111328125, 100.0
    principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
    mix_007_4.width, mix_007_4.height = 140.0, 100.0
    group_4.width, group_4.height = 212.21826171875, 100.0
    group_input_027.width, group_input_027.height = 200.9415283203125, 100.0
    math_008_2.width, math_008_2.height = 140.0, 100.0
    math_009_2.width, math_009_2.height = 140.0, 100.0

    # initialize hims links
    # group_002_4.Color -> group_4.Slot 1
    _ = hims.links.new(group_002_4.outputs[0], group_4.inputs[3])
    # group_004.Color -> group_4.Slot 2
    _ = hims.links.new(group_004.outputs[0], group_4.inputs[4])
    # group_008.Color -> group_4.Slot 3
    _ = hims.links.new(group_008.outputs[0], group_4.inputs[5])
    # group_010.Color -> group_4.Slot 4
    _ = hims.links.new(group_010.outputs[0], group_4.inputs[6])
    # group_011.Color -> group_4.Slot 5
    _ = hims.links.new(group_011.outputs[0], group_4.inputs[7])
    # group_012.Color -> group_4.Slot 6
    _ = hims.links.new(group_012.outputs[0], group_4.inputs[8])
    # group_015.Color -> group_4.Dust
    _ = hims.links.new(group_015.outputs[0], group_4.inputs[10])
    # group_016.Color -> group_4.Grime
    _ = hims.links.new(group_016.outputs[0], group_4.inputs[9])
    # group_input_17.Zone 1 Emmisive Amount -> group_013.Slot 1
    _ = hims.links.new(group_input_17.outputs[22], group_013.inputs[3])
    # group_input_17.Zone 2 Emmisive Amount -> group_013.Slot 2
    _ = hims.links.new(group_input_17.outputs[37], group_013.inputs[4])
    # group_input_17.Zone 3 Emmisive Amount -> group_013.Slot 3
    _ = hims.links.new(group_input_17.outputs[52], group_013.inputs[5])
    # group_input_17.Zone 4 Emmisive Amount -> group_013.Slot 4
    _ = hims.links.new(group_input_17.outputs[68], group_013.inputs[6])
    # group_input_17.Zone 5 Emmisive Amount -> group_013.Slot 5
    _ = hims.links.new(group_input_17.outputs[84], group_013.inputs[7])
    # group_input_17.Zone 6 Emmisive Amount -> group_013.Slot 6
    _ = hims.links.new(group_input_17.outputs[100], group_013.inputs[8])
    # group_014.Color -> group_4.Scratch
    _ = hims.links.new(group_014.outputs[0], group_4.inputs[11])
    # group_017.Color -> group_001_4.Scratch
    _ = hims.links.new(group_017.outputs[0], group_001_4.inputs[11])
    # group_018.Color -> group_009.Scratch
    _ = hims.links.new(group_018.outputs[0], group_009.inputs[11])
    # separate_rgb_4.Red -> math_001_4.Value
    _ = hims.links.new(separate_rgb_4.outputs[0], math_001_4.inputs[0])
    # group_input_004.Zone 1 Scratch Metallic -> group_017.Slot 1
    _ = hims.links.new(group_input_004.outputs[17], group_017.inputs[3])
    # group_input_004.Zone 2 Scratch Metallic -> group_017.Slot 2
    _ = hims.links.new(group_input_004.outputs[32], group_017.inputs[4])
    # group_input_004.Zone 3 Scratch Metallic -> group_017.Slot 3
    _ = hims.links.new(group_input_004.outputs[47], group_017.inputs[5])
    # group_input_004.Zone 4 Scratch Metallic -> group_017.Slot 4
    _ = hims.links.new(group_input_004.outputs[63], group_017.inputs[6])
    # group_input_004.Zone 5 Scratch Metallic -> group_017.Slot 5
    _ = hims.links.new(group_input_004.outputs[79], group_017.inputs[7])
    # group_input_004.Zone 6 Scratch Metallic -> group_017.Slot 6
    _ = hims.links.new(group_input_004.outputs[95], group_017.inputs[8])
    # group_input_005.Zone 1 ScratchColor -> group_014.Slot 1
    _ = hims.links.new(group_input_005.outputs[26], group_014.inputs[4])
    # group_input_005.Zone 2 ScratchColor -> group_014.Slot 2
    _ = hims.links.new(group_input_005.outputs[41], group_014.inputs[5])
    # group_input_005.Zone 3 ScratchColor -> group_014.Slot 3
    _ = hims.links.new(group_input_005.outputs[56], group_014.inputs[6])
    # group_input_005.Zone 4 Scratch Color -> group_014.Slot 4
    _ = hims.links.new(group_input_005.outputs[72], group_014.inputs[7])
    # group_input_005.Zone 5 Scratch Color -> group_014.Slot 5
    _ = hims.links.new(group_input_005.outputs[88], group_014.inputs[8])
    # group_input_005.Zone 6 Scratch Color -> group_014.Slot 6
    _ = hims.links.new(group_input_005.outputs[104], group_014.inputs[9])
    # group_input_006.Zone 1 Scratch Roughness -> group_018.Slot 1
    _ = hims.links.new(group_input_006.outputs[18], group_018.inputs[3])
    # group_input_006.Zone 2 Scratch Roughness -> group_018.Slot 2
    _ = hims.links.new(group_input_006.outputs[33], group_018.inputs[4])
    # group_input_006.Zone 3 Scratch Roughness -> group_018.Slot 3
    _ = hims.links.new(group_input_006.outputs[48], group_018.inputs[5])
    # group_input_006.Zone 4 Scratch Roughness -> group_018.Slot 4
    _ = hims.links.new(group_input_006.outputs[64], group_018.inputs[6])
    # group_input_006.Zone 5 Scratch Roughness -> group_018.Slot 5
    _ = hims.links.new(group_input_006.outputs[80], group_018.inputs[7])
    # group_input_006.Zone 6 Scratch Roughness -> group_018.Slot 6
    _ = hims.links.new(group_input_006.outputs[96], group_018.inputs[8])
    # group_input_007.Zone 1 Gradient Out -> group_002_4.Gradient Out
    _ = hims.links.new(group_input_007.outputs[13], group_002_4.inputs[0])
    # group_input_007.Zone 1 TopColor -> group_002_4.Top
    _ = hims.links.new(group_input_007.outputs[23], group_002_4.inputs[1])
    # group_input_007.Zone 1 MidColor -> group_002_4.Mid
    _ = hims.links.new(group_input_007.outputs[24], group_002_4.inputs[2])
    # group_input_007.Zone 1 BotColor -> group_002_4.Bot
    _ = hims.links.new(group_input_007.outputs[25], group_002_4.inputs[3])
    # group_input_008.Zone 2 Gradient Out -> group_004.Gradient Out
    _ = hims.links.new(group_input_008.outputs[28], group_004.inputs[0])
    # group_input_008.Zone 2 Top -> group_004.Top
    _ = hims.links.new(group_input_008.outputs[38], group_004.inputs[1])
    # group_input_008.Zone 2 Mid -> group_004.Mid
    _ = hims.links.new(group_input_008.outputs[39], group_004.inputs[2])
    # group_input_008.Zone 2 Bot -> group_004.Bot
    _ = hims.links.new(group_input_008.outputs[40], group_004.inputs[3])
    # group_input_009.Zone 3 Gradient Out -> group_008.Gradient Out
    _ = hims.links.new(group_input_009.outputs[43], group_008.inputs[0])
    # group_input_009.Zone 3 Top -> group_008.Top
    _ = hims.links.new(group_input_009.outputs[53], group_008.inputs[1])
    # group_input_009.Zone 3 Mid -> group_008.Mid
    _ = hims.links.new(group_input_009.outputs[54], group_008.inputs[2])
    # group_input_009.Zone 3 Bot -> group_008.Bot
    _ = hims.links.new(group_input_009.outputs[55], group_008.inputs[3])
    # group_input_010.Zone 4 Gradient Out -> group_010.Gradient Out
    _ = hims.links.new(group_input_010.outputs[59], group_010.inputs[0])
    # group_input_010.Zone 4 Top -> group_010.Top
    _ = hims.links.new(group_input_010.outputs[69], group_010.inputs[1])
    # group_input_010.Zone 4 Mid -> group_010.Mid
    _ = hims.links.new(group_input_010.outputs[70], group_010.inputs[2])
    # group_input_010.Zone 4 Bot -> group_010.Bot
    _ = hims.links.new(group_input_010.outputs[71], group_010.inputs[3])
    # group_input_011.Zone 5 Gradient Out -> group_011.Gradient Out
    _ = hims.links.new(group_input_011.outputs[75], group_011.inputs[0])
    # group_input_011.Zone 5 Top -> group_011.Top
    _ = hims.links.new(group_input_011.outputs[85], group_011.inputs[1])
    # group_input_011.Zone 5 Mid -> group_011.Mid
    _ = hims.links.new(group_input_011.outputs[86], group_011.inputs[2])
    # group_input_011.Zone 5 Bot -> group_011.Bot
    _ = hims.links.new(group_input_011.outputs[87], group_011.inputs[3])
    # group_input_012.Zone 6 Gradient Out -> group_012.Gradient Out
    _ = hims.links.new(group_input_012.outputs[91], group_012.inputs[0])
    # group_input_012.Zone 6 Top -> group_012.Top
    _ = hims.links.new(group_input_012.outputs[101], group_012.inputs[1])
    # group_input_012.Zone 6 Mid -> group_012.Mid
    _ = hims.links.new(group_input_012.outputs[102], group_012.inputs[2])
    # group_input_012.Zone 6 Bot -> group_012.Bot
    _ = hims.links.new(group_input_012.outputs[103], group_012.inputs[3])
    # group_input_014.Grime Gradient Out -> group_016.Gradient Out
    _ = hims.links.new(group_input_014.outputs[122], group_016.inputs[0])
    # group_input_014.Grime TopColor -> group_016.Top
    _ = hims.links.new(group_input_014.outputs[129], group_016.inputs[1])
    # group_input_014.Grime MidColor -> group_016.Mid
    _ = hims.links.new(group_input_014.outputs[130], group_016.inputs[2])
    # group_input_014.Grime BotColor -> group_016.Bot
    _ = hims.links.new(group_input_014.outputs[131], group_016.inputs[3])
    # group_input_015.ASG -> group_009.ASG Control
    _ = hims.links.new(group_input_015.outputs[0], group_009.inputs[0])
    # group_input_015.Zone 1 Rough Out -> group_009.Slot 1
    _ = hims.links.new(group_input_015.outputs[14], group_009.inputs[3])
    # group_input_015.Zone 2 Rough Out -> group_009.Slot 2
    _ = hims.links.new(group_input_015.outputs[29], group_009.inputs[4])
    # group_input_015.Zone 3 Rough Out -> group_009.Slot 3
    _ = hims.links.new(group_input_015.outputs[44], group_009.inputs[5])
    # group_input_015.Zone 4 Rough Out -> group_009.Slot 4
    _ = hims.links.new(group_input_015.outputs[60], group_009.inputs[6])
    # group_input_015.Zone 5 Rough Out -> group_009.Slot 5
    _ = hims.links.new(group_input_015.outputs[76], group_009.inputs[7])
    # group_input_015.Zone 6 Rough Out -> group_009.Slot 6
    _ = hims.links.new(group_input_015.outputs[92], group_009.inputs[8])
    # group_input_015.Grime Rough Out -> group_009.Grime
    _ = hims.links.new(group_input_015.outputs[123], group_009.inputs[10])
    # group_input_015.Zone 7 Rough Out -> group_009.Slot 7
    _ = hims.links.new(group_input_015.outputs[108], group_009.inputs[9])
    # group_input_016.ASG -> group_001_4.ASG Control
    _ = hims.links.new(group_input_016.outputs[0], group_001_4.inputs[0])
    # group_input_016.Zone 1 Metallic -> group_001_4.Slot 1
    _ = hims.links.new(group_input_016.outputs[19], group_001_4.inputs[3])
    # group_input_016.Zone 2 Metallic -> group_001_4.Slot 2
    _ = hims.links.new(group_input_016.outputs[34], group_001_4.inputs[4])
    # group_input_016.Zone 3 Metallic -> group_001_4.Slot 3
    _ = hims.links.new(group_input_016.outputs[49], group_001_4.inputs[5])
    # group_input_016.Zone 4 Metallic -> group_001_4.Slot 4
    _ = hims.links.new(group_input_016.outputs[65], group_001_4.inputs[6])
    # group_input_016.Zone 5 Metallic -> group_001_4.Slot 5
    _ = hims.links.new(group_input_016.outputs[81], group_001_4.inputs[7])
    # group_input_016.Zone 6 Metallic -> group_001_4.Slot 6
    _ = hims.links.new(group_input_016.outputs[97], group_001_4.inputs[8])
    # group_input_016.Zone 7 Metallic -> group_001_4.Slot 7
    _ = hims.links.new(group_input_016.outputs[113], group_001_4.inputs[9])
    # group_input_016.Grime Metallic -> group_001_4.Grime
    _ = hims.links.new(group_input_016.outputs[125], group_001_4.inputs[10])
    # group_input_017.ASG -> group_4.ASG Control
    _ = hims.links.new(group_input_017.outputs[0], group_4.inputs[0])
    # group_input_17.ASG -> group_013.ASG
    _ = hims.links.new(group_input_17.outputs[0], group_013.inputs[0])
    # group_input_17.Grime Emissive Amount -> group_013.Grime
    _ = hims.links.new(group_input_17.outputs[128], group_013.inputs[10])
    # group_input_17.Zone 7 Emissive Amount -> group_013.Slot 7
    _ = hims.links.new(group_input_17.outputs[116], group_013.inputs[9])
    # group_input_005.ASG -> group_014.ASG
    _ = hims.links.new(group_input_005.outputs[0], group_014.inputs[0])
    # group_input_004.ASG -> group_017.ASG
    _ = hims.links.new(group_input_004.outputs[0], group_017.inputs[0])
    # group_input_006.ASG -> group_018.ASG
    _ = hims.links.new(group_input_006.outputs[0], group_018.inputs[0])
    # reroute_014_3.Output -> colorramp.Fac
    _ = hims.links.new(reroute_014_3.outputs[0], colorramp.inputs[0])
    # group_input_019.ASG -> group_020.ASG
    _ = hims.links.new(group_input_019.outputs[0], group_020.inputs[0])
    # group_020.Color -> group_009.Scratch Amount
    _ = hims.links.new(group_020.outputs[0], group_009.inputs[12])
    # group_020.Color -> group_001_4.Scratch Amount
    _ = hims.links.new(group_020.outputs[0], group_001_4.inputs[12])
    # reroute_007_3.Output -> bump.Strength
    _ = hims.links.new(reroute_007_3.outputs[0], bump.inputs[0])
    # group_020.Color -> group_4.Scratch Amount
    _ = hims.links.new(group_020.outputs[0], group_4.inputs[15])
    # group_input_017.Grime Amount -> group_4.Grime Amount
    _ = hims.links.new(group_input_017.outputs[7], group_4.inputs[14])
    # group_input_016.Grime Amount -> group_001_4.Grime Amount
    _ = hims.links.new(group_input_016.outputs[7], group_001_4.inputs[13])
    # group_input_015.Grime Amount -> group_009.Grime Amount
    _ = hims.links.new(group_input_015.outputs[7], group_009.inputs[13])
    # group_input_17.Grime Amount -> group_013.Grime Amount
    _ = hims.links.new(group_input_17.outputs[7], group_013.inputs[11])
    # group_input_015.ASG -> separate_rgb_4.Color
    _ = hims.links.new(group_input_015.outputs[0], separate_rgb_4.inputs[0])
    # group_input_005.Grime Amount -> group_014.Grime Amount
    _ = hims.links.new(group_input_005.outputs[7], group_014.inputs[3])
    # bump.Normal -> bump_001.Normal
    _ = hims.links.new(bump.outputs[0], bump_001.inputs[3])
    # texture_coordinate.UV -> mapping_1.Vector
    _ = hims.links.new(texture_coordinate.outputs[2], mapping_1.inputs[0])
    # group_input_020.Grime Height Scale -> mapping_1.Scale
    _ = hims.links.new(group_input_020.outputs[9], mapping_1.inputs[3])
    # reroute_016_3.Output -> colorramp_001.Fac
    _ = hims.links.new(reroute_016_3.outputs[0], colorramp_001.inputs[0])
    # math_004_4.Value -> bump_001.Height
    _ = hims.links.new(math_004_4.outputs[0], bump_001.inputs[2])
    # colorramp_001.Color -> math_002_3.Value
    _ = hims.links.new(colorramp_001.outputs[0], math_002_3.inputs[0])
    # reroute_055.Output -> math_002_3.Value
    _ = hims.links.new(reroute_055.outputs[0], math_002_3.inputs[1])
    # math_002_3.Value -> math_003_2.Value
    _ = hims.links.new(math_002_3.outputs[0], math_003_2.inputs[0])
    # group_input_021.Grime Amount -> math_003_2.Value
    _ = hims.links.new(group_input_021.outputs[7], math_003_2.inputs[1])
    # math_003_2.Value -> math_004_4.Value
    _ = hims.links.new(math_003_2.outputs[0], math_004_4.inputs[0])
    # group_input_021.Grime Height Toggle -> math_004_4.Value
    _ = hims.links.new(group_input_021.outputs[8], math_004_4.inputs[1])
    # invert.Color -> mix_004_7.Factor
    _ = hims.links.new(invert.outputs[0], mix_004_7.inputs[0])
    # mix_006_7.Result -> group_output_17.Bake_Color_SpecEdition
    _ = hims.links.new(mix_006_7.outputs[2], group_output_17.inputs[6])
    # group_input_022.AO Amount -> math_001_4.Value
    _ = hims.links.new(group_input_022.outputs[10], math_001_4.inputs[1])
    # reroute_057.Output -> bump.Height
    _ = hims.links.new(reroute_057.outputs[0], bump.inputs[2])
    # reroute_029.Output -> group_output_17.Bake_Spec
    _ = hims.links.new(reroute_029.outputs[0], group_output_17.inputs[5])
    # group_input_025.ASG -> group_019.ASG
    _ = hims.links.new(group_input_025.outputs[0], group_019.inputs[0])
    # group_input_025.Grime Amount -> group_019.Grime Amount
    _ = hims.links.new(group_input_025.outputs[7], group_019.inputs[3])
    # group_input_025.Zone 1 SSS Amount -> group_019.Slot 1
    _ = hims.links.new(group_input_025.outputs[20], group_019.inputs[4])
    # group_input_025.Zone 2 SSS Amount -> group_019.Slot 2
    _ = hims.links.new(group_input_025.outputs[35], group_019.inputs[5])
    # group_input_025.Zone 3 SSS Amount -> group_019.Slot 3
    _ = hims.links.new(group_input_025.outputs[50], group_019.inputs[6])
    # group_input_025.Zone 4 SSS Amount -> group_019.Slot 4
    _ = hims.links.new(group_input_025.outputs[66], group_019.inputs[7])
    # group_input_025.Zone 5 SSS Amount -> group_019.Slot 5
    _ = hims.links.new(group_input_025.outputs[82], group_019.inputs[8])
    # group_input_025.Zone 6 SSS Amount -> group_019.Slot 6
    _ = hims.links.new(group_input_025.outputs[98], group_019.inputs[9])
    # group_input_025.Grime SSS Amount -> group_019.Grime
    _ = hims.links.new(group_input_025.outputs[126], group_019.inputs[11])
    # group_input_025.Zone 7 SSS Amount -> group_019.Slot 7
    _ = hims.links.new(group_input_025.outputs[114], group_019.inputs[10])
    # group_input_023.Scratch Height Amount -> math_005_4.Value
    _ = hims.links.new(group_input_023.outputs[11], math_005_4.inputs[1])
    # group_input_006.Zone 7 Scratch Roughness -> group_018.Slot 7
    _ = hims.links.new(group_input_006.outputs[112], group_018.inputs[9])
    # group_input_004.Zone 7 Scratch Metallic -> group_017.Slot 7
    _ = hims.links.new(group_input_004.outputs[111], group_017.inputs[9])
    # group_input_005.Zone 7 Scratch Color -> group_014.Slot 7
    _ = hims.links.new(group_input_005.outputs[120], group_014.inputs[10])
    # colorramp.Color -> math_005_4.Value
    _ = hims.links.new(colorramp.outputs[0], math_005_4.inputs[0])
    # gamma.Color -> combine_color.Red
    _ = hims.links.new(gamma.outputs[0], combine_color.inputs[0])
    # gamma_001.Color -> combine_color.Green
    _ = hims.links.new(gamma_001.outputs[0], combine_color.inputs[1])
    # combine_color.Color -> group_output_17.MaskMap <Unity>
    _ = hims.links.new(combine_color.outputs[0], group_output_17.inputs[9])
    # group_input_017.Color Override -> group_4.Color Override
    _ = hims.links.new(group_input_017.outputs[133], group_4.inputs[12])
    # group_input_017.Color Override Toggle -> group_4.Color Override Toggle
    _ = hims.links.new(group_input_017.outputs[134], group_4.inputs[13])
    # reroute_059.Output -> principled_bsdf.Normal
    _ = hims.links.new(reroute_059.outputs[0], principled_bsdf.inputs[5])
    # normal_map.Normal -> bump.Normal
    _ = hims.links.new(normal_map.outputs[0], bump.inputs[3])
    # math_006_1.Value -> group_output_17.SmoothnessMap <Unity>
    _ = hims.links.new(math_006_1.outputs[0], group_output_17.inputs[10])
    # reroute_030.Output -> group_output_17.BSDF
    _ = hims.links.new(reroute_030.outputs[0], group_output_17.inputs[0])
    # math_5.Value -> principled_bsdf.Specular IOR Level
    _ = hims.links.new(math_5.outputs[0], principled_bsdf.inputs[12])
    # reroute_002_4.Output -> reroute_1.Input
    _ = hims.links.new(reroute_002_4.outputs[0], reroute_1.inputs[0])
    # group_4.Color -> reroute_001_4.Input
    _ = hims.links.new(group_4.outputs[0], reroute_001_4.inputs[0])
    # reroute_001_4.Output -> reroute_002_4.Input
    _ = hims.links.new(reroute_001_4.outputs[0], reroute_002_4.inputs[0])
    # reroute_1.Output -> reroute_003_1.Input
    _ = hims.links.new(reroute_1.outputs[0], reroute_003_1.inputs[0])
    # reroute_003_1.Output -> reroute_004_4.Input
    _ = hims.links.new(reroute_003_1.outputs[0], reroute_004_4.inputs[0])
    # reroute_052.Output -> group_output_17.Bake_Emissive
    _ = hims.links.new(reroute_052.outputs[0], group_output_17.inputs[4])
    # reroute_004_4.Output -> reroute_005_4.Input
    _ = hims.links.new(reroute_004_4.outputs[0], reroute_005_4.inputs[0])
    # reroute_005_4.Output -> mix_005_6.A
    _ = hims.links.new(reroute_005_4.outputs[0], mix_005_6.inputs[6])
    # group_013.Color -> reroute_008.Input
    _ = hims.links.new(group_013.outputs[0], reroute_008.inputs[0])
    # reroute_008.Output -> reroute_011_3.Input
    _ = hims.links.new(reroute_008.outputs[0], reroute_011_3.inputs[0])
    # reroute_011_3.Output -> reroute_012.Input
    _ = hims.links.new(reroute_011_3.outputs[0], reroute_012.inputs[0])
    # reroute_012.Output -> reroute_013_3.Input
    _ = hims.links.new(reroute_012.outputs[0], reroute_013_3.inputs[0])
    # reroute_013_3.Output -> principled_bsdf.Emission Strength
    _ = hims.links.new(reroute_013_3.outputs[0], principled_bsdf.inputs[28])
    # group_020.Color -> reroute_006_3.Input
    _ = hims.links.new(group_020.outputs[0], reroute_006_3.inputs[0])
    # reroute_075.Output -> reroute_007_3.Input
    _ = hims.links.new(reroute_075.outputs[0], reroute_007_3.inputs[0])
    # separate_rgb_4.Green -> reroute_010_3.Input
    _ = hims.links.new(separate_rgb_4.outputs[1], reroute_010_3.inputs[0])
    # reroute_010_3.Output -> reroute_014_3.Input
    _ = hims.links.new(reroute_010_3.outputs[0], reroute_014_3.inputs[0])
    # separate_rgb_4.Blue -> reroute_015_3.Input
    _ = hims.links.new(separate_rgb_4.outputs[2], reroute_015_3.inputs[0])
    # reroute_015_3.Output -> reroute_016_3.Input
    _ = hims.links.new(reroute_015_3.outputs[0], reroute_016_3.inputs[0])
    # reroute_080.Output -> reroute_017.Input
    _ = hims.links.new(reroute_080.outputs[0], reroute_017.inputs[0])
    # reroute_081.Output -> mix_11.B
    _ = hims.links.new(reroute_081.outputs[0], mix_11.inputs[7])
    # reroute_017.Output -> reroute_018_3.Input
    _ = hims.links.new(reroute_017.outputs[0], reroute_018_3.inputs[0])
    # reroute_019_3.Output -> math_5.Value
    _ = hims.links.new(reroute_019_3.outputs[0], math_5.inputs[1])
    # reroute_018_3.Output -> reroute_019_3.Input
    _ = hims.links.new(reroute_018_3.outputs[0], reroute_019_3.inputs[0])
    # reroute_018_3.Output -> reroute_020.Input
    _ = hims.links.new(reroute_018_3.outputs[0], reroute_020.inputs[0])
    # reroute_026.Output -> gamma_001.Color
    _ = hims.links.new(reroute_026.outputs[0], gamma_001.inputs[0])
    # reroute_003_1.Output -> reroute_021.Input
    _ = hims.links.new(reroute_003_1.outputs[0], reroute_021.inputs[0])
    # reroute_021.Output -> reroute_022.Input
    _ = hims.links.new(reroute_021.outputs[0], reroute_022.inputs[0])
    # reroute_022.Output -> reroute_023.Input
    _ = hims.links.new(reroute_022.outputs[0], reroute_023.inputs[0])
    # reroute_023.Output -> group_output_17.Bake_Color
    _ = hims.links.new(reroute_023.outputs[0], group_output_17.inputs[1])
    # reroute_021.Output -> mix_004_7.A
    _ = hims.links.new(reroute_021.outputs[0], mix_004_7.inputs[6])
    # reroute_023.Output -> reroute_024.Input
    _ = hims.links.new(reroute_023.outputs[0], reroute_024.inputs[0])
    # reroute_024.Output -> mix_006_7.A
    _ = hims.links.new(reroute_024.outputs[0], mix_006_7.inputs[6])
    # reroute_022.Output -> reroute_025.Input
    _ = hims.links.new(reroute_022.outputs[0], reroute_025.inputs[0])
    # reroute_025.Output -> principled_bsdf.Emission Color
    _ = hims.links.new(reroute_025.outputs[0], principled_bsdf.inputs[27])
    # reroute_027.Output -> reroute_026.Input
    _ = hims.links.new(reroute_027.outputs[0], reroute_026.inputs[0])
    # reroute_020.Output -> reroute_027.Input
    _ = hims.links.new(reroute_020.outputs[0], reroute_027.inputs[0])
    # gamma_002.Color -> group_output_17.Bake_AO
    _ = hims.links.new(gamma_002.outputs[0], group_output_17.inputs[7])
    # reroute_028.Output -> reroute_029.Input
    _ = hims.links.new(reroute_028.outputs[0], reroute_029.inputs[0])
    # reroute_053.Output -> reroute_030.Input
    _ = hims.links.new(reroute_053.outputs[0], reroute_030.inputs[0])
    # mix_11.Result -> reroute_031.Input
    _ = hims.links.new(mix_11.outputs[2], reroute_031.inputs[0])
    # reroute_031.Output -> reroute_032.Input
    _ = hims.links.new(reroute_031.outputs[0], reroute_032.inputs[0])
    # reroute_035.Output -> reroute_033.Input
    _ = hims.links.new(reroute_035.outputs[0], reroute_033.inputs[0])
    # reroute_037.Output -> reroute_035.Input
    _ = hims.links.new(reroute_037.outputs[0], reroute_035.inputs[0])
    # group_019.Color -> reroute_037.Input
    _ = hims.links.new(group_019.outputs[0], reroute_037.inputs[0])
    # group_001_4.Color -> reroute_039.Input
    _ = hims.links.new(group_001_4.outputs[0], reroute_039.inputs[0])
    # reroute_039.Output -> reroute_040.Input
    _ = hims.links.new(reroute_039.outputs[0], reroute_040.inputs[0])
    # reroute_040.Output -> invert.Color
    _ = hims.links.new(reroute_040.outputs[0], invert.inputs[1])
    # reroute_042.Output -> principled_bsdf.Metallic
    _ = hims.links.new(reroute_042.outputs[0], principled_bsdf.inputs[1])
    # reroute_040.Output -> reroute_041.Input
    _ = hims.links.new(reroute_040.outputs[0], reroute_041.inputs[0])
    # reroute_041.Output -> reroute_042.Input
    _ = hims.links.new(reroute_041.outputs[0], reroute_042.inputs[0])
    # reroute_041.Output -> reroute_043.Input
    _ = hims.links.new(reroute_041.outputs[0], reroute_043.inputs[0])
    # gamma_004.Color -> group_output_17.Bake_Metallic
    _ = hims.links.new(gamma_004.outputs[0], group_output_17.inputs[2])
    # reroute_043.Output -> reroute_044.Input
    _ = hims.links.new(reroute_043.outputs[0], reroute_044.inputs[0])
    # reroute_044.Output -> mix_006_7.Factor
    _ = hims.links.new(reroute_044.outputs[0], mix_006_7.inputs[0])
    # reroute_043.Output -> reroute_045.Input
    _ = hims.links.new(reroute_043.outputs[0], reroute_045.inputs[0])
    # reroute_045.Output -> gamma.Color
    _ = hims.links.new(reroute_045.outputs[0], gamma.inputs[0])
    # group_009.Color -> reroute_046.Input
    _ = hims.links.new(group_009.outputs[0], reroute_046.inputs[0])
    # reroute_046.Output -> reroute_047.Input
    _ = hims.links.new(reroute_046.outputs[0], reroute_047.inputs[0])
    # reroute_047.Output -> principled_bsdf.Roughness
    _ = hims.links.new(reroute_047.outputs[0], principled_bsdf.inputs[2])
    # reroute_046.Output -> reroute_048.Input
    _ = hims.links.new(reroute_046.outputs[0], reroute_048.inputs[0])
    # reroute_048.Output -> reroute_049.Input
    _ = hims.links.new(reroute_048.outputs[0], reroute_049.inputs[0])
    # reroute_049.Output -> reroute_050.Input
    _ = hims.links.new(reroute_049.outputs[0], reroute_050.inputs[0])
    # reroute_050.Output -> math_006_1.Value
    _ = hims.links.new(reroute_050.outputs[0], math_006_1.inputs[1])
    # gamma_003.Color -> group_output_17.Bake_Roughness
    _ = hims.links.new(gamma_003.outputs[0], group_output_17.inputs[3])
    # mix_005_6.Result -> reroute_051.Input
    _ = hims.links.new(mix_005_6.outputs[2], reroute_051.inputs[0])
    # reroute_051.Output -> reroute_052.Input
    _ = hims.links.new(reroute_051.outputs[0], reroute_052.inputs[0])
    # principled_bsdf.BSDF -> reroute_053.Input
    _ = hims.links.new(principled_bsdf.outputs[0], reroute_053.inputs[0])
    # reroute_054.Output -> reroute_055.Input
    _ = hims.links.new(reroute_054.outputs[0], reroute_055.inputs[0])
    # math_005_4.Value -> reroute_056.Input
    _ = hims.links.new(math_005_4.outputs[0], reroute_056.inputs[0])
    # reroute_056.Output -> reroute_057.Input
    _ = hims.links.new(reroute_056.outputs[0], reroute_057.inputs[0])
    # bump_001.Normal -> reroute_058.Input
    _ = hims.links.new(bump_001.outputs[0], reroute_058.inputs[0])
    # reroute_058.Output -> reroute_059.Input
    _ = hims.links.new(reroute_058.outputs[0], reroute_059.inputs[0])
    # reroute_058.Output -> reroute_060.Input
    _ = hims.links.new(reroute_058.outputs[0], reroute_060.inputs[0])
    # reroute_061.Output -> group_output_17.Normal
    _ = hims.links.new(reroute_061.outputs[0], group_output_17.inputs[8])
    # reroute_060.Output -> reroute_061.Input
    _ = hims.links.new(reroute_060.outputs[0], reroute_061.inputs[0])
    # reroute_006_3.Output -> reroute_062.Input
    _ = hims.links.new(reroute_006_3.outputs[0], reroute_062.inputs[0])
    # reroute_062.Output -> reroute_063.Input
    _ = hims.links.new(reroute_062.outputs[0], reroute_063.inputs[0])
    # group_input_026.ASG -> group_023.ASG
    _ = hims.links.new(group_input_026.outputs[0], group_023.inputs[0])
    # group_input_026.Grime Amount -> group_023.Grime Amount
    _ = hims.links.new(group_input_026.outputs[7], group_023.inputs[3])
    # math_007_1.Value -> principled_bsdf.Alpha
    _ = hims.links.new(math_007_1.outputs[0], principled_bsdf.inputs[4])
    # group_input_026.Zone 1 Transparency Amount -> group_023.Slot 1
    _ = hims.links.new(group_input_026.outputs[21], group_023.inputs[4])
    # group_input_026.Zone 2 Transparency Amount -> group_023.Slot 2
    _ = hims.links.new(group_input_026.outputs[36], group_023.inputs[5])
    # group_input_026.Zone 3 Transparency Amount -> group_023.Slot 3
    _ = hims.links.new(group_input_026.outputs[51], group_023.inputs[6])
    # group_input_026.Zone 4 Transparency Amount -> group_023.Slot 4
    _ = hims.links.new(group_input_026.outputs[67], group_023.inputs[7])
    # group_input_026.Zone 5 Transparency Amount -> group_023.Slot 5
    _ = hims.links.new(group_input_026.outputs[83], group_023.inputs[8])
    # group_input_026.Zone 6 Transparency Amount -> group_023.Slot 6
    _ = hims.links.new(group_input_026.outputs[99], group_023.inputs[9])
    # group_input_026.Grime Transparency Amount -> group_023.Grime
    _ = hims.links.new(group_input_026.outputs[127], group_023.inputs[11])
    # group_023.Color -> reroute_064.Input
    _ = hims.links.new(group_023.outputs[0], reroute_064.inputs[0])
    # reroute_064.Output -> reroute_065.Input
    _ = hims.links.new(reroute_064.outputs[0], reroute_065.inputs[0])
    # reroute_065.Output -> math_007_1.Value
    _ = hims.links.new(reroute_065.outputs[0], math_007_1.inputs[1])
    # group_input_018.ASG -> group_005.ASG
    _ = hims.links.new(group_input_018.outputs[0], group_005.inputs[0])
    # group_input_018.Normal -> group_005.MainNormal
    _ = hims.links.new(group_input_018.outputs[3], group_005.inputs[3])
    # group_input_018.Zone 1 Norm Out -> group_005.Slot 1
    _ = hims.links.new(group_input_018.outputs[15], group_005.inputs[4])
    # group_input_018.Zone 2 Norm Out -> group_005.Slot 2
    _ = hims.links.new(group_input_018.outputs[30], group_005.inputs[5])
    # group_input_018.Zone 3 Norm Out -> group_005.Slot 3
    _ = hims.links.new(group_input_018.outputs[45], group_005.inputs[6])
    # group_input_018.Zone 4 Norm Out -> group_005.Slot 4
    _ = hims.links.new(group_input_018.outputs[61], group_005.inputs[7])
    # group_input_018.Zone 5 Norm Out -> group_005.Slot 5
    _ = hims.links.new(group_input_018.outputs[77], group_005.inputs[8])
    # group_input_018.Zone 6 Norm Out -> group_005.Slot 6
    _ = hims.links.new(group_input_018.outputs[93], group_005.inputs[9])
    # group_input_018.Grime Norm Out -> group_005.Grime
    _ = hims.links.new(group_input_018.outputs[124], group_005.inputs[11])
    # group_input_018.Zone 7 Norm Out -> group_005.Slot 7
    _ = hims.links.new(group_input_018.outputs[109], group_005.inputs[10])
    # group_input_018.Grime Amount -> group_005.Grime Amount
    _ = hims.links.new(group_input_018.outputs[7], group_005.inputs[13])
    # reroute_076.Output -> normal_map.Color
    _ = hims.links.new(reroute_076.outputs[0], normal_map.inputs[1])
    # reroute_062.Output -> group_005.Scratch Amount
    _ = hims.links.new(reroute_062.outputs[0], group_005.inputs[12])
    # group_input_018.Detail Norm Toggle -> group_005.Detail Normal Toggle
    _ = hims.links.new(group_input_018.outputs[4], group_005.inputs[14])
    # group_input_027.Mask_0 -> group_003.Mask_0
    _ = hims.links.new(group_input_027.outputs[1], group_003.inputs[0])
    # group_input_027.Mask_1 -> group_003.Mask_1
    _ = hims.links.new(group_input_027.outputs[2], group_003.inputs[1])
    # group_input_027.Zone 2 Toggle -> group_003.Zone 2 Toggle
    _ = hims.links.new(group_input_027.outputs[27], group_003.inputs[2])
    # group_input_027.Zone 3 Toggle -> group_003.Zone 3 Toggle
    _ = hims.links.new(group_input_027.outputs[42], group_003.inputs[3])
    # group_input_027.Zone 4 Toggle -> group_003.Zone 4 Toggle
    _ = hims.links.new(group_input_027.outputs[58], group_003.inputs[4])
    # group_input_027.Zone 5 Toggle -> group_003.Zone 5 Toggle
    _ = hims.links.new(group_input_027.outputs[74], group_003.inputs[5])
    # group_input_027.Zone 6 Toggle -> group_003.Zone 6 Toggle
    _ = hims.links.new(group_input_027.outputs[90], group_003.inputs[6])
    # group_input_027.Zone 7 Toggle -> group_003.Zone 7 Toggle
    _ = hims.links.new(group_input_027.outputs[106], group_003.inputs[7])
    # group_003.Mask_0 -> group_014.Mask_0
    _ = hims.links.new(group_003.outputs[0], group_014.inputs[1])
    # group_003.Mask_1 -> group_014.Mask_1
    _ = hims.links.new(group_003.outputs[1], group_014.inputs[2])
    # group_003.Mask_0 -> group_017.Mask_0
    _ = hims.links.new(group_003.outputs[0], group_017.inputs[1])
    # group_003.Mask_1 -> group_017.Mask_1
    _ = hims.links.new(group_003.outputs[1], group_017.inputs[2])
    # group_003.Mask_0 -> group_020.Mask_0
    _ = hims.links.new(group_003.outputs[0], group_020.inputs[1])
    # group_003.Mask_1 -> group_020.Mask_1
    _ = hims.links.new(group_003.outputs[1], group_020.inputs[2])
    # group_003.Mask_0 -> group_018.Mask_0
    _ = hims.links.new(group_003.outputs[0], group_018.inputs[1])
    # group_003.Mask_1 -> group_018.Mask_1
    _ = hims.links.new(group_003.outputs[1], group_018.inputs[2])
    # group_003.Mask_0 -> group_019.Mask_0
    _ = hims.links.new(group_003.outputs[0], group_019.inputs[1])
    # group_003.Mask_1 -> group_019.Mask_1
    _ = hims.links.new(group_003.outputs[1], group_019.inputs[2])
    # group_003.Mask_0 -> group_023.Mask_0
    _ = hims.links.new(group_003.outputs[0], group_023.inputs[1])
    # group_003.Mask_1 -> group_023.Mask_1
    _ = hims.links.new(group_003.outputs[1], group_023.inputs[2])
    # group_003.Mask_0 -> group_013.Mask_0
    _ = hims.links.new(group_003.outputs[0], group_013.inputs[1])
    # group_003.Mask_1 -> group_013.Mask_1
    _ = hims.links.new(group_003.outputs[1], group_013.inputs[2])
    # group_003.Mask_0 -> group_005.Mask_0
    _ = hims.links.new(group_003.outputs[0], group_005.inputs[1])
    # group_003.Mask_1 -> group_005.Mask_1
    _ = hims.links.new(group_003.outputs[1], group_005.inputs[2])
    # group_003.Mask_0 -> group_009.RGB Control
    _ = hims.links.new(group_003.outputs[0], group_009.inputs[1])
    # group_003.Mask_1 -> group_009.Blue Control
    _ = hims.links.new(group_003.outputs[1], group_009.inputs[2])
    # group_003.Mask_0 -> group_001_4.RGB Control
    _ = hims.links.new(group_003.outputs[0], group_001_4.inputs[1])
    # group_003.Mask_1 -> group_001_4.Blue Control
    _ = hims.links.new(group_003.outputs[1], group_001_4.inputs[2])
    # group_003.Mask_0 -> group_4.Mask_0
    _ = hims.links.new(group_003.outputs[0], group_4.inputs[1])
    # group_003.Mask_1 -> group_4.Mask_1
    _ = hims.links.new(group_003.outputs[1], group_4.inputs[2])
    # group_input_019.Zone 1 Scratch Amount -> group_006.Zone 1
    _ = hims.links.new(group_input_019.outputs[16], group_006.inputs[0])
    # group_input_019.Zone 2 Scratch Amount -> group_006.Zone 2
    _ = hims.links.new(group_input_019.outputs[31], group_006.inputs[1])
    # group_input_019.Zone 3 Scratch Amount -> group_006.Zone 3
    _ = hims.links.new(group_input_019.outputs[46], group_006.inputs[2])
    # group_input_019.Zone 4 Scratch Amount -> group_006.Zone 4
    _ = hims.links.new(group_input_019.outputs[62], group_006.inputs[3])
    # group_input_019.Zone 5 Scratch Amount -> group_006.Zone 5
    _ = hims.links.new(group_input_019.outputs[78], group_006.inputs[4])
    # group_input_019.Zone 6 Scratch Amount -> group_006.Zone 6
    _ = hims.links.new(group_input_019.outputs[94], group_006.inputs[5])
    # group_input_019.Zone 7 Scratch Amount -> group_006.Zone 7
    _ = hims.links.new(group_input_019.outputs[110], group_006.inputs[6])
    # group_input_019.Zone 1 Scratch Amount -> group_020.Slot 1
    _ = hims.links.new(group_input_019.outputs[16], group_020.inputs[3])
    # group_006.Zone 2 -> group_020.Slot 2
    _ = hims.links.new(group_006.outputs[0], group_020.inputs[4])
    # group_006.Zone 3 -> group_020.Slot 3
    _ = hims.links.new(group_006.outputs[1], group_020.inputs[5])
    # group_006.Zone 4 -> group_020.Slot 4
    _ = hims.links.new(group_006.outputs[2], group_020.inputs[6])
    # group_006.Zone 5 -> group_020.Slot 5
    _ = hims.links.new(group_006.outputs[3], group_020.inputs[7])
    # group_006.Zone 6 -> group_020.Slot 6
    _ = hims.links.new(group_006.outputs[4], group_020.inputs[8])
    # group_006.Zone Dust -> group_020.Slot 7
    _ = hims.links.new(group_006.outputs[5], group_020.inputs[9])
    # group_input_019.Global Scratch Toggle (Uses Zone 1 Scratch Amount) -> group_006.Scratch Global
    _ = hims.links.new(group_input_019.outputs[12], group_006.inputs[7])
    # clamp_1.Result -> group_022.Slot 1
    _ = hims.links.new(clamp_1.outputs[0], group_022.inputs[3])
    # clamp_001.Result -> group_022.Slot 2
    _ = hims.links.new(clamp_001.outputs[0], group_022.inputs[4])
    # clamp_002.Result -> group_022.Slot 3
    _ = hims.links.new(clamp_002.outputs[0], group_022.inputs[5])
    # clamp_003.Result -> group_022.Slot 4
    _ = hims.links.new(clamp_003.outputs[0], group_022.inputs[6])
    # clamp_004.Result -> group_022.Slot 5
    _ = hims.links.new(clamp_004.outputs[0], group_022.inputs[7])
    # clamp_005.Result -> group_022.Slot 6
    _ = hims.links.new(clamp_005.outputs[0], group_022.inputs[8])
    # clamp_006.Result -> group_022.Slot 7
    _ = hims.links.new(clamp_006.outputs[0], group_022.inputs[9])
    # clamp_007.Result -> group_022.Grime
    _ = hims.links.new(clamp_007.outputs[0], group_022.inputs[10])
    # group_input_17.Grime Amount -> group_022.Grime Amount
    _ = hims.links.new(group_input_17.outputs[7], group_022.inputs[11])
    # group_input_17.Zone 1 Emmisive Amount -> clamp_1.Value
    _ = hims.links.new(group_input_17.outputs[22], clamp_1.inputs[0])
    # group_input_17.Zone 2 Emmisive Amount -> clamp_001.Value
    _ = hims.links.new(group_input_17.outputs[37], clamp_001.inputs[0])
    # group_input_17.Zone 3 Emmisive Amount -> clamp_002.Value
    _ = hims.links.new(group_input_17.outputs[52], clamp_002.inputs[0])
    # group_input_17.Zone 4 Emmisive Amount -> clamp_003.Value
    _ = hims.links.new(group_input_17.outputs[68], clamp_003.inputs[0])
    # group_input_17.Zone 5 Emmisive Amount -> clamp_004.Value
    _ = hims.links.new(group_input_17.outputs[84], clamp_004.inputs[0])
    # group_input_17.Zone 6 Emmisive Amount -> clamp_005.Value
    _ = hims.links.new(group_input_17.outputs[100], clamp_005.inputs[0])
    # group_input_17.Zone 7 Emissive Amount -> clamp_006.Value
    _ = hims.links.new(group_input_17.outputs[116], clamp_006.inputs[0])
    # group_input_17.Grime Emissive Amount -> clamp_007.Value
    _ = hims.links.new(group_input_17.outputs[128], clamp_007.inputs[0])
    # group_input_17.ASG -> group_022.ASG
    _ = hims.links.new(group_input_17.outputs[0], group_022.inputs[0])
    # group_003.Mask_0 -> group_022.Mask_0
    _ = hims.links.new(group_003.outputs[0], group_022.inputs[1])
    # group_003.Mask_1 -> group_022.Mask_1
    _ = hims.links.new(group_003.outputs[1], group_022.inputs[2])
    # reroute_079.Output -> mix_005_6.B
    _ = hims.links.new(reroute_079.outputs[0], mix_005_6.inputs[7])
    # mapping_1.Vector -> musgrave_texture.Vector
    _ = hims.links.new(mapping_1.outputs[0], musgrave_texture.inputs[0])
    # reroute_027.Output -> gamma_002.Color
    _ = hims.links.new(reroute_027.outputs[0], gamma_002.inputs[0])
    # reroute_049.Output -> gamma_003.Color
    _ = hims.links.new(reroute_049.outputs[0], gamma_003.inputs[0])
    # reroute_044.Output -> gamma_004.Color
    _ = hims.links.new(reroute_044.outputs[0], gamma_004.inputs[0])
    # mix_004_7.Result -> reroute_028.Input
    _ = hims.links.new(mix_004_7.outputs[2], reroute_028.inputs[0])
    # group_003.Mask_0 -> reroute_009.Input
    _ = hims.links.new(group_003.outputs[0], reroute_009.inputs[0])
    _ = hims.links.new(reroute_009.outputs[0], reroute_067.inputs[0])
    _ = hims.links.new(group_003.outputs[1], reroute_066.inputs[0])
    _ = hims.links.new(reroute_066.outputs[0], reroute_068.inputs[0])
    _ = hims.links.new(reroute_068.outputs[0], reroute_070.inputs[0])
    _ = hims.links.new(reroute_067.outputs[0], reroute_069.inputs[0])
    _ = hims.links.new(reroute_069.outputs[0], reroute_071.inputs[0])
    _ = hims.links.new(reroute_070.outputs[0], reroute_072.inputs[0])
    _ = hims.links.new(reroute_071.outputs[0], reroute_073.inputs[0])
    _ = hims.links.new(reroute_072.outputs[0], reroute_074.inputs[0])
    _ = hims.links.new(reroute_074.outputs[0], separate_color_001.inputs[0])
    _ = hims.links.new(reroute_073.outputs[0], mix_001_9.inputs[6])
    _ = hims.links.new(separate_color_001.outputs[0], mix_001_9.inputs[0])
    _ = hims.links.new(mix_001_9.outputs[2], mix_002_7.inputs[6])
    _ = hims.links.new(separate_color_001.outputs[1], mix_002_7.inputs[0])
    _ = hims.links.new(mix_002_7.outputs[2], mix_003_7.inputs[6])
    _ = hims.links.new(separate_color_001.outputs[2], mix_003_7.inputs[0])
    _ = hims.links.new(mix_003_7.outputs[2], group_output_17.inputs[11])
    _ = hims.links.new(group_input_026.outputs[115], group_023.inputs[10])
    _ = hims.links.new(reroute_063.outputs[0], reroute_075.inputs[0])
    _ = hims.links.new(reroute_077.outputs[0], reroute_076.inputs[0])
    _ = hims.links.new(group_005.outputs[0], reroute_077.inputs[0])
    _ = hims.links.new(group_022.outputs[0], reroute_078.inputs[0])
    _ = hims.links.new(reroute_078.outputs[0], reroute_079.inputs[0])
    _ = hims.links.new(math_001_4.outputs[0], reroute_080.inputs[0])
    _ = hims.links.new(reroute_017.outputs[0], reroute_081.inputs[0])
    _ = hims.links.new(reroute_004_4.outputs[0], reroute_083.inputs[0])
    _ = hims.links.new(reroute_083.outputs[0], reroute_084.inputs[0])
    _ = hims.links.new(reroute_084.outputs[0], mix_11.inputs[6])
    _ = hims.links.new(group_input_013.outputs[107], group_015.inputs[0])
    _ = hims.links.new(group_input_013.outputs[117], group_015.inputs[1])
    _ = hims.links.new(group_input_013.outputs[118], group_015.inputs[2])
    _ = hims.links.new(group_input_013.outputs[119], group_015.inputs[3])
    _ = hims.links.new(group_input_018.outputs[5], group_005.inputs[15])
    _ = hims.links.new(group_input_018.outputs[6], group_005.inputs[16])
    _ = hims.links.new(reroute_032.outputs[0], mix_007_4.inputs[6])
    _ = hims.links.new(reroute_034.outputs[0], mix_007_4.inputs[7])
    _ = hims.links.new(reroute_033.outputs[0], mix_007_4.inputs[0])
    _ = hims.links.new(reroute_033.outputs[0], principled_bsdf.inputs[9])
    _ = hims.links.new(mix_007_4.outputs[2], principled_bsdf.inputs[0])
    _ = hims.links.new(math_009_2.outputs[0], reroute_054.inputs[0])
    _ = hims.links.new(math_008_2.outputs[0], math_009_2.inputs[0])
    _ = hims.links.new(musgrave_texture.outputs[0], math_008_2.inputs[0])
    return hims
