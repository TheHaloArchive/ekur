# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from pathlib import Path
from typing import final
from bpy.types import Context, Operator

from ..ui.animation_options import get_animation_options
from ..model.importer.animation.importer import import_animation
from ..model.importer.animation.anim_data import AnimationData

def import_anim(context: Context, path: str) -> None:
    selected_mesh = context.active_object
    if selected_mesh is None:
        return None
    anim_path = Path(path)
    if not anim_path.exists():
        return None
    with open(anim_path, "rb") as f:
        animation = AnimationData()
        animation.read(f)
        import_animation(selected_mesh, animation, anim_path.stem)

@final
class AnimationOperator(Operator):
    """Operator to import animation from a file."""

    bl_idname = "ekur.importanimation"
    bl_description = "Import Animation"
    bl_label = "Import Animation"

    def execute(self, context: Context) -> set[str]:  # ty:ignore[invalid-method-override]
        """Import animation from a file.

        Args:
            context: Blender context used to access import properties
        """
        animation_options = get_animation_options()
        if animation_options.bulk_import:
            path = animation_options.bulk_directory
            anim_path = Path(path)
            if not anim_path.exists():
                return {"CANCELLED"}
            for file in anim_path.glob("*.ekuranim"):
                import_anim(context, str(file))
        else:
            import_anim(context, animation_options.animation_path)
        return {"FINISHED"}
