from io import BufferedReader
from .vectors import NormalizedVector4


class PositionBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.positions: list[NormalizedVector4] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            position = NormalizedVector4()
            position.read(reader)
            self.positions.append(position)
