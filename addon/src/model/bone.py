# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from .vectors import Matrix4x4

__all__ = ["Bone"]


class Bone:
    def __init__(self) -> None:
        self.name: str = ""
        self.parent_index: int = -1
        self.rotation_matrix: Matrix4x4 = Matrix4x4()
        self.transformation_matrix: Matrix4x4 = Matrix4x4()
        self.world_transform: Matrix4x4 = Matrix4x4()

    def read(self, reader: BufferedReader) -> None:
        name_length = int.from_bytes(reader.read(1), "little")
        self.name = reader.read(name_length).decode("utf-8")
        self.parent_index = int.from_bytes(reader.read(4), "little", signed=True)
        self.rotation_matrix.read(reader)
        self.transformation_matrix.read(reader)
        self.world_transform.read(reader)
