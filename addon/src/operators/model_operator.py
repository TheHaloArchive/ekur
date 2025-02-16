from typing import cast, final, override

from bpy.types import Context, Operator

from ..model.importer.model_importer import ModelImporter


@final
class ImportModelOperator(Operator):
    bl_idname = "ekur.importmodel"
    bl_label = "Import"

    @override
    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}
        properties = context.scene.import_properties  # pyright: ignore[reportAttributeAccessIssue, reportUnknownVariableType, reportUnknownMemberType]
        model_path = cast(str, properties.model_path)
        ModelImporter().start_import(context, model_path)
        return {"FINISHED"}
