import json
import logging
from pathlib import Path
from typing import cast, final
import urllib.request
import urllib.error
import bpy
from bpy.types import Collection, Context, Object, Operator, ShaderNodeTree

from ..material_types.color_decal import ColorDecalShader
from ..material_types.decal_shader import DecalShader
from ..material_types.diffuse_shader import DiffuseShaderType
from ..material_types.illum_shader import IllumShader
from ..material_types.layered_shader import LayeredShader

from ..model.importer.model_importer import ModelImporter

from ..json_definitions import (
    Asset,
    Attachment,
    Coating,
    CommonMaterial,
    CommonStyleList,
    CustomizationAttachment,
    CustomizationGlobals,
    CylixCore,
    CylixIndex,
    CylixVanityResponse,
)
from ..utils import (
    get_data_folder,
    get_import_properties,
    get_materials,
    read_json_file,
    remove_nodes,
)


@final
class ImportSpartanVanityOperator(Operator):
    bl_idname = "ekur.importvanity"
    bl_label = "Import Vanity"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: Context | None) -> set[str]:
        if context is None or context.scene is None:
            return {"CANCELLED"}
        props = get_import_properties()
        data = get_data_folder()
        vanity = self.request(
            url=f"https://cylix.guide/api/vanity/profile/{props.gamertag.replace(' ', '-')}"
        )
        index = self.request(url="https://hi.cylix.guide/index.json")
        armor: CylixVanityResponse = json.loads(vanity)
        index_json: CylixIndex = json.loads(index)

        customization_path = Path(f"{data}/customization_globals.json")
        customization_globals = read_json_file(customization_path, CustomizationGlobals)
        if customization_globals is None:
            return {"CANCELLED"}
        model_path = Path(f"{data}/models/{customization_globals['model']}.ekur")
        if not model_path.exists():
            logging.warning(f"Model path does not exist!: {model_path}")
            return {"CANCELLED"}

        core_res = [
            core
            for core in index_json["manifest"]
            if core[0].lower() == armor["armor"]["theme"].lower()
        ]
        theme = self.request(id=armor["armor"]["theme"].lower(), res=core_res[0][1]["res"].lower())
        theme_json: CylixCore = json.loads(theme)

        helmet_res = [
            core
            for core in index_json["manifest"]
            if core[0].lower() == armor["armor"]["helmet"].lower()
        ]
        helmet: Asset = json.loads(
            self.request(id=armor["armor"]["helmet"].lower(), res=helmet_res[0][1]["res"].lower())
        )
        kneepad_res = [
            core
            for core in index_json["manifest"]
            if core[0].lower() == armor["armor"]["kneepads"].lower()
        ]
        kneepad: Asset = json.loads(
            self.request(id=armor["armor"]["kneepads"].lower(), res=kneepad_res[0][1]["res"])
        )
        glove_res = [
            core
            for core in index_json["manifest"]
            if core[0].lower() == armor["armor"]["gloves"].lower()
        ]
        glove: Asset = json.loads(
            self.request(id=armor["armor"]["gloves"].lower(), res=glove_res[0][1]["res"])
        )
        props.toggle_visors = True
        visor_res = [
            visor
            for visor in index_json["manifest"]
            if visor[0].lower() == armor["armor"]["visor"].lower()
        ]
        props.visors = visor_res[0][1]["title"]
        importer = ModelImporter()
        objects = importer.start_import(str(model_path))
        vanity_collection = bpy.data.collections.new(props.gamertag)

        attachments = [
            armor["armor"]["chestAttachment"],
            armor["armor"]["helmetAttachment"],
            armor["armor"]["wristAttachment"],
            armor["armor"]["hipAttachment"],
            armor["armor"]["leftShoulderPad"],
            armor["armor"]["rightShoulderPad"],
        ]

        for attachment in attachments:
            self.import_attachment(
                attachment, index_json, vanity_collection, customization_globals, importer
            )
        parts = [helmet, kneepad, glove]

        context.scene.collection.children.link(vanity_collection)  # pyright: ignore[reportUnknownMemberType]
        for object in objects:
            permutation_name = cast(int, object["permutation_name"])
            region_name = cast(int, object["region_name"])
            for reg in theme_json["CoreRegionData"]["BaseRegionData"]:
                if (
                    reg["PermutationId"]["m_identifier"] == permutation_name
                    and reg["RegionId"]["m_identifier"] == region_name
                ):
                    vanity_collection.objects.link(object)  # pyright: ignore[reportUnknownMemberType]
            for part in parts:
                for helmet_data in part["RegionData"]:
                    if (
                        permutation_name == helmet_data["PermutationId"]["m_identifier"]
                        and region_name == helmet_data["RegionId"]["m_identifier"]
                    ):
                        vanity_collection.objects.link(object)  # pyright: ignore[reportUnknownMemberType]

        coating_res = [
            coat for coat in index_json["manifest"] if coat[0] == armor["armor"]["coating"]
        ]
        coating = self.request(id=armor["armor"]["coating"], res=coating_res[0][1]["res"])
        coating_json: Coating = json.loads(coating)

        for object in vanity_collection.objects:
            object.select_set(True)  # pyright: ignore[reportUnknownMemberType]
            self.import_materials(coating_json["StyleId"]["m_identifier"])

        return {"FINISHED"}

    def request(self, id: str = "", res: str = "", url: str = "") -> str:
        request = urllib.request.Request(f"https://hi.cylix.guide/item/{id}/{res}.json")
        if url != "":
            request = urllib.request.Request(url)
        print(request.full_url)
        request.add_header("Referer", "https://cylix.guide/")
        request.add_header(
            "User-Agent",
            "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
        )
        try:
            request = urllib.request.urlopen(request)  # pyright: ignore[reportAny]
        except urllib.error.HTTPError as e:
            logging.error(f"Failed to download vanity!: {e}")
            return ""
        return cast(str, request.read().decode("utf-8"))  # pyright: ignore[reportAny]

    def import_materials(self, style_id: int) -> None:
        data = get_data_folder()
        materials = get_materials()

        for slot in materials:
            if not slot.material:
                continue
            node_tree = slot.material.node_tree
            name = slot.name
            if len(slot.name.split(".")) > 1:
                name = slot.name.split(".")[0]

            definition_path = Path(f"{data}/materials/{name}.json")
            if not node_tree:
                continue

            remove_nodes(node_tree)
            material = read_json_file(definition_path, CommonMaterial)
            if material is None:
                return
            self.run_material(material, node_tree, style_id)

    def run_material(
        self, material: CommonMaterial, node_tree: ShaderNodeTree, style_id: int
    ) -> None:
        data = get_data_folder()
        match material["shader_type"]:
            case "Layered":
                if material["style_info"] is not None:
                    styles_path = Path(
                        f"{data}/stylelists/{material['style_info']['stylelist']}.json"
                    )
                    styles = read_json_file(styles_path, CommonStyleList)
                    if styles is None:
                        return
                    layered_shader = LayeredShader(node_tree, material, styles)
                    layered_shader.create_textures()
                    layered_shader.process_styles(style_id)

            case "Diffuse":
                _ = DiffuseShaderType(material, node_tree)
            case "Decal":
                _ = DecalShader(material, node_tree)
            case "SelfIllum":
                _ = IllumShader(material, node_tree)
            case "ColorDecal":
                _ = ColorDecalShader(material, node_tree)
            case "Unknown":
                pass
            case _:
                logging.error(f"Unknown shader type!: {material['shader_type']}")

    def import_attachments(
        self,
        name: str,
        alt_name: str,
        marker: Object,
        attachment: Object,
    ) -> None:
        if marker.name == name or alt_name in marker.name:
            empty_global_transform = marker.matrix_world
            mesh_global_transform = attachment.matrix_world
            offset = (
                -(mesh_global_transform.translation - empty_global_transform.translation) * 3.048
            )
            attachment.location = offset
            attachment.rotation_euler = (0.0, 0.0, 0.0)

    def import_attachment(
        self,
        name: str,
        index: CylixIndex,
        col: Collection,
        globals: CustomizationGlobals,
        importer: ModelImporter,
    ) -> None:
        data = get_data_folder()
        attachment_res = [core for core in index["manifest"] if core[0].lower() == name.lower()]

        if attachment_res:
            attachment_data: Attachment = json.loads(
                self.request(id=name.lower(), res=attachment_res[0][1]["res"])
            )
            for theme in globals["themes"]:
                attachment = [
                    att for att in theme["attachments"] if att["tag_id"] == attachment_data["TagId"]
                ]
                if not attachment:
                    attachment: list[CustomizationAttachment] = []
                    for region in theme["regions"]:
                        for att in region["permutations"]:
                            if att["attachment"]:
                                if att["attachment"]["tag_id"] == attachment_data["TagId"]:
                                    attachment.append(att["attachment"])
                if attachment:
                    model_path = f"{data}/models/{attachment[0]['model']}.ekur"
                    attachments = ModelImporter().start_import(model_path, False)
                    alt_name = f"{attachment[0]['marker_name']}"
                    for attach in attachments:
                        for marker in importer.markers:
                            self.import_attachments("", alt_name, marker, attach)
                            if attach.name not in col.objects:
                                col.objects.link(attach)  # pyright: ignore[reportUnknownMemberType]
