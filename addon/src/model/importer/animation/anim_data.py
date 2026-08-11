# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import struct
from io import BufferedReader

from ...vectors import Vector3, Vector4

__all__ = ["AnimationData", "AnimationNode"]


class AnimationNode:
    def __init__(self) -> None:
        self.name: str = ""
        self.first_child: int = -1
        self.next_sibling: int = -1

    def read(self, reader: BufferedReader) -> None:
        name_length = int.from_bytes(reader.read(4), "little", signed=False)
        self.name = reader.read(name_length).decode("utf-8")

        self.first_child = int.from_bytes(reader.read(2), "little", signed=True)
        self.next_sibling = int.from_bytes(reader.read(2), "little", signed=True)


class AnimationTransform:
    def __init__(self) -> None:
        self.position: Vector3 = Vector3()
        self.rotation: Vector4 = Vector4()
        self.scale: float = 1.0

    def read(self, reader: BufferedReader) -> None:
        self.position.read(reader)
        self.rotation.read(reader)
        self.scale = struct.unpack("<f", reader.read(4))[0]


class AnimationFrame:
    def __init__(self, node_count: int) -> None:
        self.transforms: list[AnimationTransform] = []
        self.node_count: int = node_count

    def read(self, reader: BufferedReader) -> None:
        for _ in range(self.node_count):
            transform = AnimationTransform()
            transform.read(reader)
            self.transforms.append(transform)


class AnimationData:
    def __init__(self) -> None:
        self.total_frames: int = 0
        self.node_count: int = 0
        self.prepends_rest_pose: bool = False
        self.nodes: list[AnimationNode] = []
        self.rest_pose: list[AnimationTransform] = []
        self.frames: list[AnimationFrame] = []

    def read(self, reader: BufferedReader) -> None:
        self.total_frames = int.from_bytes(reader.read(4), "little", signed=False)
        self.node_count = int.from_bytes(reader.read(4), "little", signed=False)
        self.prepends_rest_pose = bool(int.from_bytes(reader.read(1), "little"))

        for _ in range(self.node_count):
            node = AnimationNode()
            node.read(reader)
            self.nodes.append(node)

        if self.prepends_rest_pose:
            for _ in range(self.node_count):
                transform = AnimationTransform()
                transform.read(reader)
                self.rest_pose.append(transform)

        for _ in range(self.total_frames):
            frame = AnimationFrame(self.node_count)
            frame.read(reader)
            self.frames.append(frame)
