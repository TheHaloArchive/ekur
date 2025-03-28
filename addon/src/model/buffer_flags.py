# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

__all__ = ["BufferFlags"]


class BufferFlags:
    def __init__(self) -> None:
        self.has_position: bool = False
        self.has_uv0: bool = False
        self.has_uv1: bool = False
        self.has_uv2: bool = False
        self.has_normal: bool = False
        self.has_color: bool = False
        self.has_blend_indices: bool = False
        self.has_blend_weights: bool = False
        self.has_blend_weights_extra: bool = False
        self.has_blendshape_index: bool = False
        self.has_blendshape_position: bool = False

    def read(self, reader: BufferedReader) -> None:
        self.has_position = bool.from_bytes(reader.read(1))
        self.has_uv0 = bool.from_bytes(reader.read(1))
        self.has_uv1 = bool.from_bytes(reader.read(1))
        self.has_uv2 = bool.from_bytes(reader.read(1))
        self.has_normal = bool.from_bytes(reader.read(1))
        self.has_color = bool.from_bytes(reader.read(1))
        self.has_blend_indices = bool.from_bytes(reader.read(1))
        self.has_blend_weights = bool.from_bytes(reader.read(1))
        self.has_blend_weights_extra = bool.from_bytes(reader.read(1))
        self.has_blendshape_index = bool.from_bytes(reader.read(1))
        self.has_blendshape_position = bool.from_bytes(reader.read(1))
