# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader

from .rtgo_offset import RtgoOffset
from .blendshape_bounding_box_buffer import BlendShapeBoundingBox
from .section import Section
from .bounding_box import BoundingBox
from .marker import Marker
from .bone import Bone
from .region import Region
from .header import ModelHeader

__all__ = ["Model"]


class Model:
    def __init__(self) -> None:
        self.header: ModelHeader = ModelHeader()
        self.regions: list[Region] = []
        self.bones: list[Bone] = []
        self.markers: list[Marker] = []
        self.bounding_boxes: list[BoundingBox] = []
        self.offsets: list[RtgoOffset] = []
        self.materials: list[int] = []
        self.sections: list[Section] = []
        self.blendshape_bounding_boxes: list[BlendShapeBoundingBox] = []

    def read(self, reader: BufferedReader) -> None:
        self.header.read(reader)
        for _ in range(self.header.region_count):
            region = Region()
            region.read(reader)
            self.regions.append(region)
        for _ in range(self.header.node_count):
            bone = Bone()
            bone.read(reader)
            self.bones.append(bone)
        for _ in range(self.header.marker_count):
            marker = Marker()
            marker.read(reader)
            self.markers.append(marker)
        for _ in range(self.header.bounding_box_count):
            bounding_box = BoundingBox()
            bounding_box.read(reader)
            self.bounding_boxes.append(bounding_box)
        for _ in range(self.header.offset_count):
            offset = RtgoOffset()
            offset.read(reader)
            self.offsets.append(offset)
        for _ in range(self.header.material_count):
            material = int.from_bytes(reader.read(4), "little", signed=True)
            self.materials.append(material)
        for _ in range(self.header.blendshape_bounding_box_count):
            blendshape_bounding_box = BlendShapeBoundingBox()
            blendshape_bounding_box.read(reader)
            self.blendshape_bounding_boxes.append(blendshape_bounding_box)
        for _ in range(self.header.section_count):
            section = Section()
            section.read(reader)
            self.sections.append(section)
