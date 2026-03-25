# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
"""
Ekur - A multi-purpose importer for Halo Infinite.
"""

from pathlib import Path
from typing import cast, final

import bpy
from bpy.types import AddonPreferences, Context
from bpy.utils import (
    register_class,
    unregister_class,
)

from .src.constants import version, version_string  # ty:ignore[unresolved-import]
from .src.operators.bake_operator import (  # ty:ignore[unresolved-import]
    AdvancedBakeOperator,
    AlignBakeOperator,
    BakingOperator,
)
from .src.operators.download_files_operator import (  # ty:ignore[unresolved-import]
    DownloadFilesOperator,
)
from .src.operators.dump_files_operator import DumpFilesOperator  # ty:ignore[unresolved-import]
from .src.operators.forge_map_operator import ForgeMapOperator  # ty:ignore[unresolved-import]
from .src.operators.forge_operator import ForgeOperator  # ty:ignore[unresolved-import]
from .src.operators.level_operator import ImportLevelOperator  # ty:ignore[unresolved-import]
from .src.operators.material_operator import ImportMaterialOperator  # ty:ignore[unresolved-import]
from .src.operators.model_operator import ImportModelOperator  # ty:ignore[unresolved-import]
from .src.operators.randomize_coating import (  # ty:ignore[unresolved-import]
    RandomizeCoatingOperator,
)
from .src.operators.spartan_online_operator import (  # ty:ignore[unresolved-import]
    ImportSpartanVanityOperator,
)
from .src.operators.spartan_operator import ImportSpartanOperator  # ty:ignore[unresolved-import]
from .src.ui.bake_options import BakeOptions  # ty:ignore[unresolved-import]
from .src.ui.forge_map_options import ForgeMapOptions  # ty:ignore[unresolved-import]
from .src.ui.forge_object_options import ForgeObjectOptions  # ty:ignore[unresolved-import]
from .src.ui.import_panel import EkurImportPanel  # ty:ignore[unresolved-import]
from .src.ui.level_options import LevelOptions  # ty:ignore[unresolved-import]
from .src.ui.material_options import MaterialOptions  # ty:ignore[unresolved-import]
from .src.ui.model_options import ModelOptions  # ty:ignore[unresolved-import]
from .src.ui.spartan_options import SpartanOptions  # ty:ignore[unresolved-import]
from .src.utils import get_package_name  # ty:ignore[unresolved-import]

bl_info = {
    "name": "Ekur",
    "description": "A multi-purpose importer for Halo Infinite.",
    "author": "Surasia",
    "version": version,
    "blender": (4, 3, 0),
    "category": "Import-Export",
    "support": "COMMUNITY",
}


def dump_exists() -> bool:
    extension_path = bpy.utils.extension_path_user(get_package_name(), create=True)
    return (Path(extension_path) / version_string).exists()


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

    debug: bpy.props.BoolProperty(
        name="Debug Print",
        description="Enable this if you're trying to troubleshoot issues with Ekur.",
        default=False,
    )

    def draw(self, _context: Context | None):
        layout = self.layout
        if not dump_exists():
            layout.label(
                icon="ERROR",
                text="You have not yet dumped the required files for this version!",
            )
        if not bpy.app.online_access:
            layout.label(
                icon="ERROR",
                text="Online access is disabled! Enable it in System < Network < Allow Online Access",
            )
            return
        box = layout.box()
        box.label(text="Paths", icon="FILE_FOLDER")
        box.prop(self, "data_folder")
        box.prop(self, "deploy_folder")
        box.prop(self, "dump_textures")
        box.prop(self, "is_campaign")
        box.prop(self, "debug")
        box2 = layout.box()
        _ = box2.operator("ekur.downloadfiles")
        _ = box2.operator("ekur.dumpfiles")


def register():
    register_class(ImportMaterialOperator)
    register_class(EkurImportPanel)
    register_class(EkurPreferences)
    register_class(RandomizeCoatingOperator)
    register_class(DownloadFilesOperator)
    register_class(DumpFilesOperator)
    register_class(ImportModelOperator)
    register_class(ImportSpartanOperator)
    register_class(ImportLevelOperator)
    register_class(ForgeOperator)
    register_class(ImportSpartanVanityOperator)
    register_class(ForgeMapOperator)
    register_class(BakingOperator)
    register_class(AdvancedBakeOperator)
    register_class(AlignBakeOperator)
    register_class(MaterialOptions)
    register_class(ModelOptions)
    register_class(SpartanOptions)
    register_class(ForgeObjectOptions)
    register_class(ForgeMapOptions)
    register_class(BakeOptions)
    register_class(LevelOptions)
    bpy.types.Scene.material_properties = bpy.props.PointerProperty(type=MaterialOptions)  # ty: ignore[unresolved-attribute]
    bpy.types.Scene.model_properties = bpy.props.PointerProperty(type=ModelOptions)  # ty: ignore[unresolved-attribute]
    bpy.types.Scene.spartan_properties = bpy.props.PointerProperty(type=SpartanOptions)  # ty: ignore[unresolved-attribute]
    bpy.types.Scene.forge_map_properties = bpy.props.PointerProperty(type=ForgeMapOptions)  # ty: ignore[unresolved-attribute]
    bpy.types.Scene.forge_object_properties = bpy.props.PointerProperty(type=ForgeObjectOptions)  # ty: ignore[unresolved-attribute]
    bpy.types.Scene.bake_properties = bpy.props.PointerProperty(type=BakeOptions)  # ty: ignore[unresolved-attribute]
    bpy.types.Scene.level_properties = bpy.props.PointerProperty(type=LevelOptions)  # ty: ignore[unresolved-attribute]


def unregister():
    unregister_class(ImportMaterialOperator)
    unregister_class(EkurImportPanel)
    unregister_class(EkurPreferences)
    unregister_class(RandomizeCoatingOperator)
    unregister_class(DownloadFilesOperator)
    unregister_class(DumpFilesOperator)
    unregister_class(ImportModelOperator)
    unregister_class(ImportSpartanOperator)
    unregister_class(ImportLevelOperator)
    unregister_class(ForgeOperator)
    unregister_class(ImportSpartanVanityOperator)
    unregister_class(ForgeMapOperator)
    unregister_class(BakingOperator)
    unregister_class(AdvancedBakeOperator)
    unregister_class(AlignBakeOperator)
    unregister_class(MaterialOptions)
    unregister_class(ModelOptions)
    unregister_class(SpartanOptions)
    unregister_class(ForgeObjectOptions)
    unregister_class(ForgeMapOptions)
    unregister_class(BakeOptions)
    del bpy.types.Scene.material_properties  # ty: ignore[unresolved-attribute]
    del bpy.types.Scene.model_properties  # ty: ignore[unresolved-attribute]
    del bpy.types.Scene.spartan_properties  # ty: ignore[unresolved-attribute]
    del bpy.types.Scene.forge_object_properties  # ty: ignore[unresolved-attribute]
    del bpy.types.Scene.forge_map_properties  # ty: ignore[unresolved-attribute]
    del bpy.types.Scene.bake_properties  # ty: ignore[unresolved-attribute]
    del bpy.types.Scene.level_properties  # ty: ignore[unresolved-attribute]
