from io import BufferedReader

from .buffer_flags import BufferFlags

from .vertex_buffer import VertexBuffers

from .index_buffer import IndexBuffer
from .submesh import Submesh


class Section:
    def __init__(self) -> None:
        self.region_name: int = -1
        self.permutation_name: int = -1
        self.submesh_count: int = 0
        self.submeshes: list[Submesh] = []
        self.index_buffer: IndexBuffer = IndexBuffer()
        self.vertex_flags: BufferFlags = BufferFlags()
        self.vertex_buffer: VertexBuffers = VertexBuffers()

    def read(self, reader: BufferedReader) -> None:
        self.region_name = int.from_bytes(reader.read(4), "little", signed=True)
        self.permutation_name = int.from_bytes(reader.read(4), "little", signed=True)
        self.submesh_count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.submesh_count):
            submesh = Submesh()
            submesh.read(reader)
            self.submeshes.append(submesh)
        self.index_buffer.read(reader)
        self.vertex_flags.read(reader)
        self.vertex_buffer.read(reader, self.vertex_flags)
