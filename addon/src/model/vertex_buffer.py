from io import BufferedReader

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
