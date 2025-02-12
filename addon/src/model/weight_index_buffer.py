from io import BufferedReader


class WeightIndexBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.indices: list[int] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            index = int.from_bytes(reader.read(self.stride), "little")
            self.indices.append(index)
