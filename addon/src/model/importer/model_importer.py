# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
from pathlib import Path
from typing import cast
import bpy
from bpy.types import ArmatureModifier, Context, Material, Mesh, Object
from mathutils import Vector
from .bone import import_bones
from .markers import import_markers
from ..metadata import Model
from ..section import Section
from ..vectors import NormalizedVector2

MESH_SCALE = (3.048, 3.048, 3.048)

__all__ = ["ModelImporter"]


class ModelImporter:
    def __init__(self) -> None:
        self.model: Model = Model()
        self.markers: list[Object] = []
        self.rig: Object | None = None

    def start_import(
        self,
        context: Context,
        model_path: str,
        bones: bool = True,
        materials: list[int] | None = None,
    ) -> list[Object]:
        properties = context.scene.import_properties  # pyright: ignore[reportAttributeAccessIssue, reportUnknownVariableType, reportUnknownMemberType]
        model = Path(model_path)
        if not model.exists():
            logging.warning(f"Model path does not exist: {model}")
            return []
        with open(model_path, "rb") as f:
            self.model.read(f)
        if materials:
            self.model.materials = materials
        if cast(bool, properties.import_bones) and bones:
            self.rig = import_bones(self.model)
            self.rig.scale = MESH_SCALE
            if cast(bool, properties.import_markers):
                self.markers = import_markers(self.model, self.rig)
            objects = self.import_model()
        else:
            objects = self.import_model()
        return objects

    def create_uv(
        self,
        mesh: Mesh,
        uv: list[NormalizedVector2],
        uv_scale: list[tuple[float, float, float]],
        index: int,
    ) -> None:
        uv0 = [x.vector for x in uv]
        uv_layer = mesh.uv_layers.new(name=f"UV{index}")
        for loop in range(len(mesh.loops)):
            uv_layer.data[mesh.loops[loop].index].uv = (
                uv0[mesh.loops[loop].vertex_index][0] * uv_scale[0][2] + uv_scale[0][0],
                1 - (uv0[mesh.loops[loop].vertex_index][1] * uv_scale[1][2] + uv_scale[1][0]),
            )

    def create_material_indices(self, section: Section, mesh: Mesh) -> None:
        material_slots = {}
        material_slot_indices: dict[int, int] = {}
        for submesh in range(len(section.submeshes)):
            first_face = section.submeshes[submesh].index_start
            face_count = section.submeshes[submesh].index_count
            part_faces = mesh.polygons[first_face // 3 : (first_face + face_count) // 3]
            if section.submeshes[submesh].shader_index >= len(self.model.materials):
                continue
            mat_name = str(self.model.materials[section.submeshes[submesh].shader_index])
            m = bpy.data.materials.get(mat_name)
            if not m:
                m = bpy.data.materials.new(mat_name)
            m.use_nodes = True
            mesh.materials.append(m)  # pyright: ignore[reportUnknownMemberType]
            material_slots[section.submeshes[submesh].shader_index] = mesh.materials[-1]
            material_slot_indices[section.submeshes[submesh].shader_index] = len(
                material_slot_indices
            )
            for face in part_faces:
                face.material_index = material_slot_indices[section.submeshes[submesh].shader_index]

    def create_skinning(
        self, obj: Object, name: str, armature: Object, section: Section, mesh: Mesh
    ) -> None:
        vertex_count = len(section.vertex_buffer.position_buffer.positions)
        modifier = cast(ArmatureModifier, obj.modifiers.new(f"{name}::armature", "ARMATURE"))
        if section.use_dual_quat:
            modifier.use_deform_preserve_volume = True

        modifier.object = armature

        if section.node_index >= 0 and section.node_index < len(self.model.bones):
            bone = self.model.bones[section.node_index]
            group = obj.vertex_groups.new(name=str(bone.name))
            group.add(range(vertex_count), 1.0, "REPLACE")  # pyright: ignore[reportUnknownMemberType]
        else:
            for bone in self.model.bones:
                _ = obj.vertex_groups.new(name=str(bone.name))
            for (
                vi,
                blend_indicies,
                blend_weights,
            ) in section.vertex_buffer.enumerate_blendpairs(section.vertex_type):
                for bi, bw in zip(blend_indicies, blend_weights):
                    if bi <= len(obj.vertex_groups):
                        obj.vertex_groups[bi].add([vi], bw, "REPLACE")  # pyright: ignore[reportUnknownMemberType]

        for p in mesh.polygons:
            p.use_smooth = True

    def create_normals(self, section: Section, mesh: Mesh) -> None:
        normals = [x.vector.to_tuple() for x in section.vertex_buffer.normal_buffer.normals]
        mesh.normals_split_custom_set([[0, 0, 0] for _ in mesh.loops])  # pyright: ignore[reportUnknownMemberType]
        mesh.normals_split_custom_set_from_vertices(normals)  # pyright: ignore[reportUnknownMemberType, reportArgumentType]
        _ = mesh.validate()
        mesh.update()  # pyright: ignore[reportUnknownMemberType]

    def create_section(self, section: Section) -> Object:
        permutation_name = section.permutation_name
        region_name = section.region_name
        collection_name = f"{self.model.header.tag_id}_{permutation_name}_{region_name}"

        model_scale = self.model.bounding_boxes[0].model_scale
        uv_scale = self.model.bounding_boxes[0].uv_scale
        uv_scale1 = self.model.bounding_boxes[0].uv1_scale
        uv_scale2 = self.model.bounding_boxes[0].uv2_scale

        verts = [x.vector for x in section.vertex_buffer.position_buffer.positions]
        it = len(verts[0])
        for i in range(len(verts)):
            verts[i] = Vector(
                [verts[i][j] * model_scale[j][-1] + model_scale[j][0] for j in range(it)]
            )

        ind = section.index_buffer.indices
        faces = [(ind[x], ind[x + 1], ind[x + 2]) for x in range(0, len(ind), 3)]
        mesh = bpy.data.meshes.new(collection_name)
        obj = bpy.data.objects.new(collection_name, mesh)
        obj["region_name"] = region_name
        obj["permutation_name"] = permutation_name
        obj.scale = MESH_SCALE
        mesh.from_pydata(verts, [], faces)  # pyright: ignore[reportUnknownMemberType]

        if section.vertex_flags.has_uv0:
            self.create_uv(mesh, section.vertex_buffer.uv0_buffer.uv, uv_scale, 0)
        if section.vertex_flags.has_uv1:
            self.create_uv(mesh, section.vertex_buffer.uv1_buffer.uv, uv_scale1, 1)
        if section.vertex_flags.has_uv2:
            self.create_uv(mesh, section.vertex_buffer.uv2_buffer.uv, uv_scale2, 2)

        if bpy.context.scene.import_properties.import_materials:  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
            self.create_material_indices(section, mesh)

        if self.rig:
            self.create_skinning(obj, collection_name, self.rig, section, mesh)

        return obj

    def import_model(self) -> list[Object]:
        materials: list[Material] = []
        if bpy.context.scene.import_properties.import_materials:  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
            for mat in self.model.materials:
                mat = bpy.data.materials.get(str(mat))
                if not mat:
                    mat = bpy.data.materials.new(str(mat))
                materials.append(mat)
        objects: list[Object] = []

        for section in self.model.sections:
            obj = self.create_section(section)
            self.create_normals(section, cast(Mesh, obj.data))
            objects.append(obj)
        return objects
