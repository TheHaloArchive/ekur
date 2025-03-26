# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia

# pyright: reportUnknownMemberType=false, reportUninitializedInstanceVariable=false
"""
Ekur - A multi-purpose importer for Halo Infinite.
"""

if __name__ == "addon":
    pass
else:
    from pathlib import Path
    from typing import cast, final
    import bpy
    from bpy.types import AddonPreferences, Context
    from bpy.utils import register_class, unregister_class  # pyright: ignore[reportUnknownVariableType]

    from .src.utils import get_package_name
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
    from .src.operators.bake_operator import BakingOperator, AdvancedBakeOperator, AlignBakeOperator
    from .src.constants import version, version_string

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

        def draw(self, _context: Context | None):
            layout = self.layout
            if not dump_exists():
                layout.label(
                    icon="ERROR",
                    text="You have not yet dumped the required files for this version!",
                )
            if not cast(bool, bpy.app.online_access):
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
        register_class(BakingOperator)
        register_class(AdvancedBakeOperator)
        register_class(AlignBakeOperator)
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
        unregister_class(BakingOperator)
        unregister_class(AdvancedBakeOperator)
        unregister_class(AlignBakeOperator)
        del bpy.types.Scene.import_properties  # pyright: ignore[reportAttributeAccessIssue]
