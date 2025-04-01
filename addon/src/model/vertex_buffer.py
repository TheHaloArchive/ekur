# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from collections.abc import Iterable, Iterator
from io import BufferedReader

from .blendshape_index_buffer import BlendShapeIndexBuffer
from .blendshape_position_buffer import BlendShapePositionBuffer
from .vertex_type import VertexType
from .weight_extra_buffer import WeightExtraBuffer
from .weight_buffer import WeightBuffer
from .weight_index_buffer import WeightIndexBuffer
from .color_buffer import ColorBuffer
from .normal_buffer import NormalBuffer
from .buffer_flags import BufferFlags
from .uv_buffer import UVBuffer
from .position_buffer import PositionBuffer

__all__ = ["VertexBuffers"]


class VertexBuffers:
    def __init__(self) -> None:
        self.flags: BufferFlags = BufferFlags()
        self.position_buffer: PositionBuffer = PositionBuffer()
        self.uv0_buffer: UVBuffer = UVBuffer()
        self.uv1_buffer: UVBuffer = UVBuffer()
        self.uv2_buffer: UVBuffer = UVBuffer()
        self.normal_buffer: NormalBuffer = NormalBuffer()
        self.color_buffer: ColorBuffer = ColorBuffer()
        self.weight_index_buffer: WeightIndexBuffer = WeightIndexBuffer()
        self.weight_buffer: WeightBuffer = WeightBuffer()
        self.weight_extra_buffer: WeightExtraBuffer = WeightExtraBuffer()
        self.blendshape_index_buffer: BlendShapeIndexBuffer = BlendShapeIndexBuffer()
        self.blendshape_position_buffer: BlendShapePositionBuffer = BlendShapePositionBuffer()

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
        if flags.has_blendshape_index:
            self.blendshape_index_buffer.read(reader)
        if flags.has_blendshape_position:
            self.blendshape_position_buffer.read(reader)

    def enumerate_blendpairs(
        self, mesh_flags: VertexType
    ) -> Iterator[tuple[int, Iterable[int], Iterable[float]]]:
        """
        Iterates over all corresponding tuples of (index, blendindices, blendweights).
        The returned weights will be normalised and all index/weight channels will be accounted for.
        """

        blend_indices = self.weight_index_buffer.indices

        # Determine vertex type
        rigid = len(self.weight_buffer.weights) == 0
        rigid_boned = mesh_flags == VertexType.RigidBoned and not self.flags.has_blend_weights
        implied = mesh_flags != VertexType.Skinned8Weights and self.flags.has_blend_weights

        # Only get blend weights if we're not using rigid or rigid_boned
        blend_weights = [] if (rigid or rigid_boned) else self.weight_buffer.weights

        for i in range(len(self.position_buffer.positions)):
            if i >= len(blend_indices):
                continue

            indices = [int(x) for x in blend_indices[i].vector]

            if rigid or rigid_boned:
                # For rigid boned, each index keeps its actual bone index value
                # We assign weight 1.0 to each bone index
                weights = [1.0] * len(indices)
            else:
                # For skinned vertices, get the weights from the buffer
                if i >= len(blend_weights):
                    continue
                weights = blend_weights[i].vector.to_tuple()

                # Append a 1.0 to the end of weights list for implied weights
                if implied:
                    weights = [*weights, 1.0]

                # Filter out zero weights and corresponding indices
                if 0 in weights:
                    valid_pairs = [(idx, w) for idx, w in zip(indices, weights) if w > 0]
                    indices = [pair[0] for pair in valid_pairs]
                    weights = [pair[1] for pair in valid_pairs]

            # Normalize the weights so they all add up to 1
            weight_sum = sum(weights)
            if weight_sum > 0:
                weights = [w / weight_sum for w in weights]

            yield (i, indices, weights)
