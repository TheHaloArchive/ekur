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

from .norm_normalize import NormNormalize

from ..utils import assign_value, create_node, create_socket


class Skin:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Skin Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Skin Shader",
            )
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
        _ = links.new(input.outputs[1], aorotr_srgb.inputs[0])

        ao_mult = create_node(nodes, 0, 0, ShaderNodeMix)
        ao_mult.data_type = "RGBA"
        ao_mult.blend_type = "MULTIPLY"
        assign_value(ao_mult, 0, 1.0)
        _ = links.new(input.outputs[0], ao_mult.inputs[6])
        _ = links.new(aorotr_srgb.outputs[0], ao_mult.inputs[7])
        _ = links.new(ao_mult.outputs[2], bsdf.inputs[0])
        _ = links.new(aorotr_srgb.outputs[1], bsdf.inputs[2])
        _ = links.new(aorotr_srgb.outputs[2], bsdf.inputs[18])

        specsubpore_srgb = create_node(nodes, 0, 0, ShaderNodeSeparateColor)
        lerp = create_node(nodes, 0, 0, ShaderNodeMix)
        _ = links.new(input.outputs[2], specsubpore_srgb.inputs[0])
        _ = links.new(specsubpore_srgb.outputs[0], lerp.inputs[0])
        _ = links.new(input.outputs[8], lerp.inputs[2])
        _ = links.new(input.outputs[9], lerp.inputs[3])

        spec_intensity = create_node(nodes, 0, 0, ShaderNodeMath)
        spec_intensity.operation = "MULTIPLY"
        _ = links.new(lerp.outputs[0], spec_intensity.inputs[0])
        _ = links.new(input.outputs[7], spec_intensity.inputs[1])
        _ = links.new(spec_intensity.outputs[0], bsdf.inputs[13])

        subsurf_intensity = create_node(nodes, 0, 0, ShaderNodeMath)
        subsurf_intensity.operation = "MULTIPLY"
        _ = links.new(specsubpore_srgb.outputs[1], subsurf_intensity.inputs[0])
        _ = links.new(input.outputs[6], subsurf_intensity.inputs[1])
        bsdf.subsurface_method = "RANDOM_WALK_SKIN"
        _ = links.new(subsurf_intensity.outputs[0], bsdf.inputs[8])

        pore_intensity = create_node(nodes, 0, 0, ShaderNodeMath)
        pore_intensity.operation = "MULTIPLY"
        _ = links.new(specsubpore_srgb.outputs[2], pore_intensity.inputs[0])
        _ = links.new(input.outputs[10], pore_intensity.inputs[1])

        pore_overlay = create_node(nodes, 0, 0, ShaderNodeMix)
        pore_overlay.data_type = "RGBA"
        pore_overlay.blend_type = "OVERLAY"
        _ = links.new(pore_intensity.outputs[0], pore_overlay.inputs[0])
        _ = links.new(input.outputs[3], pore_overlay.inputs[6])
        _ = links.new(input.outputs[4], pore_overlay.inputs[7])

        detail_overlay = create_node(nodes, 0, 0, ShaderNodeMix)
        detail_overlay.data_type = "RGBA"
        detail_overlay.blend_type = "OVERLAY"
        _ = links.new(input.outputs[11], detail_overlay.inputs[0])
        _ = links.new(pore_overlay.outputs[2], detail_overlay.inputs[6])
        _ = links.new(input.outputs[5], detail_overlay.inputs[7])

        norm_normalize = create_node(nodes, 0, 0, ShaderNodeGroup)
        norm_normalize.node_tree = cast(ShaderNodeTree, NormNormalize().node_tree)
        assign_value(norm_normalize, 1, 1.0)
        _ = links.new(detail_overlay.outputs[2], norm_normalize.inputs[0])

        normal_map = create_node(nodes, 0, 0, ShaderNodeNormalMap)
        _ = links.new(norm_normalize.outputs[0], normal_map.inputs[1])
        _ = links.new(normal_map.outputs[0], bsdf.inputs[5])

        _ = links.new(bsdf.outputs[0], output.inputs[0])
