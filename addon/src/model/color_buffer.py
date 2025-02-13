# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from ..exceptions import IncorrectStrideValue


class ColorBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.a: int = 0
        self.r: int = 0
        self.g: int = 0
        self.b: int = 0

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        if self.stride != 4:
            raise IncorrectStrideValue("Color buffer stride was not 4!")
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            self.a = int.from_bytes(reader.read(1))
            self.r = int.from_bytes(reader.read(1))
            self.g = int.from_bytes(reader.read(1))
            self.b = int.from_bytes(reader.read(1))
