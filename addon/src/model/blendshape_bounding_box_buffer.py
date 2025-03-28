# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader
from .vectors import Vector3

__all__ = ["BlendShapeBoundingBox"]


class BlendShapeBoundingBox:
    def __init__(self) -> None:
        self.position_scale: Vector3 = Vector3()
        self.position_offset: Vector3 = Vector3()
        self.normal_scale: Vector3 = Vector3()
        self.normal_offset: Vector3 = Vector3()

    def read(self, reader: BufferedReader) -> None:
        self.position_scale.read(reader)
        self.position_offset.read(reader)
        self.normal_scale.read(reader)
        self.normal_offset.read(reader)
