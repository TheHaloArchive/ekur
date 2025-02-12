# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader
from .vectors import NormalizedVector101010


class WeightBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.weights: list[NormalizedVector101010] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            weight = NormalizedVector101010()
            weight.read(reader)
            self.weights.append(weight)
