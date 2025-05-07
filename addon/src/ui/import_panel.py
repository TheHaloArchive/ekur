# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia

from typing import final

from bpy.types import Context, Panel

from .level_options import draw_level_options, get_level_options
from .bake_options import draw_bake_menu_options, get_bake_options
from .forge_map_options import draw_forge_map_options, get_forge_map_options
from .forge_object_options import draw_forge_object_options, get_forge_object_options
from .spartan_options import draw_spartan_options, get_spartan_options
from .model_options import draw_model_options, get_model_options
from .material_options import draw_material_options, get_material_options
from ..utils import get_addon_preferences

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
        draw_material_options(layout, get_material_options())
        draw_model_options(layout, get_model_options())
        draw_level_options(layout, get_level_options())
        if not prefs.is_campaign:
            draw_spartan_options(layout, get_spartan_options())
        if not prefs.is_campaign:
            draw_forge_object_options(layout, get_forge_object_options())
        draw_forge_map_options(layout, get_forge_map_options())
        draw_bake_menu_options(layout, get_bake_options())
