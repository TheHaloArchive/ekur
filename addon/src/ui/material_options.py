# pyright: reportUninitializedInstanceVariable=false, reportUnknownVariableType=false, reportUnknownMemberType=false
import logging
from pathlib import Path
from typing import cast
import bpy
from bpy.props import BoolProperty, EnumProperty, StringProperty
from bpy.types import Context, PropertyGroup, UILayout

from ..utils import get_data_folder, get_package_name, natural_sort_key, read_json_file
from ..json_definitions import CommonLayer, CommonMaterial, CommonStyleList

visor_cache: list[tuple[str, str, str]] | None = None
styles_cache: dict[str, CommonStyleList] | None = None
style_cache: dict[str, list[tuple[str, str, str]]] | None = None


def get_styles(context: Context) -> tuple[str, CommonStyleList] | None:
    """Get the styles for the current material slot selected.

    Args:
        context: Blender context used to access preferences.

    Returns:
        Return a list of styles for the current material slot selected if it exists.
    """
    global styles_cache
    data = get_data_folder()
    if (
        context.object is not None
        and context.object.active_material_index is not None
        and context.object.active_material_index < len(context.object.material_slots)
    ):
        bl_material = context.object.material_slots[context.object.active_material_index]
        if styles_cache and bl_material.name in styles_cache:
            return (bl_material.name, styles_cache[bl_material.name])

        definition_path = Path(f"{data}/materials/{bl_material.name.split('.')[0]}.json")
        if not definition_path.exists():
            logging.warning(f"Material path does not exist!: {definition_path}")
            return
        material = read_json_file(definition_path, CommonMaterial)
        if material is None:
            return
        if material["style_info"]:
            styles_path = Path(f"{data}/stylelists/{material['style_info']['stylelist']}.json")
            styles = read_json_file(styles_path, CommonStyleList)
            if styles is None:
                return
            styles_cache = {bl_material.name: styles}
            return (bl_material.name, styles)

    return


class MaterialSelectionLogic:
    def common_styles(self, context: Context | None) -> list[tuple[str, str, str]]:
        global style_cache
        all_styles: list[tuple[str, str, str]] = []
        import_properties = get_material_options()
        if context:
            styles = get_styles(context)
            if styles:
                if style_cache and styles[0] in style_cache:
                    return style_cache[styles[0]]
                for style, entry in styles[1]["styles"].items():
                    all_styles.append((style, entry["name"], ""))
                if import_properties.sort_by_name:
                    all_styles.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
                style_cache = {styles[0]: all_styles}
        return all_styles

    def visors(self, _context: Context | None) -> list[tuple[str, str, str]]:
        global visor_cache
        if visor_cache:
            return visor_cache
        all_visors: list[tuple[str, str, str]] = []
        extension_path = bpy.utils.extension_path_user(get_package_name(), create=True)
        properties = get_material_options()

        visors_path = Path(f"{extension_path}/all_visors.json")
        if not visors_path.exists():
            return all_visors
        visors = read_json_file(visors_path, dict[str, CommonLayer])
        if visors is None:
            return all_visors
        for name, _ in visors.items():
            all_visors.append((name, name, ""))
        if properties.sort_by_name:
            all_visors.sort(key=natural_sort_key)  # pyright: ignore[reportArgumentType, reportCallIssue]
        visor_cache = all_visors
        return all_visors


class MaterialOptions(PropertyGroup):
    use_default_coating: BoolProperty(
        name="Use Default Coating",
        description="Whether or not to enable the menu to select a custom coating.",
        default=True,
    )
    coating: EnumProperty(
        name="Coating",
        description="Coating to import.",
        items=MaterialSelectionLogic.common_styles,
    )
    coating_id: StringProperty(
        name="[Advanced] Coating ID Override",
        description="Coating ID to prioritize over selection.",
        default="",
    )
    disable_damage: BoolProperty(
        name="Disable Damage/Dirt",
        description="Disables Zone 7 or 4, usually being the damage (grime) swatch.",
        default=False,
    )
    selected_only: BoolProperty(
        name="Selected Only", description="Import coatings on selected objects only.", default=True
    )
    sort_by_name: BoolProperty(
        name="Sort by Name", description="Sorts coating and visors by name.", default=True
    )
    flip_alpha: BoolProperty(
        name="Flip Alpha", description="Flip the alpha channel of the ASG texture.", default=True
    )
    override_visor: BoolProperty(
        name="Override Visor", description="Enables visor import menu.", default=False
    )
    visor: EnumProperty(
        name="Visor", description="Visor to import.", items=MaterialSelectionLogic.visors
    )


class MaterialOptionsType:
    use_default_coating: bool = True
    coating: str = ""
    coating_id: str = ""
    disable_damage: bool = False
    selected_only: bool = True
    sort_by_name: bool = True
    flip_alpha: bool = True
    override_visor: bool = True
    visor: str = ""


def get_material_options() -> MaterialOptionsType:
    if bpy.context.scene is None:
        return MaterialOptionsType()
    props: MaterialOptions = bpy.context.scene.material_properties  # pyright: ignore[reportAttributeAccessIssue]
    if props:
        return cast(MaterialOptionsType, props)
    return MaterialOptionsType()


def draw_material_options(layout: UILayout, props: MaterialOptionsType) -> None:
    material_header, material_body = layout.panel("VIEW3D_PT_import_material", default_closed=True)
    material_header.label(icon="MATERIAL", text="Import Material")

    if material_body:
        options = material_body.box()
        options.prop(props, "use_default_coating")
        if not props.use_default_coating:
            box2 = options.box()
            box2.prop(props, "coating")
            box2.prop(props, "coating_id")
            box2.prop(props, "sort_by_name")
            _ = box2.operator("ekur.randomize")
        options.prop(props, "disable_damage")
        options.prop(props, "selected_only")
        options.prop(props, "flip_alpha")
        options.prop(props, "override_visor")
        if props.override_visor:
            options.prop(props, "visor")
        _ = material_body.operator("ekur.importmaterial")
