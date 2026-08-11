from bpy.types import Armature
import bpy
from mathutils import Quaternion, Matrix

from .anim_data import AnimationData, AnimationNode


def _get_data_bone(armature: bpy.types.Object, node_name: str):
    if type(armature.data) is Armature:
        for bone in armature.data.bones:
            if bone.name.lower() == node_name.lower():
                return bone
    return None


def _get_pose_bone(armature: bpy.types.Object, node_name: str):
    if type(armature.data) is Armature:
        for bone in armature.pose.bones: # ty: ignore[unresolved-attribute]
            if bone.name.lower() == node_name.lower():
                return bone
    return None


def _derive_parent_indices_from_child_sibling(nodes: list[AnimationNode]) -> list[int]:
    parent_index = [-1] * len(nodes)

    for node_idx, node in enumerate(nodes):
        child_idx = node.first_child
        if child_idx == -1 or child_idx < 0 or child_idx >= len(nodes):
            continue

        current = child_idx
        visited = set()

        while current != -1:
            if current in visited:
                break
            visited.add(current)

            parent_index[current] = node_idx

            sibling_idx = nodes[current].next_sibling
            if sibling_idx < -1 or sibling_idx >= len(nodes):
                break
            current = sibling_idx

    return parent_index


def import_animation(
    armature: bpy.types.Object,
    animation_data: AnimationData,
    action_name: str,
) -> bpy.types.Action | None:
    parent_index = _derive_parent_indices_from_child_sibling(animation_data.nodes)

    bone_map: dict[int, bpy.types.PoseBone] = {}
    local_rest: dict[int, Matrix] = {}

    for node_idx, node in enumerate(animation_data.nodes):
        pose_bone = _get_pose_bone(armature, node.name)
        if pose_bone is None:
            continue

        bone_map[node_idx] = pose_bone

        data_bone = _get_data_bone(armature, pose_bone.name)
        if data_bone is None:
            continue

        local_matrix = data_bone.matrix_local
        if data_bone.parent:
            local_matrix = data_bone.parent.matrix_local.inverted() @ data_bone.matrix_local

        local_rest[node_idx] = local_matrix

    action = bpy.data.actions.new(action_name)
    armature.animation_data_create()
    if armature.animation_data:
        armature.animation_data.action = action

    for frame_index in range(animation_data.total_frames):
        frame_number = frame_index + 1
        frame_data = animation_data.frames[frame_index]

        absolute_frame: list[Matrix | None] = [None] * animation_data.node_count
        for node_idx in range(animation_data.node_count):
            t = frame_data.transforms[node_idx]
            local_matrix = Matrix.LocRotScale(
                t.position.vector.to_tuple(),
                Quaternion(t.rotation.vector),
                (t.scale, t.scale, t.scale),
            )

            p_idx = parent_index[node_idx]
            if p_idx != -1 and absolute_frame[p_idx] is not None:
                absolute_frame[node_idx] = absolute_frame[p_idx] @ local_matrix  # ty: ignore[unsupported-operator]
            else:
                absolute_frame[node_idx] = local_matrix

        for node_idx, pose_bone in bone_map.items():
            transform_matrix = absolute_frame[node_idx]

            p_idx = parent_index[node_idx]
            if p_idx != -1 and absolute_frame[p_idx] is not None:
                transform_matrix = absolute_frame[p_idx].inverted() @ transform_matrix  # ty: ignore[unsupported-operator, unresolved-attribute]

            rest_local = local_rest.get(node_idx)
            if rest_local is not None:
                transform_matrix = rest_local.inverted() @ transform_matrix  # ty: ignore[unsupported-operator]

            loc, rot_quat, scl = transform_matrix.decompose()  # ty: ignore[unresolved-attribute]

            pose_bone.rotation_mode = "QUATERNION"
            pose_bone.location = loc
            pose_bone.rotation_quaternion = rot_quat
            pose_bone.scale = scl

            pose_bone.keyframe_insert("location", frame=frame_number, group=pose_bone.name)
            pose_bone.keyframe_insert(
                "rotation_quaternion", frame=frame_number, group=pose_bone.name
            )
            pose_bone.keyframe_insert("scale", frame=frame_number, group=pose_bone.name)

    if action:
        action.frame_start = 1
        action.frame_end = animation_data.total_frames
    return action
