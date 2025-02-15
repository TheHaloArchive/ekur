# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import cast, final, override
import bpy
from bpy.types import ArmatureModifier, Collection, Context, Material, Mesh, Object, Operator

from .model.section import Section
from .model.vectors import NormalizedVector2
from .model.importer.bone import import_bones
from .model.importer.markers import import_markers
from .model.metadata import Model

MESH_SCALE = (3.048, 3.048, 3.048)


@final
class ImportModelOperator(Operator):
    bl_idname = "ekur.importmodel"
    bl_label = "Import"

    def __init__(self) -> None:
        self.model = Model()

    @override
    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}
        properties = context.scene.import_properties  # pyright: ignore[reportAttributeAccessIssue, reportUnknownVariableType, reportUnknownMemberType]
        model_path = cast(str, properties.model_path)
        with open(model_path, "rb") as f:
            self.model.read(f)
        if cast(bool, properties.import_bones):
            armature = import_bones(self.model)
            armature.scale = MESH_SCALE
            if cast(bool, properties.import_markers):
                import_markers(self.model, armature)
            self.import_model(armature)
        else:
            self.import_model()
        return {"FINISHED"}

    def create_uv(
        self,
        mesh: Mesh,
        uv: list[NormalizedVector2],
        uv_scale: list[tuple[float, float, float]],
        index: int,
    ) -> None:
        uv0 = [x.to_vector() for x in uv]
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

        normals = [x.to_vector() for x in section.vertex_buffer.normal_buffer.normals]
        mesh.normals_split_custom_set([[0, 0, 0] for _ in mesh.loops])  # pyright: ignore[reportUnknownMemberType]
        mesh.normals_split_custom_set_from_vertices(normals)  # pyright: ignore[reportUnknownMemberType]
        _ = mesh.validate()
        mesh.update()  # pyright: ignore[reportUnknownMemberType]

    def import_model(self, armature_obj: Object | None = None) -> None:
        materials: list[Material] = []
        if bpy.context.scene.import_properties.import_materials:  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
            for mat in self.model.materials:
                mat = bpy.data.materials.get(str(mat))
                if not mat:
                    mat = bpy.data.materials.new(str(mat))
                materials.append(mat)

        model_scale = self.model.bounding_boxes[0].get_model_scale()
        uv_scale = self.model.bounding_boxes[0].get_uv_scale()
        model_collection = bpy.data.collections.new(str(self.model.header.tag_id))
        bpy.context.scene.collection.children.link(model_collection)  # pyright: ignore[reportUnknownMemberType]
        collections: dict[int, Collection] = {}

        for section in self.model.sections:
            permutation_name = section.permutation_name
            region_name = section.region_name
            collection_name = f"{self.model.header.tag_id}_{permutation_name}_{region_name}"

            verts = [x.to_vector() for x in section.vertex_buffer.position_buffer.positions]
            it = len(verts[0])
            for i in range(len(verts)):
                verts[i] = [verts[i][j] * model_scale[j][-1] + model_scale[j][0] for j in range(it)]

            ind = section.index_buffer.indices
            faces = [(ind[x], ind[x + 1], ind[x + 2]) for x in range(0, len(ind), 3)]
            mesh = bpy.data.meshes.new(collection_name)
            obj = bpy.data.objects.new(collection_name, mesh)
            obj.scale = MESH_SCALE
            mesh.from_pydata(verts, [], faces)  # pyright: ignore[reportUnknownMemberType]

            if section.vertex_flags.has_uv0:
                self.create_uv(mesh, section.vertex_buffer.uv0_buffer.uv, uv_scale, 0)
            if section.vertex_flags.has_uv1:
                self.create_uv(mesh, section.vertex_buffer.uv1_buffer.uv, uv_scale, 1)
            if section.vertex_flags.has_uv2:
                self.create_uv(mesh, section.vertex_buffer.uv2_buffer.uv, uv_scale, 2)

            if bpy.context.scene.import_properties.import_materials:  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
                self.create_material_indices(section, mesh)

            if armature_obj:
                self.create_skinning(obj, collection_name, armature_obj, section, mesh)

            if permutation_name not in collections:
                permutation_collection: Collection = bpy.data.collections.new(str(permutation_name))
                model_collection.children.link(permutation_collection)  # pyright: ignore[reportUnknownMemberType]
                collections[permutation_name] = permutation_collection
            else:
                permutation_collection = collections[permutation_name]

            if permutation_collection.children.get(f"{region_name}_{permutation_name}") is None:
                region_collection = bpy.data.collections.new(f"{region_name}_{permutation_name}")
                permutation_collection.children.link(region_collection)  # pyright: ignore[reportUnknownMemberType]
            else:
                region_collection = permutation_collection.children[region_name]

            region_collection.objects.link(obj)  # pyright: ignore[reportUnknownMemberType]
