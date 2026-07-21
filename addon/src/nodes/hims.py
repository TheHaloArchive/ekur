# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
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
    ShaderNodeCombineXYZ,
    ShaderNodeGamma,
    ShaderNodeGroup,
    ShaderNodeInvert,
    ShaderNodeMapping,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeNormalMap,
    ShaderNodeSeparateColor,
    ShaderNodeTexCoord,
    ShaderNodeTexNoise,
    ShaderNodeTree,
    ShaderNodeValToRGB,
)

from ..ui.model_options import get_model_options
from ..utils import assign_value, create_node, create_socket, create_link
from .color_mixer import ColorMixer
from .detail_normals import DetailNormals
from .emission import Emission
from .infinite_color import InfiniteColor
from .infinite_masking_sorter import InfiniteMaskingSorter
from .infinite_masking_sorter_nogrime import InfiniteMaskingSorterNoGrime
from .infinite_masking_sorter_nogrime_col import InfiniteMaskingSorterNoGrimeCol
from .infinite_matts import InfiniteMatts
from .mask_toggles import MaskToggles
from .scratch_global_toggle import ScratchGlobalToggle

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
                type="ShaderNodeTree", name="Halo Infinite Shader 3.1.2 by Chunch and ChromaCore"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None or self.node_tree.interface is None:
            return
        props = get_model_options()
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
        grime_h.default_value = 3.048 * props.scale_factor
        grime_hs = create_socket(interface, "Grime Height Scale", NodeSocketFloat, panel=settings)
        grime_hs.default_value = 50.0
        ao_amount = create_socket(interface, "AO Amount", NodeSocketFloat, panel=settings)
        ao_amount.default_value = 1.0
        sh = create_socket(interface, "Scratch Height Amount", NodeSocketFloat, panel=settings)
        sh.default_value = 3.048 * props.scale_factor
        gs = create_socket(interface, "Global Scratch Toggle", NodeSocketBool, panel=settings)
        gs.default_value = True

        zone1 = interface.new_panel("Zone 1")
        _ = create_socket(interface, "", NodeSocketBool, panel=zone1)
        interface.items_tree[30].hide_value = True  # ty: ignore[unresolved-attribute]
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

            colorramp_001.color_ramp.elements.remove(colorramp_001.color_ramp.elements[0])
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

            colorramp.color_ramp.elements.remove(colorramp.color_ramp.elements[0])
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
        combine_orm = create_node(nodes, 0, 0, ShaderNodeCombineColor)
        separate_asg_cubic = create_node(nodes, 0, 0, ShaderNodeSeparateColor)

        links = self.node_tree.links
        _: NodeLink
        create_link(links, addtovoronoi, multvoronoi2, 0, 0)
        if bpy.app.version > (4, 4, 0):
            create_link(links, bump, bump_001, 0, 4)
        else:
            create_link(links, bump, bump_001, 0, 3)
        create_link(links, bump_001, group_output_17, 0, 8)
        if bpy.app.version >= (5, 2, 0):
            create_link(links, bump_001, principled_bsdf, 0, 6)
        else:
            create_link(links, bump_001, principled_bsdf, 0, 5)
        create_link(links, clamp_001, group_022, 0, 4)
        create_link(links, clamp_002, group_022, 0, 5)
        create_link(links, clamp_003, group_022, 0, 6)
        create_link(links, clamp_004, group_022, 0, 7)
        create_link(links, clamp_005, group_022, 0, 8)
        create_link(links, clamp_006, group_022, 0, 9)
        create_link(links, clamp_007, group_022, 0, 10)
        create_link(links, clamp_1, group_022, 0, 3)
        create_link(links, colorramp, mult3, 0, 0)
        create_link(links, colorramp_001, mult, 0, 0)
        create_link(links, combine_color, group_output_17, 0, 9)
        create_link(links, combine_orm, group_output_17, 0, 12)
        create_link(links, combinemult, mapping_1, 0, 3)
        create_link(links, cyan, yellow, 2, 6)
        create_link(links, detailnormals, normal_map, 0, 1)
        create_link(links, gamma, combine_color, 0, 0)
        create_link(links, gamma_001, combine_color, 0, 1)
        create_link(links, gamma_002, combine_orm, 0, 0)
        create_link(links, gamma_002, group_output_17, 0, 7)
        create_link(links, gamma_003, combine_orm, 0, 1)
        create_link(links, gamma_003, group_output_17, 0, 3)
        create_link(links, gamma_004, combine_orm, 0, 2)
        create_link(links, gamma_004, group_output_17, 0, 2)
        create_link(links, group_001_4, gamma, 0, 0)
        create_link(links, group_001_4, gamma_004, 0, 0)
        create_link(links, group_001_4, invert, 0, 1)
        create_link(links, group_001_4, mix_006_7, 0, 0)
        create_link(links, group_001_4, principled_bsdf, 0, 1)
        create_link(links, group_002_4, infinite_color, 0, 3)
        create_link(links, group_004, infinite_color, 0, 4)
        create_link(links, group_006, group_020, 0, 4)
        create_link(links, group_006, group_020, 1, 5)
        create_link(links, group_006, group_020, 2, 6)
        create_link(links, group_006, group_020, 3, 7)
        create_link(links, group_006, group_020, 4, 8)
        create_link(links, group_006, group_020, 5, 9)
        create_link(links, group_009, gamma_003, 0, 0)
        create_link(links, group_009, math_006_1, 0, 1)
        create_link(links, group_009, principled_bsdf, 0, 2)
        create_link(links, group_010, infinite_color, 0, 6)
        create_link(links, group_011, infinite_color, 0, 7)
        create_link(links, group_012, infinite_color, 0, 8)
        create_link(links, group_013, group_output_17, 0, 4)
        if bpy.app.version >= (5, 2, 0):
            create_link(links, infinite_color, principled_bsdf, 0, 28)
        else:
            create_link(links, infinite_color, principled_bsdf, 0, 27)
        create_link(links, group_016, infinite_color, 0, 9)
        create_link(links, group_017, group_001_4, 0, 11)
        create_link(links, group_018, group_009, 0, 11)
        create_link(links, group_020, bump, 0, 0)
        create_link(links, group_020, detailnormals, 0, 12)
        create_link(links, group_020, group_001_4, 0, 12)
        create_link(links, group_020, group_009, 0, 12)
        create_link(links, group_020, infinite_color, 0, 15)
        create_link(links, group_022, mix_005_6, 0, 7)
        create_link(links, group_023, math_007_1, 0, 1)
        create_link(links, group_input, detailnormals, 0, 0)
        create_link(links, group_input, group_001_4, 0, 0)
        create_link(links, group_input, group_009, 0, 0)
        create_link(links, group_input, group_013, 0, 0)
        create_link(links, group_input, group_017, 0, 0)
        create_link(links, group_input, group_018, 0, 0)
        create_link(links, group_input, group_020, 0, 0)
        create_link(links, group_input, group_022, 0, 0)
        create_link(links, group_input, group_023, 0, 0)
        create_link(links, group_input, infinite_color, 0, 0)
        create_link(links, group_input, nogrimecol, 0, 0)
        create_link(links, group_input, srgb, 0, 0)
        create_link(links, group_input, masktoggles, 1, 0)
        create_link(links, group_input, masktoggles, 2, 1)
        create_link(links, group_input, detailnormals, 3, 3)
        create_link(links, group_input, detailnormals, 4, 14)
        create_link(links, group_input, detailnormals, 5, 15)
        create_link(links, group_input, detailnormals, 6, 16)
        create_link(links, group_input, detailnormals, 7, 13)
        create_link(links, group_input, group_001_4, 7, 13)
        create_link(links, group_input, group_009, 7, 13)
        create_link(links, group_input, group_013, 7, 11)
        create_link(links, group_input, group_022, 7, 11)
        create_link(links, group_input, group_023, 7, 3)
        create_link(links, group_input, infinite_color, 7, 14)
        create_link(links, group_input, math_003_2, 7, 1)
        create_link(links, group_input, nogrimecol, 7, 3)
        create_link(links, group_input, mult2, 8, 1)
        create_link(links, group_input, mult_xscale, 9, 0)
        create_link(links, group_input, mult_yscale, 9, 0)
        create_link(links, group_input, math_001_4, 10, 1)
        create_link(links, group_input, mult3, 11, 1)
        create_link(links, group_input, group_006, 12, 7)
        create_link(links, group_input, group_002_4, 14, 0)
        create_link(links, group_input, group_009, 15, 3)
        create_link(links, group_input, detailnormals, 16, 4)
        create_link(links, group_input, group_006, 17, 0)
        create_link(links, group_input, group_020, 17, 3)
        create_link(links, group_input, group_017, 18, 3)
        create_link(links, group_input, group_018, 19, 3)
        create_link(links, group_input, group_001_4, 20, 3)
        create_link(links, group_input, group_023, 21, 4)
        create_link(links, group_input, clamp_1, 22, 0)
        create_link(links, group_input, group_013, 22, 3)
        create_link(links, group_input, group_002_4, 23, 1)
        create_link(links, group_input, group_002_4, 24, 2)
        create_link(links, group_input, group_002_4, 25, 3)
        create_link(links, group_input, nogrimecol, 26, 4)
        create_link(links, group_input, masktoggles, 27, 2)
        create_link(links, group_input, group_004, 28, 0)
        create_link(links, group_input, group_009, 29, 4)
        create_link(links, group_input, detailnormals, 30, 5)
        create_link(links, group_input, group_006, 31, 1)
        create_link(links, group_input, group_017, 32, 4)
        create_link(links, group_input, group_018, 33, 4)
        create_link(links, group_input, group_001_4, 34, 4)
        create_link(links, group_input, group_023, 35, 5)
        create_link(links, group_input, clamp_001, 36, 0)
        create_link(links, group_input, group_013, 36, 4)
        create_link(links, group_input, group_004, 37, 1)
        create_link(links, group_input, group_004, 38, 2)
        create_link(links, group_input, group_004, 39, 3)
        create_link(links, group_input, nogrimecol, 40, 5)
        create_link(links, group_input, masktoggles, 41, 3)
        create_link(links, group_input, zone3, 42, 0)
        create_link(links, group_input, group_009, 43, 5)
        create_link(links, group_input, detailnormals, 44, 6)
        create_link(links, group_input, group_006, 45, 2)
        create_link(links, group_input, group_017, 46, 5)
        create_link(links, group_input, group_018, 47, 5)
        create_link(links, group_input, group_001_4, 48, 5)
        create_link(links, group_input, group_023, 49, 6)
        create_link(links, group_input, clamp_002, 50, 0)
        create_link(links, group_input, group_013, 50, 5)
        create_link(links, group_input, zone3, 51, 1)
        create_link(links, group_input, zone3, 52, 2)
        create_link(links, group_input, zone3, 53, 3)
        create_link(links, group_input, nogrimecol, 54, 6)
        create_link(links, group_input, masktoggles, 55, 4)
        create_link(links, group_input, group_010, 56, 0)
        create_link(links, group_input, group_009, 57, 6)
        create_link(links, group_input, detailnormals, 58, 7)
        create_link(links, group_input, group_006, 59, 3)
        create_link(links, group_input, group_017, 60, 6)
        create_link(links, group_input, group_018, 61, 6)
        create_link(links, group_input, group_001_4, 62, 6)
        create_link(links, group_input, group_023, 63, 7)
        create_link(links, group_input, clamp_003, 64, 0)
        create_link(links, group_input, group_013, 64, 6)
        create_link(links, group_input, group_010, 65, 1)
        create_link(links, group_input, group_010, 66, 2)
        create_link(links, group_input, group_010, 67, 3)
        create_link(links, group_input, nogrimecol, 68, 7)
        create_link(links, group_input, masktoggles, 69, 5)
        create_link(links, group_input, group_011, 70, 0)
        create_link(links, group_input, group_009, 71, 7)
        create_link(links, group_input, detailnormals, 72, 8)
        create_link(links, group_input, group_006, 73, 4)
        create_link(links, group_input, group_017, 74, 7)
        create_link(links, group_input, group_018, 75, 7)
        create_link(links, group_input, group_001_4, 76, 7)
        create_link(links, group_input, group_023, 77, 8)
        create_link(links, group_input, clamp_004, 78, 0)
        create_link(links, group_input, group_013, 78, 7)
        create_link(links, group_input, group_011, 79, 1)
        create_link(links, group_input, group_011, 80, 2)
        create_link(links, group_input, group_011, 81, 3)
        create_link(links, group_input, nogrimecol, 82, 8)
        create_link(links, group_input, masktoggles, 83, 6)
        create_link(links, group_input, group_012, 84, 0)
        create_link(links, group_input, group_009, 85, 8)
        create_link(links, group_input, detailnormals, 86, 9)
        create_link(links, group_input, group_006, 87, 5)
        create_link(links, group_input, group_017, 88, 8)
        create_link(links, group_input, group_018, 89, 8)
        create_link(links, group_input, group_001_4, 90, 8)
        create_link(links, group_input, group_023, 91, 9)
        create_link(links, group_input, clamp_005, 92, 0)
        create_link(links, group_input, group_013, 92, 8)
        create_link(links, group_input, group_012, 93, 1)
        create_link(links, group_input, group_012, 94, 2)
        create_link(links, group_input, group_012, 95, 3)
        create_link(links, group_input, nogrimecol, 96, 9)
        create_link(links, group_input, masktoggles, 97, 7)
        create_link(links, group_input, zone7, 98, 0)
        create_link(links, group_input, group_009, 99, 9)
        create_link(links, group_input, detailnormals, 100, 10)
        create_link(links, group_input, group_006, 101, 6)
        create_link(links, group_input, group_017, 102, 9)
        create_link(links, group_input, group_018, 103, 9)
        create_link(links, group_input, group_001_4, 104, 9)
        create_link(links, group_input, group_023, 105, 10)
        create_link(links, group_input, clamp_006, 106, 0)
        create_link(links, group_input, group_013, 106, 9)
        create_link(links, group_input, zone7, 107, 1)
        create_link(links, group_input, zone7, 108, 2)
        create_link(links, group_input, zone7, 109, 3)
        create_link(links, group_input, nogrimecol, 110, 10)
        create_link(links, group_input, group_016, 111, 0)
        create_link(links, group_input, group_009, 112, 10)
        create_link(links, group_input, detailnormals, 113, 11)
        create_link(links, group_input, group_001_4, 114, 10)
        create_link(links, group_input, group_023, 115, 11)
        create_link(links, group_input, clamp_007, 116, 0)
        create_link(links, group_input, group_013, 116, 10)
        create_link(links, group_input, group_016, 117, 1)
        create_link(links, group_input, group_016, 118, 2)
        create_link(links, group_input, group_016, 119, 3)
        create_link(links, group_input, infinite_color, 120, 12)
        create_link(links, group_input, infinite_color, 121, 13)
        create_link(links, group_input, mult_yscale, 122, 1)
        create_link(links, group_input, mult_xscale, 123, 1)
        create_link(links, group_input, separate_asg_cubic, 124, 0)
        create_link(links, infinite_color, group_output_17, 0, 1)
        create_link(links, infinite_color, mix_004_7, 0, 6)
        create_link(links, infinite_color, mix_005_6, 0, 6)
        create_link(links, infinite_color, mix_006_7, 0, 6)
        create_link(links, infinite_color, mix_11, 0, 6)
        if bpy.app.version >= (5, 2, 0):
            create_link(links, group_013, principled_bsdf, 0, 29)
        else:
            create_link(links, group_013, principled_bsdf, 0, 28)
        create_link(links, invert, mix_004_7, 0, 0)
        create_link(links, magenta, group_output_17, 2, 11)
        create_link(links, mapping_1, musgrave_texture, 0, 0)
        create_link(links, masktoggles, cyan, 0, 6)
        create_link(links, masktoggles, detailnormals, 0, 1)
        create_link(links, masktoggles, group_001_4, 0, 1)
        create_link(links, masktoggles, group_009, 0, 1)
        create_link(links, masktoggles, group_013, 0, 1)
        create_link(links, masktoggles, group_017, 0, 1)
        create_link(links, masktoggles, group_018, 0, 1)
        create_link(links, masktoggles, group_020, 0, 1)
        create_link(links, masktoggles, group_022, 0, 1)
        create_link(links, masktoggles, group_023, 0, 1)
        create_link(links, masktoggles, infinite_color, 0, 1)
        create_link(links, masktoggles, nogrimecol, 0, 1)
        create_link(links, masktoggles, detailnormals, 1, 2)
        create_link(links, masktoggles, group_001_4, 1, 2)
        create_link(links, masktoggles, group_009, 1, 2)
        create_link(links, masktoggles, group_013, 1, 2)
        create_link(links, masktoggles, group_017, 1, 2)
        create_link(links, masktoggles, group_018, 1, 2)
        create_link(links, masktoggles, group_020, 1, 2)
        create_link(links, masktoggles, group_022, 1, 2)
        create_link(links, masktoggles, group_023, 1, 2)
        create_link(links, masktoggles, infinite_color, 1, 2)
        create_link(links, masktoggles, nogrimecol, 1, 2)
        create_link(links, masktoggles, separate_color_001, 1, 0)
        create_link(links, math_001_4, gamma_001, 0, 0)
        create_link(links, math_001_4, gamma_002, 0, 0)
        create_link(links, math_001_4, math_5, 0, 1)
        if bpy.app.version >= (5, 2, 0):
            create_link(links, math_5, principled_bsdf, 0, 14)
        else:
            create_link(links, math_5, principled_bsdf, 0, 13)
        create_link(links, math_001_4, mix_11, 0, 7)
        create_link(links, math_003_2, mult2, 0, 0)
        create_link(links, math_006_1, group_output_17, 0, 10)
        create_link(links, math_007_1, principled_bsdf, 0, 4)
        create_link(links, mix_004_7, group_output_17, 2, 5)
        create_link(links, mix_006_7, group_output_17, 2, 6)
        create_link(links, mix_11, principled_bsdf, 2, 0)
        create_link(links, mult, math_003_2, 0, 0)
        if bpy.app.version > (4, 4, 0):
            create_link(links, mult2, bump_001, 0, 3)
        else:
            create_link(links, mult2, bump_001, 0, 2)
        if bpy.app.version > (4, 4, 0):
            create_link(links, mult3, bump, 0, 3)
        else:
            create_link(links, mult3, bump, 0, 2)

        create_link(links, mult_xscale, combinemult, 0, 1)
        create_link(links, mult_yscale, combinemult, 0, 0)
        create_link(links, multvoronoi, addtovoronoi, 0, 0)
        create_link(links, multvoronoi2, mult, 0, 1)
        create_link(links, musgrave_texture, multvoronoi, 0, 0)
        create_link(links, nogrimecol, infinite_color, 0, 11)
        if bpy.app.version > (4, 4, 0):
            create_link(links, normal_map, bump, 0, 4)
        else:
            create_link(links, normal_map, bump, 0, 3)
        create_link(links, principled_bsdf, group_output_17, 0, 0)
        create_link(links, separate_asg_cubic, colorramp, 1, 0)
        create_link(links, separate_color_001, cyan, 0, 0)
        create_link(links, separate_color_001, yellow, 1, 0)
        create_link(links, separate_color_001, magenta, 2, 0)
        create_link(links, srgb, math_001_4, 0, 0)
        create_link(links, separate_asg_cubic, colorramp_001, 2, 0)
        create_link(links, texture_coordinate, mapping_1, 2, 0)
        create_link(links, yellow, magenta, 2, 6)
        create_link(links, zone3, infinite_color, 0, 5)
        create_link(links, zone7, infinite_color, 0, 10)
