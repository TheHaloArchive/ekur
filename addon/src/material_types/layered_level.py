# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import logging
from typing import cast

from bpy.types import (
    NodeClosureInput,
    NodeClosureOutput,
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeSeparateColor,
    ShaderNodeTree,
    ShaderNodeUVMap,
)

from ..json_definitions import CommonMaterial, ConemapInfo
from ..nodes.conemap_parallax import ConemapParallax
from ..nodes.layered_level_hinf import LayeredLevelHINF
from ..nodes.nnhg_shader import NnhgShader
from ..nodes.rohg_shader import RohgShader
from ..nodes.rohm_shader import RohmShader
from ..ui.material_options import get_material_options
from ..utils import assign_value, create_image, create_node, create_link

__all__ = ["LayeredLevel"]

_LAYER_TYPE_MAP = {
    "RohmLayer": ("rohm", RohmShader),
    "RohgLayer": ("rohg", RohgShader),
    "NnhgLayer": ("nnhg", NnhgShader),
}


class LayeredLevel:
    def __init__(self, material: CommonMaterial, material_tree: ShaderNodeTree) -> None:
        self.material: CommonMaterial = material
        self.tree: ShaderNodeTree = material_tree
        self._create_nodes()

    def _get_textures_for_layer(
        self,
        layer_name: str,
        layer_type: str,
        layer_shader: ShaderNodeGroup,
        uv_map: ShaderNodeUVMap | ShaderNodeGroup,
        offset: int,
    ) -> None:
        match layer_type:
            case "RohmLayer":
                col = self.material["textures"].get(f"{layer_name}Color")
                if col:
                    color_image = create_image(self.tree.nodes, offset + 100, str(col))
                    if color_image.image:
                        color_image.image.colorspace_settings.name = "sRGB"  # ty:ignore[invalid-assignment]
                    create_link(self.tree.links, color_image, layer_shader, 0, 0)
                    create_link(self.tree.links, uv_map, color_image, 0, 0)
                contr = self.material["textures"].get(f"{layer_name}Control")
                if contr:
                    control_image = create_image(self.tree.nodes, offset, str(contr))
                    create_link(self.tree.links, control_image, layer_shader, 0, 2)
                    create_link(self.tree.links, control_image, layer_shader, 1, 3)
                    create_link(self.tree.links, uv_map, control_image, 0, 0)
                norm = self.material["textures"].get(f"{layer_name}Normal")
                if norm:
                    normal_image = create_image(self.tree.nodes, offset - 100, str(norm))
                    create_link(self.tree.links, normal_image, layer_shader, 0, 9)
                    create_link(self.tree.links, uv_map, normal_image, 0, 0)
            case "RohgLayer":
                contr = self.material["textures"].get(f"{layer_name}Control")
                if contr:
                    control_image = create_image(self.tree.nodes, offset, str(contr))
                    create_link(self.tree.links, control_image, layer_shader, 0, 1)
                    create_link(self.tree.links, control_image, layer_shader, 1, 2)
                    create_link(self.tree.links, uv_map, control_image, 0, 0)
                norm = self.material["textures"].get(f"{layer_name}Normal")
                if norm:
                    normal_image = create_image(self.tree.nodes, offset - 100, str(norm))
                    create_link(self.tree.links, normal_image, layer_shader, 0, 10)
                    create_link(self.tree.links, uv_map, normal_image, 0, 0)
            case "NnhgLayer":
                packed = self.material["textures"].get(f"{layer_name}Packed")
                if packed:
                    control_image = create_image(self.tree.nodes, offset, str(packed))
                    create_link(self.tree.links, control_image, layer_shader, 0, 1)
                    create_link(self.tree.links, control_image, layer_shader, 1, 2)
                    create_link(self.tree.links, uv_map, control_image, 0, 0)
            case _:
                return

    def _get_textures(self, nodes: ShaderNodeGroup) -> None:
        mcc = self.material["textures"].get("MacroColor")
        if mcc:
            color_image = create_image(self.tree.nodes, 100, str(mcc))
            if color_image.image:
                color_image.image.colorspace_settings.name = "sRGB"  # ty:ignore[invalid-assignment]
            create_link(self.tree.links, color_image, nodes, 0, 0)
        else:
            assign_value(nodes, 0, (1.0, 1.0, 1.0, 1.0))
        mmm = self.material["textures"].get("MacroMaskMap")
        if mmm:
            color_image = create_image(self.tree.nodes, 200, str(mmm))
            create_link(self.tree.links, color_image, nodes, 0, 3)
            create_link(self.tree.links, color_image, nodes, 1, 4)
            uv_map = create_node(self.tree.nodes, -700, 200, ShaderNodeUVMap)
            uv_map.uv_map = "UV1"  # TODO: Check if exists..
            create_link(self.tree.links, uv_map, color_image, 0, 0)
        mmn = self.material["textures"].get("MacroNormal")
        if mmn:
            color_image = create_image(self.tree.nodes, 300, str(mmn))
            create_link(self.tree.links, color_image, nodes, 0, 5)
        else:
            assign_value(nodes, 5, (0.5, 0.5, 1.0, 1.0))
        mmc = self.material["textures"].get("MacroControl")
        if mmc:
            color_image = create_image(self.tree.nodes, 400, str(mmc))
            create_link(self.tree.links, color_image, nodes, 0, 1)
            create_link(self.tree.links, color_image, nodes, 1, 2)

    def _setup_conemap_closure(self) -> NodeClosureOutput | None:
        conemap = self.material["textures"].get("MacroConemap")
        if not conemap:
            return None

        closure_input = create_node(self.tree.nodes, -1000, 600, NodeClosureInput)
        closure_output = create_node(self.tree.nodes, -300, 600, NodeClosureOutput)
        closure_output.input_items.clear()
        closure_output.input_items.new("VECTOR", "Vector")
        closure_output.output_items.clear()
        closure_output.output_items.new("FLOAT", "Height")
        closure_output.output_items.new("FLOAT", "Cone")
        closure_input.pair_with_output(closure_output)

        conemap_image = create_image(self.tree.nodes, 600, str(conemap))
        create_link(self.tree.links, closure_input, conemap_image, 0, 0)

        separate_color = create_node(self.tree.nodes, -140, 600, ShaderNodeSeparateColor)
        create_link(self.tree.links, conemap_image, separate_color, 0, 0)
        create_link(self.tree.links, separate_color, closure_output, 0, 0)
        create_link(self.tree.links, separate_color, closure_output, 0, 1)

        return closure_output

    def _setup_layer_shader(
        self,
        shader_class: type,
        layer_name: str,
        offset: int,
        conemap_info: ConemapInfo | None,
        conemap_closure: NodeClosureOutput | None,
    ) -> tuple[ShaderNodeUVMap | ShaderNodeGroup, ShaderNodeGroup]:
        uv_map = create_node(self.tree.nodes, -700, -offset, ShaderNodeUVMap)
        uv_map.uv_map = "UV2"  # TODO: Check if exists..

        uv_source: ShaderNodeUVMap | ShaderNodeGroup = uv_map
        if conemap_info:
            conemap_node = create_node(self.tree.nodes, -500, -offset, ShaderNodeGroup)
            conemap_node.hide = True
            conemap_node.label = f"{layer_name} Conemap Parallax"
            conemap_node.node_tree = cast(ShaderNodeTree, ConemapParallax().node_tree)
            create_link(self.tree.links, uv_map, conemap_node, 0, 0)
            if conemap_closure:
                create_link(self.tree.links, conemap_closure, conemap_node, 0, 1)
            assign_value(conemap_node, 2, conemap_info["parallax_depth"])
            assign_value(conemap_node, 3, conemap_info["parallax_height_offset"])
            assign_value(conemap_node, 4, conemap_info["quality"])
            assign_value(conemap_node, 5, conemap_info["cone_step_fade_near"])
            assign_value(conemap_node, 6, conemap_info["cone_step_fade_far"])
            uv_source = conemap_node

        layer_shader = create_node(self.tree.nodes, 0, -offset, ShaderNodeGroup)
        layer_shader.hide = True
        layer_shader.label = layer_name
        layer_shader.node_tree = cast(ShaderNodeTree, shader_class().node_tree)
        return uv_source, layer_shader

    def _connect_layer_outputs(
        self, layer_shader: ShaderNodeGroup, shader: ShaderNodeGroup, i: int
    ) -> None:
        for out_idx in range(7):
            self.tree.links.new(layer_shader.outputs[out_idx], shader.inputs[13 + i * 9 + out_idx])

    def _apply_rohm_values(self, layer_shader: ShaderNodeGroup, data: dict) -> None:
        assign_value(layer_shader, 1, (*data["color_tint"], 1.0))
        assign_value(layer_shader, 4, data["roughness_black"])
        assign_value(layer_shader, 5, data["roughness_white"])
        assign_value(layer_shader, 6, data["metallic_black"])
        assign_value(layer_shader, 7, data["metallic_white"])
        assign_value(layer_shader, 8, data["height_scale"])
        assign_value(layer_shader, 10, data["normal_intensity"])
        if data["extra_data"]:
            assign_value(layer_shader, 12, data["extra_data"]["opacity"])
            assign_value(layer_shader, 13, data["extra_data"]["height_blend_range"])
            assign_value(layer_shader, 14, data["extra_data"]["height_accumulation"])

    def _apply_rohg_nnhg_values(self, layer_shader: ShaderNodeGroup, data: dict) -> None:
        assign_value(layer_shader, 3, data["roughness_black"])
        assign_value(layer_shader, 4, data["roughness_white"])
        assign_value(layer_shader, 5, data["metallic"])
        assign_value(layer_shader, 6, (*data["top_color"], 1.0))
        assign_value(layer_shader, 7, (*data["mid_color"], 1.0))
        assign_value(layer_shader, 8, (*data["bottom_color"], 1.0))
        assign_value(layer_shader, 9, data["height_scale"])
        assign_value(layer_shader, 11, data["normal_intensity"])
        if data["extra_data"]:
            assign_value(layer_shader, 13, data["extra_data"]["opacity"])
            assign_value(layer_shader, 14, data["extra_data"]["height_blend_range"])
            assign_value(layer_shader, 15, data["extra_data"]["height_accumulation"])

    def _create_nodes(self) -> None:
        if not self.material["layered_level"]:
            logging.warning(
                "Layered level material has no layered_level key, this shouldn't happen!"
            )
            return
        info = self.material["layered_level"]
        if not info["layers"]:
            return

        shader = create_node(self.tree.nodes, 500, 500, ShaderNodeGroup)
        shader.node_tree = cast(ShaderNodeTree, LayeredLevelHINF().node_tree)

        macro_mask_info = info["macro_mask_info"]
        if macro_mask_info:
            assign_value(shader, 7, macro_mask_info["macro_roughness_intensity"])
            assign_value(shader, 8, macro_mask_info["macro_occlusion_intensity"])
            assign_value(shader, 9, macro_mask_info["macro_metallic_intensity"])
            assign_value(shader, 10, macro_mask_info["macro_color_intensity"])
        else:
            assign_value(shader, 7, 0)
            assign_value(shader, 8, 0)
            assign_value(shader, 9, 0)
            assign_value(shader, 10, 0)
        material_output = create_node(self.tree.nodes, 800, 0, ShaderNodeOutputMaterial)
        create_link(self.tree.links, shader, material_output, 0, 0)

        self._get_textures(shader)

        options = get_material_options()
        conemap_info = info["conemap_info"] if options.enable_parallax else None
        conemap_closure = self._setup_conemap_closure() if conemap_info else None

        for i, layer in enumerate(info["layers"]):
            layer_type = layer["layer_type"]
            if layer_type not in _LAYER_TYPE_MAP:
                continue

            data_key, shader_class = _LAYER_TYPE_MAP[layer_type]
            data = layer.get(data_key)
            if not data:
                continue

            layer_name = f"Layer{i + 1}"
            offset = i * 250

            uv_map, layer_shader = self._setup_layer_shader(
                shader_class, layer_name, offset, conemap_info, conemap_closure
            )
            assign_value(shader, 11 + i * 9, data["color_blend_mode"])
            assign_value(shader, 12 + i * 9, data["normal_blend_mode"])

            if layer_type == "RohmLayer":
                self._apply_rohm_values(layer_shader, data)
            else:
                self._apply_rohg_nnhg_values(layer_shader, data)

            self._get_textures_for_layer(layer_name, layer_type, layer_shader, uv_map, -offset)
            self._connect_layer_outputs(layer_shader, shader, i)
