# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive

import logging
import sys
from array import array
from pathlib import Path

import bpy
from bpy.types import Mesh, Object
from mathutils import Vector

from .json_definitions import Terrain
from .utils import read_json_file

__all__ = ["TerrainImporter"]


def _samples(count: int, step: int) -> list[int]:
    """Sample indices along one axis, always including the last one.

    A step that does not divide the axis evenly would otherwise stop short of
    the far edge, leaving a gap of up to step - 1 samples.
    """
    taken = list(range(0, count, step))
    if taken[-1] != count - 1:
        taken.append(count - 1)
    return taken


class TerrainImporter:
    def __init__(self, meta_path: str | Path) -> None:
        self.meta_path = Path(meta_path)
        self.meta: Terrain | None = read_json_file(self.meta_path, Terrain)

    @property
    def name(self) -> str:
        if self.meta is None:
            return self.meta_path.stem
        return str(self.meta.get("name") or self.meta_path.stem)

    def _heights(self) -> array | None:
        if self.meta is None:
            return None
        raw_name = self.meta.get("heightfield") or f"{self.meta_path.stem}.r16"
        raw = self.meta_path.parent / Path(raw_name).name
        if not raw.is_file():
            logging.error(f"Terrain heightfield missing: {raw}")
            return None
        width, height = self.meta["grid"]
        heights = array("H")
        with open(raw, "rb") as file:
            try:
                heights.fromfile(file, width * height)
            except EOFError:
                logging.error(f"Terrain heightfield is shorter than {width}x{height}")
                return None
        if sys.byteorder == "big":
            heights.byteswap()
        return heights

    def build(self, step: int = 4, name: str | None = None) -> Object | None:
        """Build the terrain mesh.

        step decimates the sample grid; the source is 0.1 world units per
        sample.
        """
        heights = self._heights()
        if heights is None or self.meta is None:
            return None

        full_width, full_height = self.meta["grid"]
        step = max(1, int(step))
        rows = _samples(full_height, step)
        columns = _samples(full_width, step)
        row_count, column_count = len(rows), len(columns)

        px, py, pz = self.meta["position"]
        sx, sy, sz = self.meta["size"]
        xs = [px - sx / 2.0 + column * (sx / (full_width - 1)) for column in columns]
        ys = [py - sy / 2.0 + row * (sy / (full_height - 1)) for row in rows]
        us = [column / (full_width - 1) for column in columns]
        vs = [row / (full_height - 1) for row in rows]

        cells = self._cells(rows, columns)
        if not cells:
            logging.warning(f"Terrain {self.name} has no active cells.")
            return None

        # Only vertices a surviving face uses are worth building
        used = bytearray(row_count * column_count)
        for row, column in cells:
            corner = row * column_count + column
            used[corner] = used[corner + 1] = 1
            corner += column_count
            used[corner] = used[corner + 1] = 1

        scale = sz / 65535.0
        remap = [-1] * (row_count * column_count)
        verts: list[Vector] = []
        for row in range(row_count):
            sample_row = rows[row] * full_width
            for column in range(column_count):
                corner = row * column_count + column
                if not used[corner]:
                    continue
                remap[corner] = len(verts)
                verts.append(
                    Vector(
                        (
                            xs[column],
                            ys[row],
                            pz + heights[sample_row + columns[column]] * scale,
                        )
                    )
                )

        faces = []
        uvs = array("f")
        for row, column in cells:
            top = row * column_count + column
            bottom = top + column_count
            faces.append(
                (remap[top], remap[top + 1], remap[bottom + 1], remap[bottom])
            )
            uvs.extend(
                (
                    us[column],
                    vs[row],
                    us[column + 1],
                    vs[row],
                    us[column + 1],
                    vs[row + 1],
                    us[column],
                    vs[row + 1],
                )
            )

        mesh_name = name or f"{self.name}_terrain"
        mesh = bpy.data.meshes.new(mesh_name)
        mesh.from_pydata(verts, [], faces)
        layer = mesh.uv_layers.new(name="UVMap")
        layer.data.foreach_set("uv", uvs)
        mesh.shade_smooth()
        _ = mesh.validate()
        mesh.update()
        return bpy.data.objects.new(mesh_name, mesh)

    def summary(self, obj: Object, step: int = 4) -> str:
        mesh = obj.data
        if self.meta is None or not isinstance(mesh, Mesh):
            return "no terrain record"
        width, _ = self.meta["grid"]
        sx, sy, _ = self.meta["size"]
        spacing = sx * max(1, int(step)) / (width - 1)
        return (
            f"{len(mesh.vertices):,} verts, {len(mesh.polygons):,} faces, "
            f"{spacing:.2f} wu spacing, {sx:.0f}x{sy:.0f} wu"
        )

    def _cells(self, rows: list[int], columns: list[int]) -> list[tuple[int, int]]:
        """The cells of the sampled grid that have a surface.
        """
        cells = [
            (row, column)
            for row in range(len(rows) - 1)
            for column in range(len(columns) - 1)
        ]
        if self.meta is None:
            return cells
        active = self.meta.get("active_leaf_indices")
        leaf_side = int(self.meta.get("leaf_node_edge_count", 0))
        if not active or leaf_side <= 0:
            return cells

        full_width, full_height = self.meta["grid"]
        leaf_rows = [
            min((rows[row] + rows[row + 1]) * leaf_side // (2 * (full_height - 1)), leaf_side - 1)
            for row in range(len(rows) - 1)
        ]
        leaf_columns = [
            min(
                (columns[column] + columns[column + 1]) * leaf_side // (2 * (full_width - 1)),
                leaf_side - 1,
            )
            for column in range(len(columns) - 1)
        ]
        # Grouping by leaf row lets whole bands of empty map be skipped without
        # testing every cell in them.
        active_columns: dict[int, set[int]] = {}
        for leaf in active:
            active_columns.setdefault(leaf // leaf_side, set()).add(leaf % leaf_side)

        return [
            (row, column)
            for row, leaf_row in enumerate(leaf_rows)
            if (wanted := active_columns.get(leaf_row))
            for column, leaf_column in enumerate(leaf_columns)
            if leaf_column in wanted
        ]
