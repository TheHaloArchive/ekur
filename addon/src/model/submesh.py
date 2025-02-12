# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader


class Submesh:
    def __init__(self) -> None:
        self.index_count: int = -1
        self.index_start: int = -1
        self.vertex_count: int = 0
        self.subset_count: int = 0
        self.subset_index: int = -1
        self.shader_index: int = -1

    def read(self, reader: BufferedReader) -> None:
        self.index_count = int.from_bytes(reader.read(4), "little", signed=True)
        self.index_start = int.from_bytes(reader.read(4), "little", signed=True)
        self.vertex_count = int.from_bytes(reader.read(2), "little")
        self.subset_count = int.from_bytes(reader.read(2), "little")
        self.subset_index = int.from_bytes(reader.read(2), "little", signed=True)
        self.shader_index = int.from_bytes(reader.read(2), "little", signed=True)
