# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from collections.abc import Iterator
from contextlib import contextmanager
from math import floor
from typing import cast, final

import bpy
from bpy.types import (
    Collection,
    Context,
    Image,
    Material,
    Mesh,
    Object,
    Operator,
    Scene,
    ShaderNodeEmission,
    ShaderNodeRGB,
    ShaderNodeTexImage,
    ShaderNodeUVMap,
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

NEUTRAL_NORMAL = (0.5, 0.5, 1.0, 1.0)
CLEARED_NORMAL = (0.5, 0.5, 1.0, 0.0)

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


@contextmanager
def standard_color_management(scene: Scene) -> Iterator[None]:
    display_settings = scene.display_settings
    view_settings = scene.view_settings
    if not display_settings or not view_settings:
        yield
        return
    previous_display = display_settings.display_device
    previous_view_transform = view_settings.view_transform
    previous_view_look = view_settings.look

    display_settings.display_device = "sRGB"  # ty: ignore[invalid-assignment]
    view_settings.view_transform = "Standard"  # ty: ignore[invalid-assignment]
    view_settings.look = "None"  # ty: ignore[invalid-assignment]
    try:
        yield
    finally:
        display_settings.display_device = previous_display
        view_settings.view_transform = previous_view_transform
        view_settings.look = previous_view_look


def get_preset(options: BakeOptionsType) -> dict[str, int]:
    preset = dict(PRESETS[options.output_workflow])
    if options.bake_ao:
        preset["AO"] = 7
    if options.bake_layer_map:
        preset["LayerMap"] = 11
    return preset


def bake_selected(options: BakeOptionsType, bake_type: str = "EMIT") -> None:
    bpy.ops.object.bake(
        type=bake_type,  # ty: ignore[invalid-argument-type]
        save_mode="EXTERNAL",
        use_clear=bake_type == "NORMAL",
        pass_filter={"EMIT"} if bake_type == "EMIT" else {"NONE"},
        margin=options.pixel_padding,
    )


def tile_coordinates(tile_number: int) -> tuple[int, int]:
    index = tile_number - 1001
    return (index % 10, index // 10)


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


def get_bake_image(name: str, material: Material, options: BakeOptionsType) -> Image:
    """Get the image to bake into, creating it when it does not exist yet."""
    image = bpy.data.images.get(name)
    if image is None:
        width = options.width
        height = options.height
        if options.align_bakes:
            width, height = get_width_height(material)
        image = bpy.data.images.new(name, height, width)
    return image


def get_base_normal(material: Material) -> ShaderNodeTexImage | None:
    if not material.node_tree:
        return None
    shader = material.node_tree.nodes.get("Group")
    if not shader or len(shader.inputs) <= 3 or not shader.inputs[3].links:
        return None
    texture_node = shader.inputs[3].links[0].from_node
    if type(texture_node) is not ShaderNodeTexImage or not texture_node.image:
        return None
    return texture_node


@final
class AlignBakeOperator(Operator):
    bl_idname = "ekur.alignbake"
    bl_description = "Align"
    bl_label = "Align"

    def execute(self, context: Context | None) -> set[str]:  # ty:ignore[invalid-method-override]
        selected_objects = bpy.context.selected_objects
        options = get_bake_options()
        if (
            selected_objects
            and len(selected_objects) >= 1
            and len(selected_objects[0].material_slots) >= 1
        ):
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
    bl_description = "Toggle Advanced Bake"
    bl_label = "Toggle"

    def execute(self, context: Context | None) -> set[str]:  # ty:ignore[invalid-method-override]
        options = get_bake_options()
        datasource = bpy.context.selected_objects
        if options.selected_objects == "All" and bpy.context.scene:
            datasource = bpy.data.objects
        if not datasource:
            return {""}
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
    bl_description = "Bake"
    bl_label = "Bake"

    def bake_detail(self, object: Object, col: Collection) -> None:
        options = get_bake_options()
        duplicate = object.copy()
        if not object.data or not bpy.context.collection:
            return
        duplicate.data = object.data.copy()
        col.objects.link(duplicate)
        for selected in bpy.context.selected_objects or []:
            selected.select_set(False)
        duplicate.select_set(True)
        scene = bpy.context.scene
        if bpy.context.view_layer:
            bpy.context.view_layer.objects.active = duplicate
        if not scene:
            return
        with standard_color_management(scene):
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            bpy.ops.object.shade_flat()
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
                self.flatten_base_normal(material)
                mat_name = f"{material.name}_DetailNormal"
                if options.merge_textures:
                    mat_name = f"{object.name}_DetailNormal"
                    tex_node = tex_nodes[idx]
                else:
                    tex_node = create_node(material.node_tree.nodes, 0, 0, ShaderNodeTexImage)
                img = get_bake_image(mat_name, material, options)

                img.colorspace_settings.name = "Non-Color"  # ty: ignore[invalid-assignment]
                material.node_tree.nodes.active = tex_node
                tex_node.image = img
                duplicate.select_set(True)
                bake_selected(options, "NORMAL")
                img.save_render(f"{options.output_path}/{mat_name}.png")
                duplicate.select_set(False)

    def flatten_base_normal(self, material: Material) -> None:
        if not material.node_tree:
            return
        shader = material.node_tree.nodes.get("Group")
        if not shader or not shader.inputs[3].links:
            return
        rgb_value = create_node(material.node_tree.nodes, 0, 0, ShaderNodeRGB)
        if rgb_value.outputs:
            rgb_value.outputs[0].default_value = NEUTRAL_NORMAL
            _ = material.node_tree.links.new(rgb_value.outputs[0], shader.inputs[3])

    def bake_material(
        self,
        context: Context,
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
        scene = context.scene
        if not shader or not mat_output or not scene:
            return
        with standard_color_management(scene):
            for m, idx in get_preset(options).items():
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
                img = get_bake_image(mat_name, material, options)
                tex_node.image = img
                object.select_set(True)
                bake_selected(options)
                img.save_render(f"{options.output_path}/{mat_name}.png")

            _ = material.node_tree.links.new(shader.outputs[0], mat_output.inputs[0])
            if shader.inputs[0].links:
                texture_node = shader.inputs[0].links[0].from_node
                if texture_node and type(texture_node) is ShaderNodeTexImage and texture_node.image:
                    texture_node.image.reload()

            base_normal = get_base_normal(material)
            if base_normal and base_normal.image and options.save_normals:
                base_normal.image.save(filepath=f"{options.output_path}/{mat_name}_BaseNormal.png")
            if options.merge_textures and options.merge_objects:
                return material.name

    def center_uvs(self, mesh: Mesh, uv_index: int) -> None:
        uvs = mesh.uv_layers[uv_index].data
        buffer = self.get_uvs(mesh, uv_index)
        if not buffer:
            return
        faces = len(mesh.polygons)
        material_indices = [0] * faces
        loop_starts = [0] * faces
        loop_totals = [0] * faces
        mesh.polygons.foreach_get("material_index", material_indices)
        mesh.polygons.foreach_get("loop_start", loop_starts)
        mesh.polygons.foreach_get("loop_total", loop_totals)

        loops_per_material: dict[int, list[int]] = {}
        for face in range(faces):
            loops = loops_per_material.setdefault(material_indices[face], [])
            loops.extend(range(loop_starts[face], loop_starts[face] + loop_totals[face]))

        for loops in loops_per_material.values():
            offset_u = -floor(min(buffer[loop * 2] for loop in loops))
            offset_v = -floor(min(buffer[loop * 2 + 1] for loop in loops))
            if offset_u == 0 and offset_v == 0:
                continue
            for loop in loops:
                buffer[loop * 2] += offset_u
                buffer[loop * 2 + 1] += offset_v
        uvs.foreach_set("uv", buffer)

    def prepare_center_uvs(
        self, object: Object, mesh: Mesh, uv_index: int
    ) -> tuple[int, int, list[tuple[Material, ShaderNodeUVMap]]]:
        original_layer = mesh.uv_layers[uv_index]
        original_name = original_layer.name
        original_render_index = next(
            (i for i, layer in enumerate(mesh.uv_layers) if layer.active_render), uv_index
        )
        buffer = self.get_uvs(mesh, uv_index)
        new_layer = mesh.uv_layers.new(name=f"{original_name}_Baked")
        new_layer.data.foreach_set("uv", buffer)
        new_index = len(mesh.uv_layers) - 1

        added_nodes: list[tuple[Material, ShaderNodeUVMap]] = []
        materials = {slot.material for slot in object.material_slots if slot.material}
        for material in materials:
            node_tree = material.node_tree
            if not node_tree:
                continue
            for node in list(node_tree.nodes):
                if type(node) is ShaderNodeTexImage:
                    if node.inputs[0].links:  # ty: ignore[not-subscriptable]
                        continue
                    uv_node = create_node(
                        node_tree.nodes,
                        node.location[0] - 200,
                        node.location[1],
                        ShaderNodeUVMap,
                    )
                    uv_node.uv_map = original_name
                    uv_output = uv_node.outputs[0]  # ty: ignore[not-subscriptable]
                    node_input = node.inputs[0]  # ty: ignore[not-subscriptable]
                    node_tree.links.new(uv_output, node_input)
                    added_nodes.append((material, uv_node))

        self.center_uvs(mesh, new_index)
        mesh.uv_layers.active_index = new_index
        for layer in mesh.uv_layers:
            layer.active_render = layer.name == new_layer.name
        return new_index, original_render_index, added_nodes

    def cleanup_center_uvs(
        self,
        mesh: Mesh,
        new_index: int,
        original_render_index: int,
        added_nodes: list[tuple[Material, ShaderNodeUVMap]],
    ) -> None:
        for material, node in added_nodes:
            if material.node_tree:
                material.node_tree.nodes.remove(node)
        mesh.uv_layers.remove(mesh.uv_layers[new_index])
        if original_render_index < len(mesh.uv_layers):
            mesh.uv_layers.active_index = original_render_index
            mesh.uv_layers[original_render_index].active_render = True

    def get_uv_index(self, mesh: Mesh, options: BakeOptionsType) -> int:
        index = int(options.uv_to_bake_to.split("UV")[-1])
        if index >= len(mesh.uv_layers):
            return len(mesh.uv_layers) - 1
        return index

    def get_uvs(self, mesh: Mesh, uv_index: int) -> list[float]:
        uvs = mesh.uv_layers[uv_index].data
        buffer = [0.0] * (len(uvs) * 2)
        uvs.foreach_get("uv", buffer)
        return buffer

    def get_occupied_tiles(self, mesh: Mesh, uv_index: int) -> set[int]:
        buffer = self.get_uvs(mesh, uv_index)
        tiles: set[int] = set()
        for i in range(0, len(buffer), 2):
            u = floor(buffer[i])
            v = floor(buffer[i + 1])
            if u < 0 or v < 0 or u > 9:
                continue
            tile_number = 1001 + u + v * 10
            if tile_number <= 2000:
                tiles.add(tile_number)
        return tiles

    def create_udim_image(
        self,
        name: str,
        tiles: set[int],
        options: BakeOptionsType,
        fill: tuple[float, float, float, float] | None = None,
    ) -> Image:
        image = bpy.data.images.get(name)
        if image and image.source != "TILED":
            bpy.data.images.remove(image)
            image = None
        if image is None:
            image = bpy.data.images.new(
                name, width=options.width, height=options.height, alpha=True, tiled=True
            )
        base_tile = image.tiles[0]
        if base_tile.number not in tiles and not image.tiles.get(min(tiles)):
            base_tile.number = min(tiles)
        for tile_number in sorted(tiles):
            if image.tiles.get(tile_number):
                continue
            with bpy.context.temp_override(edit_image=image):  # ty: ignore[invalid-context-manager]
                _ = bpy.ops.image.tile_add(
                    number=tile_number,
                    count=1,
                    fill=True,
                    width=options.width,
                    height=options.height,
                    alpha=True,
                )
        for tile in [tile for tile in image.tiles if tile.number not in tiles]:
            image.tiles.remove(tile)
        if fill:
            for index in range(len(image.tiles)):
                image.tiles.active_index = index
                with bpy.context.temp_override(edit_image=image):  # ty: ignore[invalid-context-manager]
                    _ = bpy.ops.image.tile_fill(
                        color=fill, width=options.width, height=options.height, alpha=True
                    )
        return image

    def get_material_tiles(self, options: BakeOptionsType, objects: list[Object]) -> dict[str, int]:
        material_tiles: dict[str, int] = {}
        for object in objects:
            for slot in object.material_slots:
                if not slot.material or slot.material.name in material_tiles:
                    continue
                tile_number = options.udim_first_tile + len(material_tiles)
                if tile_number > 2000:
                    continue
                material_tiles[slot.material.name] = tile_number
        return material_tiles

    def move_uvs_to_tiles(
        self, object: Object, mesh: Mesh, uv_index: int, material_tiles: dict[str, int]
    ) -> set[int]:
        uvs = mesh.uv_layers[uv_index].data
        buffer = self.get_uvs(mesh, uv_index)
        if not buffer:
            return set()
        faces = len(mesh.polygons)
        material_indices = [0] * faces
        loop_starts = [0] * faces
        loop_totals = [0] * faces
        mesh.polygons.foreach_get("material_index", material_indices)
        mesh.polygons.foreach_get("loop_start", loop_starts)
        mesh.polygons.foreach_get("loop_total", loop_totals)

        loops_per_tile: dict[int, list[int]] = {}
        for face in range(faces):
            slot_index = material_indices[face]
            if slot_index >= len(object.material_slots):
                continue
            material = object.material_slots[slot_index].material
            if not material or material.name not in material_tiles:
                continue
            loops = loops_per_tile.setdefault(material_tiles[material.name], [])
            loops.extend(range(loop_starts[face], loop_starts[face] + loop_totals[face]))

        for tile_number, loops in loops_per_tile.items():
            target_u, target_v = tile_coordinates(tile_number)
            offset_u = target_u - floor(min(buffer[loop * 2] for loop in loops))
            offset_v = target_v - floor(min(buffer[loop * 2 + 1] for loop in loops))
            if offset_u == 0 and offset_v == 0:
                continue
            for loop in loops:
                buffer[loop * 2] += offset_u
                buffer[loop * 2 + 1] += offset_v
        uvs.foreach_set("uv", buffer)
        return set(loops_per_tile)

    def layout_udim_uvs(
        self, options: BakeOptionsType, objects: list[Object]
    ) -> tuple[list[Object], set[int]]:
        material_tiles = (
            self.get_material_tiles(options, objects) if options.udim_layout_uvs else {}
        )
        laid_out: list[Object] = []
        tiles: set[int] = set()
        laid_out_meshes: dict[str, set[int]] = {}
        for object in objects:
            mesh = cast(Mesh, object.data)
            uv_index = self.get_uv_index(mesh, options)
            if uv_index < 0:
                continue
            mesh.uv_layers.active_index = uv_index
            if not options.udim_layout_uvs:
                tiles |= self.get_occupied_tiles(mesh, uv_index)
            elif mesh.name in laid_out_meshes:
                tiles |= laid_out_meshes[mesh.name]
            else:
                laid_out_meshes[mesh.name] = self.move_uvs_to_tiles(
                    object, mesh, uv_index, material_tiles
                )
                tiles |= laid_out_meshes[mesh.name]
            laid_out.append(object)
        return (laid_out, tiles)

    def get_udim_materials(self, objects: list[Object]) -> list[Material]:
        materials: list[Material] = []
        for object in objects:
            for slot in object.material_slots:
                if slot.material and slot.material.node_tree and slot.material not in materials:
                    materials.append(slot.material)
        return materials

    def bake_udim_image(
        self,
        name: str,
        materials: list[Material],
        tex_nodes: dict[str, ShaderNodeTexImage],
        tiles: set[int],
        options: BakeOptionsType,
        bake_type: str = "EMIT",
        normal_map: bool = False,
    ) -> None:
        fill = None
        if normal_map:
            fill = CLEARED_NORMAL if bake_type == "NORMAL" else NEUTRAL_NORMAL
        image = self.create_udim_image(name, tiles, options, fill=fill)
        if normal_map:
            image.colorspace_settings.name = "Non-Color"  # ty: ignore[invalid-assignment]
        for material in materials:
            if not material.node_tree:
                continue
            tex_node = tex_nodes[material.name]
            tex_node.image = image
            material.node_tree.nodes.active = tex_node
        bake_selected(options, bake_type)
        image.save_render(f"{options.output_path}/{name}.<UDIM>.png")

    def bake_udim_base_normals(
        self,
        base_name: str,
        materials: list[Material],
        tex_nodes: dict[str, ShaderNodeTexImage],
        tiles: set[int],
        options: BakeOptionsType,
    ) -> None:
        if not any(get_base_normal(material) for material in materials):
            return
        emissions: list[tuple[Material, ShaderNodeEmission]] = []
        for material in materials:
            if not material.node_tree:
                continue
            mat_output = material.node_tree.nodes.get("Material Output")
            if not mat_output:
                continue
            emission = create_node(material.node_tree.nodes, 0, 0, ShaderNodeEmission)
            if not emission.inputs or not emission.outputs:
                continue
            base_normal = get_base_normal(material)
            if base_normal and base_normal.outputs:
                _ = material.node_tree.links.new(base_normal.outputs[0], emission.inputs[0])
            else:
                emission.inputs[0].default_value = NEUTRAL_NORMAL
            _ = material.node_tree.links.new(emission.outputs[0], mat_output.inputs[0])
            emissions.append((material, emission))

        self.bake_udim_image(
            f"{base_name}_BaseNormal", materials, tex_nodes, tiles, options, normal_map=True
        )
        for material, emission in emissions:
            if material.node_tree:
                material.node_tree.nodes.remove(emission)

    def bake_udim_detail_normals(
        self,
        context: Context,
        base_name: str,
        objects: list[Object],
        tiles: set[int],
        options: BakeOptionsType,
    ) -> None:
        if context.collection is None or context.view_layer is None:
            return
        collection = bpy.data.collections.new("UDIMDetailNormals")
        context.collection.children.link(collection)
        duplicates: list[Object] = []
        for object in objects:
            object.select_set(False)
            if object.data is None:
                continue
            duplicate = object.copy()
            duplicate.data = object.data.copy()
            collection.objects.link(duplicate)
            duplicate.select_set(True)
            duplicates.append(duplicate)
        if not duplicates:
            bpy.data.collections.remove(collection)
            return
        for duplicate in duplicates:
            context.view_layer.objects.active = duplicate
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        context.view_layer.objects.active = duplicates[0]
        bpy.ops.object.shade_flat()

        for duplicate in duplicates:
            for slot in duplicate.material_slots:
                if slot.material:
                    slot.material = slot.material.copy()
        materials = self.get_udim_materials(duplicates)
        for material in materials:
            self.flatten_base_normal(material)
        tex_nodes = self.create_udim_tex_nodes(materials)
        self.bake_udim_image(
            f"{base_name}_DetailNormal",
            materials,
            tex_nodes,
            tiles,
            options,
            bake_type="NORMAL",
            normal_map=True,
        )
        bpy.data.collections.remove(collection)

    def create_udim_tex_nodes(self, materials: list[Material]) -> dict[str, ShaderNodeTexImage]:
        return {
            material.name: create_node(material.node_tree.nodes, 0, 0, ShaderNodeTexImage)
            for material in materials
            if material.node_tree
        }

    def bake_udim_tiles(self, context: Context, options: BakeOptionsType) -> set[str]:
        scene = context.scene
        if scene is None or context.view_layer is None:
            return {"CANCELLED"}
        objects = [
            object
            for object in bpy.context.selected_objects or []
            if type(object.data) is Mesh and object.material_slots
        ]
        if not objects:
            return {"CANCELLED"}

        base_name = options.udim_name if options.udim_name else objects[0].name
        objects, tiles = self.layout_udim_uvs(options, objects)
        if not objects or not tiles:
            return {"CANCELLED"}

        for object in objects:
            object.select_set(True)
        context.view_layer.objects.active = objects[0]
        materials = self.get_udim_materials(objects)
        tex_nodes = self.create_udim_tex_nodes(materials)

        with standard_color_management(scene):
            for m, idx in get_preset(options).items():
                for material in materials:
                    if not material.node_tree:
                        continue
                    shader = material.node_tree.nodes.get("Group")
                    mat_output = material.node_tree.nodes.get("Material Output")
                    if not shader or not mat_output or idx >= len(shader.outputs):
                        continue
                    _ = material.node_tree.links.new(shader.outputs[idx], mat_output.inputs[0])
                self.bake_udim_image(f"{base_name}_{m}", materials, tex_nodes, tiles, options)

            if options.save_normals:
                self.bake_udim_base_normals(base_name, materials, tex_nodes, tiles, options)

            for material in materials:
                if not material.node_tree:
                    continue
                shader = material.node_tree.nodes.get("Group")
                mat_output = material.node_tree.nodes.get("Material Output")
                if shader and mat_output:
                    _ = material.node_tree.links.new(shader.outputs[0], mat_output.inputs[0])
                material.node_tree.nodes.remove(tex_nodes[material.name])

            if options.bake_detail_normals:
                self.bake_udim_detail_normals(context, base_name, objects, tiles, options)

        for object in objects:
            object.select_set(True)
        context.view_layer.objects.active = objects[0]
        return {"FINISHED"}

    def execute(self, context: Context | None) -> set[str]:  # ty:ignore[invalid-method-override]
        if context is None or context.scene is None:
            return {"CANCELLED"}
        selected_objects = bpy.context.selected_objects
        options = get_bake_options()
        settings = context.scene.render.image_settings
        if options.bit_depth == "16":
            settings.color_depth = "16"
        else:
            settings.color_depth = "8"

        if options.bake_udim:
            result = self.bake_udim_tiles(context, options)
            bpy.ops.outliner.orphans_purge()
            return result

        if options.bake_detail_normals and context.collection:
            duplicate_collection = bpy.data.collections.new("Duplicate")
            context.collection.children.link(duplicate_collection)

        override_mat: str = ""
        if not selected_objects:
            return {""}
        for object in selected_objects:
            center_uvs_state = None
            if type(object.data) is Mesh:
                uv_index = int(options.uv_to_bake_to.split("UV")[-1])
                object.data.uv_layers.active_index = uv_index
                if options.center_uvs and uv_index < len(object.data.uv_layers):
                    center_uvs_state = self.prepare_center_uvs(object, object.data, uv_index)
                if options.bake_detail_normals:
                    self.bake_detail(object, duplicate_collection)

            material_trees = [
                (material.material, material.material.node_tree)
                for material in object.material_slots
                if material.material and material.material.node_tree
            ]
            [material for material, _ in material_trees]
            tex_nodes = [
                create_node(node_tree.nodes, 0, 0, ShaderNodeTexImage)
                for _, node_tree in material_trees
            ]
            for (_, node_tree), tex_node in zip(material_trees, tex_nodes):
                node_tree.nodes.active = tex_node

            for i, (material, node_tree) in enumerate(material_trees):
                if options.merge_textures or options.merge_objects:
                    m = self.bake_material(
                        context, material, object, options, tex_nodes[i], override_mat
                    )
                    if options.merge_objects and m:
                        override_mat = m
                else:
                    _ = self.bake_material(context, material, object, options, tex_nodes[i])
                node_tree.nodes.remove(tex_nodes[i])

            if center_uvs_state is not None and type(object.data) is Mesh:
                self.cleanup_center_uvs(object.data, *center_uvs_state)

        if options.bake_detail_normals:
            bpy.data.collections.remove(duplicate_collection)
        bpy.ops.outliner.orphans_purge()
        return {"FINISHED"}
