# pyright: reportAttributeAccessIssue=false

# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import (
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketShader,
    NodeSocketVector,
    ShaderNodeBsdfPrincipled,
    ShaderNodeCombineColor,
    ShaderNodeGamma,
    ShaderNodeGroup,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
)

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

from ..utils import create_node, create_socket


class HIMS:
    def __init__(self) -> None:
        self.node_tree = bpy.data.node_groups.get(
            "Halo Infinite Shader 3.0 by Chunch and ChromaCore"
        )
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Halo Infinite Shader 3.0 by Chunch and ChromaCore",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        interface = self.node_tree.interface
        outputs = interface.new_panel("Outputs")
        _ = create_socket(interface, "BSDF", NodeSocketShader, False, outputs)
        _ = create_socket(interface, "Bake Color", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Bake Metallic", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Bake Roughness", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Bake Emissive", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Bake Spec", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Bake SpecColor", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Bake AO", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Bake Normal", NodeSocketVector, False, outputs)
        _ = create_socket(interface, "Bake Unity Mask Map", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Bake Unity Smoothness Map", NodeSocketColor, False, outputs)
        _ = create_socket(interface, "Bake ID Mask", NodeSocketColor, False, outputs)

        textures = interface.new_panel("Base Textures")
        _ = create_socket(interface, "ASG Texture", NodeSocketColor, panel=textures)
        _ = create_socket(interface, "Mask 0", NodeSocketColor, panel=textures)
        _ = create_socket(interface, "Mask 1", NodeSocketColor, panel=textures)
        _ = create_socket(interface, "Normal", NodeSocketColor, panel=textures)

        settings = interface.new_panel("Globals")
        norm_toggle = create_socket(
            interface, "Detail Normal Toggle", NodeSocketFloat, panel=settings
        )
        norm_toggle.default_value = 1.0
        base_flip = create_socket(interface, "Base Normal Flip", NodeSocketFloat, panel=settings)
        base_flip.default_value = 1.0
        detail_flip = create_socket(
            interface, "Detail normal Flip", NodeSocketFloat, panel=settings
        )
        detail_flip.default_value = 1.0
        _ = create_socket(interface, "Grime Amount", NodeSocketFloat, panel=settings)
        grime_height = create_socket(
            interface, "Grime Height Toggle", NodeSocketFloat, panel=settings
        )
        grime_height.default_value = 1.0
        grime_height_scale = create_socket(
            interface, "Grime Height Scale", NodeSocketFloat, panel=settings
        )
        grime_height_scale.default_value = 100.0
        ao_amount = create_socket(interface, "AO Amount", NodeSocketFloat, panel=settings)
        ao_amount.default_value = 1.0
        scratch_height = create_socket(
            interface, "Scratch Height Amount", NodeSocketFloat, panel=settings
        )
        scratch_height.default_value = 1.0
        global_scratch = create_socket(
            interface, "Global Scratch Toggle", NodeSocketFloat, panel=settings
        )
        global_scratch.default_value = 1.0

        zone1 = interface.new_panel("Zone 1")
        _ = create_socket(interface, "Zone 1 Gradient Out", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Rough Out", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Norm Out", NodeSocketColor, panel=zone1)
        _ = create_socket(interface, "Zone 1 Scratch Amount", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Scratch Metallic", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Scratch Roughness", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Metallic", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 SSS Amount", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Transparency Amount", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Emissive Amount", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Top Color", NodeSocketColor, panel=zone1)
        _ = create_socket(interface, "Zone 1 Mid Color", NodeSocketColor, panel=zone1)
        _ = create_socket(interface, "Zone 1 Bot Color", NodeSocketColor, panel=zone1)
        _ = create_socket(interface, "Zone 1 Scratch Color", NodeSocketColor, panel=zone1)

        zone2 = interface.new_panel("Zone 2")
        _ = create_socket(interface, "Zone 2 Toggle", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Gradient Out", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Rough Out", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Norm Out", NodeSocketColor, panel=zone2)
        _ = create_socket(interface, "Zone 2 Scratch Amount", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Scratch Metallic", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Scratch Roughness", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Metallic", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 SSS Amount", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Transparency Amount", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Emissive Amount", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Top Color", NodeSocketColor, panel=zone2)
        _ = create_socket(interface, "Zone 2 Mid Color", NodeSocketColor, panel=zone2)
        _ = create_socket(interface, "Zone 2 Bot Color", NodeSocketColor, panel=zone2)
        _ = create_socket(interface, "Zone 2 Scratch Color", NodeSocketColor, panel=zone2)

        zone3 = interface.new_panel("Zone 3")
        _ = create_socket(interface, "Zone 3 Toggle", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Gradient Out", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Rough Out", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Norm Out", NodeSocketColor, panel=zone3)
        _ = create_socket(interface, "Zone 3 Scratch Amount", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Scratch Metallic", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Scratch Roughness", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Metallic", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 SSS Amount", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Transparency Amount", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Emissive Amount", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Top Color", NodeSocketColor, panel=zone3)
        _ = create_socket(interface, "Zone 3 Mid Color", NodeSocketColor, panel=zone3)
        _ = create_socket(interface, "Zone 3 Bot Color", NodeSocketColor, panel=zone3)
        _ = create_socket(interface, "Zone 3 Scratch Color", NodeSocketColor, panel=zone3)
        _ = create_socket(interface, "Zone 3 SSS Color", NodeSocketColor, panel=zone3)

        zone4 = interface.new_panel("Zone 4")
        _ = create_socket(interface, "Zone 4 Toggle", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Gradient Out", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Rough Out", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Norm Out", NodeSocketColor, panel=zone4)
        _ = create_socket(interface, "Zone 4 Scratch Amount", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Scratch Metallic", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Scratch Roughness", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Metallic", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 SSS Amount", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Transparency Amount", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Emissive Amount", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Top Color", NodeSocketColor, panel=zone4)
        _ = create_socket(interface, "Zone 4 Mid Color", NodeSocketColor, panel=zone4)
        _ = create_socket(interface, "Zone 4 Bot Color", NodeSocketColor, panel=zone4)
        _ = create_socket(interface, "Zone 4 Scratch Color", NodeSocketColor, panel=zone4)
        _ = create_socket(interface, "Zone 4 SSS Color", NodeSocketColor, panel=zone4)

        zone5 = interface.new_panel("Zone 5")
        _ = create_socket(interface, "Zone 5 Toggle", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Gradient Out", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Rough Out", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Norm Out", NodeSocketColor, panel=zone5)
        _ = create_socket(interface, "Zone 5 Scratch Amount", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Scratch Metallic", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Scratch Roughness", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Metallic", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 SSS Amount", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Transparency Amount", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Emissive Amount", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Top Color", NodeSocketColor, panel=zone5)
        _ = create_socket(interface, "Zone 5 Mid Color", NodeSocketColor, panel=zone5)
        _ = create_socket(interface, "Zone 5 Bot Color", NodeSocketColor, panel=zone5)
        _ = create_socket(interface, "Zone 5 Scratch Color", NodeSocketColor, panel=zone5)
        _ = create_socket(interface, "Zone 5 SSS Color", NodeSocketColor, panel=zone5)

        zone6 = interface.new_panel("Zone 6")
        _ = create_socket(interface, "Zone 6 Toggle", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Gradient Out", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Rough Out", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Norm Out", NodeSocketColor, panel=zone6)
        _ = create_socket(interface, "Zone 6 Scratch Amount", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Scratch Metallic", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Scratch Roughness", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Metallic", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 SSS Amount", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Transparency Amount", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Emissive Amount", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Top Color", NodeSocketColor, panel=zone6)
        _ = create_socket(interface, "Zone 6 Mid Color", NodeSocketColor, panel=zone6)
        _ = create_socket(interface, "Zone 6 Bot Color", NodeSocketColor, panel=zone6)
        _ = create_socket(interface, "Zone 6 Scratch Color", NodeSocketColor, panel=zone6)
        _ = create_socket(interface, "Zone 6 SSS Color", NodeSocketColor, panel=zone6)

        zone7 = interface.new_panel("Zone 7")
        _ = create_socket(interface, "Zone 7 Toggle", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Gradient Out", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Rough Out", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Norm Out", NodeSocketColor, panel=zone7)
        _ = create_socket(interface, "Zone 7 Scratch Amount", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Scratch Metallic", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Scratch Roughness", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Metallic", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 SSS Amount", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Transparency Amount", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Emissive Amount", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Top Color", NodeSocketColor, panel=zone7)
        _ = create_socket(interface, "Zone 7 Mid Color", NodeSocketColor, panel=zone7)
        _ = create_socket(interface, "Zone 7 Bot Color", NodeSocketColor, panel=zone7)
        _ = create_socket(interface, "Zone 7 Scratch Color", NodeSocketColor, panel=zone7)
        _ = create_socket(interface, "Zone 7 SSS Color", NodeSocketColor, panel=zone7)

        grime = interface.new_panel("Grime")
        _ = create_socket(interface, "Grime Gradient Out", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime Rough Out", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime Norm Out", NodeSocketColor, panel=grime)
        _ = create_socket(interface, "Grime Metallic", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime SSS Amount", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime Transparency Amount", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime Emissive Amount", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime Top Color", NodeSocketColor, panel=grime)
        _ = create_socket(interface, "Grime Mid Color", NodeSocketColor, panel=grime)
        _ = create_socket(interface, "Grime Bot Color", NodeSocketColor, panel=grime)
        _ = create_socket(interface, "Grime SSS Color", NodeSocketColor, panel=grime)

        overrides = interface.new_panel("Color Overrides")
        _ = create_socket(interface, "Color Override", NodeSocketColor, panel=overrides)
        override_toggle = create_socket(
            interface, "Color Override Toggle", NodeSocketFloat, panel=overrides
        )
        override_toggle.default_value = 0.0

    def create_nodes(self) -> None:
        nodes = self.node_tree.nodes

        srgb = create_node(nodes, 1210, 366, ShaderNodeSeparateColor)
        mult = create_node(nodes, 2175, 168, ShaderNodeMath)
        mult.operation = "MULTIPLY"

        mult2 = create_node(nodes, 2615, 168, ShaderNodeMath)
        mult2.operation = "MULTIPLY"
        mult2.use_clamp = True

        mult3 = create_node(nodes, 2175, -286, ShaderNodeMath)
        mult3.operation = "MULTIPLY"

        math_003_2 = create_node(nodes, 2395, -17, ShaderNodeMath)
        math_003_2.operation = "MULTIPLY"

        normal_map = nodes.new("ShaderNodeNormalMap")
        reroute_002_4 = nodes.new("NodeReroute")
        reroute_011_3 = nodes.new("NodeReroute")
        reroute_010_3 = nodes.new("NodeReroute")
        reroute_014_3 = nodes.new("NodeReroute")
        reroute_015_3 = nodes.new("NodeReroute")
        reroute_018_3 = nodes.new("NodeReroute")
        reroute_003_1 = nodes.new("NodeReroute")
        reroute_021 = nodes.new("NodeReroute")
        invert = nodes.new("ShaderNodeInvert")
        reroute_023 = nodes.new("NodeReroute")
        reroute_020 = nodes.new("NodeReroute")
        reroute_026 = nodes.new("NodeReroute")
        reroute_027 = nodes.new("NodeReroute")
        reroute_028 = nodes.new("NodeReroute")
        reroute_019_3 = nodes.new("NodeReroute")
        reroute_025 = nodes.new("NodeReroute")
        reroute_013_3 = nodes.new("NodeReroute")
        reroute_022 = nodes.new("NodeReroute")
        reroute_032 = nodes.new("NodeReroute")
        reroute_033 = nodes.new("NodeReroute")
        reroute_034 = nodes.new("NodeReroute")
        reroute_035 = nodes.new("NodeReroute")
        reroute_037 = nodes.new("NodeReroute")
        reroute_016_3 = nodes.new("NodeReroute")
        reroute_040 = nodes.new("NodeReroute")
        reroute_045 = nodes.new("NodeReroute")
        reroute_047 = nodes.new("NodeReroute")
        reroute_050 = nodes.new("NodeReroute")
        reroute_049 = nodes.new("NodeReroute")
        reroute_012 = nodes.new("NodeReroute")
        reroute_051 = nodes.new("NodeReroute")
        reroute_053 = nodes.new("NodeReroute")
        reroute_024 = nodes.new("NodeReroute")
        reroute_029 = nodes.new("NodeReroute")
        reroute_030 = nodes.new("NodeReroute")
        reroute_054 = nodes.new("NodeReroute")
        reroute_055 = nodes.new("NodeReroute")
        reroute_057 = nodes.new("NodeReroute")
        reroute_056 = nodes.new("NodeReroute")
        reroute_060 = nodes.new("NodeReroute")
        reroute_061 = nodes.new("NodeReroute")
        reroute_059 = nodes.new("NodeReroute")
        reroute_006_3 = nodes.new("NodeReroute")
        reroute_063 = nodes.new("NodeReroute")
        reroute_065 = nodes.new("NodeReroute")
        reroute_064 = nodes.new("NodeReroute")
        reroute_031 = nodes.new("NodeReroute")
        reroute_004_4 = nodes.new("NodeReroute")
        reroute_039 = nodes.new("NodeReroute")
        reroute_042 = nodes.new("NodeReroute")
        reroute_1 = nodes.new("NodeReroute")
        reroute_001_4 = nodes.new("NodeReroute")
        reroute_041 = nodes.new("NodeReroute")
        reroute_043 = nodes.new("NodeReroute")
        reroute_044 = nodes.new("NodeReroute")
        reroute_062 = nodes.new("NodeReroute")

        zone3 = create_node(nodes, -1609, 1866, ShaderNodeGroup)
        zone3.node_tree = ColorMixer().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        group_input = nodes.new("NodeGroupInput")

        group_016 = nodes.new("ShaderNodeGroup")
        group_016.node_tree = ColorMixer().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        group_017 = nodes.new("ShaderNodeGroup")
        group_017.node_tree = InfiniteMaskingSorterNoGrime().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        group_020 = nodes.new("ShaderNodeGroup")
        group_020.node_tree = InfiniteMaskingSorterNoGrime().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        clamp_1 = nodes.new("ShaderNodeClamp")
        clamp_001 = nodes.new("ShaderNodeClamp")
        clamp_002 = nodes.new("ShaderNodeClamp")
        clamp_003 = nodes.new("ShaderNodeClamp")
        clamp_004 = nodes.new("ShaderNodeClamp")
        clamp_005 = nodes.new("ShaderNodeClamp")
        clamp_006 = nodes.new("ShaderNodeClamp")
        clamp_007 = nodes.new("ShaderNodeClamp")

        mix_005_6 = create_node(nodes, 2505, -803, ShaderNodeMix)
        mix_005_6.blend_type = "MULTIPLY"
        mix_005_6.clamp_result = True
        mix_005_6.data_type = "RGBA"

        gamma = nodes.new("ShaderNodeGamma")
        gamma.inputs[1].default_value = 2.2

        math_006_1 = nodes.new("ShaderNodeMath")
        math_006_1.operation = "SUBTRACT"
        math_006_1.use_clamp = True
        math_006_1.inputs[0].default_value = 1.0
        math_006_1.inputs[2].default_value = 0.5
        texture_coordinate = nodes.new("ShaderNodeTexCoord")
        texture_coordinate.from_instancer = False

        mapping_1 = nodes.new("ShaderNodeMapping")
        mapping_1.vector_type = "POINT"
        mapping_1.inputs[1].default_value = (0.0, 0.0, 0.0)
        mapping_1.inputs[2].default_value = (0.0, 0.0, 0.0)

        musgrave_texture = nodes.new("ShaderNodeTexNoise")
        musgrave_texture.noise_dimensions = "2D"
        musgrave_texture.normalize = False
        musgrave_texture.inputs[1].default_value = 0.0
        musgrave_texture.inputs[2].default_value = 3.0
        musgrave_texture.inputs[3].default_value = 0.0
        musgrave_texture.inputs[4].default_value = 0.6944444179534912
        musgrave_texture.inputs[5].default_value = 1.2000000476837158
        musgrave_texture.inputs[6].default_value = 0.0
        musgrave_texture.inputs[7].default_value = 1.0
        musgrave_texture.inputs[8].default_value = 0.0

        colorramp_001 = nodes.new("ShaderNodeValToRGB")
        colorramp_001.color_ramp.color_mode = "RGB"
        colorramp_001.color_ramp.hue_interpolation = "NEAR"
        colorramp_001.color_ramp.interpolation = "LINEAR"

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

        bump = nodes.new("ShaderNodeBump")
        bump.invert = True
        bump.inputs[1].default_value = 0.004000000189989805

        colorramp = nodes.new("ShaderNodeValToRGB")
        colorramp.color_ramp.color_mode = "RGB"
        colorramp.color_ramp.hue_interpolation = "NEAR"
        colorramp.color_ramp.interpolation = "LINEAR"

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

        group_006 = nodes.new("ShaderNodeGroup")
        group_006.node_tree = ScratchGlobalToggle().node_tree

        group_012 = nodes.new("ShaderNodeGroup")
        group_012.node_tree = ColorMixer().node_tree

        group_018 = nodes.new("ShaderNodeGroup")
        group_018.node_tree = InfiniteMaskingSorterNoGrime().node_tree

        group_023 = nodes.new("ShaderNodeGroup")
        group_023.node_tree = InfiniteMaskingSorter().node_tree

        group_019 = nodes.new("ShaderNodeGroup")
        group_019.node_tree = InfiniteMaskingSorter().node_tree

        group_004 = nodes.new("ShaderNodeGroup")
        group_004.node_tree = ColorMixer().node_tree

        group_013 = nodes.new("ShaderNodeGroup")
        group_013.node_tree = Emission().node_tree

        group_022 = nodes.new("ShaderNodeGroup")
        group_022.node_tree = Emission().node_tree

        gamma_004 = nodes.new("ShaderNodeGamma")
        gamma_004.inputs[1].default_value = 2.2

        mix_004_7 = nodes.new("ShaderNodeMix")
        mix_004_7.clamp_result = True
        mix_004_7.inputs[7].default_value = (
            0.24701076745986938,
            0.24701084196567535,
            0.24701106548309326,
            1.0,
        )

        mix_006_7 = nodes.new("ShaderNodeMix")
        mix_006_7.blend_type = "MULTIPLY"
        mix_006_7.clamp_result = True
        mix_006_7.data_type = "RGBA"
        mix_006_7.inputs[7].default_value = (0.0, 0.0, 0.0, 1.0)

        gamma_002 = nodes.new("ShaderNodeGamma")
        gamma_002.inputs[1].default_value = 2.2

        reroute_009 = nodes.new("NodeReroute")
        reroute_066 = nodes.new("NodeReroute")
        reroute_068 = nodes.new("NodeReroute")
        reroute_067 = nodes.new("NodeReroute")
        reroute_069 = nodes.new("NodeReroute")
        reroute_070 = nodes.new("NodeReroute")
        reroute_071 = nodes.new("NodeReroute")
        reroute_072 = nodes.new("NodeReroute")
        reroute_074 = nodes.new("NodeReroute")
        reroute_073 = nodes.new("NodeReroute")
        group_011 = nodes.new("ShaderNodeGroup")
        group_011.node_tree = ColorMixer().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        group_010 = nodes.new("ShaderNodeGroup")
        group_010.node_tree = ColorMixer().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        reroute_058 = nodes.new("NodeReroute")
        bump_001 = nodes.new("ShaderNodeBump")
        strength: NodeSocketFloat = bump_001.inputs[0]
        strength.default_value = 1.0
        distance: NodeSocketFloat = bump_001.inputs[1]
        distance.default_value = 0.0075

        group_output_17 = nodes.new("NodeGroupOutput")

        reroute_075 = nodes.new("NodeReroute")
        reroute_007_3 = nodes.new("NodeReroute")
        reroute_076 = nodes.new("NodeReroute")
        reroute_077 = nodes.new("NodeReroute")
        reroute_078 = nodes.new("NodeReroute")
        reroute_005_4 = nodes.new("NodeReroute")
        reroute_079 = nodes.new("NodeReroute")
        reroute_008 = nodes.new("NodeReroute")
        reroute_052 = nodes.new("NodeReroute")

        gamma_003 = nodes.new("ShaderNodeGamma")
        gam: NodeSocketFloat = gamma_003.inputs[1]
        gam.default_value = 2.2

        reroute_048 = nodes.new("NodeReroute")
        reroute_046 = nodes.new("NodeReroute")

        mix_11 = create_node(nodes, 2478, 560, ShaderNodeMix)
        mix_11.blend_type = "MULTIPLY"
        mix_11.data_type = "RGBA"

        math_001_4 = create_node(nodes, 1747, 329, ShaderNodeMath)
        math_001_4.operation = "POWER"

        reroute_080 = nodes.new("NodeReroute")
        reroute_083 = nodes.new("NodeReroute")
        reroute_084 = nodes.new("NodeReroute")
        reroute_081 = nodes.new("NodeReroute")
        reroute_017 = nodes.new("NodeReroute")

        math_007_1 = create_node(nodes, 3092, 35, ShaderNodeMath)
        math_007_1.operation = "SUBTRACT"
        sub: NodeSocketFloat = math_007_1.inputs[0]
        sub.default_value = 1.0

        gamma_001 = create_node(nodes, 4111, -118, ShaderNodeGamma)
        gam_val: NodeSocketFloat = gamma_001.inputs[1]
        gam_val.default_value = 2.2

        combine_color = create_node(nodes, 4491, -5, ShaderNodeCombineColor)
        zero: NodeSocketFloat = combine_color.inputs[2]
        zero.default_value = 0.0

        group_009 = create_node(nodes, -50, 306, ShaderNodeGroup)
        group_009.node_tree = InfiniteMatts().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        group_001_4 = create_node(nodes, -50, 800, ShaderNodeGroup)
        group_001_4.node_tree = InfiniteMatts().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        nogrimecol = create_node(nodes, -1688, 753, ShaderNodeGroup)
        nogrimecol.node_tree = InfiniteMaskingSorterNoGrimeCol().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        masktoggles = create_node(nodes, -3035, -233, ShaderNodeGroup)
        masktoggles.node_tree = MaskToggles().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        zone7 = create_node(nodes, -1609, 1146, ShaderNodeGroup)
        zone7.node_tree = ColorMixer().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        separate_color_001 = create_node(nodes, 4255, -1000, ShaderNodeSeparateColor)

        cyan = create_node(nodes, 4436, -963, ShaderNodeMix)
        cyan.data_type = "RGBA"
        col: NodeSocketColor = cyan.inputs[7]
        col.default_value = (0.0, 1.0, 1.0, 1.0)

        magenta = create_node(nodes, 4847, -963, ShaderNodeMix)
        magenta.data_type = "RGBA"
        col = magenta.inputs[7]
        col.default_value = (1.0, 0.0, 1.0, 1.0)

        yellow = create_node(nodes, 4649, -963, ShaderNodeMix)
        yellow.data_type = "RGBA"
        col = yellow.inputs[7]
        col.default_value = (1.0, 1.0, 0.0, 1.0)

        math_5 = create_node(nodes, 3287, 127, ShaderNodeMath)
        math_5.operation = "MULTIPLY"

        detailnormals = create_node(nodes, -30, -142, ShaderNodeGroup)
        detailnormals.node_tree = DetailNormals().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        group_002_4 = create_node(nodes, -1609, 2226, ShaderNodeGroup)
        group_002_4.node_tree = ColorMixer().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        principled_bsdf = create_node(nodes, 3693, 316, ShaderNodeBsdfPrincipled)
        principled_bsdf.distribution = "GGX"
        principled_bsdf.subsurface_method = "RANDOM_WALK_SKIN"

        mixemission = create_node(nodes, 3494, 196, ShaderNodeMix)
        mixemission.data_type = "RGBA"

        infinite_color = create_node(nodes, 1210, 366, ShaderNodeGroup)
        infinite_color.node_tree = InfiniteColor().node_tree  # pyright: ignore[reportAttributeAccessIssue]

        multvoronoi = create_node(nodes, 1321, 1613, ShaderNodeMath)
        multvoronoi.operation = "MULTIPLY"
        _: NodeSocketFloat = multvoronoi.inputs[1]
        _.default_value = 0.44

        addtovoronoi = create_node(nodes, 1321, 1613, ShaderNodeMath)
        _: NodeSocketFloat = addtovoronoi.inputs[1]
        _.default_value = 0.5600000023841858

        srgb.location = (1210.0343017578125, 366.75048828125)
        mult.location = (2175.57666015625, 167.1549072265625)
        mult2.location = (2615.739501953125, -140.130126953125)
        mult3.location = (2167.04150390625, -286.380126953125)
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
        zone3.location = (-1609.9658203125, 1866.7508544921875)
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
        mix_005_6.location = (2505.625244140625, -803.4283447265625)
        gamma.location = (4112.35986328125, -12.653839111328125)
        math_006_1.location = (4489.9873046875, -158.54791259765625)
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
        group_013.location = (-42.23020935058594, -901.8160400390625)
        group_022.location = (-36.950374603271484, -1272.497802734375)
        gamma_004.location = (4798.55859375, 358.29608154296875)
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
        group_010.location = (-1609.9658203125, 1686.7501220703125)
        reroute_058.location = (3324.754638671875, -448.6982116699219)
        bump_001.location = (3108.949462890625, -414.1265563964844)
        group_output_17.location = (5216.7314453125, 406.7503967285156)
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
        group_009.location = (-49.96565628051758, 306.75048828125)
        group_001_4.location = (-49.96565628051758, 806.75048828125)
        nogrimecol.location = (-1688.847900390625, 753.6773681640625)
        masktoggles.location = (-3035.89697265625, -233.072265625)
        zone7.location = (-1609.9658203125, 1146.75048828125)
        separate_color_001.location = (4255.1904296875, -999.6777954101562)
        cyan.location = (4436.95654296875, -965.3305053710938)
        magenta.location = (4877.5087890625, -961.576171875)
        yellow.location = (4649.0185546875, -963.38232421875)
        math_5.location = (3287.00830078125, 127.77780151367188)
        detailnormals.location = (-30.266983032226562, -142.71868896484375)
        group_002_4.location = (-1609.9658203125, 2226.75048828125)
        principled_bsdf.location = (3693.52001953125, 316.2340087890625)
        mixemission.location = (3494.010498046875, 196.2340087890625)
        infinite_color.location = (-53.98965072631836, 1419.260498046875)
        multvoronoi.location = (1321.500244140625, 1573.3026123046875)
        addtovoronoi.location = (1321.500244140625, 1613.3026123046875)

        _ = self.node_tree.links.new(group_002_4.outputs[0], infinite_color.inputs[3])
        _ = self.node_tree.links.new(group_004.outputs[0], infinite_color.inputs[4])
        _ = self.node_tree.links.new(zone3.outputs[0], infinite_color.inputs[5])
        _ = self.node_tree.links.new(group_010.outputs[0], infinite_color.inputs[6])
        _ = self.node_tree.links.new(group_011.outputs[0], infinite_color.inputs[7])
        _ = self.node_tree.links.new(group_012.outputs[0], infinite_color.inputs[8])
        _ = self.node_tree.links.new(zone7.outputs[0], infinite_color.inputs[10])
        _ = self.node_tree.links.new(group_016.outputs[0], infinite_color.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[22], group_013.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[37], group_013.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[52], group_013.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[68], group_013.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[84], group_013.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[100], group_013.inputs[8])
        _ = self.node_tree.links.new(nogrimecol.outputs[0], infinite_color.inputs[11])
        _ = self.node_tree.links.new(group_017.outputs[0], group_001_4.inputs[11])
        _ = self.node_tree.links.new(group_018.outputs[0], group_009.inputs[11])
        _ = self.node_tree.links.new(srgb.outputs[0], math_001_4.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[17], group_017.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[32], group_017.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[47], group_017.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[63], group_017.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[79], group_017.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[95], group_017.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[26], nogrimecol.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[41], nogrimecol.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[56], nogrimecol.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[72], nogrimecol.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[88], nogrimecol.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[104], nogrimecol.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[18], group_018.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[33], group_018.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[48], group_018.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[64], group_018.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[80], group_018.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[96], group_018.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[13], group_002_4.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[23], group_002_4.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[24], group_002_4.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[25], group_002_4.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[28], group_004.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[38], group_004.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[39], group_004.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[40], group_004.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[43], zone3.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[53], zone3.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[54], zone3.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[55], zone3.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[59], group_010.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[69], group_010.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[70], group_010.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[71], group_010.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[75], group_011.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[85], group_011.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[86], group_011.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[87], group_011.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[91], group_012.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[101], group_012.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[102], group_012.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[103], group_012.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[122], group_016.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[129], group_016.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[130], group_016.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[131], group_016.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[0], group_009.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[14], group_009.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[29], group_009.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[44], group_009.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[60], group_009.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[76], group_009.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[92], group_009.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[123], group_009.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[108], group_009.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[0], group_001_4.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[19], group_001_4.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[34], group_001_4.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[49], group_001_4.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[65], group_001_4.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[81], group_001_4.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[97], group_001_4.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[113], group_001_4.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[125], group_001_4.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[0], infinite_color.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_013.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[128], group_013.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[116], group_013.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[0], nogrimecol.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_017.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_018.inputs[0])
        _ = self.node_tree.links.new(reroute_014_3.outputs[0], colorramp.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_020.inputs[0])
        _ = self.node_tree.links.new(group_020.outputs[0], group_009.inputs[12])
        _ = self.node_tree.links.new(group_020.outputs[0], group_001_4.inputs[12])
        _ = self.node_tree.links.new(reroute_007_3.outputs[0], bump.inputs[0])
        _ = self.node_tree.links.new(group_020.outputs[0], infinite_color.inputs[15])
        _ = self.node_tree.links.new(group_input.outputs[7], infinite_color.inputs[14])
        _ = self.node_tree.links.new(group_input.outputs[7], group_001_4.inputs[13])
        _ = self.node_tree.links.new(group_input.outputs[7], group_009.inputs[13])
        _ = self.node_tree.links.new(group_input.outputs[7], group_013.inputs[11])
        _ = self.node_tree.links.new(group_input.outputs[0], srgb.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[7], nogrimecol.inputs[3])
        _ = self.node_tree.links.new(bump.outputs[0], bump_001.inputs[3])
        _ = self.node_tree.links.new(texture_coordinate.outputs[2], mapping_1.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[9], mapping_1.inputs[3])
        _ = self.node_tree.links.new(reroute_016_3.outputs[0], colorramp_001.inputs[0])
        _ = self.node_tree.links.new(mult2.outputs[0], bump_001.inputs[2])
        _ = self.node_tree.links.new(colorramp_001.outputs[0], mult.inputs[0])
        _ = self.node_tree.links.new(reroute_055.outputs[0], mult.inputs[1])
        _ = self.node_tree.links.new(mult.outputs[0], math_003_2.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[7], math_003_2.inputs[1])
        _ = self.node_tree.links.new(math_003_2.outputs[0], mult2.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[8], mult2.inputs[1])
        _ = self.node_tree.links.new(invert.outputs[0], mix_004_7.inputs[0])
        _ = self.node_tree.links.new(mix_006_7.outputs[2], group_output_17.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[10], math_001_4.inputs[1])
        _ = self.node_tree.links.new(reroute_057.outputs[0], bump.inputs[2])
        _ = self.node_tree.links.new(reroute_029.outputs[0], group_output_17.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[0], group_019.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[7], group_019.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[20], group_019.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[35], group_019.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[50], group_019.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[66], group_019.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[82], group_019.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[98], group_019.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[126], group_019.inputs[11])
        _ = self.node_tree.links.new(group_input.outputs[114], group_019.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[11], mult3.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[112], group_018.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[111], group_017.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[120], nogrimecol.inputs[10])
        _ = self.node_tree.links.new(colorramp.outputs[0], mult3.inputs[0])
        _ = self.node_tree.links.new(gamma.outputs[0], combine_color.inputs[0])
        _ = self.node_tree.links.new(gamma_001.outputs[0], combine_color.inputs[1])
        _ = self.node_tree.links.new(combine_color.outputs[0], group_output_17.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[133], infinite_color.inputs[12])
        _ = self.node_tree.links.new(group_input.outputs[134], infinite_color.inputs[13])
        _ = self.node_tree.links.new(reroute_059.outputs[0], principled_bsdf.inputs[5])
        _ = self.node_tree.links.new(normal_map.outputs[0], bump.inputs[3])
        _ = self.node_tree.links.new(math_006_1.outputs[0], group_output_17.inputs[10])
        _ = self.node_tree.links.new(reroute_030.outputs[0], group_output_17.inputs[0])
        _ = self.node_tree.links.new(math_5.outputs[0], principled_bsdf.inputs[12])
        _ = self.node_tree.links.new(reroute_002_4.outputs[0], reroute_1.inputs[0])
        _ = self.node_tree.links.new(infinite_color.outputs[0], reroute_001_4.inputs[0])
        _ = self.node_tree.links.new(reroute_001_4.outputs[0], reroute_002_4.inputs[0])
        _ = self.node_tree.links.new(reroute_1.outputs[0], reroute_003_1.inputs[0])
        _ = self.node_tree.links.new(reroute_003_1.outputs[0], reroute_004_4.inputs[0])
        _ = self.node_tree.links.new(reroute_052.outputs[0], group_output_17.inputs[4])
        _ = self.node_tree.links.new(reroute_004_4.outputs[0], reroute_005_4.inputs[0])
        _ = self.node_tree.links.new(reroute_005_4.outputs[0], mix_005_6.inputs[6])
        _ = self.node_tree.links.new(group_013.outputs[0], reroute_008.inputs[0])
        _ = self.node_tree.links.new(reroute_008.outputs[0], reroute_011_3.inputs[0])
        _ = self.node_tree.links.new(reroute_011_3.outputs[0], reroute_012.inputs[0])
        _ = self.node_tree.links.new(reroute_012.outputs[0], reroute_013_3.inputs[0])
        _ = self.node_tree.links.new(reroute_013_3.outputs[0], principled_bsdf.inputs[28])
        _ = self.node_tree.links.new(group_020.outputs[0], reroute_006_3.inputs[0])
        _ = self.node_tree.links.new(reroute_075.outputs[0], reroute_007_3.inputs[0])
        _ = self.node_tree.links.new(srgb.outputs[1], reroute_010_3.inputs[0])
        _ = self.node_tree.links.new(reroute_010_3.outputs[0], reroute_014_3.inputs[0])
        _ = self.node_tree.links.new(srgb.outputs[2], reroute_015_3.inputs[0])
        _ = self.node_tree.links.new(reroute_015_3.outputs[0], reroute_016_3.inputs[0])
        _ = self.node_tree.links.new(reroute_080.outputs[0], reroute_017.inputs[0])
        _ = self.node_tree.links.new(reroute_081.outputs[0], mix_11.inputs[7])
        _ = self.node_tree.links.new(reroute_017.outputs[0], reroute_018_3.inputs[0])
        _ = self.node_tree.links.new(reroute_019_3.outputs[0], math_5.inputs[1])
        _ = self.node_tree.links.new(reroute_018_3.outputs[0], reroute_019_3.inputs[0])
        _ = self.node_tree.links.new(reroute_018_3.outputs[0], reroute_020.inputs[0])
        _ = self.node_tree.links.new(reroute_026.outputs[0], gamma_001.inputs[0])
        _ = self.node_tree.links.new(reroute_003_1.outputs[0], reroute_021.inputs[0])
        _ = self.node_tree.links.new(reroute_021.outputs[0], reroute_022.inputs[0])
        _ = self.node_tree.links.new(reroute_022.outputs[0], reroute_023.inputs[0])
        _ = self.node_tree.links.new(reroute_023.outputs[0], group_output_17.inputs[1])
        _ = self.node_tree.links.new(reroute_021.outputs[0], mix_004_7.inputs[6])
        _ = self.node_tree.links.new(reroute_023.outputs[0], reroute_024.inputs[0])
        _ = self.node_tree.links.new(reroute_024.outputs[0], mix_006_7.inputs[6])
        _ = self.node_tree.links.new(reroute_022.outputs[0], reroute_025.inputs[0])
        _ = self.node_tree.links.new(reroute_025.outputs[0], principled_bsdf.inputs[27])
        _ = self.node_tree.links.new(reroute_027.outputs[0], reroute_026.inputs[0])
        _ = self.node_tree.links.new(reroute_020.outputs[0], reroute_027.inputs[0])
        _ = self.node_tree.links.new(gamma_002.outputs[0], group_output_17.inputs[7])
        _ = self.node_tree.links.new(reroute_028.outputs[0], reroute_029.inputs[0])
        _ = self.node_tree.links.new(reroute_053.outputs[0], reroute_030.inputs[0])
        _ = self.node_tree.links.new(mix_11.outputs[2], reroute_031.inputs[0])
        _ = self.node_tree.links.new(reroute_031.outputs[0], reroute_032.inputs[0])
        _ = self.node_tree.links.new(reroute_035.outputs[0], reroute_033.inputs[0])
        _ = self.node_tree.links.new(reroute_037.outputs[0], reroute_035.inputs[0])
        _ = self.node_tree.links.new(group_019.outputs[0], reroute_037.inputs[0])
        _ = self.node_tree.links.new(group_001_4.outputs[0], reroute_039.inputs[0])
        _ = self.node_tree.links.new(reroute_039.outputs[0], reroute_040.inputs[0])
        _ = self.node_tree.links.new(reroute_040.outputs[0], invert.inputs[1])
        _ = self.node_tree.links.new(reroute_042.outputs[0], principled_bsdf.inputs[1])
        _ = self.node_tree.links.new(reroute_040.outputs[0], reroute_041.inputs[0])
        _ = self.node_tree.links.new(reroute_041.outputs[0], reroute_042.inputs[0])
        _ = self.node_tree.links.new(reroute_041.outputs[0], reroute_043.inputs[0])
        _ = self.node_tree.links.new(gamma_004.outputs[0], group_output_17.inputs[2])
        _ = self.node_tree.links.new(reroute_043.outputs[0], reroute_044.inputs[0])
        _ = self.node_tree.links.new(reroute_044.outputs[0], mix_006_7.inputs[0])
        _ = self.node_tree.links.new(reroute_043.outputs[0], reroute_045.inputs[0])
        _ = self.node_tree.links.new(reroute_045.outputs[0], gamma.inputs[0])
        _ = self.node_tree.links.new(group_009.outputs[0], reroute_046.inputs[0])
        _ = self.node_tree.links.new(reroute_046.outputs[0], reroute_047.inputs[0])
        _ = self.node_tree.links.new(reroute_047.outputs[0], principled_bsdf.inputs[2])
        _ = self.node_tree.links.new(reroute_046.outputs[0], reroute_048.inputs[0])
        _ = self.node_tree.links.new(reroute_048.outputs[0], reroute_049.inputs[0])
        _ = self.node_tree.links.new(reroute_049.outputs[0], reroute_050.inputs[0])
        _ = self.node_tree.links.new(reroute_050.outputs[0], math_006_1.inputs[1])
        _ = self.node_tree.links.new(gamma_003.outputs[0], group_output_17.inputs[3])
        _ = self.node_tree.links.new(mix_005_6.outputs[2], reroute_051.inputs[0])
        _ = self.node_tree.links.new(reroute_051.outputs[0], reroute_052.inputs[0])
        _ = self.node_tree.links.new(principled_bsdf.outputs[0], reroute_053.inputs[0])
        _ = self.node_tree.links.new(reroute_054.outputs[0], reroute_055.inputs[0])
        _ = self.node_tree.links.new(mult3.outputs[0], reroute_056.inputs[0])
        _ = self.node_tree.links.new(reroute_056.outputs[0], reroute_057.inputs[0])
        _ = self.node_tree.links.new(bump_001.outputs[0], reroute_058.inputs[0])
        _ = self.node_tree.links.new(reroute_058.outputs[0], reroute_059.inputs[0])
        _ = self.node_tree.links.new(reroute_058.outputs[0], reroute_060.inputs[0])
        _ = self.node_tree.links.new(reroute_061.outputs[0], group_output_17.inputs[8])
        _ = self.node_tree.links.new(reroute_060.outputs[0], reroute_061.inputs[0])
        _ = self.node_tree.links.new(reroute_006_3.outputs[0], reroute_062.inputs[0])
        _ = self.node_tree.links.new(reroute_062.outputs[0], reroute_063.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_023.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[7], group_023.inputs[3])
        _ = self.node_tree.links.new(math_007_1.outputs[0], principled_bsdf.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[21], group_023.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[36], group_023.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[51], group_023.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[67], group_023.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[83], group_023.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[99], group_023.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[127], group_023.inputs[11])
        _ = self.node_tree.links.new(group_023.outputs[0], reroute_064.inputs[0])
        _ = self.node_tree.links.new(reroute_064.outputs[0], reroute_065.inputs[0])
        _ = self.node_tree.links.new(reroute_065.outputs[0], math_007_1.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[0], detailnormals.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[3], detailnormals.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[15], detailnormals.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[30], detailnormals.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[45], detailnormals.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[61], detailnormals.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[77], detailnormals.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[93], detailnormals.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[124], detailnormals.inputs[11])
        _ = self.node_tree.links.new(group_input.outputs[109], detailnormals.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[7], detailnormals.inputs[13])
        _ = self.node_tree.links.new(reroute_076.outputs[0], normal_map.inputs[1])
        _ = self.node_tree.links.new(reroute_062.outputs[0], detailnormals.inputs[12])
        _ = self.node_tree.links.new(group_input.outputs[4], detailnormals.inputs[14])
        _ = self.node_tree.links.new(group_input.outputs[1], masktoggles.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[2], masktoggles.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[27], masktoggles.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[42], masktoggles.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[58], masktoggles.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[74], masktoggles.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[90], masktoggles.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[106], masktoggles.inputs[7])
        _ = self.node_tree.links.new(masktoggles.outputs[0], nogrimecol.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], nogrimecol.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_017.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_017.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_020.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_020.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_018.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_018.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_019.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_019.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_023.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_023.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_013.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_013.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[0], detailnormals.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], detailnormals.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_009.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_009.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_001_4.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_001_4.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[0], infinite_color.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], infinite_color.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[16], group_006.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[31], group_006.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[46], group_006.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[62], group_006.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[78], group_006.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[94], group_006.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[110], group_006.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[16], group_020.inputs[3])
        _ = self.node_tree.links.new(group_006.outputs[0], group_020.inputs[4])
        _ = self.node_tree.links.new(group_006.outputs[1], group_020.inputs[5])
        _ = self.node_tree.links.new(group_006.outputs[2], group_020.inputs[6])
        _ = self.node_tree.links.new(group_006.outputs[3], group_020.inputs[7])
        _ = self.node_tree.links.new(group_006.outputs[4], group_020.inputs[8])
        _ = self.node_tree.links.new(group_006.outputs[5], group_020.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[12], group_006.inputs[7])
        _ = self.node_tree.links.new(clamp_1.outputs[0], group_022.inputs[3])
        _ = self.node_tree.links.new(clamp_001.outputs[0], group_022.inputs[4])
        _ = self.node_tree.links.new(clamp_002.outputs[0], group_022.inputs[5])
        _ = self.node_tree.links.new(clamp_003.outputs[0], group_022.inputs[6])
        _ = self.node_tree.links.new(clamp_004.outputs[0], group_022.inputs[7])
        _ = self.node_tree.links.new(clamp_005.outputs[0], group_022.inputs[8])
        _ = self.node_tree.links.new(clamp_006.outputs[0], group_022.inputs[9])
        _ = self.node_tree.links.new(clamp_007.outputs[0], group_022.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[7], group_022.inputs[11])
        _ = self.node_tree.links.new(group_input.outputs[22], clamp_1.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[37], clamp_001.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[52], clamp_002.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[68], clamp_003.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[84], clamp_004.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[100], clamp_005.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[116], clamp_006.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[128], clamp_007.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_022.inputs[0])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_022.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_022.inputs[2])
        _ = self.node_tree.links.new(reroute_079.outputs[0], mix_005_6.inputs[7])
        _ = self.node_tree.links.new(mapping_1.outputs[0], musgrave_texture.inputs[0])
        _ = self.node_tree.links.new(reroute_027.outputs[0], gamma_002.inputs[0])
        _ = self.node_tree.links.new(reroute_049.outputs[0], gamma_003.inputs[0])
        _ = self.node_tree.links.new(reroute_044.outputs[0], gamma_004.inputs[0])
        _ = self.node_tree.links.new(mix_004_7.outputs[2], reroute_028.inputs[0])
        _ = self.node_tree.links.new(masktoggles.outputs[0], reroute_009.inputs[0])
        _ = self.node_tree.links.new(reroute_009.outputs[0], reroute_067.inputs[0])
        _ = self.node_tree.links.new(masktoggles.outputs[1], reroute_066.inputs[0])
        _ = self.node_tree.links.new(reroute_066.outputs[0], reroute_068.inputs[0])
        _ = self.node_tree.links.new(reroute_068.outputs[0], reroute_070.inputs[0])
        _ = self.node_tree.links.new(reroute_067.outputs[0], reroute_069.inputs[0])
        _ = self.node_tree.links.new(reroute_069.outputs[0], reroute_071.inputs[0])
        _ = self.node_tree.links.new(reroute_070.outputs[0], reroute_072.inputs[0])
        _ = self.node_tree.links.new(reroute_071.outputs[0], reroute_073.inputs[0])
        _ = self.node_tree.links.new(reroute_072.outputs[0], reroute_074.inputs[0])
        _ = self.node_tree.links.new(reroute_074.outputs[0], separate_color_001.inputs[0])
        _ = self.node_tree.links.new(reroute_073.outputs[0], cyan.inputs[6])
        _ = self.node_tree.links.new(separate_color_001.outputs[0], cyan.inputs[0])
        _ = self.node_tree.links.new(cyan.outputs[2], yellow.inputs[6])
        _ = self.node_tree.links.new(separate_color_001.outputs[1], yellow.inputs[0])
        _ = self.node_tree.links.new(yellow.outputs[2], magenta.inputs[6])
        _ = self.node_tree.links.new(separate_color_001.outputs[2], magenta.inputs[0])
        _ = self.node_tree.links.new(magenta.outputs[2], group_output_17.inputs[11])
        _ = self.node_tree.links.new(group_input.outputs[115], group_023.inputs[10])
        _ = self.node_tree.links.new(reroute_063.outputs[0], reroute_075.inputs[0])
        _ = self.node_tree.links.new(reroute_077.outputs[0], reroute_076.inputs[0])
        _ = self.node_tree.links.new(detailnormals.outputs[0], reroute_077.inputs[0])
        _ = self.node_tree.links.new(group_022.outputs[0], reroute_078.inputs[0])
        _ = self.node_tree.links.new(reroute_078.outputs[0], reroute_079.inputs[0])
        _ = self.node_tree.links.new(math_001_4.outputs[0], reroute_080.inputs[0])
        _ = self.node_tree.links.new(reroute_017.outputs[0], reroute_081.inputs[0])
        _ = self.node_tree.links.new(reroute_004_4.outputs[0], reroute_083.inputs[0])
        _ = self.node_tree.links.new(reroute_083.outputs[0], reroute_084.inputs[0])
        _ = self.node_tree.links.new(reroute_084.outputs[0], mix_11.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[107], zone7.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[117], zone7.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[118], zone7.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[119], zone7.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[5], detailnormals.inputs[15])
        _ = self.node_tree.links.new(group_input.outputs[6], detailnormals.inputs[16])
        _ = self.node_tree.links.new(reroute_032.outputs[0], mixemission.inputs[6])
        _ = self.node_tree.links.new(reroute_034.outputs[0], mixemission.inputs[7])
        _ = self.node_tree.links.new(reroute_033.outputs[0], mixemission.inputs[0])
        _ = self.node_tree.links.new(reroute_033.outputs[0], principled_bsdf.inputs[9])
        _ = self.node_tree.links.new(mixemission.outputs[2], principled_bsdf.inputs[0])
        _ = self.node_tree.links.new(addtovoronoi.outputs[0], reroute_054.inputs[0])
        _ = self.node_tree.links.new(multvoronoi.outputs[0], addtovoronoi.inputs[0])
        _ = self.node_tree.links.new(musgrave_texture.outputs[0], multvoronoi.inputs[0])
