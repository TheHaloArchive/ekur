"""
Ekur - Simple coating import for Reclaimer to Blender.
"""

import bpy
import subprocess

from pathlib import Path
from bpy.types import AddonPreferences, Operator, Context
from bpy.utils import register_class, unregister_class
from .src.import_panel import CoatingImportPanel, ImportProperties, RandomizeCoatingOperator
from .src.import_logic import ImportCoatingOperator

bl_info = {
    "name": "Ekur",
    "description": "A multi-purpose importer for Halo Infinite.",
    "author": "Surasia",
    "version": (0, 1, 0),
    "blender": (4, 3, 0),
    "category": "Import-Export",
    "support": "COMMUNITY",
}


class DownloadStringsOperator(Operator):
    bl_idname = "ekur.downloadstrings"
    bl_label = "Download Strings"

    def execute(self, context: Context | None) -> set[str]:
        data = context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder  # pyright: ignore[reportAttributeAccessIssue]
        _save_path = f"{data}/strings.txt"
        return {"FINISHED"}


class DumpFilesOperator(Operator):
    bl_idname = "ekur.dumpfiles"
    bl_label = "Dump Required Files"

    def execute(self, context: Context | None) -> set[str]:
        data: EkurPreferences = context.preferences.addons["bl_ext.user_default.ekur"].preferences
        ekur_save_path = Path(f"{data.data_folder}/ekur.exe")
        _ = Path(f"{data.data_folder}/all_visors.json")
        save_path = f"{data.data_folder}/strings.txt"
        _ = subprocess.run(
            [
                ekur_save_path,
                "--save-path",
                data.data_folder,
                "--module-path",
                data.deploy_folder,
                "--strings-path",
                save_path,
            ]
        )
        return {"FINISHED"}


class EkurPreferences(AddonPreferences):
    bl_idname = __name__

    data_folder: bpy.props.StringProperty(
        subtype="DIR_PATH",
        name="Data Folder",
        description="Path to the dump coatings to.",
        default="",
    )

    deploy_folder: bpy.props.StringProperty(
        subtype="DIR_PATH",
        name="Deploy Folder",
        description="Path to the 'deploy' folder in your Halo Infinite installation directory.",
        default="",
    )

    def draw(self, _context: Context | None):
        layout = self.layout
        box = layout.box()
        box.label(text="Paths", icon="FILE_FOLDER")
        box.prop(self, "data_folder")
        box.prop(self, "deploy_folder")
        box2 = layout.box()
        _ = box2.operator("ekur.downloadstrings")
        _ = box2.operator("ekur.dumpfiles")


# Just copied from Reclaimer's RMF importer :3
package_version = bl_info["version"]
package_version_string = ".".join(str(i) for i in package_version)


def register():
    register_class(ImportCoatingOperator)
    register_class(CoatingImportPanel)
    register_class(EkurPreferences)
    register_class(ImportProperties)
    register_class(RandomizeCoatingOperator)
    register_class(DownloadStringsOperator)
    register_class(DumpFilesOperator)
    bpy.types.Scene.import_properties = bpy.props.PointerProperty(type=ImportProperties)  # pyright: ignore[reportAttributeAccessIssue]


def unregister():
    unregister_class(ImportCoatingOperator)
    unregister_class(EkurPreferences)
    unregister_class(CoatingImportPanel)
    unregister_class(ImportProperties)
    unregister_class(RandomizeCoatingOperator)
    unregister_class(DownloadStringsOperator)
    unregister_class(DumpFilesOperator)
    del bpy.types.Scene.import_properties  # pyright: ignore[reportAttributeAccessIssue]
