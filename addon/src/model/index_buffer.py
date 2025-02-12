from enum import IntEnum
from io import BufferedReader


class IndexBufferType(IntEnum):
    Default = 0
    LineList = 1
    LineStrip = 2
    TriangleList = 3
    TrianglePatch = 4
    TriangleStrip = 5
    QuadList = 6


class IndexBuffer:
    def __init__(self) -> None:
        self.index_buffer_type: IndexBufferType = IndexBufferType.Default
        self.stride: int = -1
        self.count: int = 0
        self.indices: list[int] = []

    def read(self, reader: BufferedReader) -> None:
        self.index_buffer_type = IndexBufferType(int.from_bytes(reader.read(1), "little"))
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            index = int.from_bytes(reader.read(self.stride), "little")
            self.indices.append(index)
