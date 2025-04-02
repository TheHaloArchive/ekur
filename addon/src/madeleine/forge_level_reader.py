# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader, BytesIO
import logging
from typing import Self
import urllib.request
import urllib.error

from .madeleine import BondValue
from .bond_reader import get_base_struct


class ForgeObject:
    index: int = 0
    global_id: int = 0
    position: list[float] = []
    rotation_up: list[float] = []
    rotation_forward: list[float] = []
    scale: list[float] = []
    variant: int = 0


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
    forge_object.position = [0.0, 0.0, 0.0]
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
    forge_object.rotation_up = [0.0, 0.0, 0.0]
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
    forge_object.rotation_forward = [0.0, 0.0, 0.0]
    forge_object.scale = [1.0, 1.0, 1.0]
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
    variant_selector = properties.get_by_id(24)
    if not variant_selector:
        return
    variant_selector = variant_selector.get_value(0)
    if not variant_selector:
        return
    variant = variant_selector.get_value(1)
    if not variant:
        return
    variant = variant.get_value(0)
    if not variant:
        return
    if type(variant.value) is int:
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


def read_forge_map(reader: BufferedReader) -> tuple[list[ForgeObject], list[ForgeFolder], int]:
    objects: list[ForgeObject] = []
    categories: list[ForgeFolder] = []
    base_struct = get_base_struct(reader)
    base = base_struct.get_by_id(3)
    if base:
        for idx, item in enumerate(base.get_elements()):
            forge_object = get_forge_item(item)
            if forge_object:
                forge_object.index = idx
                objects.append(forge_object)
    folders = base_struct.get_by_id(6)
    root_folder = 0
    if folders:
        categories = get_category(folders)
        root = folders.get_by_id(1)
        if root and type(root.value) is int:
            root_folder = root.value
    return objects, categories, root_folder


def get_forge_map(
    asset_id: str, version_id: str, file: str
) -> tuple[list[ForgeObject], list[ForgeFolder], int]:
    objects: list[ForgeObject] = []
    categories: list[ForgeFolder] = []
    root_folder: int = 0
    url = f"https://blobs-infiniteugc.svc.halowaypoint.com/ugcstorage/map/{asset_id}/{version_id}/map.mvar"
    if file != "":
        with open(file, "rb") as f:
            return read_forge_map(f)
    try:
        with urllib.request.urlopen(url) as response:  # pyright: ignore[reportAny]
            response = response.read()  # pyright: ignore[reportAny]
            objects, categories, root_folder = read_forge_map(BytesIO(response))  # pyright: ignore[reportAny, reportArgumentType]

    except urllib.error.HTTPError as e:
        logging.error(f"Failed to download forge map: {e.status}")
    return objects, categories, root_folder
