import logging
from pathlib import Path
from typing import cast, final, override

from bpy.types import Context, Operator

from .model.importer.model_importer import ModelImporter

from .json_definitions import CustomizationGlobals
from .utils import read_json_file


@final
class ImportSpartanOperator(Operator):
    bl_idname = "ekur.importspartan"
    bl_label = "Import Spartan"

    @override
    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}

        data_folder = cast(
            str,
            context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder,  # pyright: ignore[reportAttributeAccessIssue]
        )
        customization_path = Path(f"{data_folder}/customization_globals.json")
        if not customization_path.exists():
            logging.warning(f"Customization globals path does not exist!: {customization_path}")
            return {"CANCELLED"}

        customization_globals = read_json_file(customization_path, CustomizationGlobals)
        model_path = Path(f"{data_folder}/models/{customization_globals['model']}.ekur")
        if not model_path.exists():
            logging.warning(f"Model path does not exist!: {model_path}")
            return {"CANCELLED"}
        ModelImporter().start_import(context, str(model_path))
        return {"FINISHED"}
