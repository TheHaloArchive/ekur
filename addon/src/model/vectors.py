# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import struct

from io import BufferedReader
from typing import cast
from mathutils import Matrix, Vector

__all__ = [
    "Vector4",
    "NormalizedVector4",
    "Matrix4x4",
    "Vector3",
    "NormalizedVector2",
    "NormalizedVector101010",
    "ByteVector4",
    "Bounds",
    "NormalizedVector1010102PackedAsUnorm",
]


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

    @property
    def vector(self) -> Vector:
        return Vector((self.x, self.y, self.z, self.w))


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

    @property
    def vector(self) -> Vector:
        return Vector((self.x, self.y, self.z))


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

    @property
    def matrix(self) -> Matrix:
        return Matrix(
            (
                self.m1.vector.to_tuple(),
                self.m2.vector.to_tuple(),
                self.m3.vector.to_tuple(),
                self.m4.vector.to_tuple(),
            )
        )


class Vector3:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0

    def read(self, reader: BufferedReader) -> None:
        self.x = struct.unpack("f", reader.read(4))[0]
        self.y = struct.unpack("f", reader.read(4))[0]
        self.z = struct.unpack("f", reader.read(4))[0]

    @property
    def vector(self) -> Vector:
        return Vector((self.x, self.y, self.z))


class WordVector3DNormalizedWith4Word:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.index: int = 0

    def read(self, reader: BufferedReader) -> None:
        x = int.from_bytes(reader.read(2), "little")
        y = int.from_bytes(reader.read(2), "little")
        z = int.from_bytes(reader.read(2), "little")
        self.index = int.from_bytes(reader.read(2), "little")
        self.x = x / 65535.0
        self.y = y / 65535.0
        self.z = z / 65535.0

    @property
    def vector(self) -> Vector:
        return Vector((self.x, self.y, self.z))


class NormalizedVector2:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0

    def read(self, reader: BufferedReader) -> None:
        x = int.from_bytes(reader.read(2), "little")
        y = int.from_bytes(reader.read(2), "little")
        self.x = x / 65535.0
        self.y = y / 65535.0

    @property
    def vector(self) -> Vector:
        return Vector((self.x, self.y))


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

    @property
    def vector(self) -> Vector:
        return Vector((self.x, self.y, self.z))


class ByteVector4:
    def __init__(self) -> None:
        self.x: int = 0
        self.y: int = 0
        self.z: int = 0
        self.w: int = 0

    def read(self, reader: BufferedReader) -> None:
        self.x = int.from_bytes(reader.read(1))
        self.y = int.from_bytes(reader.read(1))
        self.z = int.from_bytes(reader.read(1))
        self.w = int.from_bytes(reader.read(1))

    @property
    def vector(self) -> Vector:
        return Vector((self.x, self.y, self.z, self.w))


class ShortVector4:
    def __init__(self) -> None:
        self.x: int = 0
        self.y: int = 0
        self.z: int = 0
        self.w: int = 0

    def read(self, reader: BufferedReader) -> None:
        self.x = int.from_bytes(reader.read(2), byteorder="little")
        self.y = int.from_bytes(reader.read(2), byteorder="little")
        self.z = int.from_bytes(reader.read(2), byteorder="little")
        self.w = int.from_bytes(reader.read(2), byteorder="little")

    @property
    def vector(self) -> Vector:
        return Vector((self.x, self.y, self.z, self.w))


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

        max_10_bit = (1 << 10) - 1  # 1023
        max_2_bit = (1 << 2) - 1  # 3

        self.x = (packed & max_10_bit) / max_10_bit * 2.0 - 1.0
        self.y = ((packed >> 10) & max_10_bit) / max_10_bit * 2.0 - 1.0
        self.z = ((packed >> 20) & max_10_bit) / max_10_bit * 2.0 - 1.0
        self.w = ((packed >> 30) & max_2_bit) / max_2_bit * 2.0 - 1.0

        length_sq = self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w
        if abs(length_sq) > 1e-6:
            length: float = cast(float, (length_sq) ** 0.5)
            self.x /= length
            self.y /= length
            self.z /= length
            self.w /= length

    @property
    def vector(self) -> Vector:
        return Vector((self.x, self.y, self.z))
