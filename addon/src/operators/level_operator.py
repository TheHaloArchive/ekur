import math
from pathlib import Path
from typing import cast, final
import bpy
from bpy.types import Context, Operator, Object
from mathutils import Matrix, Quaternion, Vector

from ..json_definitions import Level
from ..model.importer.model_importer import ModelImporter
from ..utils import read_json_file


def create_from_rotation_matrix(matrix: Matrix) -> Quaternion:
    trace = matrix[0][0] + matrix[1][1] + matrix[2][2]
    q = Quaternion()  # Quaternion [x, y, z, w]

    if trace > 0.0:
        s = math.sqrt(trace + 1.0)
        q[3] = s * 0.5  # w
        s = 0.5 / s
        q[0] = (matrix[1][2] - matrix[2][1]) * s  # x
        q[1] = (matrix[2][0] - matrix[0][2]) * s  # y
        q[2] = (matrix[0][1] - matrix[1][0]) * s  # z
    else:
        if matrix[0][0] >= matrix[1][1] and matrix[0][0] >= matrix[2][2]:
            s = math.sqrt(1.0 + matrix[0][0] - matrix[1][1] - matrix[2][2])
            inv_s = 0.5 / s
            q[0] = 0.5 * s  # x
            q[1] = (matrix[0][1] + matrix[1][0]) * inv_s  # y
            q[2] = (matrix[0][2] + matrix[2][0]) * inv_s  # z
            q[3] = (matrix[1][2] - matrix[2][1]) * inv_s  # w
        elif matrix[1][1] > matrix[2][2]:
            s = math.sqrt(1.0 + matrix[1][1] - matrix[0][0] - matrix[2][2])
            inv_s = 0.5 / s
            q[0] = (matrix[1][0] + matrix[0][1]) * inv_s  # x
            q[1] = 0.5 * s  # y
            q[2] = (matrix[2][1] + matrix[1][2]) * inv_s  # z
            q[3] = (matrix[2][0] - matrix[0][2]) * inv_s  # w
        else:
            s = math.sqrt(1.0 + matrix[2][2] - matrix[0][0] - matrix[1][1])
            inv_s = 0.5 / s
            q[0] = (matrix[2][0] + matrix[0][2]) * inv_s  # x
            q[1] = (matrix[2][1] + matrix[1][2]) * inv_s  # y
            q[2] = 0.5 * s  # z
            q[3] = (matrix[0][1] - matrix[1][0]) * inv_s  # w

    return q


@final
class ImportLevelOperator(Operator):
    bl_idname = "ekur.importlevel"
    bl_label = "Import"

    _geometry_cache: dict[str, Object] = {}

    def _get_or_create_geometry(
        self, context: Context, global_id: str, data_folder: str, materials: list[int]
    ) -> Object:
        if global_id in self._geometry_cache:
            return self._geometry_cache[global_id]

        path = f"{data_folder}/runtime_geo/{global_id}.ekur"
        geo_importer = ModelImporter()
        imported_objects = geo_importer.start_import(
            context, path, materials=materials, bones=False
        )

        source_object = imported_objects[0]
        master_collection = bpy.data.collections.get("Master Geometries")
        if not master_collection:
            master_collection = bpy.data.collections.new("Master Geometries")
            bpy.context.scene.collection.children.link(master_collection)

        if source_object.name in bpy.context.collection.objects:
            bpy.context.collection.objects.unlink(source_object)
        master_collection.objects.link(source_object)

        self._geometry_cache[global_id] = source_object
        return source_object

    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}

        level_path = Path(cast(str, context.scene.import_properties.level_path))  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        level = read_json_file(level_path, Level)
        data = cast(
            str,
            context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder,  # pyright: ignore[reportAttributeAccessIssue]
        )

        for instance in level["instances"]:
            source_object = self._get_or_create_geometry(
                context, str(instance["global_id"]), data, instance["material"]
            )

            instance_obj = bpy.data.objects.new(
                name=f"{source_object.name}_instance", object_data=source_object.data
            )
            rotmat = Matrix(
                (
                    (*instance["forward"], 0.0),
                    (*instance["left"], 0.0),
                    (*instance["up"], 0.0),
                    (0.0, 0.0, 0.0, 1.0),
                )
            )
            rot = create_from_rotation_matrix(rotmat)
            rot = Quaternion((rot[3], rot[0], rot[1], rot[2]))
            print(rot)
            instance_obj.scale = Vector(instance["scale"])
            instance_obj.location = Vector(instance["position"])
            instance_obj.rotation_mode = "QUATERNION"
            instance_obj.rotation_quaternion = rot

            bpy.context.collection.objects.link(instance_obj)

        return {"FINISHED"}
