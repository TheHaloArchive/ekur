# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import logging
import platform
import subprocess
from pathlib import Path
from typing import final

import bpy
from bpy.types import Context, Operator

from ..constants import version_string
from ..utils import debug_print, get_addon_preferences, get_data_folder, get_package_name


@final
class DumpFilesOperator(Operator):
    bl_idname = "ekur.dumpfiles"
    bl_label = "Dump Required Files"
    bl_description = "Dump"

    def execute(self, context: Context | None) -> set[str]:  # ty:ignore[invalid-method-override]
        if context is None:
            return {"CANCELLED"}
        data = get_data_folder()
        prefs = get_addon_preferences()

        extension_path = bpy.utils.extension_path_user(get_package_name(), create=True)

        save_path = f"{extension_path}/strings.txt"
        mapid_path = f"{extension_path}/map_ids.txt"
        modelid_path = f"{extension_path}/model_ids.txt"
        ekur_save_path = Path(f"{extension_path}/ekur-{version_string}")
        if platform.system() == "Windows":
            ekur_save_path = Path(f"{ekur_save_path}.exe")

        proc = [
            str(ekur_save_path),
            "--save-path",
            data,
            "--module-path",
            prefs.deploy_folder,
            "--strings-path",
            save_path,
            "--mapid-path",
            mapid_path,
            "--modelid-path",
            modelid_path,
        ]
        if not prefs.dump_textures:
            proc.append("--skip-bitmaps")
        if prefs.is_campaign:
            proc.append("--is-campaign")
        if not ekur_save_path.exists():
            logging.error(f"Ekur was not found at {ekur_save_path}!")
            return {"CANCELLED"}

        debug_print(f"[dump_files_operator.py] proc: {proc}")
        _ = subprocess.run(proc)
        with open(f"{extension_path}/{version_string}", "w") as f:
            _ = f.write(version_string)
        return {"FINISHED"}
