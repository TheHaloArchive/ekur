# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia

# pyright: reportUnknownMemberType=false, reportUninitializedInstanceVariable=false
import random
from typing import final

from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty  # pyright: ignore[reportUnknownVariableType]
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
    scale_factor: FloatProperty(
        name="Scale Factor",
        description="Factor to scale the mesh up by from its in-game size.",
        default=1.0,
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
    url: StringProperty(name="URL", default="")
    use_file: BoolProperty(name="Use MVAR File", default=False)
    import_folders: BoolProperty(name="Import Folders", default=True)
    mvar_file: StringProperty(
        name="MVAR File",
        description="Path to .mvar file to import.",
        subtype="FILE_PATH",
    )
    output_path: StringProperty(name="Output Path", default="", subtype="DIR_PATH")
    output_workflow: EnumProperty(
        name="Output Workflow",
        description="Workflow to use for baking textures.",
        items=[
            ("PBR MetRough", "PBR MetRough", ""),
            ("PBR SpecGloss", "PBR SpecGloss", ""),
            ("PBR MetRoughSpecColor", "PBR MetRoughSpecColor", ""),
            ("PBR ORM", "PBR ORM", ""),
            ("Unity Smoothness/Mask", "Unity Smoothness/Mask", ""),
            ("Color", "Color", ""),
            ("Metallic", "Metallic", ""),
            ("Roughness", "Roughness", ""),
            ("Emission", "Emission", ""),
            ("Specular", "Specular", ""),
            ("SpecColor", "SpecColor", ""),
            ("AO", "AO", ""),
            ("Normal", "Normal", ""),
            ("Unity Mask Map", "Unity Mask Map", ""),
            ("Smoothness", "Smoothness", ""),
            ("ID Mask", "ID Mask", ""),
            ("ORM", "ORM", ""),
        ],
    )
    width: IntProperty(name="Width", default=1024)
    height: IntProperty(name="Height", default=1024)
    bit_depth: EnumProperty(name="Bit Depth", items=[("8", "8", ""), ("16", "16", "")])
    bake_detail_normals: BoolProperty(name="Bake Detail Normals", default=False)
    merge_textures: BoolProperty(name="Merge Textures Into Single Bake", default=False)
    bake_ao: BoolProperty(name="Bake Ambient Occlusion", default=False)
    bake_layer_map: BoolProperty(name="Bake Layer Map", default=False)
    advanced_bake: BoolProperty(name="Toggle Advanced Bake Options", default=False)
    selected_layer: EnumProperty(
        name="Selected Layer",
        description="Layer to bake for objects.",
        items=[
            ("None", "None", ""),
            ("Color", "Color", ""),
            ("Metallic", "Metallic", ""),
            ("Roughness", "Roughness", ""),
            ("Emission", "Emission", ""),
            ("Specular", "Specular", ""),
            ("SpecColor", "SpecColor", ""),
            ("AO", "AO", ""),
            ("Normal", "Normal", ""),
            ("Unity Mask Map", "Unity Mask Map", ""),
            ("Smoothness", "Smoothness", ""),
            ("ID Mask", "ID Mask", ""),
            ("ORM", "ORM", ""),
        ],
    )
    selected_objects: EnumProperty(
        name="Objects to Bake",
        description="Objects to bake for.",
        items=[("Selected", "Selected", ""), ("All", "All", "")],
    )
    pixel_padding: IntProperty(name="Pixel Padding", default=16)
    uv_to_bake_to: EnumProperty(
        name="UV Map to Bake To", items=[("UV0", "UV0", ""), ("UV1", "UV1", ""), ("UV2", "UV2", "")]
    )
    center_x_uv: BoolProperty(name="Center X UV", default=False)
    center_y_uv: BoolProperty(name="Center Y UV", default=False)


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
        self.draw_forge_map(import_properties)
        self.draw_bake_menu(import_properties)

    def draw_material_options(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        material_header, material_body = layout.panel(
            "VIEW3D_PT_import_material", default_closed=True
        )
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
        model_header, model_body = layout.panel("VIEW3D_PT_import_model", default_closed=True)
        model_header.label(icon="MESH_CUBE", text="Import Model")
        if model_body:
            model_opts = model_body.box()
            model_opts.prop(import_properties, "model_path")
            model_opts.prop(import_properties, "import_markers")
            model_opts.prop(import_properties, "import_bones")
            model_opts.prop(import_properties, "import_materials")
            model_opts.prop(import_properties, "import_collections")
            model_opts.prop(import_properties, "import_vertex_color")
            model_opts.prop(import_properties, "scale_factor")
            _ = model_body.operator("ekur.importmodel")

    def draw_ocgd(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        ocgd_header, ocgd_body = layout.panel("VIEW3D_PT_import_ocgd", default_closed=True)
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
        level_header, level_body = layout.panel("VIEW3D_PT_import_level", default_closed=True)
        level_header.label(icon="MESH_GRID", text="Import Level")
        if level_body:
            level_opts = level_body.box()
            level_opts.prop(import_properties, "level_path")
            _ = level_body.operator("ekur.importlevel")

    def draw_forge(self, context: Context | None, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None or context is None:
            return
        forge_header, forge_body = layout.panel("VIEW3D_PT_import_forge", default_closed=True)
        forge_header.label(icon="TOOL_SETTINGS", text="Import Forge Object")
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
        forge_header, forge_body = layout.panel("VIEW3D_PT_import_forge_map", default_closed=True)
        forge_header.label(icon="MAT_SPHERE_SKY", text="Import Forge Map")
        if forge_body:
            forge_opts = forge_body.box()
            forge_opts.prop(import_properties, "url")
            forge_opts.prop(import_properties, "import_folders")
            op = forge_opts.operator("wm.url_open", text="Browse Maps (Cylix)", icon="URL")
            op.url = "https://cylix.guide/discovery/"  # pyright: ignore[reportAttributeAccessIssue]
            op = forge_opts.operator("wm.url_open", text="Browse Maps (Waypoint)", icon="URL")
            op.url = "https://www.halowaypoint.com/halo-infinite/ugc/browse"  # pyright: ignore[reportAttributeAccessIssue]
            forge_opts.prop(import_properties, "use_file")
            if import_properties.use_file:
                forge_opts.prop(import_properties, "mvar_file")
            _ = forge_body.operator("ekur.importforgemap")

    def draw_bake_menu(self, import_properties: ImportPropertiesType) -> None:
        layout = self.layout
        if layout is None:
            return
        bake_header, bake_body = layout.panel("VIEW3D_PT_bake_menu", default_closed=True)
        bake_header.label(icon="SHADING_TEXTURE", text="Bake Textures")
        if bake_body:
            bake_opts = bake_body.box()
            bake_opts.prop(import_properties, "output_path")
            bake_opts.prop(import_properties, "output_workflow")
            bake_opts.prop(import_properties, "width")
            bake_opts.prop(import_properties, "height")
            _ = bake_opts.operator("ekur.alignbake")
            bake_opts.prop(import_properties, "pixel_padding")
            bake_opts.prop(import_properties, "bit_depth")
            bake_opts.prop(import_properties, "bake_detail_normals")
            bake_opts.prop(import_properties, "merge_textures")
            bake_opts.prop(import_properties, "bake_ao")
            bake_opts.prop(import_properties, "bake_layer_map")
            bake_opts.prop(import_properties, "uv_to_bake_to")
            bake_opts.prop(import_properties, "advanced_bake")
            bake_opts.prop(import_properties, "center_x_uv")
            bake_opts.prop(import_properties, "center_y_uv")
            if import_properties.advanced_bake:
                advanced_opts = bake_opts.box()
                advanced_opts.prop(import_properties, "selected_layer")
                advanced_opts.prop(import_properties, "selected_objects")
                _ = advanced_opts.operator("ekur.toggleadvancedbake")
            _ = bake_body.operator("ekur.baketextures")
