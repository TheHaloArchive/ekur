# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from .vectors import Bounds

__all__ = ["BoundingBox"]


class BoundingBox:
    def __init__(self) -> None:
        self.x_bounds: Bounds = Bounds()
        self.y_bounds: Bounds = Bounds()
        self.z_bounds: Bounds = Bounds()
        self.u_bounds: Bounds = Bounds()
        self.v_bounds: Bounds = Bounds()
        self.u_bounds1: Bounds = Bounds()
        self.v_bounds1: Bounds = Bounds()
        self.u_bounds2: Bounds = Bounds()
        self.v_bounds2: Bounds = Bounds()

    def read(self, reader: BufferedReader) -> None:
        self.x_bounds.read(reader)
        self.y_bounds.read(reader)
        self.z_bounds.read(reader)
        self.u_bounds.read(reader)
        self.v_bounds.read(reader)
        self.u_bounds1.read(reader)
        self.v_bounds1.read(reader)
        self.u_bounds2.read(reader)
        self.v_bounds2.read(reader)

    @property
    def model_scale(self) -> list[tuple[float, float, float]]:
        return [
            (self.x_bounds.min, self.x_bounds.max, self.x_bounds.max - self.x_bounds.min),
            (self.y_bounds.min, self.y_bounds.max, self.y_bounds.max - self.y_bounds.min),
            (self.z_bounds.min, self.z_bounds.max, self.z_bounds.max - self.z_bounds.min),
        ]

    @property
    def uv_scale(self) -> list[tuple[float, float, float]]:
        return [
            (self.u_bounds.min, self.u_bounds.max, self.u_bounds.max - self.u_bounds.min),
            (self.v_bounds.min, self.v_bounds.max, self.v_bounds.max - self.v_bounds.min),
        ]

    @property
    def uv1_scale(self) -> list[tuple[float, float, float]]:
        return [
            (self.u_bounds1.min, self.u_bounds1.max, self.u_bounds1.max - self.u_bounds1.min),
            (self.v_bounds1.min, self.v_bounds1.max, self.v_bounds1.max - self.v_bounds1.min),
        ]

    @property
    def uv2_scale(self) -> list[tuple[float, float, float]]:
        return [
            (self.u_bounds2.min, self.u_bounds2.max, self.u_bounds2.max - self.u_bounds2.min),
            (self.v_bounds2.min, self.v_bounds2.max, self.v_bounds2.max - self.v_bounds2.min),
        ]
