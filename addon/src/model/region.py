# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

__all__ = ["Permutation"]


class Permutation:
    def __init__(self) -> None:
        self.name: int = -1
        self.section_count: int = 0
        self.section_index: int = 0

    def read(self, reader: BufferedReader) -> None:
        self.name = int.from_bytes(reader.read(4), "little", signed=True)
        self.section_count = int.from_bytes(reader.read(2), "little")
        self.section_index = int.from_bytes(reader.read(2), "little")


class Region:
    def __init__(self) -> None:
        self.name: int = -1
        self.permutation_count: int = 0
        self.permutations: list[Permutation] = []

    def read(self, reader: BufferedReader) -> None:
        self.name = int.from_bytes(reader.read(4), "little", signed=True)
        self.permutation_count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.permutation_count):
            permutation = Permutation()
            permutation.read(reader)
            self.permutations.append(permutation)
