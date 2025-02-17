from pathlib import Path
from typing import cast, final
import bpy
from bpy.types import Context, Operator, Object
from mathutils import Matrix, Quaternion, Vector

from ..json_definitions import Level
from ..model.importer.model_importer import ModelImporter
from ..utils import read_json_file


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
            # Get or create the source geometry
            source_object = self._get_or_create_geometry(
                context, str(instance["global_id"]), data, instance["material"]
            )

            # Create instance
            instance_obj = bpy.data.objects.new(
                name=f"{source_object.name}_instance", object_data=source_object.data
            )
            locrotscale = Matrix.LocRotScale(
                Vector(instance["position"]),
                Quaternion(instance["rotation"]),
                Vector(instance["scale"]),
            )
            instance_obj.matrix_world = locrotscale

            # Link instance to current collection
            bpy.context.collection.objects.link(instance_obj)

        return {"FINISHED"}
