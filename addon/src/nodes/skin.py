# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import cast

import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketShader,
    NodeTree,
    ShaderNodeBsdfPrincipled,
    ShaderNodeGroup,
    ShaderNodeMath,
    ShaderNodeMix,
    ShaderNodeNormalMap,
    ShaderNodeSeparateColor,
    ShaderNodeTree,
)

from ..utils import assign_value, create_node, create_socket, create_link
from .norm_normalize import NormNormalize


class Skin:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Skin Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Skin Shader")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        _ = create_socket(interface, "Color", NodeSocketColor)
        _ = create_socket(interface, "AoRoughnessTransmission", NodeSocketColor)
        _ = create_socket(interface, "SpecularSubsurfacePore", NodeSocketColor)
        _ = create_socket(interface, "Normal Map", NodeSocketColor)
        _ = create_socket(interface, "Pore Map", NodeSocketColor)
        _ = create_socket(interface, "Micro Normal", NodeSocketColor)
        _ = create_socket(interface, "Subsurface Strength", NodeSocketFloat)
        _ = create_socket(interface, "Specular Intensity", NodeSocketFloat)
        _ = create_socket(interface, "Specular White", NodeSocketFloat)
        _ = create_socket(interface, "Specular Black", NodeSocketFloat)
        _ = create_socket(interface, "Pore Intensity", NodeSocketFloat)
        _ = create_socket(interface, "Micro Normal Intensity", NodeSocketFloat)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        nodes = self.node_tree.nodes
        links = self.node_tree.links

        input = create_node(nodes, 0, 0, NodeGroupInput)
        output = create_node(nodes, 0, 0, NodeGroupOutput)
        bsdf = create_node(nodes, 0, 0, ShaderNodeBsdfPrincipled)

        aorotr_srgb = create_node(nodes, 0, 0, ShaderNodeSeparateColor)
        create_link(links, input, aorotr_srgb, 1, 0)

        ao_mult = create_node(nodes, 0, 0, ShaderNodeMix)
        ao_mult.data_type = "RGBA"
        ao_mult.blend_type = "MULTIPLY"
        assign_value(ao_mult, 0, 1.0)
        create_link(links, input, ao_mult, 0, 6)
        create_link(links, aorotr_srgb, ao_mult, 0, 7)
        create_link(links, ao_mult, bsdf, 2, 0)
        create_link(links, aorotr_srgb, bsdf, 1, 2)
        create_link(links, aorotr_srgb, bsdf, 2, 18)

        specsubpore_srgb = create_node(nodes, 0, 0, ShaderNodeSeparateColor)
        lerp = create_node(nodes, 0, 0, ShaderNodeMix)
        create_link(links, input, specsubpore_srgb, 2, 0)
        create_link(links, specsubpore_srgb, lerp, 0, 0)
        create_link(links, input, lerp, 8, 2)
        create_link(links, input, lerp, 9, 3)

        spec_intensity = create_node(nodes, 0, 0, ShaderNodeMath)
        spec_intensity.operation = "MULTIPLY"
        create_link(links, lerp, spec_intensity, 0, 0)
        create_link(links, input, spec_intensity, 7, 1)
        if bpy.app.version >= (5, 2, 0):
            create_link(links, spec_intensity, bsdf, 0, 14)
        else:
            create_link(links, spec_intensity, bsdf, 0, 13)

        subsurf_intensity = create_node(nodes, 0, 0, ShaderNodeMath)
        subsurf_intensity.operation = "MULTIPLY"
        create_link(links, specsubpore_srgb, subsurf_intensity, 1, 0)
        create_link(links, input, subsurf_intensity, 6, 1)
        bsdf.subsurface_method = "RANDOM_WALK_SKIN"
        if bpy.app.version >= (5, 2, 0):
            create_link(links, subsurf_intensity, bsdf, 0, 9)
        else:
            create_link(links, subsurf_intensity, bsdf, 0, 8)

        pore_intensity = create_node(nodes, 0, 0, ShaderNodeMath)
        pore_intensity.operation = "MULTIPLY"
        create_link(links, specsubpore_srgb, pore_intensity, 2, 0)
        create_link(links, input, pore_intensity, 10, 1)

        pore_overlay = create_node(nodes, 0, 0, ShaderNodeMix)
        pore_overlay.data_type = "RGBA"
        pore_overlay.blend_type = "OVERLAY"
        create_link(links, pore_intensity, pore_overlay, 0, 0)
        create_link(links, input, pore_overlay, 3, 6)
        create_link(links, input, pore_overlay, 4, 7)

        detail_overlay = create_node(nodes, 0, 0, ShaderNodeMix)
        detail_overlay.data_type = "RGBA"
        detail_overlay.blend_type = "OVERLAY"
        create_link(links, input, detail_overlay, 11, 0)
        create_link(links, pore_overlay, detail_overlay, 2, 6)
        create_link(links, input, detail_overlay, 5, 7)

        norm_normalize = create_node(nodes, 0, 0, ShaderNodeGroup)
        norm_normalize.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)
        assign_value(norm_normalize, 1, 1.0)
        create_link(links, detail_overlay, norm_normalize, 2, 0)

        normal_map = create_node(nodes, 0, 0, ShaderNodeNormalMap)
        create_link(links, norm_normalize, normal_map, 0, 1)
        if bpy.app.version >= (5, 2, 0):
            create_link(links, normal_map, bsdf, 0, 6)
        else:
            create_link(links, normal_map, bsdf, 0, 5)
        create_link(links, bsdf, output, 0, 0)
