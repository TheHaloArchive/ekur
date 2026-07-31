# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
from io import BufferedReader

from ..exceptions import IncorrectStrideValue

__all__ = ["BlendShapeIndexBuffer"]


class BlendShapeIndexBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.indices: list[int] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        if self.stride != 4:
            raise IncorrectStrideValue("Blendshape Index buffer stride was not 4!")
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            index = int.from_bytes(reader.read(4), "little", signed=True)
            self.indices.append(index)

    def decode(self, vertex_index: int) -> tuple[int, int] | None:
        """
        Decodes the packed (offset, count) range for a given vertex.

        Each entry is a single packed 32-bit value: a sentinel value of -1 means
        the vertex has no blend shape targets. Otherwise, the low 8 bits are the
        number of blend shape targets ("count") that affect the vertex, and the
        remaining upper 24 bits are the starting offset ("offset") of that
        vertex's targets inside `BlendShapePositionBuffer.positions`.

        Returns:
        - A tuple of (offset, count), or None if the vertex has no blend shapes.
        """
        if vertex_index >= len(self.indices):
            return None
        value = self.indices[vertex_index]
        if value == -1:
            return None
        offset = value >> 8
        count = value & 0xFF
        return (offset, count)
