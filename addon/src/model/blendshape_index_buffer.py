# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
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
