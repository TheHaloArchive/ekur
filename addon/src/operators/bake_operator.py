# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy

from typing import cast, final
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

from ..ui.bake_options import BakeOptionsType, get_bake_options
from ..utils import create_node

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


def get_width_height(material: Material) -> tuple[int, int]:
    if not material.node_tree:
        return (1, 1)
    group = material.node_tree.nodes.get("Group")
    if not group:
        return (1, 1)
    if not group.inputs[0].links:
        return (1, 1)
    tex = group.inputs[0].links[0].from_node
    if not tex:
        return (1, 1)
    tex = cast(ShaderNodeTexImage, tex)
    if tex.image:
        return (tex.image.size[1], tex.image.size[0])
    return (1, 1)


@final
class AlignBakeOperator(Operator):
    bl_idname = "ekur.alignbake"
    bl_label = "Align"

    def execute(self, context: Context | None) -> set[str]:
        selected_objects = bpy.context.selected_objects
        options = get_bake_options()
        if len(selected_objects) >= 1 and len(selected_objects[0].material_slots) >= 1:
            if selected_objects[0].active_material_index is None:
                return {"CANCELLED"}
            material_slot = selected_objects[0].material_slots[
                selected_objects[0].active_material_index
            ]
            if not material_slot.material or not material_slot.material.node_tree:
                return {"CANCELLED"}
            width, height = get_width_height(material_slot.material)
            options.width = width
            options.height = height
        return {"FINISHED"}


@final
class AdvancedBakeOperator(Operator):
    bl_idname = "ekur.toggleadvancedbake"
    bl_label = "Toggle"

    def execute(self, context: Context | None) -> set[str]:
        options = get_bake_options()
        datasource = bpy.context.selected_objects
        if options.selected_objects == "All" and bpy.context.scene:
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
                    if m == options.selected_layer:
                        _ = material.material.node_tree.links.new(
                            shader.outputs[idx], material_output.inputs[0]
                        )
        return {"FINISHED"}


@final
class BakingOperator(Operator):
    bl_idname = "ekur.baketextures"
    bl_label = "Bake"

    def bake_detail(self, object: Object, col: Collection) -> None:
        options = get_bake_options()
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
        if options.merge_textures:
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
            if options.merge_textures:
                mat_name = f"{object.name}_DetailNormal"
                tex_node = tex_nodes[idx]
            else:
                tex_node = create_node(material.node_tree.nodes, 0, 0, ShaderNodeTexImage)
            img = bpy.data.images.get(mat_name)
            height = options.height
            width = options.width
            if options.align_bakes:
                width, height = get_width_height(material)
            if img is None:
                img = bpy.data.images.new(mat_name, height, width)

            img.colorspace_settings.name = "Non-Color"  # pyright: ignore[reportAttributeAccessIssue, reportOptionalMemberAccess]
            material.node_tree.nodes.active = tex_node
            tex_node.image = img
            duplicate.select_set(True)  # pyright: ignore[reportUnknownMemberType]
            bpy.ops.object.bake(  # pyright: ignore[reportUnknownMemberType]
                type="NORMAL",
                save_mode="EXTERNAL",
                pass_filter={"NONE"},
                margin=options.pixel_padding,
            )
            img.save_render(f"{options.output_path}/{mat_name}.png")  # pyright: ignore[reportUnknownMemberType]
            duplicate.select_set(False)  # pyright: ignore[reportUnknownMemberType]

    def bake_material(
        self,
        material: Material,
        object: Object,
        options: BakeOptionsType,
        tex_node: ShaderNodeTexImage | None,
        override_mat: str = "",
    ) -> str | None:
        mat_name = ""
        if material.node_tree is None:
            return
        shader = material.node_tree.nodes.get("Group")
        mat_output = material.node_tree.nodes.get("Material Output")
        if not shader or not mat_output:
            return
        preset = PRESETS[options.output_workflow]

        if options.bake_ao:
            preset["AO"] = 7
        if options.bake_layer_map:
            preset["LayerMap"] = 11
        for m, idx in preset.items():
            if idx >= len(shader.outputs):
                return
            _ = material.node_tree.links.new(shader.outputs[idx], mat_output.inputs[0])
            mat_name = f"{material.name}_{m}"
            if override_mat != "":
                mat_name = f"{override_mat}_{m}"
            if not tex_node:
                tex_node = create_node(material.node_tree.nodes, 0, 0, ShaderNodeTexImage)
            material.node_tree.nodes.active = tex_node

            if options.merge_textures and not options.merge_objects:
                mat_name = f"{object.name}_{m}"
            img = bpy.data.images.get(mat_name)
            width = options.width
            height = options.height
            if options.align_bakes:
                width, height = get_width_height(material)
            if img is None:
                img = bpy.data.images.new(mat_name, height, width)
            tex_node.image = img
            object.select_set(True)  # pyright: ignore[reportUnknownMemberType]
            bpy.ops.object.bake(  # pyright: ignore[reportUnknownMemberType]
                type="EMIT",
                save_mode="EXTERNAL",
                use_clear=False,
                pass_filter={"EMIT"},
                margin=options.pixel_padding,
            )
            img.save_render(f"{options.output_path}/{mat_name}.png")  # pyright: ignore[reportUnknownMemberType]

        _ = material.node_tree.links.new(shader.outputs[0], mat_output.inputs[0])
        if shader.inputs[0].links:
            texture_node = shader.inputs[0].links[0].from_node
            if texture_node and type(texture_node) is ShaderNodeTexImage and texture_node.image:
                texture_node.image.reload()  # pyright: ignore[reportUnknownMemberType]

        if len(shader.inputs) > 3 and shader.inputs[3].links:
            texture_node = shader.inputs[3].links[0].from_node
            if (
                texture_node
                and type(texture_node) is ShaderNodeTexImage
                and texture_node.image
                and options.save_normals
            ):
                texture_node.image.save(  # pyright: ignore[reportUnknownMemberType]
                    filepath=f"{options.output_path}/{mat_name}_BaseNormal.png"
                )
        if options.merge_textures and options.merge_objects:
            return material.name

    def execute(self, context: Context | None) -> set[str]:
        if context is None or context.scene is None:
            return {"CANCELLED"}
        selected_objects = bpy.context.selected_objects
        options = get_bake_options()
        settings = context.scene.render.image_settings
        if options.bit_depth == "16":
            settings.color_depth = "16"
        else:
            settings.color_depth = "8"

        if options.bake_detail_normals and context.collection:
            duplicate_collection = bpy.data.collections.new("Duplicate")
            context.collection.children.link(duplicate_collection)  # pyright: ignore[reportUnknownMemberType]

        override_mat: str = ""

        for object in selected_objects:
            if type(object.data) is Mesh:
                object.data.uv_layers.active_index = int(options.uv_to_bake_to.split("UV")[-1])
                if options.bake_detail_normals:
                    self.bake_detail(object, duplicate_collection)  # pyright: ignore[reportPossiblyUnboundVariable]

            materials = [
                material.material for material in object.material_slots if material.material
            ]
            tex_nodes = []
            if options.merge_textures or options.merge_objects:
                tex_nodes = [
                    create_node(material.node_tree.nodes, 0, 0, ShaderNodeTexImage)
                    for material in materials
                    if material.node_tree
                ]

            i: int = 0
            for material in materials:
                if material.node_tree:
                    if options.merge_textures or options.merge_objects:
                        m = self.bake_material(
                            material, object, options, tex_nodes[i], override_mat
                        )
                        if options.merge_objects and m:
                            override_mat = m
                        material.node_tree.nodes.remove(tex_nodes[i])  # pyright: ignore[reportUnknownMemberType]
                        i += 1

                    else:
                        _ = self.bake_material(material, object, options, None)

        if options.bake_detail_normals:
            bpy.data.collections.remove(duplicate_collection)  # pyright: ignore[reportUnknownMemberType, reportPossiblyUnboundVariable]
        bpy.ops.outliner.orphans_purge()  # pyright: ignore[reportUnknownMemberType]
        return {"FINISHED"}
