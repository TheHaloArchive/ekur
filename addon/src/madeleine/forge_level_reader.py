# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import logging
import urllib.request
import urllib.error

from typing import Self
from io import BufferedReader, BytesIO

from .bond_types import ForgeObjectMode
from .madeleine import BondValue
from .bond_reader import get_base_struct


class ForgeLayer:
    swatch: int = 0
    color: int = 0
    color_intensity: float = 0.0
    color_spread: float = 0.0
    roughness: float = 0.0
    force_metallic: bool = False
    force_off_metallic: bool = False


class ForgeMat:
    name: int
    layers: list[ForgeLayer]
    grime: int
    scratch_amount: float
    grime_amount: float

    def __init__(self):
        self.name = 0
        self.layers = []  # Each instance gets its own list
        self.grime = 0
        self.scratch_amount = 0.0
        self.grime_amount = 0.0


class ForgeObject:
    index: int = 0
    global_id: int = 0
    position: list[float] = [0.0, 0.0, 0.0]
    rotation_up: list[float] = [0.0, 0.0, 0.0]
    rotation_forward: list[float] = [0.0, 0.0, 0.0]
    scale: list[float] = [1.0, 1.0, 1.0]
    variant: int = 0
    mode: ForgeObjectMode = ForgeObjectMode(2)
    variant_index: int = 0
    material_id: int = 0


class ForgeFolderEntry:
    name: str = ""
    index: int = 0
    parent: int = 0


class ForgeFolder:
    name: str = ""
    id: int = 0
    parent: int = 0
    objects: list[ForgeFolderEntry] = []
    subcategories: list[Self] = []


class ForgeLevel:
    objects: list[ForgeObject] = []
    categories: list[ForgeFolder] = []
    materials: list[ForgeMat] = []
    root_category: int = 0


def get_forge_item(item: BondValue) -> ForgeObject | None:
    forge_object = ForgeObject()
    id_struct = item.get_by_id(2)
    if not id_struct:
        return
    global_id = id_struct.get_value(0)
    if not global_id:
        return
    if type(global_id.value) is int:
        forge_object.global_id = global_id.value
    position_selector = item.get_by_id(3)
    if not position_selector:
        return
    for element in position_selector.get_elements():
        if element.id == 0 and type(element.value) is float:
            forge_object.position[0] = element.value
        elif element.id == 1 and type(element.value) is float:
            forge_object.position[1] = element.value
        elif element.id == 2 and type(element.value) is float:
            forge_object.position[2] = element.value
    rotation_selector = item.get_by_id(4)
    if not rotation_selector:
        return
    for value in rotation_selector.get_elements():
        if value.id == 0 and type(value.value) is float:
            forge_object.rotation_up[0] = value.value
        elif value.id == 1 and type(value.value) is float:
            forge_object.rotation_up[1] = value.value
        elif value.id == 2 and type(value.value) is float:
            forge_object.rotation_up[2] = value.value
    rotation_selector = item.get_by_id(5)
    if not rotation_selector:
        return
    for value in rotation_selector.get_elements():
        if value.id == 0 and type(value.value) is float:
            forge_object.rotation_forward[0] = value.value
        elif value.id == 1 and type(value.value) is float:
            forge_object.rotation_forward[1] = value.value
        elif value.id == 2 and type(value.value) is float:
            forge_object.rotation_forward[2] = value.value
    properties = item.get_by_id(8)
    if not properties:
        return

    material_id = properties.get_by_id(0)
    if material_id:
        misc_properties = material_id.get_by_id(0)
        if misc_properties:
            matprops = misc_properties.get_by_id(13)
            if matprops and len(matprops.get_elements()) > 0:
                m = matprops.get_elements()[0].value
                if type(m) is int:
                    forge_object.material_id = m

    variant_selector = properties.get_by_id(24)
    if variant_selector:
        variant_selector = variant_selector.get_value(0)
        if variant_selector:
            index = variant_selector.get_by_id(0)
            if index and type(index.value) is int:
                forge_object.mode = ForgeObjectMode(index.value)
            variant_id = variant_selector.get_by_id(2)
            if variant_id and type(variant_id.value) is int:
                forge_object.variant_index = variant_id.value
            variant = variant_selector.get_by_id(1)
            if variant:
                variant = variant.get_by_id(0)
                if variant and type(variant.value) is int:
                    forge_object.variant = variant.value

    scale_selector = properties.get_by_id(23)
    if not scale_selector:
        return forge_object
    scale_selector = scale_selector.get_by_id(0)
    if not scale_selector:
        return forge_object
    scale_selector = scale_selector.get_by_id(0)
    if not scale_selector:
        return forge_object

    for element in scale_selector.get_elements():
        if element.id == 0 and type(element.value) is float:
            forge_object.scale[0] = element.value
        elif element.id == 1 and type(element.value) is float:
            forge_object.scale[1] = element.value
        elif element.id == 2 and type(element.value) is float:
            forge_object.scale[2] = element.value
    return forge_object


def get_objects(value: BondValue) -> ForgeFolderEntry:
    object = ForgeFolderEntry()
    index = value.get_by_id(8)
    if index and type(index.value) is int:
        object.index = index.value
    name = value.get_by_id(2)
    if name and type(name.value) is str:
        object.name = name.value
    parent = value.get_by_id(6)
    if parent and type(parent.value) is int:
        object.parent = parent.value
    return object


def get_category(value: BondValue) -> list[ForgeFolder]:
    folders = value.get_by_id(0)
    forge_categories: list[ForgeFolder] = []
    if not folders:
        return forge_categories
    for folder in folders.get_elements():
        root_folder = ForgeFolder()
        name = folder.get_by_id(2)
        if name and type(name.value) is str:
            root_folder.name = name.value
        id = folder.get_by_id(0)  # if id does not exist, root!
        if id and type(id.value) is int:
            root_folder.id = id.value
        else:
            root_folder.id = 4294967295
        obj_subfolders = folder.get_by_id(1)
        if not obj_subfolders:
            continue
        for obj_sub in obj_subfolders.get_elements():
            is_subfolder = obj_sub.get_by_id(0) is None
            if is_subfolder:
                subfolder = ForgeFolder()
                id = obj_sub.get_by_id(1)
                if id and type(id.value) is int:
                    subfolder.id = id.value
                name = obj_sub.get_by_id(2)
                if name and type(name.value) is str:
                    subfolder.name = name.value
                parent = obj_sub.get_by_id(5)
                if parent and type(parent.value) is int:
                    subfolder.parent = parent.value
                subfolder_objects = obj_sub.get_by_id(7)
                if not subfolder_objects:
                    continue
                for object in subfolder_objects.get_elements():
                    ob = get_objects(object)
                    if ob.parent == subfolder.id:
                        subfolder.objects.append(ob)
                root_folder.subcategories.append(subfolder)
            else:
                root_folder.objects.append(get_objects(obj_sub))
        forge_categories.append(root_folder)
    return forge_categories


def read_layer(value: BondValue) -> ForgeLayer:
    layer = ForgeLayer()
    _swatch_id = value.get_by_id(1)
    if _swatch_id and len(_swatch_id.get_elements()) > 0:
        swatch_id = _swatch_id.get_elements()[0]
        if type(swatch_id.value) is int:
            layer.swatch = swatch_id.value
    color = value.get_by_id(10)
    if color and type(color.value) is int:
        layer.color = color.value
    color_intensity = value.get_by_id(3)
    if color_intensity and type(color_intensity.value) is float:
        layer.color_intensity = color_intensity.value
    color_spread = value.get_by_id(8)
    if color_spread and type(color_spread.value) is float:
        layer.color_spread = color_spread.value
    roughness = value.get_by_id(4)
    if roughness and type(roughness.value) is float:
        layer.roughness = roughness.value
    force_on = value.get_by_id(5)
    if force_on and type(force_on.value) is bool:
        layer.force_metallic = force_on.value
    force_off = value.get_by_id(6)
    if force_off and type(force_off.value) is bool:
        layer.force_off_metallic = force_off.value
    return layer


def read_forge_map(reader: BufferedReader) -> ForgeLevel:
    level = ForgeLevel()
    base_struct = get_base_struct(reader)
    base = base_struct.get_by_id(3)
    if base:
        for idx, item in enumerate(base.get_elements()):
            forge_object = get_forge_item(item)
            if forge_object:
                forge_object.index = idx
                level.objects.append(forge_object)
    folders = base_struct.get_by_id(6)
    mats = base_struct.get_by_id(8)
    if mats:
        for mat in mats.get_elements():
            material = ForgeMat()
            layers = [mat.get_by_id(3), mat.get_by_id(4), mat.get_by_id(5), mat.get_by_id(6)]
            for layer in layers:
                if layer:
                    material.layers.append(read_layer(layer))
            scratch_amount = mat.get_by_id(9)
            if scratch_amount and type(scratch_amount.value) is float:
                material.scratch_amount = scratch_amount.value
            grime_amount = mat.get_by_id(10)
            if grime_amount and type(grime_amount.value) is float:
                material.grime_amount = grime_amount.value
            grime = mat.get_by_id(8)
            if grime and len(grime.get_elements()) > 0:
                grime_id = grime.get_elements()[0]
                if type(grime_id.value) is int:
                    material.grime = grime_id.value

            id = mat.get_by_id(1)
            if id and len(id.get_elements()) > 0:
                id = id.get_elements()[0]
                if type(id.value) is int:
                    material.name = id.value

            level.materials.append(material)

    if folders:
        level.categories = get_category(folders)

        root = folders.get_by_id(1)
        if root and type(root.value) is int:
            level.root_category = root.value
    return level


def get_forge_map(asset_id: str, version_id: str, file: str) -> ForgeLevel:
    level = ForgeLevel()
    url = f"https://blobs-infiniteugc.svc.halowaypoint.com/ugcstorage/map/{asset_id}/{version_id}/map.mvar"
    if file != "":
        with open(file, "rb") as f:
            return read_forge_map(f)
    try:
        with urllib.request.urlopen(url) as response:  # pyright: ignore[reportAny]
            response = response.read()  # pyright: ignore[reportAny]
            level = read_forge_map(BytesIO(response))  # pyright: ignore[reportAny, reportArgumentType]

    except urllib.error.HTTPError as e:
        logging.error(f"Failed to download forge map: {e.status}")

    return level
