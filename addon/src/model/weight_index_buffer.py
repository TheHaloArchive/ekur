# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from .vectors import ByteVector4
from ..exceptions import IncorrectStrideValue

__all__ = ["WeightIndexBuffer"]


class WeightIndexBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.indices: list[ByteVector4] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        if self.stride % 2 != 0:
            raise IncorrectStrideValue("WeightIndex buffer stride was not a multiple of 2!")

        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            vector = ByteVector4()
            vector.read(reader)
            self.indices.append(vector)
