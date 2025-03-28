# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from .vectors import WordVector3DNormalizedWith4Word
from ..exceptions import IncorrectStrideValue

__all__ = ["BlendShapePositionBuffer"]


class BlendShapePositionBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.positions: list[list[WordVector3DNormalizedWith4Word]] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        if self.stride != 8:
            raise IncorrectStrideValue("Blendshape position buffer stride was not 8!")
        self.count = int.from_bytes(reader.read(4), "little")
        positions: list[WordVector3DNormalizedWith4Word] = []
        for _ in range(self.count):
            position = WordVector3DNormalizedWith4Word()
            position.read(reader)
            positions.append(position)

        unique_index: set[int] = set()
        unique_index.update([x.index for x in positions])
        print(unique_index)

        for unique in unique_index:
            self.positions.append([x for x in positions if x.index == unique])
