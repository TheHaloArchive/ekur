# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import json
import logging
from pathlib import Path
from typing import cast

import bpy
from bpy.types import (
    NodeTree,
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTexImage,
    ShaderNodeTree,
)

from ..json_definitions import (
    CoatingGlobalEntries,
    CommonCoating,
    CommonLayer,
    CommonMaterial,
    CommonRegion,
    CommonStyleList,
    get_intentions,
)
from ..nodes.hims import HIMS
from ..nodes.layer import Layer
from ..utils import (
    assign_value,
    create_node,
    get_data_folder,
    get_import_properties,
    get_package_name,
    read_json_file,
    read_texture,
)

MP_VISOR: int = 1420626520
ANY_REGION: str = "192819851"

__all__ = ["LayeredShader"]


class LayeredShader:
    def __init__(
        self, material_tree: ShaderNodeTree, material: CommonMaterial, styles: CommonStyleList
    ) -> None:
        self.node_tree: ShaderNodeTree = material_tree
        self.styles: CommonStyleList = styles
        self.material: CommonMaterial = material
        self.index: int = 0
        self.data_folder: str = get_data_folder()
        self.has_mask0: bool = False
        self.has_mask1: bool = False
        self.shader: ShaderNodeGroup = create_node(self.node_tree.nodes, 700, 600, ShaderNodeGroup)
        self.create_nodes()

    def create_nodes(self):
        self.shader.node_tree = cast(ShaderNodeTree, HIMS().node_tree)
        self.shader.width = 400
        material_output = create_node(self.node_tree.nodes, 2000, 150, ShaderNodeOutputMaterial)
        _ = self.node_tree.links.new(self.shader.outputs[0], material_output.inputs[0])

    def create_image(self, shader: NodeTree, name: int, y: int) -> ShaderNodeTexImage:
        texture = create_node(shader.nodes, 0, y, ShaderNodeTexImage)
        texture.hide = True
        texture.image = read_texture(str(name))
        return texture

    def create_textures(self) -> None:
        textures = self.material["textures"]
        if textures.get("Asg"):
            tex = self.create_image(self.node_tree, textures["Asg"], 120)
            tex.interpolation = "Cubic"
            if (
                tex.image
                and cast(bool, tex.image.get("use_alpha"))  # pyright: ignore[reportUnknownMemberType]
                and self.material["alpha_blend_mode"] != "Opaque"
            ):
                transparencies = [21, 35, 49, 63, 77, 91, 105]
                for i in transparencies:
                    _ = self.node_tree.links.new(tex.outputs[1], self.shader.inputs[i])
            _ = self.node_tree.links.new(tex.outputs[0], self.shader.inputs[0])
        if textures.get("Mask0"):
            self.has_mask0 = True
            tex = self.create_image(self.node_tree, textures["Mask0"], 80)
            _ = self.node_tree.links.new(tex.outputs[0], self.shader.inputs[1])
        if textures.get("Mask1"):
            self.has_mask1 = True
            tex = self.create_image(self.node_tree, textures["Mask1"], 40)
            _ = self.node_tree.links.new(tex.outputs[0], self.shader.inputs[2])
        if textures.get("Normal") and textures["Normal"] != -1:
            tex = self.create_image(self.node_tree, textures["Normal"], 0)
            _ = self.node_tree.links.new(tex.outputs[0], self.shader.inputs[3])

    def process_styles(self, custom_id: int = 0) -> None:
        style = self.styles["default_style"]["reference"]
        data = get_data_folder()
        import_props = get_import_properties()
        custom_style = import_props.coat_id
        coating = import_props.coatings
        use_default = import_props.use_default

        if custom_style != "" and not use_default and self.styles["styles"].get(custom_style):
            style = self.styles["styles"][custom_style]["reference"]
        if custom_style == "" and not use_default and self.styles["styles"].get(coating):
            style = self.styles["styles"][coating]["reference"]
        if custom_id != 0 and self.styles["styles"].get(str(custom_id)):
            style = self.styles["styles"][str(custom_id)]["reference"]

        style_json = read_json_file(Path(f"{data}/styles/{style}.json"), CommonCoating)
        globals_json = read_json_file(Path(f"{data}/globals.json"), CoatingGlobalEntries)
        if style_json and globals_json:
            self.create_style(style_json, globals_json)

    def create_style(self, style: CommonCoating, globals: CoatingGlobalEntries) -> None:
        style_info = self.material["style_info"]
        if not style_info:
            return

        intentions = get_intentions(style_info)

        all = style["regions"].get(ANY_REGION)
        reg: CommonRegion | None = None
        if style["regions"].get(str(style_info["region_name"])):
            reg = style["regions"][str(style_info["region_name"])]
        self.index = 0

        for i, intention in enumerate(intentions[: style_info["supported_layers"]]):
            intention = str(intention)
            self.find_intention(intention, reg, all, globals, i)

        assign_value(self.shader, 7, style["grime_amount"])
        if style["grime_swatch"]["disabled"]:
            assign_value(self.shader, 7, 0.0)
        assign_value(self.shader, 17, style["scratch_amount"])
        assign_value(self.shader, 12, True)  # Global Scratch Toggle
        assign_value(self.shader, 122, style_info["texel_density"][0])
        assign_value(self.shader, 123, style_info["texel_density"][1])

        self.index = 97
        grime_hash = str(hash(json.dumps(style["grime_swatch"])))
        top = style["grime_swatch"]["top_color"]
        swatch = cast(ShaderNodeTree, Layer(style["grime_swatch"], grime_hash).node_tree)
        emissive_amount = style["grime_swatch"]["emissive_amount"]
        self.create_swatch(swatch, top, 6.9, emissive_amount, is_grime=True)
        toggle_damage = get_import_properties().toggle_damage
        if toggle_damage and style_info["supported_layers"] == 7:
            assign_value(self.shader, 97, False)
        if toggle_damage and style_info["supported_layers"] == 4:
            assign_value(self.shader, 55, False)
        if not self.has_mask1 and style_info["supported_layers"] == 4:
            assign_value(self.shader, 55, False)
        if not self.has_mask1 and style_info["supported_layers"] == 7:
            assign_value(self.shader, 97, False)
        self.index = 0

    def create_swatch(
        self,
        shader_group: ShaderNodeTree,
        color: tuple[float, float, float],
        location: float,
        emissive: float,
        is_grime: bool = False,
        disabled: bool = False,
    ):
        redo2 = False
        if location == 1 and not self.shader.inputs[23].is_linked:
            location = 0
            self.index -= 14
            redo2 = True

        swatch = cast(ShaderNodeGroup, self.node_tree.nodes.new("ShaderNodeGroup"))
        swatch.hide = True
        swatch.use_custom_color = True
        swatch.color = color
        swatch.node_tree = shader_group
        swatch.location = (500, -232 + location * -320)
        if self.material["style_info"]:
            assign_value(swatch, 0, self.material["style_info"]["texel_density"][0])
            assign_value(swatch, 1, self.material["style_info"]["texel_density"][1])
            assign_value(swatch, 6, self.material["style_info"]["material_offset"][0])
            assign_value(swatch, 7, self.material["style_info"]["material_offset"][1])

        _ = self.node_tree.links.new(swatch.outputs[0], self.shader.inputs[14 + self.index])
        _ = self.node_tree.links.new(swatch.outputs[1], self.shader.inputs[15 + self.index])
        _ = self.node_tree.links.new(swatch.outputs[2], self.shader.inputs[16 + self.index])
        if is_grime:
            _ = self.node_tree.links.new(swatch.outputs[5], self.shader.inputs[17 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[6], self.shader.inputs[20 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[7], self.shader.inputs[21 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[8], self.shader.inputs[22 + self.index])
        else:
            if not disabled:
                assign_value(self.shader, 13 + self.index, True)
            assign_value(self.shader, 22 + self.index, emissive)
            _ = self.node_tree.links.new(swatch.outputs[3], self.shader.inputs[18 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[4], self.shader.inputs[19 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[5], self.shader.inputs[20 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[6], self.shader.inputs[23 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[7], self.shader.inputs[24 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[8], self.shader.inputs[25 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[9], self.shader.inputs[26 + self.index])
        if redo2:
            self.index += 14
            self.create_swatch(shader_group, color, 2, emissive)

    def get_intention(
        self,
        intention: str,
        reg: CommonRegion | None,
        all: CommonRegion | None,
        globals: CoatingGlobalEntries,
    ) -> CommonLayer | None:
        if reg and reg["layers"].get(intention):
            return reg["layers"][intention]
        elif all and all["layers"].get(str(intention)):
            return all["layers"][intention]
        elif globals["entries"].get(intention):
            if globals["entries"][intention]["fallback"] != 0:
                fallback = str(globals["entries"][intention]["fallback"])
                return self.get_intention(fallback, reg, all, globals)
            return globals["entries"][intention]["layer"]
        else:
            logging.warning(f"Intention not found at all, skipping!: {intention}")

    def find_intention(
        self,
        intention: str,
        mat_reg: CommonRegion | None,
        any_reg: CommonRegion | None,
        globals: CoatingGlobalEntries,
        i: int,
    ) -> None:
        """Finds the intention provided in the "common", "local" and "global" regions.

        Args:
            intention: Name of intention to search for.
            mat_reg: Region of the material containing intentions that should be prioritized.
            any_reg: "common" (index 0) region on a coating.
            globals: Intentions found in the "CoatingGlobals" tag
            difference: Difference between the indices of the inputs between the zones on the shader.
            i: Index of the intention.
        """
        layer = self.get_intention(intention, mat_reg, any_reg, globals)
        properties = get_import_properties()
        extension_path = bpy.utils.extension_path_user(get_package_name(), create=True)
        info = self.material.get("style_info")
        if i == 0 and info and info["region_name"] == MP_VISOR and properties.toggle_visors:
            visors_path = Path(f"{extension_path}/all_visors.json")
            visors = read_json_file(visors_path, dict[str, CommonLayer])
            if visors is None:
                return
            layer = visors[properties.visors]
        if layer:
            swatch = cast(
                ShaderNodeTree, Layer(layer, f"{intention}_{hash(json.dumps(layer))}").node_tree
            )
            emissive = float(layer["emissive_amount"])
            self.create_swatch(swatch, layer["mid_color"], i, emissive, layer["disabled"])
        self.index += 14
