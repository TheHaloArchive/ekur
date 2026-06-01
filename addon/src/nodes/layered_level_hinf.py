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

from ..utils import assign_value, create_node, create_socket
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
        assign_value(
            mix, 6, (0.019999999552965164, 0.019999999552965164, 0.019999999552965164, 1.0)
        )

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
        assign_value(
            metallic_bsdf, 1, (0.6949999928474426, 0.7260000109672546, 0.7699999809265137, 1.0)
        )
        assign_value(metallic_bsdf, 5, 0.0)
        assign_value(metallic_bsdf, 6, 0.0)
        assign_value(metallic_bsdf, 8, (0.0, 0.0, 0.0))
        assign_value(metallic_bsdf, 10, 0.0)
        assign_value(metallic_bsdf, 11, 1.3300000429153442)

        diffuse_bsdf = create_node(nodes, 52, 860, ShaderNodeBsdfDiffuse)

        add_shader = create_node(nodes, 368, 752, ShaderNodeAddShader)

        bump_002 = create_node(nodes, -67, 239, ShaderNodeBump)
        bump_002.invert = False
        assign_value(bump_002, 2, 1.0)

        value = create_node(nodes, -265, -16, ShaderNodeValue)
        cast(NodeSocketFloat, value.outputs[0]).default_value = 0.02500000037252903

        _ = links.new(group_input_001.outputs[2], group_004.inputs[0])
        _ = links.new(group_input_001.outputs[3], group_004.inputs[1])
        _ = links.new(group_input_001.outputs[16], group_004.inputs[2])
        _ = links.new(group_input_001.outputs[17], group_004.inputs[3])
        _ = links.new(group_input_001.outputs[25], group_004.inputs[4])
        _ = links.new(group_input_001.outputs[26], group_004.inputs[5])
        _ = links.new(group_input_001.outputs[34], group_004.inputs[6])
        _ = links.new(group_input_001.outputs[35], group_004.inputs[7])
        _ = links.new(group_input_001.outputs[43], group_004.inputs[8])
        _ = links.new(group_input_001.outputs[44], group_004.inputs[9])

        _ = links.new(group_004.outputs[1], reroute.inputs[0])
        _ = links.new(group_004.outputs[0], reroute_001.inputs[0])
        _ = links.new(group_004.outputs[0], group_003.inputs[0])
        _ = links.new(group_004.outputs[1], group_003.inputs[1])
        _ = links.new(group_004.outputs[0], group_006.inputs[0])
        _ = links.new(group_004.outputs[1], group_006.inputs[1])

        _ = links.new(reroute.outputs[0], group_002.inputs[1])
        _ = links.new(reroute.outputs[0], group.inputs[1])
        _ = links.new(reroute.outputs[0], group_001.inputs[1])
        _ = links.new(reroute.outputs[0], group_005.inputs[1])

        _ = links.new(reroute_001.outputs[0], group_002.inputs[0])
        _ = links.new(reroute_001.outputs[0], group.inputs[0])
        _ = links.new(reroute_001.outputs[0], group_001.inputs[0])
        _ = links.new(reroute_001.outputs[0], group_005.inputs[0])

        _ = links.new(group_input.outputs[0], separate_color.inputs[0])

        _ = links.new(separate_color.outputs[0], group.inputs[2])

        _ = links.new(group_input.outputs[6], group.inputs[3])
        _ = links.new(group_input.outputs[12], group.inputs[4])
        _ = links.new(group_input.outputs[21], group.inputs[5])
        _ = links.new(group_input.outputs[30], group.inputs[6])
        _ = links.new(group_input.outputs[39], group.inputs[7])

        _ = links.new(group_input.outputs[3], group_001.inputs[2])
        _ = links.new(group_input.outputs[8], group_001.inputs[3])
        _ = links.new(group_input.outputs[13], group_001.inputs[4])
        _ = links.new(group_input.outputs[22], group_001.inputs[5])
        _ = links.new(group_input.outputs[31], group_001.inputs[6])
        _ = links.new(group_input.outputs[40], group_001.inputs[7])

        _ = links.new(group_input.outputs[11], group_002.inputs[2])
        _ = links.new(group_input.outputs[9], group_002.inputs[3])
        _ = links.new(group_input.outputs[20], group_002.inputs[4])
        _ = links.new(group_input.outputs[18], group_002.inputs[5])
        _ = links.new(group_input.outputs[29], group_002.inputs[6])
        _ = links.new(group_input.outputs[27], group_002.inputs[7])
        _ = links.new(group_input.outputs[38], group_002.inputs[8])
        _ = links.new(group_input.outputs[36], group_002.inputs[9])

        _ = links.new(group_input.outputs[16], group_003.inputs[2])
        _ = links.new(group_input.outputs[25], group_003.inputs[4])
        _ = links.new(group_input.outputs[34], group_003.inputs[6])
        _ = links.new(group_input.outputs[43], group_003.inputs[8])

        _ = links.new(group_003.outputs[0], separate_xyz.inputs[0])

        _ = links.new(group_input.outputs[4], group_005.inputs[2])
        _ = links.new(group_input.outputs[15], group_005.inputs[3])
        _ = links.new(group_input.outputs[10], group_005.inputs[4])
        _ = links.new(group_input.outputs[24], group_005.inputs[5])
        _ = links.new(group_input.outputs[19], group_005.inputs[6])
        _ = links.new(group_input.outputs[33], group_005.inputs[7])
        _ = links.new(group_input.outputs[28], group_005.inputs[8])
        _ = links.new(group_input.outputs[42], group_005.inputs[9])
        _ = links.new(group_input.outputs[37], group_005.inputs[10])

        _ = links.new(separate_color.outputs[1], group_006.inputs[2])
        _ = links.new(group_input.outputs[7], group_006.inputs[3])
        _ = links.new(group_input.outputs[14], group_006.inputs[4])
        _ = links.new(group_input.outputs[23], group_006.inputs[5])
        _ = links.new(group_input.outputs[32], group_006.inputs[6])
        _ = links.new(group_input.outputs[41], group_006.inputs[7])

        _ = links.new(group_001.outputs[0], mix.inputs[0])
        _ = links.new(group_002.outputs[0], mix.inputs[7])
        _ = links.new(group_002.outputs[0], mix_001.inputs[6])
        _ = links.new(group_001.outputs[0], mix_001.inputs[0])

        _ = links.new(mix_001.outputs[2], mix_003.inputs[6])
        _ = links.new(group_006.outputs[0], mix_003.inputs[7])
        _ = links.new(mix.outputs[2], mix_004.inputs[6])
        _ = links.new(group_006.outputs[0], mix_004.inputs[7])

        _ = links.new(value.outputs[0], bump_002.inputs[0])
        _ = links.new(group_input.outputs[5], bump_002.inputs[1])
        _ = links.new(mix_005.outputs[2], bump_002.inputs[3])
        _ = links.new(group_005.outputs[0], bump_002.inputs[4])

        _ = links.new(separate_color.outputs[2], mix_005.inputs[6])
        _ = links.new(separate_xyz.outputs[2], mix_005.inputs[7])

        _ = links.new(group.outputs[0], diffuse_bsdf.inputs[1])
        _ = links.new(group.outputs[0], metallic_bsdf.inputs[4])
        _ = links.new(mix_003.outputs[2], diffuse_bsdf.inputs[0])
        _ = links.new(mix_004.outputs[2], metallic_bsdf.inputs[0])
        _ = links.new(bump_002.outputs[0], diffuse_bsdf.inputs[2])
        _ = links.new(bump_002.outputs[0], metallic_bsdf.inputs[7])
        _ = links.new(diffuse_bsdf.outputs[0], add_shader.inputs[0])
        _ = links.new(metallic_bsdf.outputs[0], add_shader.inputs[1])
        _ = links.new(add_shader.outputs[0], group_output.inputs[0])
