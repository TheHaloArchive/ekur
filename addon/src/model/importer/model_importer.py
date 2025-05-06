# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
import bpy

from pathlib import Path
from typing import cast
from bpy.types import ArmatureModifier, Material, Mesh, Object
from mathutils import Vector

from .bone import import_bones
from .markers import import_markers
from ..rtgo_offset import RtgoOffset
from ..metadata import Model
from ..section import Section
from ..vectors import NormalizedVector2
from ...constants import FEET_TO_METER
from ...ui.model_options import get_model_options


__all__ = ["ModelImporter"]


class ModelImporter:
    def __init__(self) -> None:
        self.model: Model = Model()
        self.markers: list[Object] = []
        self.rig: Object | None = None

    def start_import(
        self,
        model_path: str,
        bones: bool = True,
        materials: list[int] | None = None,
        custom_rig: Object | None = None,
    ) -> list[Object]:
        """
        Imports the model from the given path.

        Args:
        - model_path: The path to the model file.
        - bones: Whether to import bones.
        - materials: Optional list of materials to use (useful for RTGOs)
        - custom_rig: Optional custom rig to use.

        Returns:
        - The list of imported objects.
        """
        options = get_model_options()
        model = Path(model_path)
        if not model.exists() or model.is_dir():
            logging.warning(f"Model path does not exist: {model}")
            return []
        with open(model_path, "rb") as f:
            self.model.read(f)
        if materials:
            self.model.materials = materials
        if options.import_bones and bones:
            if custom_rig is None:
                self.rig = import_bones(self.model)
                scl = (options.scale_factor,) * 3
                self.rig.scale = Vector((FEET_TO_METER, FEET_TO_METER, FEET_TO_METER)) * Vector(scl)
            else:
                self.rig = custom_rig
            if options.import_markers:
                self.markers = import_markers(self.model, self.rig)
            objects = self._import_model()
        else:
            objects = self._import_model()
        return objects

    def _create_uv(
        self,
        mesh: Mesh,
        uv: list[NormalizedVector2],
        uv_scale: list[tuple[float, float, float]],
        index: int,
    ) -> None:
        """
        Create a UV layer for the mesh. Gets compression info from the bounding box, scales the UVs,
        and assigns them to the mesh.

        Args:
        - mesh: The mesh to create the UV layer for.
        - uv: The UV coordinates to assign.
        - uv_scale: The UV scale (compression) to apply.
        - index: The index of the UV layer.
        """
        uv0 = [x.vector for x in uv]
        uv_layer = mesh.uv_layers.new(name=f"UV{index}")
        for loop in range(len(mesh.loops)):
            uv_layer.data[mesh.loops[loop].index].uv = (
                uv0[mesh.loops[loop].vertex_index][0] * uv_scale[0][2] + uv_scale[0][0],
                1 - (uv0[mesh.loops[loop].vertex_index][1] * uv_scale[1][2] + uv_scale[1][0]),
            )

    def _create_material_indices(self, section: Section, mesh: Mesh) -> None:
        """
        Create material indices for the mesh. Assigns materials to the mesh based on the shader index of the submeshes.

        Args:
        - section: The section to create the material indices for.
        - mesh: The mesh to assign the materials to.
        """
        material_slots: dict[int, Material] = {}
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
            if m.name not in mesh.materials:
                mesh.materials.append(m)  # pyright: ignore[reportUnknownMemberType]
            if len(mesh.materials) > 0:
                mat = mesh.materials[-1]
                if mat:
                    material_slots[section.submeshes[submesh].shader_index] = mat
                material_slot_indices[section.submeshes[submesh].shader_index] = len(
                    material_slot_indices
                )
                for face in part_faces:
                    face.material_index = material_slot_indices[
                        section.submeshes[submesh].shader_index
                    ]

    def _create_skinning(
        self, obj: Object, name: str, armature: Object, section: Section, mesh: Mesh
    ) -> None:
        """
        Create skinning for the mesh. Assigns vertex groups to the mesh based on the bone indices and weights.

        Args:
        - obj: The object to assign the vertex groups to.
        - name: The name of the collection to assign to the armature.
        - armature: The armature to assign the vertex groups to.
        - section: The section to create the skinning for.
        - mesh: The mesh to assign the vertex groups to.
        """
        vertex_count = len(section.vertex_buffer.position_buffer.positions)
        modifier = cast(ArmatureModifier, obj.modifiers.new(f"{name}::armature", "ARMATURE"))
        if section.use_dual_quat:
            modifier.use_deform_preserve_volume = True

        modifier.object = armature

        if section.node_index != 255 and section.node_index < len(self.model.bones):
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

        # Removes that weird shading that happens when you twist a bone
        for p in mesh.polygons:
            p.use_smooth = True

    def _create_color(self, section: Section, mesh: Mesh) -> None:
        """
        Create vertex colors for the mesh. Assigns vertex colors to the mesh based on the color buffer.

        Args:
        - section: The section to create the vertex colors for.
        - mesh: The mesh to assign the vertex colors to.
        """
        for i, color in enumerate(section.vertex_buffer.color_buffer.color):
            ca = mesh.color_attributes.new(name=f"Color{i}", type="BYTE_COLOR", domain="FACE")
            for loop in range(len(mesh.loops) // 3):
                ca.data[loop].color = color  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

    def _create_normals(self, section: Section, mesh: Mesh) -> None:
        """
        Create normals for the mesh. Assigns normals to the mesh based on the normal buffer.

        Args:
        - section: The section to create the normals for.
        - mesh: The mesh to assign the normals to.
        """
        normals = [x.vector.to_tuple() for x in section.vertex_buffer.normal_buffer.normals]
        mesh.shade_smooth()  # pyright: ignore[reportUnknownMemberType]
        mesh.normals_split_custom_set_from_vertices(normals)  # pyright: ignore[reportUnknownMemberType, reportArgumentType]
        _ = mesh.validate()
        mesh.update()  # pyright: ignore[reportUnknownMemberType]

    def _create_section(self, section: Section, offset: RtgoOffset | None = None) -> Object | None:
        """
        Create a section (submesh) of the model.

        Args:
        - section: The section to create the object for.

        Returns:
        - The object representing the section.
        """
        permutation_name = section.permutation_name
        region_name = section.region_name
        collection_name = f"{self.model.header.tag_id}_{permutation_name}_{region_name}"
        options = get_model_options()

        if len(self.model.bounding_boxes) == 0:
            return None
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
        obj.scale = Vector((FEET_TO_METER, FEET_TO_METER, FEET_TO_METER)) * Vector(
            (options.scale_factor,) * 3
        )
        mesh.from_pydata(verts, [], faces)  # pyright: ignore[reportUnknownMemberType]
        if section.vertex_flags.has_uv0:
            self._create_uv(mesh, section.vertex_buffer.uv0_buffer.uv, uv_scale, 0)
        if section.vertex_flags.has_uv1:
            self._create_uv(mesh, section.vertex_buffer.uv1_buffer.uv, uv_scale1, 1)
        if section.vertex_flags.has_uv2:
            self._create_uv(mesh, section.vertex_buffer.uv2_buffer.uv, uv_scale2, 2)

        if options.import_materials:
            self._create_material_indices(section, mesh)
        if options.import_vertex_color:
            self._create_color(section, mesh)
        if self.rig and options.import_bones:
            self._create_skinning(obj, collection_name, self.rig, section, mesh)

        if offset:
            obj.location = offset.position.vector
            obj["permutation_name"] = offset.name
        return obj

    def _import_model(self) -> list[Object]:
        """
        Imports the model by creating sections.

        Returns:
        - The list of imported objects.
        """
        materials: list[Material] = []
        options = get_model_options()
        if options.import_materials:
            for mat in self.model.materials:
                mat = bpy.data.materials.get(str(mat))
                if not mat:
                    mat = bpy.data.materials.new(str(mat))
                materials.append(mat)
        objects: list[Object] = []

        for idx, section in enumerate(self.model.sections):
            per_mesh_data = None
            per_mesh_datas = [pmd for pmd in self.model.offsets if pmd.mesh_index == idx]
            if per_mesh_datas != []:
                per_mesh_data = per_mesh_datas[0]
            obj = self._create_section(section, per_mesh_data)
            if obj:
                self._create_normals(section, cast(Mesh, obj.data))
                objects.append(obj)
        return objects
