# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import Object
from mathutils import Matrix, Quaternion

from ..marker import Marker, MarkerInstance

from .bone import get_bone_transforms
from ..metadata import Model

__all__ = ["import_markers"]


def get_name(marker: Marker, instance: MarkerInstance, model: Model):
    name = str(marker.name)
    if instance.region_index >= 0 and len(model.regions) > instance.region_index:
        name += f"_{model.regions[instance.region_index].name}"
        if instance.permutation_index >= 0:
            name += f"_{model.regions[instance.region_index].permutations[instance.permutation_index].name}"
    return name


def import_markers(model: Model, armature: Object) -> list[Object]:
    MARKER_SIZE = 0.01

    bone_transforms = get_bone_transforms(model)
    markers: list[Object] = []

    for marker in model.markers:
        for instance in marker.instances:
            name = get_name(marker, instance, model)

            marker_obj = bpy.data.objects.new(str(name), None)
            marker_obj.empty_display_type = "SPHERE"
            marker_obj.empty_display_size = MARKER_SIZE
            marker_obj.scale = (3.048, 3.048, 3.048)

            world_transform = (
                Matrix.Translation([v for v in instance.position.vector])
                @ Quaternion(instance.rotation.vector).to_matrix().to_4x4()
            )

            if instance.node_index >= 0 and len(bone_transforms) > instance.node_index:
                world_transform = bone_transforms[instance.node_index] @ world_transform
                marker_obj.parent = armature
                marker_obj.parent_type = "BONE"
                marker_obj.parent_bone = str(model.bones[instance.node_index].name)

            marker_obj.hide_render = True
            marker_obj.matrix_world = world_transform
            bpy.context.scene.collection.objects.link(marker_obj)  # pyright: ignore[reportUnknownMemberType]
            markers.append(marker_obj)
    return markers
