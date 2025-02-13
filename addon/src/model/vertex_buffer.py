# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from collections.abc import Iterable, Iterator
from io import BufferedReader

from .vertex_type import VertexType
from .weight_extra_buffer import WeightExtraBuffer
from .weight_buffer import WeightBuffer
from .weight_index_buffer import WeightIndexBuffer
from .color_buffer import ColorBuffer
from .normal_buffer import NormalBuffer
from .buffer_flags import BufferFlags
from .uv_buffer import UVBuffer
from .position_buffer import PositionBuffer


class VertexBuffers:
    def __init__(self) -> None:
        self.position_buffer: PositionBuffer = PositionBuffer()
        self.uv0_buffer: UVBuffer = UVBuffer()
        self.uv1_buffer: UVBuffer = UVBuffer()
        self.uv2_buffer: UVBuffer = UVBuffer()
        self.normal_buffer: NormalBuffer = NormalBuffer()
        self.color_buffer: ColorBuffer = ColorBuffer()
        self.weight_index_buffer: WeightIndexBuffer = WeightIndexBuffer()
        self.weight_buffer: WeightBuffer = WeightBuffer()
        self.weight_extra_buffer: WeightExtraBuffer = WeightExtraBuffer()

    def read(self, reader: BufferedReader, flags: BufferFlags) -> None:
        self.flags = flags
        if flags.has_position:
            self.position_buffer.read(reader)
        if flags.has_uv0:
            self.uv0_buffer.read(reader)
        if flags.has_uv1:
            self.uv1_buffer.read(reader)
        if flags.has_uv2:
            self.uv2_buffer.read(reader)
        if flags.has_normal:
            self.normal_buffer.read(reader)
        if flags.has_color:
            self.color_buffer.read(reader)
        if flags.has_blend_indices:
            self.weight_index_buffer.read(reader)
        if flags.has_blend_weights:
            self.weight_buffer.read(reader)
        if flags.has_blend_weights_extra:
            self.weight_extra_buffer.read(reader)

    def enumerate_blendpairs(
        self, mesh_flags: VertexType
    ) -> Iterator[tuple[int, Iterable[int], Iterable[float]]]:
        """
        Iterates over all corresponding tuples of (index, blendindices, blendweights).
        The returned weights will be normalised and all index/weight channels will be accounted for.
        """

        dummy_weights = [1.0]
        blend_weights = []
        rigid = len(self.weight_buffer.weights) == 0
        implied = mesh_flags != VertexType.Skinned8Weights and self.flags.has_blend_weights
        blend_indicies = self.weight_index_buffer.indices
        if not rigid:
            blend_weights = self.weight_buffer.weights

        for i in range(len(self.position_buffer.positions)):
            indices = blend_indicies[i].to_vector()
            weights = dummy_weights if rigid else blend_weights[i].to_vector()

            # append a 1 to the end of the weights list
            if implied:
                weights = [*weights, 1.0]

            if rigid:
                # only take the first index (dummy_weights already only has one weight)
                indices = [indices[0]]
            elif 0 in weights:
                indices = list(indices[i] for i, w in enumerate(weights) if w > 0)
                weights = list(weights[i] for i, w in enumerate(weights) if w > 0)

            # normalise the weights before returning them so they all add up to 1
            weight_sum = sum(weights)
            if weight_sum > 0:
                weights = list(w / weight_sum for w in weights)

            yield (i, indices, weights)
