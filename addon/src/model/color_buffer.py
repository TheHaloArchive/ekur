# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from ..exceptions import IncorrectStrideValue

__all__ = ["ColorBuffer"]


class ColorBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.color: list[tuple[int, int, int, int]] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        if self.stride != 4:
            raise IncorrectStrideValue("Color buffer stride was not 4!")
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            a = int.from_bytes(reader.read(1))
            r = int.from_bytes(reader.read(1))
            g = int.from_bytes(reader.read(1))
            b = int.from_bytes(reader.read(1))
            self.color.append((a, r, g, b))
