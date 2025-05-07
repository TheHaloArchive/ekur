from random import choice
from typing import final
from bpy.types import Context, Operator

from ..ui.material_options import get_material_options, get_styles


@final
class RandomizeCoatingOperator(Operator):
    """Operator to randomize the coating style on the selected material."""

    bl_idname = "ekur.randomize"
    bl_label = "Surprise Me"

    def execute(self, context: Context) -> set[str]:
        """Select a random style from the available styles.

        Args:
            context: Blender context used to access import properties
        """
        styles = get_styles(context)
        if styles:
            props = get_material_options()
            props.coating_id = choice(list(styles[1]["styles"].keys()))

        return {"FINISHED"}
