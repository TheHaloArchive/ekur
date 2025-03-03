# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from pathlib import Path
import platform
import subprocess
from typing import final

from bpy.types import Context, Operator

from ..utils import get_addon_preferences, get_data_folder
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

        save_path = f"{data}/strings.txt"
        ekur_save_path = Path(f"{data}/ekur-{version_string}")
        if platform.system() == "Windows":
            ekur_save_path = Path(f"{ekur_save_path}.exe")

        save_path = f"{data}/strings.txt"
        proc = [
            ekur_save_path,
            "--save-path",
            data,
            "--module-path",
            prefs.deploy_folder,
            "--strings-path",
            save_path,
        ]
        if not prefs.dump_textures:
            proc.append("--skip-bitmaps")

        _ = subprocess.run(proc)
        return {"FINISHED"}
