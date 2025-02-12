# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader
from .vectors import NormalizedVector2


class UVBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.uv: list[NormalizedVector2] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        self.count = int.from_bytes(reader.read(4), "little")
        if self.stride % 4 != 0:
            raise ValueError("Invalid UV buffer stride")
        for _ in range(self.count):
            uv = NormalizedVector2()
            uv.read(reader)
            self.uv.append(uv)
