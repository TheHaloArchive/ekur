# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from pathlib import Path
from typing import cast, final

import bpy
from bpy.types import (
    Context,
    Material,
    Mesh,
    Node,
    Object,
    Operator,
    ShaderNodeGroup,
    ShaderNodeTree,
)

from ..nodes.layer import Layer
from .material_operator import import_materials
from ..json_definitions import CommonMaterial, ForgeMaterial, ForgeObjectDefinition
from ..utils import (
    assign_value,
    create_node,
    get_data_folder,
    get_import_properties,
    read_json_file,
)
from ..model.importer.model_importer import ModelImporter

__all__ = ["ForgeOperator"]


@final
class ForgeOperator(Operator):
    bl_idname = "ekur.importforge"
    bl_label = "Import"
    bl_options = {"REGISTER", "UNDO"}

    def __init__(self, *args, **kwargs) -> None:  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        super().__init__(*args, **kwargs)
        self.index: int = 0

    def import_layer(
        self,
        material: CommonMaterial,
        shader: ShaderNodeGroup,
        swatch: Node,
        mat: Material,
        emissive: float,
        is_grime: bool,
    ) -> None:
        if material["style_info"]:
            assign_value(swatch, 0, material["style_info"]["texel_density"][0])
            assign_value(swatch, 1, material["style_info"]["texel_density"][1])
            assign_value(swatch, 6, material["style_info"]["material_offset"][0])
            assign_value(swatch, 7, material["style_info"]["material_offset"][1])
        if not mat.node_tree:
            return
        _ = mat.node_tree.links.new(swatch.outputs[0], shader.inputs[14 + self.index])
        _ = mat.node_tree.links.new(swatch.outputs[1], shader.inputs[15 + self.index])
        _ = mat.node_tree.links.new(swatch.outputs[2], shader.inputs[16 + self.index])
        if is_grime:
            _ = mat.node_tree.links.new(swatch.outputs[5], shader.inputs[17 + self.index])
            _ = mat.node_tree.links.new(swatch.outputs[6], shader.inputs[20 + self.index])
            _ = mat.node_tree.links.new(swatch.outputs[7], shader.inputs[21 + self.index])
            _ = mat.node_tree.links.new(swatch.outputs[8], shader.inputs[22 + self.index])
        else:
            assign_value(shader, 22 + self.index, emissive)
            _ = mat.node_tree.links.new(swatch.outputs[3], shader.inputs[18 + self.index])
            _ = mat.node_tree.links.new(swatch.outputs[4], shader.inputs[19 + self.index])
            _ = mat.node_tree.links.new(swatch.outputs[5], shader.inputs[20 + self.index])
            _ = mat.node_tree.links.new(swatch.outputs[6], shader.inputs[23 + self.index])
            _ = mat.node_tree.links.new(swatch.outputs[7], shader.inputs[24 + self.index])
            _ = mat.node_tree.links.new(swatch.outputs[8], shader.inputs[25 + self.index])
            _ = mat.node_tree.links.new(swatch.outputs[9], shader.inputs[26 + self.index])

    def import_materials(self, object: Object) -> None:
        props = get_import_properties()
        materials = [mat.material for mat in object.material_slots if mat.material]
        data = get_data_folder()
        globals_path = Path(f"{data}/forge_materials.json")
        globals = read_json_file(globals_path, ForgeMaterial)
        if not globals:
            return
        for mat in materials:
            name = mat.name
            if len(mat.name.split(".")) > 1:
                name = mat.name.split(".")[0]

            definition_path = Path(f"{data}/materials/{name}.json")
            material = read_json_file(definition_path, CommonMaterial)
            if material is None:
                return

            if not mat.node_tree:
                continue
            shader = mat.node_tree.nodes.get("Group")
            if not shader:
                continue
            shader = cast(ShaderNodeGroup, shader)
            if not shader.node_tree:
                continue
            if shader.node_tree.name != "Halo Infinite Shader 3.1.2 by Chunch and ChromaCore":
                continue
            layers = [props.layer1, props.layer2, props.layer3, props.grime]
            assign_value(shader, 7, props.grime_amount)
            assign_value(shader, 17, props.scratch_amount)
            for idx, lay in enumerate(layers):
                if idx == 3:
                    self.index = 97
                l1 = [layer for layer in globals["layers"].items() if layer[0] == lay][0]
                layer = Layer(l1[1]["layer"], l1[0])
                swatch = create_node(mat.node_tree.nodes, 0, 0, ShaderNodeGroup)
                swatch.node_tree = cast(ShaderNodeTree, layer.node_tree)
                is_grime = idx == 3
                self.import_layer(
                    material, shader, swatch, mat, l1[1]["layer"]["emissive_amount"], is_grime
                )
                self.index += 14

    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}
        properties = get_import_properties()
        selected_model = properties.objects

        represnt = properties.object_representation
        data = get_data_folder()

        objects_path = Path(f"{data}/forge_objects.json")
        definition = read_json_file(objects_path, ForgeObjectDefinition)
        if definition is None:
            return {"CANCELLED"}
        if context.scene is None:
            return {"CANCELLED"}

        for category in definition["root_categories"]:
            if category["sub_categories"] is None:
                continue
            for subcategory in category["sub_categories"]:
                if subcategory["objects"] is None:
                    continue
                for obj in subcategory["objects"]:
                    if not obj["name"] == selected_model:
                        continue
                    for representation in obj["representations"]:
                        if not representation["name"] == represnt:
                            continue
                        model_path = Path(f"{data}/models/{representation['model']}.ekur")
                        objects = ModelImporter().start_import(str(model_path), bones=False)
                        collection = bpy.data.collections.new(obj["name"])
                        count = 0
                        for bl_obj in objects:
                            if type(bl_obj.data) is Mesh and "UV1" in bl_obj.data.uv_layers:
                                bl_obj.data.uv_layers["UV1"].active_render = True
                                bl_obj.data.uv_layers["UV1"].active = True
                            if str(representation["name_int"]) == str(
                                bl_obj["permutation_name"]  # pyright: ignore[reportAny]
                            ):
                                count += 1
                                collection.objects.link(bl_obj)  # pyright: ignore[reportUnknownMemberType]
                        if count == 0:
                            for bl_obj in objects:
                                if (
                                    bl_obj["permutation_name"] == 528041935
                                    or bl_obj["region_name"] == 528041935
                                ):
                                    count += 1
                                    collection.objects.link(bl_obj)  # pyright: ignore[reportUnknownMemberType]
                        if count == 0:
                            for bl_obj in objects:
                                collection.objects.link(bl_obj)  # pyright: ignore[reportUnknownMemberType]
                        context.scene.collection.children.link(collection)  # pyright: ignore[reportUnknownMemberType]
                        for object in collection.objects:
                            object.select_set(True)  # pyright: ignore[reportUnknownMemberType]
                            if context.view_layer:
                                context.view_layer.objects.active = object
                            properties.use_default = False
                            properties.coat_id = str(obj["id"])
                            import_materials()
                            if properties.override_materials:
                                self.import_materials(object)
                        break

        return {"FINISHED"}
