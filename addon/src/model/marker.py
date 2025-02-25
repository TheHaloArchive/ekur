# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader


from .vectors import Vector3, Vector4

__all__ = ["MarkerInstance", "Marker"]


class MarkerInstance:
    def __init__(self) -> None:
        self.position: Vector3 = Vector3()
        self.rotation: Vector4 = Vector4()
        self.region_index: int = -1
        self.permutation_index: int = -1
        self.node_index: int = -1

    def read(self, reader: BufferedReader) -> None:
        self.position.read(reader)
        self.rotation.read(reader)
        self.region_index = int.from_bytes(reader.read(1), byteorder="little", signed=True)
        self.permutation_index = int.from_bytes(reader.read(4), byteorder="little", signed=True)
        self.node_index = int.from_bytes(reader.read(1), byteorder="little", signed=False)


class Marker:
    def __init__(self) -> None:
        self.name: int = -1
        self.instance_count: int = 0
        self.instances: list[MarkerInstance] = []

    def read(self, reader: BufferedReader) -> None:
        self.name = int.from_bytes(reader.read(4), byteorder="little", signed=True)
        self.instance_count = int.from_bytes(reader.read(4), byteorder="little", signed=True)
        for _ in range(self.instance_count):
            instance = MarkerInstance()
            instance.read(reader)
            self.instances.append(instance)
