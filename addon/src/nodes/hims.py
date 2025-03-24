# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import cast
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeLink,
    NodeSocket,
    NodeSocketBool,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketShader,
    NodeSocketVector,
    NodeTree,
    ShaderNodeBsdfPrincipled,
    ShaderNodeBump,
    ShaderNodeClamp,
    ShaderNodeCombineColor,
    ShaderNodeCombineRGB,
    ShaderNodeCombineXYZ,
    ShaderNodeGamma,
    ShaderNodeGroup,
    ShaderNodeInvert,
    ShaderNodeMapping,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeNormalMap,
    ShaderNodeSeparateColor,
    ShaderNodeSeparateRGB,
    ShaderNodeTexCoord,
    ShaderNodeTexNoise,
    ShaderNodeTree,
    ShaderNodeValToRGB,
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

from ..utils import assign_value, create_node, create_socket

__all__ = ["HIMS"]


class HIMS:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get(
            "Halo Infinite Shader 3.1.2 by Chunch and ChromaCore"
        )
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Halo Infinite Shader 3.1.2 by Chunch and ChromaCore",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None or self.node_tree.interface is None:
            return
        interface = self.node_tree.interface
        outputs = interface.new_panel("Outputs")
        _: NodeSocket
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
        _ = create_socket(interface, "Bake ORM", NodeSocketColor, False, outputs)

        textures = interface.new_panel("Base Textures")
        asg = create_socket(interface, "ASG Texture", NodeSocketColor, panel=textures)
        asg.default_value = (1.0, 1.0, 1.0, 1.0)
        _ = create_socket(interface, "Mask 0", NodeSocketColor, panel=textures)
        _ = create_socket(interface, "Mask 1", NodeSocketColor, panel=textures)
        normal = create_socket(interface, "Normal", NodeSocketColor, panel=textures)
        normal.default_value = (0.5, 0.5, 1.0, 1.0)

        settings = interface.new_panel("Globals")
        norm = create_socket(interface, "Detail Normal Toggle", NodeSocketBool, panel=settings)
        norm.default_value = True
        base_flip = create_socket(interface, "Base Normal Flip", NodeSocketBool, panel=settings)
        base_flip.default_value = True
        detail_flip = create_socket(interface, "Detail Normal Flip", NodeSocketBool, panel=settings)
        detail_flip.default_value = True

        _ = create_socket(interface, "Grime Amount", NodeSocketFloat, panel=settings)
        grime_h = create_socket(interface, "Grime Height Toggle", NodeSocketFloat, panel=settings)
        grime_h.default_value = 3.048
        grime_hs = create_socket(interface, "Grime Height Scale", NodeSocketFloat, panel=settings)
        grime_hs.default_value = 50.0
        ao_amount = create_socket(interface, "AO Amount", NodeSocketFloat, panel=settings)
        ao_amount.default_value = 1.0
        sh = create_socket(interface, "Scratch Height Amount", NodeSocketFloat, panel=settings)
        sh.default_value = 3.048
        gs = create_socket(interface, "Global Scratch Toggle", NodeSocketBool, panel=settings)
        gs.default_value = True

        zone1 = interface.new_panel("Zone 1")
        _ = create_socket(interface, "", NodeSocketBool, panel=zone1)
        interface.items_tree[30].hide_value = True  # pyright: ignore[reportAttributeAccessIssue]
        _ = create_socket(interface, "Zone 1 Gradient Out", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Rough Out", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Norm Out", NodeSocketColor, panel=zone1)
        _ = create_socket(interface, "Zone 1 Scratch Amount", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Scratch Metallic", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Scratch Roughness", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Metallic", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Transparency Amount", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Emissive Amount", NodeSocketFloat, panel=zone1)
        _ = create_socket(interface, "Zone 1 Top Color", NodeSocketColor, panel=zone1)
        _ = create_socket(interface, "Zone 1 Mid Color", NodeSocketColor, panel=zone1)
        _ = create_socket(interface, "Zone 1 Bot Color", NodeSocketColor, panel=zone1)
        _ = create_socket(interface, "Zone 1 Scratch Color", NodeSocketColor, panel=zone1)

        zone2 = interface.new_panel("Zone 2")
        _ = create_socket(interface, "Zone 2 Toggle", NodeSocketBool, panel=zone2)
        _ = create_socket(interface, "Zone 2 Gradient Out", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Rough Out", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Norm Out", NodeSocketColor, panel=zone2)
        _ = create_socket(interface, "Zone 2 Scratch Amount", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Scratch Metallic", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Scratch Roughness", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Metallic", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Transparency Amount", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Emissive Amount", NodeSocketFloat, panel=zone2)
        _ = create_socket(interface, "Zone 2 Top Color", NodeSocketColor, panel=zone2)
        _ = create_socket(interface, "Zone 2 Mid Color", NodeSocketColor, panel=zone2)
        _ = create_socket(interface, "Zone 2 Bot Color", NodeSocketColor, panel=zone2)
        _ = create_socket(interface, "Zone 2 Scratch Color", NodeSocketColor, panel=zone2)

        zone3 = interface.new_panel("Zone 3")
        _ = create_socket(interface, "Zone 3 Toggle", NodeSocketBool, panel=zone3)
        _ = create_socket(interface, "Zone 3 Gradient Out", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Rough Out", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Norm Out", NodeSocketColor, panel=zone3)
        _ = create_socket(interface, "Zone 3 Scratch Amount", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Scratch Metallic", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Scratch Roughness", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Metallic", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Transparency Amount", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Emissive Amount", NodeSocketFloat, panel=zone3)
        _ = create_socket(interface, "Zone 3 Top Color", NodeSocketColor, panel=zone3)
        _ = create_socket(interface, "Zone 3 Mid Color", NodeSocketColor, panel=zone3)
        _ = create_socket(interface, "Zone 3 Bot Color", NodeSocketColor, panel=zone3)
        _ = create_socket(interface, "Zone 3 Scratch Color", NodeSocketColor, panel=zone3)

        zone4 = interface.new_panel("Zone 4")
        _ = create_socket(interface, "Zone 4 Toggle", NodeSocketBool, panel=zone4)
        _ = create_socket(interface, "Zone 4 Gradient Out", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Rough Out", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Norm Out", NodeSocketColor, panel=zone4)
        _ = create_socket(interface, "Zone 4 Scratch Amount", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Scratch Metallic", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Scratch Roughness", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Metallic", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Transparency Amount", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Emissive Amount", NodeSocketFloat, panel=zone4)
        _ = create_socket(interface, "Zone 4 Top Color", NodeSocketColor, panel=zone4)
        _ = create_socket(interface, "Zone 4 Mid Color", NodeSocketColor, panel=zone4)
        _ = create_socket(interface, "Zone 4 Bot Color", NodeSocketColor, panel=zone4)
        _ = create_socket(interface, "Zone 4 Scratch Color", NodeSocketColor, panel=zone4)

        zone5 = interface.new_panel("Zone 5")
        _ = create_socket(interface, "Zone 5 Toggle", NodeSocketBool, panel=zone5)
        _ = create_socket(interface, "Zone 5 Gradient Out", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Rough Out", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Norm Out", NodeSocketColor, panel=zone5)
        _ = create_socket(interface, "Zone 5 Scratch Amount", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Scratch Metallic", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Scratch Roughness", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Metallic", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Transparency Amount", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Emissive Amount", NodeSocketFloat, panel=zone5)
        _ = create_socket(interface, "Zone 5 Top Color", NodeSocketColor, panel=zone5)
        _ = create_socket(interface, "Zone 5 Mid Color", NodeSocketColor, panel=zone5)
        _ = create_socket(interface, "Zone 5 Bot Color", NodeSocketColor, panel=zone5)
        _ = create_socket(interface, "Zone 5 Scratch Color", NodeSocketColor, panel=zone5)

        zone6 = interface.new_panel("Zone 6")
        _ = create_socket(interface, "Zone 6 Toggle", NodeSocketBool, panel=zone6)
        _ = create_socket(interface, "Zone 6 Gradient Out", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Rough Out", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Norm Out", NodeSocketColor, panel=zone6)
        _ = create_socket(interface, "Zone 6 Scratch Amount", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Scratch Metallic", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Scratch Roughness", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Metallic", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Transparency Amount", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Emissive Amount", NodeSocketFloat, panel=zone6)
        _ = create_socket(interface, "Zone 6 Top Color", NodeSocketColor, panel=zone6)
        _ = create_socket(interface, "Zone 6 Mid Color", NodeSocketColor, panel=zone6)
        _ = create_socket(interface, "Zone 6 Bot Color", NodeSocketColor, panel=zone6)
        _ = create_socket(interface, "Zone 6 Scratch Color", NodeSocketColor, panel=zone6)

        zone7 = interface.new_panel("Zone 7")
        _ = create_socket(interface, "Zone 7 Toggle", NodeSocketBool, panel=zone7)
        _ = create_socket(interface, "Zone 7 Gradient Out", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Rough Out", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Norm Out", NodeSocketColor, panel=zone7)
        _ = create_socket(interface, "Zone 7 Scratch Amount", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Scratch Metallic", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Scratch Roughness", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Metallic", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Transparency Amount", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Emissive Amount", NodeSocketFloat, panel=zone7)
        _ = create_socket(interface, "Zone 7 Top Color", NodeSocketColor, panel=zone7)
        _ = create_socket(interface, "Zone 7 Mid Color", NodeSocketColor, panel=zone7)
        _ = create_socket(interface, "Zone 7 Bot Color", NodeSocketColor, panel=zone7)
        _ = create_socket(interface, "Zone 7 Scratch Color", NodeSocketColor, panel=zone7)

        grime = interface.new_panel("Grime")
        _ = create_socket(interface, "Grime Gradient Out", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime Rough Out", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime Norm Out", NodeSocketColor, panel=grime)
        _ = create_socket(interface, "Grime Metallic", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime Transparency Amount", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime Emissive Amount", NodeSocketFloat, panel=grime)
        _ = create_socket(interface, "Grime Top Color", NodeSocketColor, panel=grime)
        _ = create_socket(interface, "Grime Mid Color", NodeSocketColor, panel=grime)
        _ = create_socket(interface, "Grime Bot Color", NodeSocketColor, panel=grime)

        overrides = interface.new_panel("Color Overrides")
        _ = create_socket(interface, "Color Override", NodeSocketColor, panel=overrides)
        override_toggle = create_socket(
            interface, "Color Override Toggle", NodeSocketFloat, panel=overrides
        )
        override_toggle.default_value = 0.0
        scale_options = interface.new_panel("Scale Options")
        _ = create_socket(interface, "Base Scale X", NodeSocketFloat, panel=scale_options)
        _ = create_socket(interface, "Base Scale Y", NodeSocketFloat, panel=scale_options)
        _ = create_socket(interface, "ASG Cubic", NodeSocketColor, panel=scale_options)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
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

        normal_map = create_node(nodes, 0, 0, ShaderNodeNormalMap)
        invert = create_node(nodes, 0, 0, ShaderNodeInvert)
        zone3 = create_node(nodes, -1609, 1866, ShaderNodeGroup)
        zone3.node_tree = cast(ShaderNodeTree, ColorMixer().node_tree)

        group_input = create_node(nodes, 0, 0, NodeGroupInput)

        group_016 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_016.node_tree = cast(ShaderNodeTree, ColorMixer().node_tree)

        group_017 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_017.node_tree = cast(ShaderNodeTree, InfiniteMaskingSorterNoGrime().node_tree)

        group_020 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_020.node_tree = cast(ShaderNodeTree, InfiniteMaskingSorterNoGrime().node_tree)

        clamp_1 = create_node(nodes, 0, 0, ShaderNodeClamp)
        clamp_001 = create_node(nodes, 0, 0, ShaderNodeClamp)
        clamp_002 = create_node(nodes, 0, 0, ShaderNodeClamp)
        clamp_003 = create_node(nodes, 0, 0, ShaderNodeClamp)
        clamp_004 = create_node(nodes, 0, 0, ShaderNodeClamp)
        clamp_005 = create_node(nodes, 0, 0, ShaderNodeClamp)
        clamp_006 = create_node(nodes, 0, 0, ShaderNodeClamp)
        clamp_007 = create_node(nodes, 0, 0, ShaderNodeClamp)

        mix_005_6 = create_node(nodes, 2505, -803, ShaderNodeMix)
        mix_005_6.blend_type = "MULTIPLY"
        mix_005_6.clamp_result = True
        mix_005_6.data_type = "RGBA"

        gamma = create_node(nodes, 0, 0, ShaderNodeGamma)
        assign_value(gamma, 1, 2.2)

        math_006_1 = create_node(nodes, 0, 0, ShaderNodeMath)
        math_006_1.operation = "SUBTRACT"
        math_006_1.use_clamp = True
        assign_value(math_006_1, 0, 1.0)
        assign_value(math_006_1, 2, 0.5)

        texture_coordinate = create_node(nodes, 0, 0, ShaderNodeTexCoord)

        mapping_1 = create_node(nodes, 0, 0, ShaderNodeMapping)
        mapping_1.vector_type = "POINT"
        assign_value(mapping_1, 1, (0.0, 0.0, 0.0))
        assign_value(mapping_1, 2, (0.0, 0.0, 0.0))

        musgrave_texture = create_node(nodes, 0, 0, ShaderNodeTexNoise)
        musgrave_texture.noise_dimensions = "2D"
        musgrave_texture.normalize = False
        assign_value(musgrave_texture, 1, 0.0)
        assign_value(musgrave_texture, 2, 3.0)
        assign_value(musgrave_texture, 3, 2.0)
        assign_value(musgrave_texture, 4, 0.695)
        assign_value(musgrave_texture, 5, 1.6)
        assign_value(musgrave_texture, 6, 0.0)
        assign_value(musgrave_texture, 7, 1.0)
        assign_value(musgrave_texture, 8, 0.0)

        colorramp_001 = create_node(nodes, 0, 0, ShaderNodeValToRGB)
        if colorramp_001.color_ramp:
            colorramp_001.color_ramp.color_mode = "RGB"
            colorramp_001.color_ramp.hue_interpolation = "NEAR"
            colorramp_001.color_ramp.interpolation = "LINEAR"

            colorramp_001.color_ramp.elements.remove(colorramp_001.color_ramp.elements[0])  # pyright: ignore[reportUnknownMemberType]
            colorramp_001_cre_0 = colorramp_001.color_ramp.elements[0]
            colorramp_001_cre_0.position = 0.5
            colorramp_001_cre_0.color = (0.0, 0.0, 0.0, 1.0)

            colorramp_001_cre_1 = colorramp_001.color_ramp.elements.new(0.6425)
            colorramp_001_cre_1.color = (0.005, 0.005, 0.005, 1.0)

            colorramp_001_cre_2 = colorramp_001.color_ramp.elements.new(0.885)
            colorramp_001_cre_2.color = (0.0223, 0.0223, 0.0223, 1.0)

        bump = create_node(nodes, 0, 0, ShaderNodeBump)
        bump.invert = True
        assign_value(bump, 1, 0.004)

        colorramp = create_node(nodes, 0, 0, ShaderNodeValToRGB)
        if colorramp.color_ramp:
            colorramp.color_ramp.color_mode = "RGB"
            colorramp.color_ramp.hue_interpolation = "NEAR"
            colorramp.color_ramp.interpolation = "LINEAR"

            colorramp.color_ramp.elements.remove(colorramp.color_ramp.elements[0])  # pyright: ignore[reportUnknownMemberType]
            colorramp_cre_0 = colorramp.color_ramp.elements[0]
            colorramp_cre_0.position = 0.1393
            colorramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

            colorramp_cre_1 = colorramp.color_ramp.elements.new(0.738)
            colorramp_cre_1.color = (0.0123, 0.0123, 0.0123, 1.0)

            colorramp_cre_2 = colorramp.color_ramp.elements.new(1.0)
            colorramp_cre_2.color = (0.0152, 0.0152, 0.0152, 1.0)

        group_006 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_006.node_tree = cast(ShaderNodeTree, ScratchGlobalToggle().node_tree)

        group_012 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_012.node_tree = cast(ShaderNodeTree, ColorMixer().node_tree)

        group_018 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_018.node_tree = cast(ShaderNodeTree, InfiniteMaskingSorterNoGrime().node_tree)

        group_023 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_023.node_tree = cast(ShaderNodeTree, InfiniteMaskingSorter().node_tree)

        group_004 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_004.node_tree = cast(ShaderNodeTree, ColorMixer().node_tree)

        group_013 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_013.node_tree = cast(ShaderNodeTree, Emission().node_tree)

        group_022 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_022.node_tree = cast(ShaderNodeTree, Emission().node_tree)

        gamma_004 = create_node(nodes, 0, 0, ShaderNodeGamma)
        assign_value(gamma_004, 1, 2.2)

        mix_004_7 = create_node(nodes, 0, 0, ShaderNodeMix)
        mix_004_7.data_type = "RGBA"
        mix_004_7.clamp_result = True
        assign_value(mix_004_7, 7, (0.247, 0.247, 0.247, 1.0))

        mix_006_7 = create_node(nodes, 0, 0, ShaderNodeMix)
        mix_006_7.blend_type = "MULTIPLY"
        mix_006_7.clamp_result = True
        mix_006_7.data_type = "RGBA"
        assign_value(mix_006_7, 7, (0.0, 0.0, 0.0, 1.0))

        gamma_002 = create_node(nodes, 0, 0, ShaderNodeGamma)
        assign_value(gamma_002, 1, 2.2)

        group_011 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_011.node_tree = cast(ShaderNodeTree, ColorMixer().node_tree)

        group_010 = create_node(nodes, 0, 0, ShaderNodeGroup)
        group_010.node_tree = cast(ShaderNodeTree, ColorMixer().node_tree)

        bump_001 = create_node(nodes, 0, 0, ShaderNodeBump)
        assign_value(bump_001, 0, 1.0)
        assign_value(bump_001, 1, 0.0075)

        group_output_17 = create_node(nodes, 0, 0, NodeGroupOutput)

        gamma_003 = create_node(nodes, 0, 0, ShaderNodeGamma)
        assign_value(gamma_003, 1, 2.2)

        mix_11 = create_node(nodes, 2478, 560, ShaderNodeMix)
        mix_11.blend_type = "MULTIPLY"
        mix_11.data_type = "RGBA"
        assign_value(mix_11, 0, 1.0)

        math_001_4 = create_node(nodes, 1747, 329, ShaderNodeMath)
        math_001_4.operation = "POWER"

        math_007_1 = create_node(nodes, 3092, 35, ShaderNodeMath)
        math_007_1.operation = "SUBTRACT"
        assign_value(math_007_1, 0, 1.0)

        gamma_001 = create_node(nodes, 4111, -118, ShaderNodeGamma)
        assign_value(gamma_001, 1, 2.2)

        combine_color = create_node(nodes, 4491, -5, ShaderNodeCombineColor)
        assign_value(combine_color, 2, 0.0)

        group_009 = create_node(nodes, -50, 306, ShaderNodeGroup)
        group_009.node_tree = cast(ShaderNodeTree, InfiniteMatts().node_tree)

        group_001_4 = create_node(nodes, -50, 800, ShaderNodeGroup)
        group_001_4.node_tree = cast(ShaderNodeTree, InfiniteMatts().node_tree)

        nogrimecol = create_node(nodes, -1688, 753, ShaderNodeGroup)
        nogrimecol.node_tree = cast(ShaderNodeTree, InfiniteMaskingSorterNoGrimeCol().node_tree)

        masktoggles = create_node(nodes, -3035, -233, ShaderNodeGroup)
        masktoggles.node_tree = cast(ShaderNodeTree, MaskToggles().node_tree)

        zone7 = create_node(nodes, -1609, 1146, ShaderNodeGroup)
        zone7.node_tree = cast(ShaderNodeTree, ColorMixer().node_tree)

        separate_color_001 = create_node(nodes, 4255, -1000, ShaderNodeSeparateColor)

        cyan = create_node(nodes, 4436, -963, ShaderNodeMix)
        cyan.data_type = "RGBA"
        assign_value(cyan, 7, (0.0, 1.0, 1.0, 1.0))

        magenta = create_node(nodes, 4847, -963, ShaderNodeMix)
        magenta.data_type = "RGBA"
        assign_value(magenta, 7, (1.0, 0.0, 1.0, 1.0))

        yellow = create_node(nodes, 4649, -963, ShaderNodeMix)
        yellow.data_type = "RGBA"
        assign_value(yellow, 7, (1.0, 1.0, 1.0, 1.0))

        math_5 = create_node(nodes, 3287, 127, ShaderNodeMath)
        math_5.operation = "MULTIPLY"

        detailnormals = create_node(nodes, -30, -142, ShaderNodeGroup)
        detailnormals.node_tree = cast(ShaderNodeTree, DetailNormals().node_tree)

        group_002_4 = create_node(nodes, -1609, 2226, ShaderNodeGroup)
        group_002_4.node_tree = cast(ShaderNodeTree, ColorMixer().node_tree)

        principled_bsdf = create_node(nodes, 3693, 316, ShaderNodeBsdfPrincipled)
        principled_bsdf.distribution = "GGX"
        principled_bsdf.subsurface_method = "RANDOM_WALK_SKIN"

        infinite_color = create_node(nodes, 1210, 366, ShaderNodeGroup)
        infinite_color.node_tree = cast(ShaderNodeTree, InfiniteColor().node_tree)

        multvoronoi = create_node(nodes, 1321, 1613, ShaderNodeMath)
        multvoronoi.operation = "MULTIPLY"
        assign_value(multvoronoi, 1, 0.44)

        addtovoronoi = create_node(nodes, 1321, 1613, ShaderNodeMath)
        assign_value(addtovoronoi, 1, 0.56)

        multvoronoi2 = create_node(nodes, 1321, 1613, ShaderNodeMath)
        multvoronoi2.operation = "MULTIPLY"
        assign_value(multvoronoi2, 1, 0.5)

        mult_yscale = create_node(nodes, 0, 0, ShaderNodeMath)
        mult_yscale.operation = "MULTIPLY"

        mult_xscale = create_node(nodes, 0, 0, ShaderNodeMath)
        mult_xscale.operation = "MULTIPLY"

        combinemult = create_node(nodes, 0, 0, ShaderNodeCombineXYZ)
        combine_orm = create_node(nodes, 0, 0, ShaderNodeCombineRGB)
        separate_asg_cubic = create_node(nodes, 0, 0, ShaderNodeSeparateRGB)

        _: NodeLink
        _ = self.node_tree.links.new(addtovoronoi.outputs[0], multvoronoi2.inputs[0])
        _ = self.node_tree.links.new(bump.outputs[0], bump_001.inputs[3])
        _ = self.node_tree.links.new(bump_001.outputs[0], group_output_17.inputs[8])
        _ = self.node_tree.links.new(bump_001.outputs[0], principled_bsdf.inputs[5])
        _ = self.node_tree.links.new(clamp_001.outputs[0], group_022.inputs[4])
        _ = self.node_tree.links.new(clamp_002.outputs[0], group_022.inputs[5])
        _ = self.node_tree.links.new(clamp_003.outputs[0], group_022.inputs[6])
        _ = self.node_tree.links.new(clamp_004.outputs[0], group_022.inputs[7])
        _ = self.node_tree.links.new(clamp_005.outputs[0], group_022.inputs[8])
        _ = self.node_tree.links.new(clamp_006.outputs[0], group_022.inputs[9])
        _ = self.node_tree.links.new(clamp_007.outputs[0], group_022.inputs[10])
        _ = self.node_tree.links.new(clamp_1.outputs[0], group_022.inputs[3])
        _ = self.node_tree.links.new(colorramp.outputs[0], mult3.inputs[0])
        _ = self.node_tree.links.new(colorramp_001.outputs[0], mult.inputs[0])
        _ = self.node_tree.links.new(combine_color.outputs[0], group_output_17.inputs[9])
        _ = self.node_tree.links.new(combine_orm.outputs[0], group_output_17.inputs[12])
        _ = self.node_tree.links.new(combinemult.outputs[0], mapping_1.inputs[3])
        _ = self.node_tree.links.new(cyan.outputs[2], yellow.inputs[6])
        _ = self.node_tree.links.new(detailnormals.outputs[0], normal_map.inputs[1])
        _ = self.node_tree.links.new(gamma.outputs[0], combine_color.inputs[0])
        _ = self.node_tree.links.new(gamma_001.outputs[0], combine_color.inputs[1])
        _ = self.node_tree.links.new(gamma_002.outputs[0], combine_orm.inputs[0])
        _ = self.node_tree.links.new(gamma_002.outputs[0], group_output_17.inputs[7])
        _ = self.node_tree.links.new(gamma_003.outputs[0], combine_orm.inputs[1])
        _ = self.node_tree.links.new(gamma_003.outputs[0], group_output_17.inputs[3])
        _ = self.node_tree.links.new(gamma_004.outputs[0], combine_orm.inputs[2])
        _ = self.node_tree.links.new(gamma_004.outputs[0], group_output_17.inputs[2])
        _ = self.node_tree.links.new(group_001_4.outputs[0], gamma.inputs[0])
        _ = self.node_tree.links.new(group_001_4.outputs[0], gamma_004.inputs[0])
        _ = self.node_tree.links.new(group_001_4.outputs[0], invert.inputs[1])
        _ = self.node_tree.links.new(group_001_4.outputs[0], mix_006_7.inputs[0])
        _ = self.node_tree.links.new(group_001_4.outputs[0], principled_bsdf.inputs[1])
        _ = self.node_tree.links.new(group_002_4.outputs[0], infinite_color.inputs[3])
        _ = self.node_tree.links.new(group_004.outputs[0], infinite_color.inputs[4])
        _ = self.node_tree.links.new(group_006.outputs[0], group_020.inputs[4])
        _ = self.node_tree.links.new(group_006.outputs[1], group_020.inputs[5])
        _ = self.node_tree.links.new(group_006.outputs[2], group_020.inputs[6])
        _ = self.node_tree.links.new(group_006.outputs[3], group_020.inputs[7])
        _ = self.node_tree.links.new(group_006.outputs[4], group_020.inputs[8])
        _ = self.node_tree.links.new(group_006.outputs[5], group_020.inputs[9])
        _ = self.node_tree.links.new(group_009.outputs[0], gamma_003.inputs[0])
        _ = self.node_tree.links.new(group_009.outputs[0], math_006_1.inputs[1])
        _ = self.node_tree.links.new(group_009.outputs[0], principled_bsdf.inputs[2])
        _ = self.node_tree.links.new(group_010.outputs[0], infinite_color.inputs[6])
        _ = self.node_tree.links.new(group_011.outputs[0], infinite_color.inputs[7])
        _ = self.node_tree.links.new(group_012.outputs[0], infinite_color.inputs[8])
        _ = self.node_tree.links.new(group_013.outputs[0], group_output_17.inputs[4])
        _ = self.node_tree.links.new(group_013.outputs[0], principled_bsdf.inputs[28])
        _ = self.node_tree.links.new(group_016.outputs[0], infinite_color.inputs[9])
        _ = self.node_tree.links.new(group_017.outputs[0], group_001_4.inputs[11])
        _ = self.node_tree.links.new(group_018.outputs[0], group_009.inputs[11])
        _ = self.node_tree.links.new(group_020.outputs[0], bump.inputs[0])
        _ = self.node_tree.links.new(group_020.outputs[0], detailnormals.inputs[12])
        _ = self.node_tree.links.new(group_020.outputs[0], group_001_4.inputs[12])
        _ = self.node_tree.links.new(group_020.outputs[0], group_009.inputs[12])
        _ = self.node_tree.links.new(group_020.outputs[0], infinite_color.inputs[15])
        _ = self.node_tree.links.new(group_022.outputs[0], mix_005_6.inputs[7])
        _ = self.node_tree.links.new(group_023.outputs[0], math_007_1.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[0], detailnormals.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_001_4.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_009.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_013.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_017.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_018.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_020.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_022.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], group_023.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], infinite_color.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], nogrimecol.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[0], srgb.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[1], masktoggles.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[2], masktoggles.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[3], detailnormals.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[4], detailnormals.inputs[14])
        _ = self.node_tree.links.new(group_input.outputs[5], detailnormals.inputs[15])
        _ = self.node_tree.links.new(group_input.outputs[6], detailnormals.inputs[16])
        _ = self.node_tree.links.new(group_input.outputs[7], detailnormals.inputs[13])
        _ = self.node_tree.links.new(group_input.outputs[7], group_001_4.inputs[13])
        _ = self.node_tree.links.new(group_input.outputs[7], group_009.inputs[13])
        _ = self.node_tree.links.new(group_input.outputs[7], group_013.inputs[11])
        _ = self.node_tree.links.new(group_input.outputs[7], group_022.inputs[11])
        _ = self.node_tree.links.new(group_input.outputs[7], group_023.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[7], infinite_color.inputs[14])
        _ = self.node_tree.links.new(group_input.outputs[7], math_003_2.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[7], nogrimecol.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[8], mult2.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[9], mult_xscale.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[9], mult_yscale.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[10], math_001_4.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[11], mult3.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[12], group_006.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[14], group_002_4.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[15], group_009.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[16], detailnormals.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[17], group_006.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[17], group_020.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[18], group_017.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[19], group_018.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[20], group_001_4.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[21], group_023.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[22], clamp_1.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[22], group_013.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[23], group_002_4.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[24], group_002_4.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[25], group_002_4.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[26], nogrimecol.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[27], masktoggles.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[28], group_004.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[29], group_009.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[30], detailnormals.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[31], group_006.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[32], group_017.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[33], group_018.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[34], group_001_4.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[35], group_023.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[36], clamp_001.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[36], group_013.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[37], group_004.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[38], group_004.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[39], group_004.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[40], nogrimecol.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[41], masktoggles.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[42], zone3.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[43], group_009.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[44], detailnormals.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[45], group_006.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[46], group_017.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[47], group_018.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[48], group_001_4.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[49], group_023.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[50], clamp_002.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[50], group_013.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[51], zone3.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[52], zone3.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[53], zone3.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[54], nogrimecol.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[55], masktoggles.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[56], group_010.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[57], group_009.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[58], detailnormals.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[59], group_006.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[60], group_017.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[61], group_018.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[62], group_001_4.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[63], group_023.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[64], clamp_003.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[64], group_013.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[65], group_010.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[66], group_010.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[67], group_010.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[68], nogrimecol.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[69], masktoggles.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[70], group_011.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[71], group_009.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[72], detailnormals.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[73], group_006.inputs[4])
        _ = self.node_tree.links.new(group_input.outputs[74], group_017.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[75], group_018.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[76], group_001_4.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[77], group_023.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[78], clamp_004.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[78], group_013.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[79], group_011.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[80], group_011.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[81], group_011.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[82], nogrimecol.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[83], masktoggles.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[84], group_012.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[85], group_009.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[86], detailnormals.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[87], group_006.inputs[5])
        _ = self.node_tree.links.new(group_input.outputs[88], group_017.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[89], group_018.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[90], group_001_4.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[91], group_023.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[92], clamp_005.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[92], group_013.inputs[8])
        _ = self.node_tree.links.new(group_input.outputs[93], group_012.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[94], group_012.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[95], group_012.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[96], nogrimecol.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[97], masktoggles.inputs[7])
        _ = self.node_tree.links.new(group_input.outputs[98], zone7.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[99], group_009.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[100], detailnormals.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[101], group_006.inputs[6])
        _ = self.node_tree.links.new(group_input.outputs[102], group_017.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[103], group_018.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[104], group_001_4.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[105], group_023.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[106], clamp_006.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[106], group_013.inputs[9])
        _ = self.node_tree.links.new(group_input.outputs[107], zone7.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[108], zone7.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[109], zone7.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[110], nogrimecol.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[111], group_016.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[112], group_009.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[113], detailnormals.inputs[11])
        _ = self.node_tree.links.new(group_input.outputs[114], group_001_4.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[115], group_023.inputs[11])
        _ = self.node_tree.links.new(group_input.outputs[116], clamp_007.inputs[0])
        _ = self.node_tree.links.new(group_input.outputs[116], group_013.inputs[10])
        _ = self.node_tree.links.new(group_input.outputs[117], group_016.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[118], group_016.inputs[2])
        _ = self.node_tree.links.new(group_input.outputs[119], group_016.inputs[3])
        _ = self.node_tree.links.new(group_input.outputs[120], infinite_color.inputs[12])
        _ = self.node_tree.links.new(group_input.outputs[121], infinite_color.inputs[13])
        _ = self.node_tree.links.new(group_input.outputs[122], mult_yscale.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[123], mult_xscale.inputs[1])
        _ = self.node_tree.links.new(group_input.outputs[124], separate_asg_cubic.inputs[0])
        _ = self.node_tree.links.new(infinite_color.outputs[0], group_output_17.inputs[1])
        _ = self.node_tree.links.new(infinite_color.outputs[0], mix_004_7.inputs[6])
        _ = self.node_tree.links.new(infinite_color.outputs[0], mix_005_6.inputs[6])
        _ = self.node_tree.links.new(infinite_color.outputs[0], mix_006_7.inputs[6])
        _ = self.node_tree.links.new(infinite_color.outputs[0], mix_11.inputs[6])
        _ = self.node_tree.links.new(infinite_color.outputs[0], principled_bsdf.inputs[27])
        _ = self.node_tree.links.new(invert.outputs[0], mix_004_7.inputs[0])
        _ = self.node_tree.links.new(magenta.outputs[2], group_output_17.inputs[11])
        _ = self.node_tree.links.new(mapping_1.outputs[0], musgrave_texture.inputs[0])
        _ = self.node_tree.links.new(masktoggles.outputs[0], cyan.inputs[6])
        _ = self.node_tree.links.new(masktoggles.outputs[0], detailnormals.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_001_4.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_009.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_013.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_017.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_018.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_020.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_022.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[0], group_023.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[0], infinite_color.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[0], nogrimecol.inputs[1])
        _ = self.node_tree.links.new(masktoggles.outputs[1], detailnormals.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_001_4.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_009.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_013.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_017.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_018.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_020.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_022.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], group_023.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], infinite_color.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], nogrimecol.inputs[2])
        _ = self.node_tree.links.new(masktoggles.outputs[1], separate_color_001.inputs[0])
        _ = self.node_tree.links.new(math_001_4.outputs[0], gamma_001.inputs[0])
        _ = self.node_tree.links.new(math_001_4.outputs[0], gamma_002.inputs[0])
        _ = self.node_tree.links.new(math_001_4.outputs[0], math_5.inputs[1])
        _ = self.node_tree.links.new(math_001_4.outputs[0], mix_11.inputs[7])
        _ = self.node_tree.links.new(math_003_2.outputs[0], mult2.inputs[0])
        _ = self.node_tree.links.new(math_006_1.outputs[0], group_output_17.inputs[10])
        _ = self.node_tree.links.new(math_007_1.outputs[0], principled_bsdf.inputs[4])
        _ = self.node_tree.links.new(mix_004_7.outputs[2], group_output_17.inputs[5])
        _ = self.node_tree.links.new(mix_006_7.outputs[2], group_output_17.inputs[6])
        _ = self.node_tree.links.new(mix_11.outputs[2], principled_bsdf.inputs[0])
        _ = self.node_tree.links.new(mult.outputs[0], math_003_2.inputs[0])
        _ = self.node_tree.links.new(mult2.outputs[0], bump_001.inputs[2])
        _ = self.node_tree.links.new(mult3.outputs[0], bump.inputs[2])
        _ = self.node_tree.links.new(mult_xscale.outputs[0], combinemult.inputs[1])
        _ = self.node_tree.links.new(mult_yscale.outputs[0], combinemult.inputs[0])
        _ = self.node_tree.links.new(multvoronoi.outputs[0], addtovoronoi.inputs[0])
        _ = self.node_tree.links.new(multvoronoi2.outputs[0], mult.inputs[1])
        _ = self.node_tree.links.new(musgrave_texture.outputs[0], multvoronoi.inputs[0])
        _ = self.node_tree.links.new(nogrimecol.outputs[0], infinite_color.inputs[11])
        _ = self.node_tree.links.new(normal_map.outputs[0], bump.inputs[3])
        _ = self.node_tree.links.new(principled_bsdf.outputs[0], group_output_17.inputs[0])
        _ = self.node_tree.links.new(separate_asg_cubic.outputs[1], colorramp.inputs[0])
        _ = self.node_tree.links.new(separate_color_001.outputs[0], cyan.inputs[0])
        _ = self.node_tree.links.new(separate_color_001.outputs[1], yellow.inputs[0])
        _ = self.node_tree.links.new(separate_color_001.outputs[2], magenta.inputs[0])
        _ = self.node_tree.links.new(srgb.outputs[0], math_001_4.inputs[0])
        _ = self.node_tree.links.new(separate_asg_cubic.outputs[2], colorramp_001.inputs[0])
        _ = self.node_tree.links.new(texture_coordinate.outputs[2], mapping_1.inputs[0])
        _ = self.node_tree.links.new(yellow.outputs[2], magenta.inputs[6])
        _ = self.node_tree.links.new(zone3.outputs[0], infinite_color.inputs[5])
        _ = self.node_tree.links.new(zone7.outputs[0], infinite_color.inputs[10])
