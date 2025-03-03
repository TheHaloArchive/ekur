# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
from pathlib import Path
import platform
from typing import final
import urllib.error
import urllib.request

from bpy.types import Context, Operator

from ..utils import get_data_folder
from ..constants import version_string

STRINGS_URL = "https://github.com/Surasia/ReclaimerFiles/raw/refs/heads/master/strings.txt"
VISORS_URL = "https://github.com/Surasia/ekur/raw/refs/heads/master/assets/all_visors.json"
REGIONS_URL = (
    "https://github.com/Surasia/ekur/raw/refs/heads/master/assets/regions_and_permutations.json"
)


@final
class DownloadFilesOperator(Operator):
    bl_idname = "ekur.downloadfiles"
    bl_label = "Download Required Files"

    def execute(self, context: Context | None) -> set[str]:
        if context is None:
            return {"CANCELLED"}

        data = get_data_folder()
        save_path = f"{data}/strings.txt"
        visors_path = f"{data}/all_visors.json"
        regions_path = f"{data}/regions_and_permutations.json"
        ekur_save_path = Path(f"{data}/ekur-{version_string}")

        ekur_url = f"https://github.com/Surasia/ekur/releases/download/{version_string}/ekur-{version_string}"
        if platform.system() == "Windows":
            ekur_save_path = Path(f"{ekur_save_path}.exe")
            ekur_url = f"{ekur_url}.exe"

        if not ekur_save_path.exists():
            try:
                with (
                    urllib.request.urlopen(ekur_url) as response,  # pyright: ignore[reportAny]
                    open(ekur_save_path, "wb") as out_file,
                ):
                    _ = out_file.write(response.read())  # pyright: ignore[reportAny]
            except urllib.error.HTTPError as e:
                logging.error(f"Failed to download ekur: {e.status}")
                return {"CANCELLED"}

        try:
            with (
                urllib.request.urlopen(STRINGS_URL) as response,  # pyright: ignore[reportAny]
                open(save_path, "wb") as out_file,
            ):
                _ = out_file.write(response.read())  # pyright: ignore[reportAny]
        except urllib.error.HTTPError as e:
            logging.error(f"Failed to download strings.txt: {e}")
            return {"CANCELLED"}

        try:
            with (
                urllib.request.urlopen(VISORS_URL) as response,  # pyright: ignore[reportAny]
                open(visors_path, "w") as out_file,
            ):
                _ = out_file.write(response.read().decode("utf-8"))  # pyright: ignore[reportAny]
        except urllib.error.HTTPError as e:
            logging.error(f"Failed to download all_visors.json: {e.status}")
            return {"CANCELLED"}

        try:
            with (
                urllib.request.urlopen(REGIONS_URL) as response,  # pyright: ignore[reportAny]
                open(regions_path, "w") as out_file,
            ):
                _ = out_file.write(response.read().decode("utf-8"))  # pyright: ignore[reportAny]
        except urllib.error.HTTPError as e:
            logging.error(f"Failed to download regions_and_permutations.json: {e.status}")
            return {"CANCELLED"}

        return {"FINISHED"}
