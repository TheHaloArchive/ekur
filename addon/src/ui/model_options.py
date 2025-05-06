# pyright: reportUninitializedInstanceVariable=false, reportUnknownVariableType=false, reportUnknownMemberType=false
import bpy

from typing import cast
from bpy.props import BoolProperty, FloatProperty, StringProperty
from bpy.types import PropertyGroup, UILayout


class ModelOptions(PropertyGroup):
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


class ModelOptionsType:
    model_path: str = ""
    import_materials: bool = True
    import_markers: bool = True
    import_bones: bool = True
    import_collections: bool = True
    import_vertex_color: bool = False
    scale_factor: float = 1.0


def get_model_options() -> ModelOptionsType:
    if bpy.context.scene is None:
        return ModelOptionsType()
    props: ModelOptions = bpy.context.scene.model_properties  # pyright: ignore[reportAttributeAccessIssue]
    if props:
        return cast(ModelOptionsType, props)
    return ModelOptionsType()


def draw_model_options(layout: UILayout, props: ModelOptionsType) -> None:
    model_header, model_body = layout.panel("VIEW3D_PT_import_model", default_closed=True)
    model_header.label(icon="MESH_CUBE", text="Import Model")
    if model_body:
        model_opts = model_body.box()
        model_opts.prop(props, "model_path")
        model_opts.prop(props, "import_markers")
        model_opts.prop(props, "import_bones")
        model_opts.prop(props, "import_materials")
        model_opts.prop(props, "import_collections")
        model_opts.prop(props, "import_vertex_color")
        model_opts.prop(props, "scale_factor")
        _ = model_body.operator("ekur.importmodel")
