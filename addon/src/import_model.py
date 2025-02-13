# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import ArmatureModifier, Context, Mesh, Object, Operator

from .model.section import Section
from .model.vectors import NormalizedVector2
from .model.importer.bone import import_bones
from .model.importer.markers import import_markers
from .model.metadata import Model


class ImportModelOperator(Operator):
    bl_idname = "ekur.importmodel"
    bl_label = "Import"

    def execute(self, context: Context | None) -> set[str]:
        self.model = Model()
        model_path = context.scene.import_properties.model_path  # pyright: ignore[reportAttributeAccessIssue]
        with open(model_path, "rb") as f:
            self.model.read(f)
        if context.scene.import_properties.import_bones:  # pyright: ignore[reportAttributeAccessIssue]
            armature = import_bones(self.model)
            armature.scale = (3.048, 3.048, 3.048)
            if context.scene.import_properties.import_markers:  # pyright: ignore[reportAttributeAccessIssue]
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
        material_slot_indices = {}
        for submesh in range(len(section.submeshes)):
            first_face = section.submeshes[submesh].index_start
            face_count = section.submeshes[submesh].index_count
            part_faces = mesh.polygons[first_face // 3 : (first_face + face_count) // 3]
            mat_name = str(self.model.materials[section.submeshes[submesh].shader_index])
            m = bpy.data.materials.get(mat_name)
            if not m:
                m = bpy.data.materials.new(mat_name)
            m.use_nodes = True
            mesh.materials.append(m)
            material_slots[section.submeshes[submesh].shader_index] = mesh.materials[-1]
            material_slot_indices[section.submeshes[submesh].shader_index] = len(
                material_slot_indices
            )
            for face in part_faces:
                face.material_index = material_slot_indices[section.submeshes[submesh].shader_index]

    def import_model(self, armature_obj: Object | None = None) -> None:
        materials = []
        if bpy.context.scene.import_properties.import_materials:  # pyright: ignore[reportAttributeAccessIssue]
            for mat in self.model.materials:
                mat = bpy.data.materials.get(str(mat))
                if not mat:
                    mat = bpy.data.materials.new(str(mat))
                materials.append(mat)

        model_scale = self.model.bounding_boxes[0].get_model_scale()
        uv_scale = self.model.bounding_boxes[0].get_uv_scale()
        model_collection = bpy.data.collections.new(str(self.model.header.tag_id))
        bpy.context.scene.collection.children.link(model_collection)
        collections = {}

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
            obj.scale = (3.048, 3.048, 3.048)
            mesh.from_pydata(verts, [], faces)

            if section.vertex_flags.has_uv0:
                self.create_uv(mesh, section.vertex_buffer.uv0_buffer.uv, uv_scale, 0)
            if section.vertex_flags.has_uv1:
                self.create_uv(mesh, section.vertex_buffer.uv1_buffer.uv, uv_scale, 1)
            if section.vertex_flags.has_uv2:
                self.create_uv(mesh, section.vertex_buffer.uv2_buffer.uv, uv_scale, 2)

            if bpy.context.scene.import_properties.import_materials:  # pyright: ignore[reportAttributeAccessIssue]
                self.create_material_indices(section, mesh)

            vertex_count = len(section.vertex_buffer.position_buffer.positions)
            modifier: ArmatureModifier = obj.modifiers.new(
                f"{collection_name}::armature", "ARMATURE"
            )
            if section.use_dual_quat:
                modifier.use_deform_preserve_volume = True

            modifier.object = armature_obj

            if section.node_index >= 0:
                # only need one vertex group
                bone = self.model.bones[section.node_index]
                group = obj.vertex_groups.new(name=str(bone.name))
                group.add(range(vertex_count), 1.0, "ADD")  # set every vertex to 1.0 in one go
            else:
                # create a vertex group for each bone so the bone indices are 1:1 with the vertex groups
                for bone in self.model.bones:
                    _ = obj.vertex_groups.new(name=str(bone.name))
                for (
                    vi,
                    blend_indicies,
                    blend_weights,
                ) in section.vertex_buffer.enumerate_blendpairs(section.vertex_type):
                    for bi, bw in zip(blend_indicies, blend_weights):
                        if bi <= len(obj.vertex_groups):
                            obj.vertex_groups[bi].add([vi], bw, "ADD")

            for p in mesh.polygons:
                p.use_smooth = True

            normals = [x.to_vector() for x in section.vertex_buffer.normal_buffer.normals]
            mesh.normals_split_custom_set([[0, 0, 0] for _ in mesh.loops])
            mesh.normals_split_custom_set_from_vertices(normals)
            _ = mesh.validate()
            mesh.update()

            if permutation_name not in collections:
                permutation_collection = bpy.data.collections.new(str(permutation_name))
                model_collection.children.link(permutation_collection)
                collections[permutation_name] = permutation_collection
            else:
                permutation_collection = collections[permutation_name]

            if permutation_collection.children.get(f"{region_name}_{permutation_name}") is None:
                region_collection = bpy.data.collections.new(f"{region_name}_{permutation_name}")
                permutation_collection.children.link(region_collection)
            else:
                region_collection = permutation_collection.children[region_name]

            region_collection.objects.link(obj)
