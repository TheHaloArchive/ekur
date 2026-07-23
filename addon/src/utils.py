# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import json
import logging
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import TypeVar, cast

import bpy
from bpy.types import (
    Image,
    Node,
    Nodes,
    NodeSocket,
    NodeSocketBool,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketInt,
    NodeSocketVector,
    NodeTreeInterface,
    NodeTreeInterfacePanel,
    ShaderNodeTexImage,
    ShaderNodeTree,
    NodeLinks,
    NodeLink,
)

from .exceptions import NodeInterfaceDoesNotExist

__all__ = [
    "read_texture",
    "read_json_file",
    "remove_nodes",
    "create_socket",
    "create_node",
    "create_link",
    "assign_value",
    "get_data_folder",
    "is_debug",
    "get_addon_preferences",
    "AddonPreferencesType",
    "create_image",
    "download_file",
]


def read_texture(texturepath: str) -> Image | None:
    """Load a texture from the given path. If the texture is already loaded, it will return the existing texture.

    Args:
        texturepath: The path to the texture file relative to the data folder.

    Returns:
        The loaded image.
    """
    data_folder = get_data_folder()
    image = bpy.data.images.get(texturepath.split("\\")[-1])
    if image:
        return image

    image = bpy.data.images.new(texturepath.split("\\")[-1], 1, 1)
    image.source = "FILE"
    tex_path = Path(f"{data_folder}/bitmaps/{texturepath}_0.png")
    if not tex_path.exists():
        tex_path = Path(f"{data_folder}/bitmaps/{texturepath}_0_t.png")
        image["use_alpha"] = True
    else:
        image["use_alpha"] = False
    image.filepath = str(tex_path)
    if image.colorspace_settings:
        image.colorspace_settings.name = "Non-Color"  # ty: ignore[invalid-assignment]
    return image


JsonT = TypeVar("JsonT")


def read_json_file(file_path: Path, T: type[JsonT]) -> JsonT | None:
    """Load a json file from the given path.

    Args:
        file_path: Path to the json file.

    Returns:
        The loaded json data.
    """
    if not file_path.exists() or not file_path.is_file():
        logging.warning(f"File path does not exist!: {file_path}")
        return
    with open(file_path, "r") as file:
        data: T = cast(T, json.load(file))
        return data


def remove_nodes(node_tree: ShaderNodeTree) -> None:
    """Remove all nodes from the given node tree.

    Args:
        node_tree: Node tree to remove all nodes from.
    """
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)


NodeSocketT = TypeVar("NodeSocketT", bound=NodeSocket)


def create_socket(
    interface: NodeTreeInterface | None,
    name: str,
    _type: type[NodeSocketT],
    is_input: bool = True,
    panel: NodeTreeInterfacePanel | None = None,
) -> NodeSocketT:
    """Creates a new node socket on the given node interface.

    Args:
        interface: Interface to create the socket on.
        name: User-facing name for the socket.
        type: Socket type.
        is_input: Whether the socket is an input or output.

    Returns:
        The created socket.
    """
    in_out = "INPUT" if is_input else "OUTPUT"
    if interface is None:
        raise NodeInterfaceDoesNotExist("Interface cannot be None!")
    out = cast(
        _type,
        interface.new_socket(name=name, in_out=in_out, socket_type=_type.__name__, parent=panel),  # ty: ignore[invalid-argument-type]
    )
    return out


NodeT = TypeVar("NodeT", bound=Node)


def create_node(nodes: Nodes, x: float, y: float, _type: type[NodeT]) -> NodeT:
    """Creates a new node of the given type on the node tree.

    Args:
        nodes: Collection of nodes from node tree.
        x: X coordinate of the node.
        y: Y coordinate of the node.
        _type: Type of the node to create.

    Returns:
        Returns the created node of the same type provided.
    """
    node = cast(_type, nodes.new(type=_type.__name__))
    node.location = (x, y)
    return node


class AddonPreferencesType:
    data_folder: str = ""
    deploy_folder: str = ""
    dump_textures: bool = True
    is_campaign: bool = False
    debug: bool = False


def is_debug() -> bool:
    return get_addon_preferences().debug


def debug_print(*values: object):
    if is_debug():
        print(values)


def get_data_folder() -> str:
    """Get the data folder path from the preferences.

    Returns:
        The data folder path.
    """
    return get_addon_preferences().data_folder


def get_package_name() -> str:
    if __package__ is None:
        return ""
    return __package__.split(".src")[0]


def get_addon_preferences() -> AddonPreferencesType:
    """Get the addon preferences from the scene.

    Returns:
        The addon preferences.
    """
    if bpy.context.preferences is None:
        return AddonPreferencesType()
    preferences = bpy.context.preferences.addons[get_package_name()].preferences
    if not preferences:
        return AddonPreferencesType()
    return cast(AddonPreferencesType, preferences)


def assign_value(
    node: Node,
    index: int,
    value: float | tuple[float, float, float] | tuple[float, float, float, float] | bool | int,
) -> None:
    if len(node.inputs) <= index:
        logging.warning(f"Node {node.name} does not have an input at index {index}")
        return
    if type(value) is bool:
        cast(NodeSocketBool, node.inputs[index]).default_value = value
    if type(value) is tuple and len(value) == 3:
        cast(NodeSocketVector, node.inputs[index]).default_value = value
    if type(value) is float:
        cast(NodeSocketFloat, node.inputs[index]).default_value = value
    if type(value) is tuple and len(value) == 4:
        cast(NodeSocketColor, node.inputs[index]).default_value = value
    if type(value) is int:
        cast(NodeSocketInt, node.inputs[index]).default_value = value


def create_link(
    links: NodeLinks, node_one: Node, node_two: Node, node_one_index: int, node_two_index: int
) -> NodeLink | None:
    if node_one.outputs and node_two.inputs:
        return links.new(node_one.outputs[node_one_index], node_two.inputs[node_two_index])
    return


def create_image(nodes: Nodes, y: int, name: str) -> ShaderNodeTexImage:
    texture = create_node(nodes, -300, y, ShaderNodeTexImage)
    texture.hide = True
    texture.image = read_texture(name)
    return texture


def download_file(url: str, file_path: str) -> None:
    try:
        with (
            urllib.request.urlopen(url) as response,
            open(file_path, "wb") as out_file,
        ):
            _ = out_file.write(response.read())
    except urllib.error.HTTPError as e:
        logging.error(f"Failed to download: {url}: {e.status}")


_nsre = re.compile("([0-9]+)")


def natural_sort_key(s: str) -> list[int | str]:
    """Natural sort order implementation.

    Args:
        s: String to sort

    Returns:
        Sorted list of strings and integers
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s[1])]
