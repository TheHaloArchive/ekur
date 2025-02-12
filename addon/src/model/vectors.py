from io import BufferedReader
import struct

from mathutils import Matrix


class Vector4:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.w: float = 0.0

    def read(self, reader: BufferedReader) -> None:
        self.x = struct.unpack("f", reader.read(4))[0]
        self.y = struct.unpack("f", reader.read(4))[0]
        self.z = struct.unpack("f", reader.read(4))[0]
        self.w = struct.unpack("f", reader.read(4))[0]

    def to_vector(self) -> list[float]:
        return [self.x, self.y, self.z, self.w]


class NormalizedVector4:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.w: float = 0.0

    def read(self, reader: BufferedReader) -> None:
        x = int.from_bytes(reader.read(2), "little")
        y = int.from_bytes(reader.read(2), "little")
        z = int.from_bytes(reader.read(2), "little")
        w = int.from_bytes(reader.read(2), "little")
        self.x = x / 65535.0
        self.y = y / 65535.0
        self.z = z / 65535.0
        self.w = w / 65535.0

    def to_vector(self) -> list[float]:
        return [self.x, self.y, self.z]


class Matrix4x4:
    def __init__(self) -> None:
        self.m1: Vector4 = Vector4()
        self.m2: Vector4 = Vector4()
        self.m3: Vector4 = Vector4()
        self.m4: Vector4 = Vector4()

    def read(self, reader: BufferedReader) -> None:
        self.m1.read(reader)
        self.m2.read(reader)
        self.m3.read(reader)
        self.m4.read(reader)

    def to_matrix(self) -> Matrix:
        matrix = Matrix(
            (self.m1.to_vector(), self.m2.to_vector(), self.m3.to_vector(), self.m4.to_vector())
        )
        return matrix


class Vector3:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0

    def read(self, reader: BufferedReader) -> None:
        self.x = struct.unpack("f", reader.read(4))[0]
        self.y = struct.unpack("f", reader.read(4))[0]
        self.z = struct.unpack("f", reader.read(4))[0]

    def to_vector(self) -> list[float]:
        return [self.x, self.y, self.z]


class NormalizedVector2:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0

    def read(self, reader: BufferedReader) -> None:
        x = int.from_bytes(reader.read(2), "little")
        y = int.from_bytes(reader.read(2), "little")
        self.x = x / 65535.0
        self.y = y / 65535.0

    def to_vector(self) -> list[float]:
        return [self.x, self.y]


class NormalizedVector101010:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0

    def read(self, reader: BufferedReader) -> None:
        val = int.from_bytes(reader.read(4), "little")
        self.x = (val & 0x3FF) / 1023.0
        self.y = (val >> 10 & 0x3FF) / 1023.0
        self.z = (val >> 20 & 0x3FF) / 1023.0

    def to_vector(self) -> list[float]:
        return [self.x, self.y, self.z]


class Bounds:
    def __init__(self) -> None:
        self.min: float = 0.0
        self.max: float = 0.0

    def read(self, reader: BufferedReader) -> None:
        self.min = struct.unpack("f", reader.read(4))[0]
        self.max = struct.unpack("f", reader.read(4))[0]


class NormalizedVector1010102PackedAsUnorm:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.w: float = 0.0

    def read(self, reader: BufferedReader) -> None:
        packed = int.from_bytes(reader.read(4), "little")
        self.x = ((packed & 0x3FF) / 1023.0) * 2 - 1.0
        self.y = (((packed >> 10) & 0x3FF) / 1023.0) * 2 - 1.0
        self.z = (((packed >> 20) & 0x3FF) / 1023.0) * 2 - 1.0
        self.w = (((packed >> 30) & 0x3) / 3.0) * 2 - 1.0

    def to_vector(self) -> list[float]:
        return [self.x, self.y, self.z]
