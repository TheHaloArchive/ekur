# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from typing import final

from bpy.types import Context, Panel

from ..utils import get_addon_preferences
from .bake_options import draw_bake_menu_options, get_bake_options
from .forge_map_options import draw_forge_map_options, get_forge_map_options
from .forge_object_options import draw_forge_object_options, get_forge_object_options
from .level_options import draw_level_options, get_level_options
from .material_options import draw_material_options, get_material_options
from .model_options import draw_model_options, get_model_options
from .spartan_options import draw_spartan_options, get_spartan_options
from .vanity_options import draw_vanity_options, get_vanity_options

__all__ = ["EkurImportPanel"]


@final
class EkurImportPanel(Panel):
    bl_idname = "VIEW3D_PT_ekur_import"
    bl_label = "Ekur"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ekur"

    def draw(self, context: Context | None) -> None:
        layout = self.layout
        if layout is None or context is None:
            return
        prefs = get_addon_preferences()
        generic_header, generic_body = layout.panel("VIEW3D_PT_import_generic")
        generic_header.label(text="General")
        if generic_body:
            draw_material_options(generic_body, get_material_options())
            draw_model_options(generic_body, get_model_options())
            draw_level_options(generic_body, get_level_options())
        spartan_header, spartan_body = layout.panel("VIEW3D_PT_import_spartan")
        spartan_header.label(text="Spartan")
        if spartan_body:
            if not prefs.is_campaign:
                draw_spartan_options(spartan_body, get_spartan_options())
                draw_vanity_options(spartan_body, get_vanity_options())
        if not prefs.is_campaign:
            forge_header, forge_body = layout.panel("VIEW3D_PT_import_forgep")
            forge_header.label(text="Forge")
            if forge_body:
                draw_forge_object_options(forge_body, get_forge_object_options())
                draw_forge_map_options(forge_body, get_forge_map_options())
        misc_header, misc_body = layout.panel("VIEW3D_PT_import_misc")
        misc_header.label(text="Miscellaneous")
        if misc_body:
            draw_bake_menu_options(misc_body, get_bake_options())
