# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from .buffer_flags import BufferFlags

from .vertex_buffer import VertexBuffers
from .vertex_type import VertexType
from .index_buffer import IndexBuffer
from .submesh import Submesh

__all__ = ["Section"]


class Section:
    def __init__(self) -> None:
        self.region_name: int = -1
        self.permutation_name: int = -1
        self.submesh_count: int = 0
        self.node_index: int = 0
        self.vertex_type: VertexType = VertexType.World
        self.use_dual_quat: bool = False
        self.submeshes: list[Submesh] = []
        self.index_buffer: IndexBuffer = IndexBuffer()
        self.vertex_flags: BufferFlags = BufferFlags()
        self.vertex_buffer: VertexBuffers = VertexBuffers()

    def read(self, reader: BufferedReader) -> None:
        self.region_name = int.from_bytes(reader.read(4), "little", signed=True)
        self.permutation_name = int.from_bytes(reader.read(4), "little", signed=True)
        self.submesh_count = int.from_bytes(reader.read(4), "little")
        self.node_index = int.from_bytes(reader.read(1), "little", signed=True)
        self.vertex_type = VertexType(int.from_bytes(reader.read(1), "little"))
        self.use_dual_quat = bool(int.from_bytes(reader.read(1), "little"))
        for _ in range(self.submesh_count):
            submesh = Submesh()
            submesh.read(reader)
            self.submeshes.append(submesh)
        self.index_buffer.read(reader)
        self.vertex_flags.read(reader)
        self.vertex_buffer.read(reader, self.vertex_flags)
