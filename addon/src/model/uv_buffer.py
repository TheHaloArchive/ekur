# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from ..exceptions import IncorrectStrideValue
from .vectors import NormalizedVector2

__all__ = ["UVBuffer"]


class UVBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.uv: list[NormalizedVector2] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        if self.stride != 4:
            raise IncorrectStrideValue("UV buffer stride was not 4!")
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            uv = NormalizedVector2()
            uv.read(reader)
            self.uv.append(uv)
