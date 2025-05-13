# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
import platform
import bpy

from typing import cast, final
from bpy.types import Context, Operator

from ..utils import download_file, get_package_name
from ..constants import version_string

STRINGS_URL = "https://github.com/Surasia/ReclaimerFiles/raw/refs/heads/master/strings.txt"
EKUR = "https://github.com/TheHaloArchive/ekur/raw/refs/heads/master/assets"
REGIONS_URL = f"{EKUR}/regions_and_permutations.json"
CUSTOM_RIG_URL = f"{EKUR}/purp.blend"
VISORS_URL = f"{EKUR}/all_visors.json"


@final
class DownloadFilesOperator(Operator):
    bl_idname = "ekur.downloadfiles"
    bl_label = "Download Required Files"

    def execute(self, context: Context | None) -> set[str]:
        if context is None or not cast(bool, bpy.app.online_access):
            logging.error("Online access is disabled")
            return {"CANCELLED"}
        extension_path = bpy.utils.extension_path_user(get_package_name(), create=True)
        ekur_save_path = f"{extension_path}/ekur-{version_string}"
        save_path = f"{extension_path}/strings.txt"
        visors_path = f"{extension_path}/all_visors.json"
        regions_path = f"{extension_path}/regions_and_permutations.json"
        customs_path = f"{extension_path}/purp.blend"

        ekur_url = f"https://github.com/TheHaloArchive/ekur/releases/download/{version_string}/ekur-{version_string}"
        if platform.system() == "Windows":
            ekur_save_path = f"{ekur_save_path}.exe"
            ekur_url = f"{ekur_url}.exe"

        download_file(ekur_url, ekur_save_path)
        download_file(STRINGS_URL, save_path)
        download_file(CUSTOM_RIG_URL, customs_path)
        download_file(VISORS_URL, visors_path)
        download_file(REGIONS_URL, regions_path)

        return {"FINISHED"}
