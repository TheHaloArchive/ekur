# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import json
from pathlib import Path
from typing import TypeVar

import bpy
from bpy.types import (
    Image,
    MaterialSlot,
    Node,
    Nodes,
    NodeSocket,
    NodeTreeInterface,
    NodeTreeInterfacePanel,
)


def read_texture(texturepath: str) -> Image:
    """Load a texture from the given path. If the texture is already loaded, it will return the existing texture.

    Args:
        texturepath: The path to the texture file relative to the data folder.

    Returns:
        The loaded image.
    """
    preferences = bpy.context.preferences.addons["bl_ext.user_default.ekur"].preferences
    image = bpy.data.images.get(texturepath.split("\\")[-1])
    if image:
        return image

    image = bpy.data.images.new(texturepath.split("\\")[-1], 1, 1)
    image.source = "FILE"
    image.filepath = f"{preferences.data_folder}/bitmaps/{texturepath}_0.png"  # pyright: ignore[reportAttributeAccessIssue]
    image.colorspace_settings.name = "Non-Color"  # pyright: ignore[reportAttributeAccessIssue]
    return image


def get_materials() -> list[MaterialSlot]:
    """Get all materials from the selected objects or all objects in the scene.

    Returns:
        A list of all material slots.
    """
    data_source = bpy.data.objects
    if bpy.context.scene.import_properties.selected_only:  # pyright: ignore[reportAttributeAccessIssue]
        data_source = bpy.context.selected_objects
    meshes = [obj for obj in data_source if obj.type == "MESH"]
    return [mat_slot for obj in meshes for mat_slot in obj.material_slots]


def read_json_file(file_path: Path):
    """Load a json file from the given path.

    Args:
        file_path: Path to the json file.

    Returns:
        The loaded json data.
    """
    with open(file_path, "r") as file:
        return json.load(file)


def remove_nodes(node_tree: bpy.types.NodeTree | None) -> None:
    """Remove all nodes from the given node tree.

    Args:
        node_tree: Node tree to remove all nodes from.
    """
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)


NodeSocketT = TypeVar("NodeSocketT", bound=NodeSocket)


def create_socket(
    interface: NodeTreeInterface,
    name: str,
    type: type[NodeSocketT],
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
    out: NodeSocketT = interface.new_socket(
        name=name, in_out=in_out, socket_type=type.__name__, parent=panel
    )
    return out


NodeT = TypeVar("NodeT", bound=Node)


def create_node(nodes: Nodes, x: int, y: int, _type: type[NodeT]) -> NodeT:
    """Creates a new node of the given type on the node tree.

    Args:
        nodes: Collection of nodes from node tree.
        x: X coordinate of the node.
        y: Y coordinate of the node
        _type: Type of the node to create.

    Returns:
        Returns the created node of the same type provided.
    """
    node: NodeT = nodes.new(type=_type.__name__)
    node.location = (x, y)
    return node
