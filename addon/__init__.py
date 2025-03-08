# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia

# pyright: reportUnknownMemberType=false, reportUninitializedInstanceVariable=false
"""
Ekur - A multi-purpose importer for Halo Infinite.
"""

from typing import cast, final
import bpy
from bpy.types import AddonPreferences, Context
from bpy.utils import register_class, unregister_class  # pyright: ignore[reportUnknownVariableType]


from .src.operators.material_operator import ImportMaterialOperator
from .src.ui.import_panel import CoatingImportPanel, ImportProperties, RandomizeCoatingOperator
from .src.operators.dump_files_operator import DumpFilesOperator
from .src.operators.model_operator import ImportModelOperator
from .src.operators.spartan_operator import ImportSpartanOperator
from .src.operators.level_operator import ImportLevelOperator
from .src.operators.forge_operator import ForgeOperator
from .src.operators.spartan_online_operator import ImportSpartanVanityOperator
from .src.operators.download_files_operator import DownloadFilesOperator
from .src.operators.forge_map_operator import ForgeMapOperator
from .src.constants import version

bl_info = {
    "name": "Ekur",
    "description": "A multi-purpose importer for Halo Infinite.",
    "author": "Surasia",
    "version": version,
    "blender": (4, 3, 0),
    "category": "Import-Export",
    "support": "COMMUNITY",
}


@final
class EkurPreferences(AddonPreferences):
    bl_idname = cast(str, __package__)

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

    dump_textures: bpy.props.BoolProperty(
        name="Dump Textures",
        description="Whether to dump textures or not. This can speed up the dumping process if you have already done it once.",
        default=True,
    )

    is_campaign: bpy.props.BoolProperty(
        name="Is Campaign",
        description="Whether the deploy folder is for campaign or not",
        default=False,
    )

    enable_forge: bpy.props.BoolProperty(
        name="Enable Forge Map Importer",
        description="Whether to enable Forge map importer or not. Please note that this is experimental and may not work as expected.",
        default=False,
    )

    def draw(self, _context: Context | None):
        layout = self.layout
        box = layout.box()
        box.label(text="Paths", icon="FILE_FOLDER")
        box.prop(self, "data_folder")
        box.prop(self, "deploy_folder")
        box.prop(self, "dump_textures")
        box.prop(self, "is_campaign")
        experimental_box = box.box()
        experimental_box.label(text="Experimental", icon="ERROR")
        experimental_box.prop(self, "enable_forge")
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
    register_class(ImportSpartanOperator)
    register_class(ImportLevelOperator)
    register_class(ForgeOperator)
    register_class(ImportSpartanVanityOperator)
    register_class(ForgeMapOperator)
    bpy.types.Scene.import_properties = bpy.props.PointerProperty(type=ImportProperties)  # pyright: ignore[reportAttributeAccessIssue]


def unregister():
    unregister_class(ImportMaterialOperator)
    unregister_class(CoatingImportPanel)
    unregister_class(EkurPreferences)
    unregister_class(ImportProperties)
    unregister_class(RandomizeCoatingOperator)
    unregister_class(DownloadFilesOperator)
    unregister_class(DumpFilesOperator)
    unregister_class(ImportModelOperator)
    unregister_class(ImportSpartanOperator)
    unregister_class(ImportLevelOperator)
    unregister_class(ForgeOperator)
    unregister_class(ImportSpartanVanityOperator)
    unregister_class(ForgeMapOperator)
    del bpy.types.Scene.import_properties  # pyright: ignore[reportAttributeAccessIssue]
