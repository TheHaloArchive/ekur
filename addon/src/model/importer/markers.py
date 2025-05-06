# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import Object
from mathutils import Matrix, Quaternion, Vector

from ...ui.model_options import get_model_options
from ...constants import FEET_TO_METER

from ..marker import Marker, MarkerInstance

from .bone import get_bone_transforms
from ..metadata import Model

__all__ = ["import_markers"]


def _get_name(marker: Marker, instance: MarkerInstance, model: Model) -> str:
    """
    Gets the name of the marker instance, including the region and permutation if available.

    Args:
    - marker: The marker to get the name of.
    - instance: The instance of the marker to get the name of.
    - model: The model containing the marker.

    Returns:
    - The name of the marker instance.
    """
    name = str(marker.name)
    if instance.region_index >= 0 and len(model.regions) > instance.region_index:
        name += f"_{model.regions[instance.region_index].name}"
        if (
            instance.permutation_index >= 0
            and len(model.regions[instance.region_index].permutations) > instance.permutation_index
        ):
            name += f"_{model.regions[instance.region_index].permutations[instance.permutation_index].name}"
    return name


def import_markers(model: Model, armature: Object) -> list[Object]:
    """
    Imports the markers of the model.

    Args:
    - model: The model to import the markers from.
    - armature: The armature to parent the markers to.

    Returns:
    - The list of imported markers (as empties)
    """
    props = get_model_options()
    MARKER_SIZE = 0.01 * props.scale_factor
    bone_transforms = get_bone_transforms(model)
    markers: list[Object] = []

    for marker in model.markers:
        for instance in marker.instances:
            name = _get_name(marker, instance, model)

            marker_obj = bpy.data.objects.new(str(name), None)
            marker_obj.empty_display_type = "SPHERE"
            marker_obj.empty_display_size = MARKER_SIZE
            marker_obj.scale = Vector((FEET_TO_METER, FEET_TO_METER, FEET_TO_METER)) * Vector(
                (props.scale_factor,) * 3
            )
            world_transform = (
                Matrix.Translation([v for v in instance.position.vector])
                @ Quaternion(instance.rotation.vector).to_matrix().to_4x4()
            )

            if instance.node_index != 255 and len(bone_transforms) > instance.node_index:
                world_transform = bone_transforms[instance.node_index] @ world_transform
                marker_obj.parent = armature
                marker_obj.parent_type = "BONE"
                marker_obj.parent_bone = str(model.bones[instance.node_index].name)

            marker_obj.hide_render = True
            marker_obj.matrix_world = world_transform
            if bpy.context.scene:
                bpy.context.scene.collection.objects.link(marker_obj)  # pyright: ignore[reportUnknownMemberType]
            markers.append(marker_obj)
    return markers
