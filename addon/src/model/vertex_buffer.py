from io import BufferedReader

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
