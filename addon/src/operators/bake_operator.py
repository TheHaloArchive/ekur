# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import cast, final
import bpy
from bpy.types import (
    Collection,
    Context,
    Material,
    Mesh,
    NodeSocketColor,
    Object,
    Operator,
    ShaderNodeRGB,
    ShaderNodeTexImage,
)

from ..utils import ImportPropertiesType, create_node, get_import_properties

PRESETS = {
    "PBR MetRough": {"Color": 1, "Roughness": 3, "Metallic": 2, "Emission": 4},
    "PBR SpecGloss": {"SpecColor": 6, "Smoothness": 10, "Specular": 5, "Emission": 4},
    "PBR MetRoughSpecColor": {"Color": 1, "Roughness": 3, "Metallic": 2, "SpecColor": 6},
    "PBR ORM": {"Color": 1, "ORM": 12, "Emission": 4},
    "Unity Smoothness/Mask": {"Color": 1, "MaskMap": 9, "Smoothness": 10, "Emission": 4},
    "Color": {"Color": 1},
    "Metallic": {"Metallic": 2},
    "Roughness": {"Roughness": 3},
    "Emission": {"Emission": 4},
    "Specular": {"Specular": 5},
    "SpecColor": {"SpecColor": 6},
    "AO": {"AO": 7},
    "Normal": {"Normal": 8},
    "Unity Mask Map": {"Unity Mask Map": 9},
    "Smoothness": {"Smoothness": 10},
    "ID Mask": {"ID Mask": 11},
    "ORM": {"ORM": 12},
}

INDEXES = [
    "None",
    "Color",
    "Metallic",
    "Roughness",
    "Emission",
    "Specular",
    "SpecColor",
    "AO",
    "Normal",
    "Unity Mask Map",
    "Smoothness",
    "ID Mask",
    "ORM",
]


@final
class AlignBakeOperator(Operator):
    bl_idname = "ekur.alignbake"
    bl_label = "Align"

    def execute(self, context: Context | None) -> set[str]:
        selected_objects = bpy.context.selected_objects
        props = get_import_properties()
        if len(selected_objects) >= 1 and len(selected_objects[0].material_slots) >= 1:
            if selected_objects[0].active_material_index is None:
                return {"CANCELLED"}
            material_slot = selected_objects[0].material_slots[
                selected_objects[0].active_material_index
            ]
            if not material_slot.material or not material_slot.material.node_tree:
                return {"CANCELLED"}
            group = material_slot.material.node_tree.nodes.get("Group")
            if not group:
                return {"CANCELLED"}
            if not group.inputs[0].links:
                return {"CANCELLED"}
            tex = group.inputs[0].links[0].from_node
            if not tex:
                return {"CANCELLED"}
            tex = cast(ShaderNodeTexImage, tex)
            if tex.image:
                props.height = tex.image.size[0]
                props.width = tex.image.size[1]

        return {"FINISHED"}


@final
class AdvancedBakeOperator(Operator):
    bl_idname = "ekur.toggleadvancedbake"
    bl_label = "Toggle"

    def execute(self, context: Context | None) -> set[str]:
        props = get_import_properties()
        datasource = bpy.context.selected_objects
        if props.selected_objects == "All" and bpy.context.scene:
            datasource = bpy.data.objects
        for object in datasource:
            if object.type != "MESH" or not object.material_slots:
                continue
            for material in object.material_slots:
                if not material.material or not material.material.node_tree:
                    continue
                shader = material.material.node_tree.nodes.get("Group")
                material_output = material.material.node_tree.nodes.get("Material Output")
                if not shader or not material_output or not len(shader.outputs) > 12:
                    continue
                for idx, m in enumerate(INDEXES):
                    if m == props.selected_layer:
                        _ = material.material.node_tree.links.new(
                            shader.outputs[idx], material_output.inputs[0]
                        )
        return {"FINISHED"}


@final
class BakingOperator(Operator):
    bl_idname = "ekur.baketextures"
    bl_label = "Bake"

    def bake_detail(self, object: Object, col: Collection) -> None:
        props = get_import_properties()
        duplicate = object.copy()
        if not object.data or not bpy.context.collection:
            return
        duplicate.data = object.data.copy()
        col.objects.link(duplicate)  # pyright: ignore[reportUnknownMemberType]
        object.select_set(False)  # pyright: ignore[reportUnknownMemberType]
        duplicate.select_set(True)  # pyright: ignore[reportUnknownMemberType]
        if bpy.context.view_layer:
            bpy.context.view_layer.objects.active = duplicate
        bpy.ops.mesh.customdata_custom_splitnormals_clear()  # pyright: ignore[reportUnknownMemberType]
        bpy.ops.object.shade_flat()  # pyright: ignore[reportUnknownMemberType]
        for mat in duplicate.material_slots:
            if mat.material:
                mat.material = mat.material.copy()
        dup_materials = [
            material.material for material in duplicate.material_slots if material.material
        ]
        tex_nodes = []
        if props.merge_textures:
            tex_nodes = [
                create_node(material.node_tree.nodes, 0, 0, ShaderNodeTexImage)
                for material in dup_materials
                if material.node_tree
            ]

        for idx, material in enumerate(dup_materials):
            if not material.node_tree:
                continue
            shader = material.node_tree.nodes.get("Group")
            if shader and shader.inputs[3].links:
                rgb_value = create_node(material.node_tree.nodes, 0, 0, ShaderNodeRGB)
                val = (0.5, 0.5, 1.0, 1.0)
                cast(NodeSocketColor, rgb_value.outputs[0]).default_value = val
                _ = material.node_tree.links.new(rgb_value.outputs[0], shader.inputs[3])
            mat_name = f"{material.name}_DetailNormal"
            if props.merge_textures:
                mat_name = f"{object.name}_DetailNormal"
                tex_node = tex_nodes[idx]
            else:
                tex_node = create_node(material.node_tree.nodes, 0, 0, ShaderNodeTexImage)
            img = bpy.data.images.get(mat_name)
            if img is None:
                img = bpy.data.images.new(mat_name, props.height, props.width)

            img.colorspace_settings.name = "Non-Color"  # pyright: ignore[reportAttributeAccessIssue, reportOptionalMemberAccess]
            material.node_tree.nodes.active = tex_node
            tex_node.image = img
            duplicate.select_set(True)  # pyright: ignore[reportUnknownMemberType]
            bpy.ops.object.bake(  # pyright: ignore[reportUnknownMemberType]
                type="NORMAL",
                save_mode="EXTERNAL",
                pass_filter={"NONE"},
                margin=props.pixel_padding,
            )
            img.save_render(f"{props.output_path}/{mat_name}.png")  # pyright: ignore[reportUnknownMemberType]
            duplicate.select_set(False)  # pyright: ignore[reportUnknownMemberType]

    def bake_material(
        self,
        material: Material,
        object: Object,
        props: ImportPropertiesType,
        tex_node: ShaderNodeTexImage | None,
    ) -> None:
        if material.node_tree is None:
            return
        shader = material.node_tree.nodes.get("Group")
        mat_output = material.node_tree.nodes.get("Material Output")
        if not shader or not mat_output:
            return
        preset = PRESETS[props.output_workflow]
        if props.bake_ao:
            preset["AO"] = 7
        if props.bake_layer_map:
            preset["LayerMap"] = 11
        for m, idx in preset.items():
            _ = material.node_tree.links.new(shader.outputs[idx], mat_output.inputs[0])
            mat_name = f"{material.name}_{m}"
            if not tex_node:
                tex_node = create_node(material.node_tree.nodes, 0, 0, ShaderNodeTexImage)
            material.node_tree.nodes.active = tex_node
            if props.merge_textures:
                mat_name = f"{object.name}_{m}"
            img = bpy.data.images.get(mat_name)
            if img is None:
                img = bpy.data.images.new(mat_name, props.height, props.width)
            tex_node.image = img
            object.select_set(True)  # pyright: ignore[reportUnknownMemberType]
            bpy.ops.object.bake(  # pyright: ignore[reportUnknownMemberType]
                type="EMIT",
                save_mode="EXTERNAL",
                use_clear=False,
                pass_filter={"EMIT"},
                margin=props.pixel_padding,
            )
            img.save_render(f"{props.output_path}/{mat_name}.png")  # pyright: ignore[reportUnknownMemberType]

        _ = material.node_tree.links.new(shader.outputs[0], mat_output.inputs[0])
        if shader.inputs[3].links:
            texture_node = shader.inputs[3].links[0].from_node
            if texture_node and type(texture_node) is ShaderNodeTexImage and texture_node.image:
                texture_node.image.save(  # pyright: ignore[reportUnknownMemberType]
                    filepath=f"{props.output_path}/{material.name}_BaseNormal.png"
                )

    def execute(self, context: Context | None) -> set[str]:
        if context is None or context.scene is None:
            return {"CANCELLED"}
        selected_objects = bpy.context.selected_objects
        props = get_import_properties()
        settings = context.scene.render.image_settings
        if props.bit_depth == "16":
            settings.color_depth = "16"
        else:
            settings.color_depth = "8"

        if props.bake_detail_normals and context.collection:
            duplicate_collection = bpy.data.collections.new("Duplicate")
            context.collection.children.link(duplicate_collection)  # pyright: ignore[reportUnknownMemberType]

        for object in selected_objects:
            if type(object.data) is Mesh:
                object.data.uv_layers.active_index = int(props.uv_to_bake_to.split("UV")[-1])
            if props.bake_detail_normals:
                self.bake_detail(object, duplicate_collection)  # pyright: ignore[reportPossiblyUnboundVariable]

            materials = [
                material.material for material in object.material_slots if material.material
            ]
            tex_nodes = []
            if props.merge_textures:
                tex_nodes = [
                    create_node(material.node_tree.nodes, 0, 0, ShaderNodeTexImage)
                    for material in materials
                    if material.node_tree
                ]

            i: int = 0
            for material in materials:
                if material.node_tree:
                    for node in material.node_tree.nodes:
                        node.select = False
                    if props.merge_textures:
                        self.bake_material(material, object, props, tex_nodes[i])
                        material.node_tree.nodes.remove(tex_nodes[i])  # pyright: ignore[reportUnknownMemberType]
                        i += 1
                    else:
                        self.bake_material(material, object, props, None)

        if props.bake_detail_normals:
            bpy.data.collections.remove(duplicate_collection)  # pyright: ignore[reportUnknownMemberType, reportPossiblyUnboundVariable]
        bpy.ops.outliner.orphans_purge()  # pyright: ignore[reportUnknownMemberType]
        return {"FINISHED"}
