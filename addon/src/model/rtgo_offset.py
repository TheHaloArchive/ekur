# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from .vectors import Vector3

__all__ = ["RtgoOffset"]


class RtgoOffset:
    def __init__(self) -> None:
        self.name: int = 0
        self.mesh_index: int = 0
        self.position: Vector3 = Vector3()

    def read(self, reader: BufferedReader) -> None:
        self.name = int.from_bytes(reader.read(4), "little", signed=True)
        self.mesh_index = int.from_bytes(reader.read(2), "little", signed=True)
        self.position.read(reader)
