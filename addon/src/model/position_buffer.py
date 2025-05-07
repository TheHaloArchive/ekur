# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from .vectors import NormalizedVector4
from ..exceptions import IncorrectStrideValue

__all__ = ["PositionBuffer"]


class PositionBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.positions: list[NormalizedVector4] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        if self.stride != 8:
            raise IncorrectStrideValue("Position buffer stride was not 8!")
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            position = NormalizedVector4()
            position.read(reader)
            self.positions.append(position)
