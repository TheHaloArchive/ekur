# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from .vectors import NormalizedVector1010102PackedAsUnorm
from ..exceptions import IncorrectStrideValue

__all__ = ["NormalBuffer"]


class NormalBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.normals: list[NormalizedVector1010102PackedAsUnorm] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        if self.stride != 4:
            raise IncorrectStrideValue("Normal buffer stride was not 4!")
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            normal = NormalizedVector1010102PackedAsUnorm()
            normal.read(reader)
            self.normals.append(normal)
