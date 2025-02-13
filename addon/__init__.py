# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
"""
Ekur - A multi-purpose importer for Halo Infinite.
"""

import logging
import platform
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

import bpy
from bpy.types import AddonPreferences, Context, Operator
from bpy.utils import register_class, unregister_class

from .src.import_logic import ImportMaterialOperator
from .src.import_panel import CoatingImportPanel, ImportProperties, RandomizeCoatingOperator
from .src.import_model import ImportModelOperator

bl_info = {
    "name": "Ekur",
    "description": "A multi-purpose importer for Halo Infinite.",
    "author": "Surasia",
    "version": (0, 2, 1),
    "blender": (4, 3, 0),
    "category": "Import-Export",
    "support": "COMMUNITY",
}

# Just copied from Reclaimer's RMF importer :3
package_version = bl_info["version"]
package_version_string = ".".join(str(i) for i in package_version)

STRINGS_URL = "https://github.com/Surasia/ReclaimerFiles/raw/refs/heads/master/strings.txt"
VISORS_URL = "https://github.com/Surasia/ekur/raw/refs/heads/master/assets/all_visors.json"


class DownloadFilesOperator(Operator):
    bl_idname = "ekur.downloadfiles"
    bl_label = "Download Required Files"

    def execute(self, context: Context | None) -> set[str]:
        data = context.preferences.addons["bl_ext.user_default.ekur"].preferences.data_folder  # pyright: ignore[reportAttributeAccessIssue]
        save_path = f"{data}/strings.txt"
        visors_path = f"{data}/all_visors.json"
        try:
            with (
                urllib.request.urlopen(STRINGS_URL) as response,
                open(save_path, "wb") as out_file,
            ):
                _ = out_file.write(response.read())
        except urllib.error.HTTPError as e:
            logging.error(f"Failed to download strings.txt: {e}")
            return {"CANCELLED"}

        try:
            with (
                urllib.request.urlopen(VISORS_URL) as response,
                open(visors_path, "w") as out_file,
            ):
                _ = out_file.write(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            logging.error(f"Failed to download all_visors.json: {e.status}")
            return {"CANCELLED"}

        _ = Path(f"{data}/all_visors.json")

        return {"FINISHED"}


class DumpFilesOperator(Operator):
    bl_idname = "ekur.dumpfiles"
    bl_label = "Dump Required Files"

    def execute(self, context: Context | None) -> set[str]:
        data: EkurPreferences = context.preferences.addons["bl_ext.user_default.ekur"].preferences
        ekur_save_path = Path(f"{data.data_folder}/ekur")
        ekur_url = f"https://github.com/Surasia/ekur/releases/download/{package_version_string}/ekur-{package_version_string}"
        if platform.system() == "Windows":
            ekur_save_path = Path(f"{ekur_save_path}.exe")
            ekur_url = f"{ekur_url}.exe"

        if not ekur_save_path.exists():
            try:
                with (
                    urllib.request.urlopen(ekur_url) as response,
                    open(ekur_save_path, "wb") as out_file,
                ):
                    _ = out_file.write(response.read())
            except urllib.error.HTTPError as e:
                logging.error(f"Failed to download ekur: {e.status}")
                return {"CANCELLED"}

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
        _ = box2.operator("ekur.downloadfiles")
        _ = box2.operator("ekur.dumpfiles")


def register():
    register_class(ImportMaterialOperator)
    register_class(CoatingImportPanel)
    register_class(EkurPreferences)
    register_class(ImportProperties)
    register_class(RandomizeCoatingOperator)
    register_class(DownloadFilesOperator)
    register_class(DumpFilesOperator)
    register_class(ImportModelOperator)
    bpy.types.Scene.import_properties = bpy.props.PointerProperty(type=ImportProperties)  # pyright: ignore[reportAttributeAccessIssue]


def unregister():
    unregister_class(ImportMaterialOperator)
    unregister_class(EkurPreferences)
    unregister_class(CoatingImportPanel)
    unregister_class(ImportProperties)
    unregister_class(RandomizeCoatingOperator)
    unregister_class(DownloadFilesOperator)
    unregister_class(DumpFilesOperator)
    unregister_class(ImportModelOperator)
    del bpy.types.Scene.import_properties  # pyright: ignore[reportAttributeAccessIssue]
