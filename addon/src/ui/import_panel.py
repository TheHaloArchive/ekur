# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia

# pyright: reportUnknownMemberType=false, reportUninitializedInstanceVariable=false
import random
from typing import final

from bpy.props import BoolProperty, EnumProperty, StringProperty  # pyright: ignore[reportUnknownVariableType]
from bpy.types import Context, Panel, PropertyGroup, Operator

from ..utils import ImportPropertiesType, get_addon_preferences, get_import_properties
from .import_utils import GrabStrings, get_styles

__all__ = ["RandomizeCoatingOperator", "ImportProperties", "CoatingImportPanel"]


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
            props = get_import_properties()
            props.coat_id = random.choice(list(styles[1]["styles"].keys()))

        return {"FINISHED"}


class ImportProperties(PropertyGroup):
    use_default: BoolProperty(
        name="Use Default Coating",
        description="Whether or not to enable the menu to select a custom coating.",
        default=True,
    )
    coat_id: StringProperty(
        name="Coating ID Override",
        description="Advanced: coating id (m_identifier) from cylix.guide",
        default="",
    )
    toggle_damage: BoolProperty(
        name="Disable Damage",
        description="Disables Zone 7 or 4, usually being the damage swatch.",
        default=False,
    )
    selected_only: BoolProperty(
        name="Selected Only", description="Import coatings for selected objects only.", default=True
    )
    sort_by_name: BoolProperty(
        name="Sort by Name", description="Sorts coating and visors by name.", default=True
    )
    flip_alpha: BoolProperty(
        name="Flip Alpha", description="Flip the alpha channel of the ASG texture.", default=False
    )
    coatings: EnumProperty(
        name="Coating",
        description="Coating to import onto object.",
        items=GrabStrings.common_styles,
    )
    toggle_visors: BoolProperty(
        name="Override Visor", description="Enables visor import menu.", default=False
    )
    visors: EnumProperty(
        name="Visor", description="Visor to import onto helmet visors.", items=GrabStrings.visors
    )
    model_path: StringProperty(
        default="",
        name="Model Path",
        description="Path to .ekur model file to import.",
        subtype="FILE_PATH",
    )
    import_materials: BoolProperty(
        name="Import Materials",
        description="Whether to import material slots for model.",
        default=True,
    )
    import_markers: BoolProperty(
        name="Import Markers",
        description="Whether to import markers as empties for model.",
        default=True,
    )
    import_bones: BoolProperty(
        name="Import Bones", description="Import armatures and weight data for model.", default=True
    )
    import_collections: BoolProperty(
        name="Import Collections",
        description="Sort model regions and permutations into collections",
        default=True,
    )
    import_vertex_color: BoolProperty(
        name="Import Vertex Color",
        description="Whether to import vertex color as a mesh attribute for models that support it.",
        default=False,
    )
    level_path: StringProperty(
        default="",
        name="Level Path",
        description="Path to .json level file to import.",
        subtype="FILE_PATH",
    )
    import_specific_core: BoolProperty(
        name="Import Specific Core",
        description="Whether to filter out a specific armor core for spartans.",
        default=False,
    )
    import_names: BoolProperty(
        name="Import Names of Armor Pieces",
        description="Whether to replace object name hashes with their proper in-game names",
        default=True,
    )
    use_purp_rig: BoolProperty(
        default=True,
        description="Whether to use Purplmunkii's IK/FK Control rig for spartans.",
        name="Use Purp's IK Rig",
    )
    gamertag: StringProperty(
        name="Gamertag", description="Gamertag of the spartan you want to import.", default=""
    )
    body_type: EnumProperty(
        name="Body Type",
        description="Body type of the spartan you want to import.",
        items=[
            ("Body Type 1", "Body Type 1", ""),
            ("Body Type 2", "Body Type 2", ""),
            ("Body Type 3", "Body Type 3", ""),
        ],
    )
    left_arm: EnumProperty(
        name="Left Arm",
        description="Prosthesis for the left arm.",
        items=[
            ("None", "None", ""),
            ("Transhumeral", "Transhumeral", ""),
            ("Transradial", "Transradial", ""),
            ("Hand", "Hand", ""),
        ],
    )
    right_arm: EnumProperty(
        name="Right Arm",
        description="Prosthesis for the right arm.",
        items=[
            ("None", "None", ""),
            ("Transhumeral", "Transhumeral", ""),
            ("Transradial", "Transradial", ""),
            ("Hand", "Hand", ""),
        ],
    )
    left_leg: EnumProperty(
        name="Left Leg",
        description="Prosthesis for the left leg.",
        items=[
            ("None", "None", ""),
            ("Transfemoral", "Transfemoral", ""),
        ],
    )
    right_leg: EnumProperty(
        name="Right Leg",
        description="Prosthesis for the right leg.",
        items=[
            ("None", "None", ""),
            ("Transfemoral", "Transfemoral", ""),
        ],
    )
    core: EnumProperty(
        name="Core", description="Specific armor core you want to import.", items=GrabStrings.cores
    )
    root_category: EnumProperty(
        name="Root Category", description="", items=GrabStrings.root_categories
    )
    subcategory: EnumProperty(name="Subcategory", items=GrabStrings.subcategories)
    objects: EnumProperty(name="Object", items=GrabStrings.objects)
    object_representation: EnumProperty(
        name="Object Representation", items=GrabStrings.object_representations
    )
    sort_objects: BoolProperty(name="Sort Objects By Name", default=True)
    asset_id: StringProperty(name="Asset ID", default="")
    version_id: StringProperty(name="Version ID", default="")


@final
class CoatingImportPanel(Panel):
    bl_idname = "VIEW3D_PT_coating_import"
    bl_label = "Ekur"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ekur"

    def draw(self, context: Context | None) -> None:
        layout = self.layout
        if layout is None:
            return
        import_properties = get_import_properties()
        prefs = get_addon_preferences()
        self.draw_material_options(import_properties)
        self.draw_model_options(import_properties)
        if not prefs.is_campaign:
            self.draw_ocgd(import_properties)
        self.draw_level(import_properties)
        if not prefs.is_campaign:
            self.draw_forge(context, import_properties)
        if prefs.enable_forge:
            self.draw_forge_map(import_properties)

    def draw_material_options(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        material_header, material_body = layout.panel("VIEW3D_PT_import_material")
        material_header.label(icon="MATERIAL", text="Import Material")

        if material_body:
            options = material_body.box()
            options.prop(import_properties, "use_default")
            if not import_properties.use_default:
                box2 = options.box()
                box2.prop(import_properties, "coatings")
                box2.prop(import_properties, "coat_id")
                box2.prop(import_properties, "sort_by_name")
                _ = box2.operator("ekur.randomize")
            options.prop(import_properties, "toggle_damage")
            options.prop(import_properties, "selected_only")
            options.prop(import_properties, "flip_alpha")
            options.prop(import_properties, "toggle_visors")
            if import_properties.toggle_visors:
                options.prop(import_properties, "visors")
            _ = material_body.operator("ekur.importmaterial")

    def draw_model_options(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        model_header, model_body = layout.panel("VIEW3D_PT_import_model")
        model_header.label(icon="MESH_CUBE", text="Import Model")
        if model_body:
            model_opts = model_body.box()
            model_opts.prop(import_properties, "model_path")
            model_opts.prop(import_properties, "import_markers")
            model_opts.prop(import_properties, "import_bones")
            model_opts.prop(import_properties, "import_materials")
            model_opts.prop(import_properties, "import_collections")
            model_opts.prop(import_properties, "import_vertex_color")
            _ = model_body.operator("ekur.importmodel")

    def draw_ocgd(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        ocgd_header, ocgd_body = layout.panel("VIEW3D_PT_import_ocgd")
        ocgd_header.label(icon="ARMATURE_DATA", text="Import Spartan")
        if ocgd_body:
            ocgd_body.prop(import_properties, "use_purp_rig")
            ocgd_opts = ocgd_body.box()
            ocgd_opts.prop(import_properties, "import_specific_core")
            if import_properties.import_specific_core:
                ocgd_opts.prop(import_properties, "core")

            ocgd_opts.prop(import_properties, "import_names")
            _ = ocgd_opts.operator("ekur.importspartan")
            vanity_opts = ocgd_body.box()
            vanity_opts.prop(import_properties, "body_type")
            vanity_opts.prop(import_properties, "left_arm")
            vanity_opts.prop(import_properties, "right_arm")
            vanity_opts.prop(import_properties, "left_leg")
            vanity_opts.prop(import_properties, "right_leg")
            vanity_opts.prop(import_properties, "gamertag")
            _ = vanity_opts.operator("ekur.importvanity")

    def draw_level(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        level_header, level_body = layout.panel("VIEW3D_PT_import_level")
        level_header.label(icon="MESH_GRID", text="Import Level")
        if level_body:
            level_opts = level_body.box()
            level_opts.prop(import_properties, "level_path")
            _ = level_body.operator("ekur.importlevel")

    def draw_forge(self, context: Context | None, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None or context is None:
            return
        forge_header, forge_body = layout.panel("VIEW3D_PT_import_forge")
        forge_header.label(icon="TOOL_SETTINGS", text="Import Forge")
        if forge_body:
            forge_opts = forge_body.box()
            forge_opts.prop(import_properties, "sort_objects")
            forge_opts.prop(import_properties, "root_category")
            category = import_properties.root_category
            cat = GrabStrings().get_category(context, category)
            if cat and cat["sub_categories"]:
                forge_opts.prop(import_properties, "subcategory")
                forge_opts.prop(import_properties, "objects")
                forge_opts.prop(import_properties, "object_representation")
            _ = forge_body.operator("ekur.importforge")

    def draw_forge_map(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        forge_header, forge_body = layout.panel("VIEW3D_PT_import_forge_map")
        forge_header.label(icon="MAT_SPHERE_SKY", text="Import Forge Map")
        if forge_body:
            forge_opts = forge_body.box()
            forge_opts.prop(import_properties, "asset_id")
            forge_opts.prop(import_properties, "version_id")
            _ = forge_body.operator("ekur.importforgemap")
