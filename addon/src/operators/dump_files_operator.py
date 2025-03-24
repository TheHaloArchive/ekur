# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
from pathlib import Path
import platform
import subprocess
from typing import final

import bpy
from bpy.types import Context, Operator

from ..utils import get_addon_preferences, get_data_folder, get_package_name
from ..constants import version_string


@final
class DumpFilesOperator(Operator):
    bl_idname = "ekur.dumpfiles"
    bl_label = "Dump Required Files"

    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}
        data = get_data_folder()
        prefs = get_addon_preferences()

        extension_path = bpy.utils.extension_path_user(get_package_name(), create=True)

        save_path = f"{extension_path}/strings.txt"
        ekur_save_path = Path(f"{extension_path}/ekur-{version_string}")
        if platform.system() == "Windows":
            ekur_save_path = Path(f"{ekur_save_path}.exe")

        save_path = f"{extension_path}/strings.txt"
        proc = [
            str(ekur_save_path),
            "--save-path",
            data,
            "--module-path",
            prefs.deploy_folder,
            "--strings-path",
            save_path,
        ]
        if not prefs.dump_textures:
            proc.append("--skip-bitmaps")
        if prefs.is_campaign:
            proc.append("--is-campaign")
        if not ekur_save_path.exists():
            logging.error(f"Ekur was not found at {ekur_save_path}!")
            return {"CANCELLED"}
        _ = subprocess.run(proc)
        with open(f"{extension_path}/{version_string}", "w") as f:
            _ = f.write(version_string)
        return {"FINISHED"}
