# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import cast

import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeReroute,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketInt,
    NodeSocketShader,
    NodeSocketVector,
    NodeTree,
    ShaderNodeAddShader,
    ShaderNodeBsdfDiffuse,
    ShaderNodeBsdfMetallic,
    ShaderNodeBump,
    ShaderNodeGroup,
    ShaderNodeMix,
    ShaderNodeSeparateColor,
    ShaderNodeSeparateXYZ,
    ShaderNodeTree,
    ShaderNodeValue,
)

from ..utils import assign_value, create_node, create_socket, create_link
from .color_blend import ColorBlend
from .float_blend import FloatBlend
from .layer_blending import LayerBlending
from .normal_blend import NormalBlend
from .occlusion_blend import OcclusionBlend

__all__ = ["LayeredLevelHINF"]


class LayeredLevelHINF:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("LayeredLevel_HINF")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree", name="LayeredLevel_HINF"
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        _ = create_socket(interface, "Control", NodeSocketColor)
        _ = create_socket(interface, "Control Alpha", NodeSocketFloat)
        _ = create_socket(interface, "MacroMask", NodeSocketColor)
        _ = create_socket(interface, "MacroMask Alpha", NodeSocketFloat)
        _ = create_socket(interface, "Macro Normal", NodeSocketColor)
        _ = create_socket(interface, "parallax_depth", NodeSocketFloat)
        _ = create_socket(interface, "macro_roughness_intensity", NodeSocketFloat)
        _ = create_socket(interface, "macro_occlusion_intensity", NodeSocketFloat)
        _ = create_socket(interface, "macro_metallic_intensity", NodeSocketFloat)
        _ = create_socket(interface, "Layer 1 Color Blend Mode", NodeSocketInt)
        _ = create_socket(interface, "Layer 1 Normal Blend Mode", NodeSocketInt)
        _ = create_socket(interface, "Layer 1 Color", NodeSocketColor)
        _ = create_socket(interface, "Layer 1 Roughness", NodeSocketFloat)
        _ = create_socket(interface, "Layer 1 Metallic", NodeSocketFloat)
        _ = create_socket(interface, "Layer 1 Occlusion", NodeSocketFloat)
        _ = create_socket(interface, "Layer 1 Normal", NodeSocketVector)
        _ = create_socket(interface, "Layer 1 Height Info", NodeSocketVector)
        _ = create_socket(interface, "Layer 1 Extra", NodeSocketVector)
        _ = create_socket(interface, "Layer 2 Color Blend Mode", NodeSocketInt)
        _ = create_socket(interface, "Layer 2 Normal Blend Mode", NodeSocketInt)
        _ = create_socket(interface, "Layer 2 Color", NodeSocketColor)
        _ = create_socket(interface, "Layer 2 Roughness", NodeSocketFloat)
        _ = create_socket(interface, "Layer 2 Metallic", NodeSocketFloat)
        _ = create_socket(interface, "Layer 2 Occlusion", NodeSocketFloat)
        _ = create_socket(interface, "Layer 2 Normal", NodeSocketVector)
        _ = create_socket(interface, "Layer 2 Height Info", NodeSocketVector)
        _ = create_socket(interface, "Layer 2 Extra", NodeSocketVector)
        _ = create_socket(interface, "Layer 3 Color Blend Mode", NodeSocketInt)
        _ = create_socket(interface, "Layer 3 Normal Blend Mode", NodeSocketInt)
        _ = create_socket(interface, "Layer 3 Color", NodeSocketColor)
        _ = create_socket(interface, "Layer 3 Roughness", NodeSocketFloat)
        _ = create_socket(interface, "Layer 3 Metallic", NodeSocketFloat)
        _ = create_socket(interface, "Layer 3 Occlusion", NodeSocketFloat)
        _ = create_socket(interface, "Layer 3 Normal", NodeSocketVector)
        _ = create_socket(interface, "Layer 3 Height Info", NodeSocketVector)
        _ = create_socket(interface, "Layer 3 Extra", NodeSocketVector)
        _ = create_socket(interface, "Layer 4 Color Blend Mode", NodeSocketInt)
        _ = create_socket(interface, "Layer 4 Normal Blend Mode", NodeSocketInt)
        _ = create_socket(interface, "Layer 4 Color", NodeSocketColor)
        _ = create_socket(interface, "Layer 4 Roughness", NodeSocketFloat)
        _ = create_socket(interface, "Layer 4 Metallic", NodeSocketFloat)
        _ = create_socket(interface, "Layer 4 Occlusion", NodeSocketFloat)
        _ = create_socket(interface, "Layer 4 Normal", NodeSocketVector)
        _ = create_socket(interface, "Layer 4 Height Info", NodeSocketVector)
        _ = create_socket(interface, "Layer 4 Extra", NodeSocketVector)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        links = self.node_tree.links

        group_input = create_node(nodes, -2455, 771, NodeGroupInput)
        group_input_001 = create_node(nodes, -3041, 1138, NodeGroupInput)
        group_output = create_node(nodes, 998, 770, NodeGroupOutput)

        separate_color = create_node(nodes, -1712, 1077, ShaderNodeSeparateColor)
        separate_color.mode = "RGB"

        group = create_node(nodes, -874, 777, ShaderNodeGroup)
        group.node_tree = cast(ShaderNodeTree, FloatBlend().node_tree)

        group_001 = create_node(nodes, -875, 428, ShaderNodeGroup)
        group_001.node_tree = cast(ShaderNodeTree, FloatBlend().node_tree)

        group_002 = create_node(nodes, -873, 1130, ShaderNodeGroup)
        group_002.node_tree = cast(ShaderNodeTree, ColorBlend().node_tree)

        group_003 = create_node(nodes, -872, -212, ShaderNodeGroup)
        group_003.node_tree = cast(ShaderNodeTree, ColorBlend().node_tree)
        cast(NodeSocketInt, group_003.inputs[3]).default_value = 0
        cast(NodeSocketInt, group_003.inputs[5]).default_value = 0
        cast(NodeSocketInt, group_003.inputs[7]).default_value = 0
        cast(NodeSocketInt, group_003.inputs[9]).default_value = 1

        group_004 = create_node(nodes, -2792, 1318, ShaderNodeGroup)
        group_004.node_tree = cast(ShaderNodeTree, LayerBlending().node_tree)

        group_005 = create_node(nodes, -867, 135, ShaderNodeGroup)
        group_005.node_tree = cast(ShaderNodeTree, NormalBlend().node_tree)

        group_006 = create_node(nodes, -869, -521, ShaderNodeGroup)
        group_006.node_tree = cast(ShaderNodeTree, OcclusionBlend().node_tree)

        reroute = create_node(nodes, -1421, 1102, NodeReroute)
        reroute_001 = create_node(nodes, -1424, 1148, NodeReroute)

        separate_xyz = create_node(nodes, -551, -183, ShaderNodeSeparateXYZ)

        mix = create_node(nodes, -490, 560, ShaderNodeMix)
        mix.blend_type = "MIX"
        mix.clamp_factor = True
        mix.clamp_result = False
        mix.data_type = "RGBA"
        mix.factor_mode = "UNIFORM"
        assign_value(mix, 6, (0.02, 0.02, 0.02, 1.0))

        mix_001 = create_node(nodes, -451, 889, ShaderNodeMix)
        mix_001.blend_type = "MIX"
        mix_001.clamp_factor = True
        mix_001.clamp_result = False
        mix_001.data_type = "RGBA"
        mix_001.factor_mode = "UNIFORM"
        assign_value(mix_001, 7, (0.0, 0.0, 0.0, 1.0))

        mix_003 = create_node(nodes, -206, 898, ShaderNodeMix)
        mix_003.blend_type = "MULTIPLY"
        mix_003.clamp_factor = True
        mix_003.clamp_result = False
        mix_003.data_type = "RGBA"
        mix_003.factor_mode = "UNIFORM"
        assign_value(mix_003, 0, 1.0)

        mix_004 = create_node(nodes, -190, 583, ShaderNodeMix)
        mix_004.blend_type = "MULTIPLY"
        mix_004.clamp_factor = True
        mix_004.clamp_result = False
        mix_004.data_type = "RGBA"
        mix_004.factor_mode = "UNIFORM"
        assign_value(mix_004, 0, 1.0)

        mix_005 = create_node(nodes, -372, 223, ShaderNodeMix)
        mix_005.blend_type = "OVERLAY"
        mix_005.clamp_factor = True
        mix_005.clamp_result = False
        mix_005.data_type = "RGBA"
        mix_005.factor_mode = "UNIFORM"
        assign_value(mix_005, 0, 1.0)

        metallic_bsdf = create_node(nodes, 171, 565, ShaderNodeBsdfMetallic)
        metallic_bsdf.distribution = "MULTI_GGX"
        metallic_bsdf.fresnel_type = "F82"
        assign_value(metallic_bsdf, 1, (0.695, 0.726, 0.77, 1.0))
        assign_value(metallic_bsdf, 5, 0.0)
        assign_value(metallic_bsdf, 6, 0.0)
        assign_value(metallic_bsdf, 8, (0.0, 0.0, 0.0))
        assign_value(metallic_bsdf, 10, 0.0)
        assign_value(metallic_bsdf, 11, 1.33)

        diffuse_bsdf = create_node(nodes, 52, 860, ShaderNodeBsdfDiffuse)

        add_shader = create_node(nodes, 368, 752, ShaderNodeAddShader)

        bump_002 = create_node(nodes, -67, 239, ShaderNodeBump)
        bump_002.invert = False
        assign_value(bump_002, 2, 1.0)

        value = create_node(nodes, -265, -16, ShaderNodeValue)
        if value.outputs:
            value.outputs[0].default_value = 0.025

        create_link(links, group_input_001, group_004, 2, 0)
        create_link(links, group_input_001, group_004, 3, 1)
        create_link(links, group_input_001, group_004, 16, 2)
        create_link(links, group_input_001, group_004, 17, 3)
        create_link(links, group_input_001, group_004, 25, 4)
        create_link(links, group_input_001, group_004, 26, 5)
        create_link(links, group_input_001, group_004, 34, 6)
        create_link(links, group_input_001, group_004, 35, 7)
        create_link(links, group_input_001, group_004, 43, 8)
        create_link(links, group_input_001, group_004, 44, 9)

        create_link(links, group_004, reroute, 1, 0)
        create_link(links, group_004, reroute_001, 0, 0)
        create_link(links, group_004, group_003, 0, 0)
        create_link(links, group_004, group_003, 1, 1)
        create_link(links, group_004, group_006, 0, 0)
        create_link(links, group_004, group_006, 1, 1)

        create_link(links, reroute, group_002, 0, 1)
        create_link(links, reroute, group, 0, 1)
        create_link(links, reroute, group_001, 0, 1)
        create_link(links, reroute, group_005, 0, 1)

        create_link(links, reroute_001, group_002, 0, 0)
        create_link(links, reroute_001, group, 0, 0)
        create_link(links, reroute_001, group_001, 0, 0)
        create_link(links, reroute_001, group_005, 0, 0)

        create_link(links, group_input, separate_color, 0, 0)

        create_link(links, separate_color, group, 0, 2)

        create_link(links, group_input, group, 6, 3)
        create_link(links, group_input, group, 12, 4)
        create_link(links, group_input, group, 21, 5)
        create_link(links, group_input, group, 30, 6)
        create_link(links, group_input, group, 39, 7)

        create_link(links, group_input, group_001, 3, 2)
        create_link(links, group_input, group_001, 8, 3)
        create_link(links, group_input, group_001, 13, 4)
        create_link(links, group_input, group_001, 22, 5)
        create_link(links, group_input, group_001, 31, 6)
        create_link(links, group_input, group_001, 40, 7)

        create_link(links, group_input, group_002, 11, 2)
        create_link(links, group_input, group_002, 9, 3)
        create_link(links, group_input, group_002, 20, 4)
        create_link(links, group_input, group_002, 18, 5)
        create_link(links, group_input, group_002, 29, 6)
        create_link(links, group_input, group_002, 27, 7)
        create_link(links, group_input, group_002, 38, 8)
        create_link(links, group_input, group_002, 36, 9)

        create_link(links, group_input, group_003, 16, 2)
        create_link(links, group_input, group_003, 25, 4)
        create_link(links, group_input, group_003, 34, 6)
        create_link(links, group_input, group_003, 43, 8)

        create_link(links, group_003, separate_xyz, 0, 0)

        create_link(links, group_input, group_005, 4, 2)
        create_link(links, group_input, group_005, 15, 3)
        create_link(links, group_input, group_005, 10, 4)
        create_link(links, group_input, group_005, 24, 5)
        create_link(links, group_input, group_005, 19, 6)
        create_link(links, group_input, group_005, 33, 7)
        create_link(links, group_input, group_005, 28, 8)
        create_link(links, group_input, group_005, 42, 9)
        create_link(links, group_input, group_005, 37, 10)

        create_link(links, separate_color, group_006, 1, 2)
        create_link(links, group_input, group_006, 7, 3)
        create_link(links, group_input, group_006, 14, 4)
        create_link(links, group_input, group_006, 23, 5)
        create_link(links, group_input, group_006, 32, 6)
        create_link(links, group_input, group_006, 41, 7)

        create_link(links, group_001, mix, 0, 0)
        create_link(links, group_002, mix, 0, 7)
        create_link(links, group_002, mix_001, 0, 6)
        create_link(links, group_001, mix_001, 0, 0)

        create_link(links, mix_001, mix_003, 2, 6)
        create_link(links, group_006, mix_003, 0, 7)
        create_link(links, mix, mix_004, 2, 6)
        create_link(links, group_006, mix_004, 0, 7)

        create_link(links, value, bump_002, 0, 0)
        create_link(links, group_input, bump_002, 5, 1)
        create_link(links, mix_005, bump_002, 2, 3)
        create_link(links, group_005, bump_002, 0, 4)

        create_link(links, separate_color, mix_005, 2, 6)
        create_link(links, separate_xyz, mix_005, 2, 7)

        create_link(links, group, diffuse_bsdf, 0, 1)
        create_link(links, group, metallic_bsdf, 0, 4)
        create_link(links, mix_003, diffuse_bsdf, 2, 0)
        create_link(links, mix_004, metallic_bsdf, 2, 0)
        create_link(links, bump_002, diffuse_bsdf, 0, 2)
        create_link(links, bump_002, metallic_bsdf, 0, 7)
        create_link(links, diffuse_bsdf, add_shader, 0, 0)
        create_link(links, metallic_bsdf, add_shader, 0, 1)
        create_link(links, add_shader, group_output, 0, 0)
