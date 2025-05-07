# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
import operator
import bpy

from bpy.types import Armature, EditBone, Object
from mathutils import Matrix
from typing import cast
from functools import reduce

from ..bone import Bone
from ..metadata import Model
from ...ui.model_options import get_model_options

__all__ = ["import_bones", "get_bone_transforms"]


def _create_transform(rot_matrix: Matrix, trans_matrix: Matrix) -> Matrix:
    """
    Create a transformation matrix from the given rotation and translation matrices.

    Args:
    - rot_matrix: The rotation matrix.
    - trans_matrix: The translation matrix.

    Returns:
    - The transformation matrix.
    """
    transform = rot_matrix @ trans_matrix

    m = transform.transposed()
    translation, rotation, _ = m.decompose()
    return Matrix.Translation(translation * 1) @ rotation.to_matrix().to_4x4()


def _get_bone_lineage(model: Model, bone: Bone) -> list[Bone]:
    """
    Get the lineage (list of bones up to it) of the given bone.

    - model: The model containing the rig to get the lineage from.
    - bone: The bone to get the lineage of.

    Returns:
    - The lineage of the bone.
    """
    lineage = [bone]
    current_bone = bone
    while current_bone.parent_index >= 0:
        if current_bone.parent_index <= len(model.bones):
            current_bone = model.bones[current_bone.parent_index]
            lineage.append(current_bone)
    lineage.reverse()
    return lineage


def get_bone_transforms(model: Model) -> list[Matrix]:
    """
    Get the global transformation matrices of all bones in the model created through getting the bone lineage.

    Args:
    - model: The model containing the rig to get the bone transforms from.

    Returns:
    - The transformation matrices of all bones in the model.
    """
    result: list[Matrix] = []
    for bone in model.bones:
        lineage = _get_bone_lineage(model, bone)
        transforms = [
            _create_transform(x.rotation_matrix.matrix, x.transformation_matrix.matrix)
            for x in lineage
        ]
        res = cast(Matrix, reduce(operator.matmul, transforms))
        result.append(res)
    return result


def _create_armature(model: Model) -> tuple[Armature, Object]:
    """
    Creates a new armature given a model.

    Args:
    - model: The model to create the armature from.

    Returns:
    - The armature data and object.
    """
    armature_data = bpy.data.armatures.new(f"{model.header.tag_id}_Armature")
    armature_obj = bpy.data.objects.new(f"{model.header.tag_id}_Armature", armature_data)

    if bpy.context.scene is not None:
        bpy.context.scene.collection.objects.link(armature_obj)  # pyright: ignore[reportUnknownMemberType]
    else:
        logging.warning("No scene found to link the armature to!")

    bpy.ops.object.select_all(action="DESELECT")  # pyright: ignore[reportUnknownMemberType]
    armature_obj.select_set(True)  # pyright: ignore[reportUnknownMemberType]
    if bpy.context.view_layer is not None:
        bpy.context.view_layer.objects.active = armature_obj
    else:
        logging.warning("No view layer found to set the armature object to!")
    bpy.ops.object.mode_set(mode="EDIT")  # pyright: ignore[reportUnknownMemberType]
    return armature_data, armature_obj


def import_bones(model: Model) -> Object:
    """
    Import the bones from the given model.

    Args:
    - model: The model to import the bones from.

    Returns:
    - The armature object containing the bones.
    """
    props = get_model_options()
    armature_data, armature_obj = _create_armature(model)
    bone_transforms = get_bone_transforms(model)

    editbones: list[EditBone] = []
    for bone in model.bones:
        editbone = armature_data.edit_bones.new(str(bone.name))
        editbones.append(editbone)

    for i, bone in enumerate(model.bones):
        editbone = editbones[i]  # directly accessing the list is fine here
        editbone.length = props.scale_factor * props.bone_size
        editbone.matrix = bone_transforms[i]
        if bone.parent_index >= 0:
            editbone.parent = editbones[bone.parent_index]

    bpy.ops.object.mode_set(mode="OBJECT")  # pyright: ignore[reportUnknownMemberType]
    return armature_obj
