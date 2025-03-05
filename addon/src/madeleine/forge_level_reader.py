from io import BytesIO
import logging
import urllib.request
import urllib.error

from .madeleine import BondValue
from .bond_reader import get_base_struct


class ForgeObject:
    global_id: int = 0
    position: list[float] = []
    rotation_up: list[float] = []
    rotation_forward: list[float] = []
    scale: list[float] = []
    variant: int = 0


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
    forge_object.position = [
        element.value
        for element in position_selector.get_elements()
        if type(element.value) is float
    ]
    rotation_selector = item.get_by_id(4)
    if not rotation_selector:
        return
    forge_object.rotation_up = [
        element.value
        for element in rotation_selector.get_elements()
        if type(element.value) is float
    ]
    rotation_selector = item.get_by_id(5)
    if not rotation_selector:
        return
    forge_object.rotation_forward = [
        element.value
        for element in rotation_selector.get_elements()
        if type(element.value) is float
    ]
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

    if len(forge_object.rotation_forward) == 1:
        forge_object.rotation_forward = [forge_object.rotation_forward[0], 0, 0]
    elif len(forge_object.rotation_forward) == 2:
        forge_object.rotation_forward = [
            forge_object.rotation_forward[0],
            forge_object.rotation_forward[1],
            0,
        ]
    if len(forge_object.rotation_up) == 1:
        forge_object.rotation_up = [forge_object.rotation_up[0], 0, 1]
    elif len(forge_object.rotation_up) == 2:
        forge_object.rotation_up = [
            forge_object.rotation_up[0],
            forge_object.rotation_up[1],
            1,
        ]
    scale_selector = properties.get_by_id(23)
    if not scale_selector:
        return forge_object
    scale_selector = scale_selector.get_by_id(0)
    if not scale_selector:
        return forge_object
    scale_selector = scale_selector.get_by_id(0)
    if not scale_selector:
        return forge_object
    forge_object.scale = [
        element.value for element in scale_selector.get_elements() if type(element.value) is float
    ]
    return forge_object


def get_forge_map(asset_id: str, version_id: str) -> list[ForgeObject]:
    objects: list[ForgeObject] = []
    url = f"https://blobs-infiniteugc.svc.halowaypoint.com/ugcstorage/map/{asset_id}/{version_id}/map.mvar"
    try:
        with urllib.request.urlopen(url) as response:
            response = response.read()
            base_struct = get_base_struct(BytesIO(response))
            base = base_struct.get_by_id(3)
            if base:
                for item in base.get_elements():
                    forge_object = get_forge_item(item)
                    if forge_object:
                        objects.append(forge_object)

    except urllib.error.HTTPError as e:
        logging.error(f"Failed to download all_visors.json: {e.status}")
    return objects
