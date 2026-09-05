# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
import time
from pathlib import Path
from typing import final

import bpy
from bpy.types import Collection, Context, Event, Object, Operator
from mathutils import Matrix

from ..json_definitions import Instance, Level
from ..model.importer.model_importer import ModelImporter
from ..terrain_importer import TerrainImporter
from ..ui.level_options import LevelOptionsType, get_level_options
from ..utils import get_data_folder, read_json_file

__all__ = ["ImportLevelOperator"]


def _collection(name: str, parent: Collection | None = None) -> Collection:
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        if parent is None and bpy.context.scene is not None:
            parent = bpy.context.scene.collection
        if parent is not None:
            parent.children.link(coll)
    return coll


@final
class ImportLevelOperator(Operator):
    bl_idname = "ekur.importlevel"
    bl_label = "Import"
    bl_description = "Import a whole level"
    bl_options = {"REGISTER", "UNDO"}

    _timer = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._queue: list[tuple[Instance, Collection]] = []
        self._cache: dict[str, list[Object]] = {}
        self._missing: set[str] = set()
        self._cursor: int = 0
        self._placed: int = 0
        self._batch: int = 250
        self._started: float = 0.0
        self._data: str = ""

    def _geometry(self, global_id: str, materials: list[int]) -> list[Object]:
        cached = self._cache.get(global_id)
        if cached is not None:
            return cached

        path = Path(f"{self._data}/runtime_geo/{global_id}.ekur")
        if not path.is_file():
            path = Path(f"{self._data}/models/{global_id}.ekur")
        if not path.is_file():
            self._missing.add(global_id)
            self._cache[global_id] = []
            return []

        importer = ModelImporter()
        objects = importer.start_import(str(path), materials=materials, bones=False)

        master = _collection("Master Geometries")
        master.hide_viewport = True
        master.hide_render = True
        for obj in objects:
            scene = bpy.context.scene
            if scene is not None and obj.name in scene.collection.objects:
                scene.collection.objects.unlink(obj)
            if obj.name not in master.objects:
                master.objects.link(obj)

        self._cache[global_id] = objects
        return objects

    def _place(self, instance: Instance, target: Collection) -> None:
        objects = self._geometry(str(instance["global_id"]), instance["material"])
        if not objects:
            return

        rotation = Matrix(
            (
                (instance["forward"][0], instance["left"][0], instance["up"][0], 0.0),
                (instance["forward"][1], instance["left"][1], instance["up"][1], 0.0),
                (instance["forward"][2], instance["left"][2], instance["up"][2], 0.0),
                (0.0, 0.0, 0.0, 1.0),
            )
        )
        world = Matrix.LocRotScale(
            instance["position"], rotation.to_quaternion(), instance["scale"]
        )
        for source in objects:
            instance_obj = bpy.data.objects.new(
                name=f"{source.name}_instance", object_data=source.data
            )
            instance_obj.matrix_world = world
            target.objects.link(instance_obj)
        self._placed += 1

    def _terrain(self, level: Level, options: LevelOptionsType, target: Collection) -> None:
        if not options.import_terrain:
            return
        name = level.get("terrain")
        if not name:
            return
        meta = Path(self._data) / "terrain" / Path(name).name
        if not meta.is_file():
            self.report({"WARNING"}, f"Terrain record {meta.name} is not in the data folder.")
            return
        importer = TerrainImporter(meta)
        obj = importer.build(step=options.terrain_step)
        if obj is None:
            return
        target.objects.link(obj)
        self.report({"INFO"}, f"Terrain: {importer.summary(obj, options.terrain_step)}")

    def invoke(self, context: Context | None, _event: Event | None) -> set[str]:  # ty:ignore[invalid-method-override]
        if context is None or context.collection is None or context.window_manager is None:
            return {"CANCELLED"}
        options = get_level_options()
        level = read_json_file(Path(options.level_path), Level)
        if level is None:
            self.report({"ERROR"}, "Could not read the level file.")
            return {"CANCELLED"}

        self._data = get_data_folder()
        self._queue = []
        self._cache = {}
        self._missing = set()
        self._cursor = 0
        self._placed = 0
        self._batch = max(1, options.batch_size)
        self._started = time.perf_counter()

        name = level.get("name") or Path(options.level_path).stem
        root = _collection(name)
        for bsp in level["bsps"]:
            if not bsp["instances"]:
                continue
            if bsp["is_vista"] and not options.import_vista:
                continue
            if options.only_active_bsps and not bsp["is_active"] and not bsp["is_vista"]:
                continue
            target = _collection(f"{name}_{bsp['name']}", root)
            self._queue += [(instance, target) for instance in bsp["instances"]]

        self._terrain(level, options, root)

        window_manager = context.window_manager
        window_manager.progress_begin(0, len(self._queue))
        self._timer = window_manager.event_timer_add(0.01, window=context.window)
        window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context: Context | None, event: Event | None) -> set[str]:  # ty:ignore[invalid-method-override]
        if event is not None and event.type == "ESC":
            return self._finish(context, cancelled=True)
        if event is None or event.type != "TIMER":
            return {"PASS_THROUGH"}

        end = min(self._cursor + self._batch, len(self._queue))
        for index in range(self._cursor, end):
            instance, collection = self._queue[index]
            self._place(instance, collection)
        self._cursor = end

        if context is not None and context.window_manager is not None:
            context.window_manager.progress_update(self._cursor)
        if context is not None and context.workspace is not None:
            percent = 100.0 * self._cursor / max(1, len(self._queue))
            context.workspace.status_text_set(
                f"Importing level: {self._cursor:,}/{len(self._queue):,} ({percent:.0f}%)"
            )

        if self._cursor >= len(self._queue):
            return self._finish(context, cancelled=False)
        return {"RUNNING_MODAL"}

    def _finish(self, context: Context | None, cancelled: bool) -> set[str]:
        if context is not None and context.window_manager is not None:
            if self._timer is not None:
                context.window_manager.event_timer_remove(self._timer)
            context.window_manager.progress_end()
        if context is not None and context.workspace is not None:
            context.workspace.status_text_set(None)
        self._timer = None

        if self._missing:
            self.report(
                {"WARNING"},
                f"{len(self._missing)} geometry files were not in the data folder.",
            )
        self.report(
            {"INFO"},
            f"{'Cancelled after' if cancelled else 'Imported'} {self._placed:,} instances, "
            f"{len(self._cache)} unique meshes, {time.perf_counter() - self._started:.1f}s",
        )
        self._queue = []
        self._cache = {}
        return {"CANCELLED" if cancelled else "FINISHED"}

    def execute(self, context: Context | None) -> set[str]:  # ty:ignore[invalid-method-override]
        return self.invoke(context, None)
