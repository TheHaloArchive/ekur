# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader
from .vectors import Matrix4x4

__all__ = ["Bone"]


class Bone:
    def __init__(self) -> None:
        self.name: int = -1
        self.parent_index: int = -1
        self.local_transform: Matrix4x4 = Matrix4x4()
        self.world_transform: Matrix4x4 = Matrix4x4()

    def read(self, reader: BufferedReader) -> None:
        self.name = int.from_bytes(reader.read(4), "little", signed=True)
        self.parent_index = int.from_bytes(reader.read(4), "little", signed=True)
        self.local_transform.read(reader)
        self.world_transform.read(reader)
