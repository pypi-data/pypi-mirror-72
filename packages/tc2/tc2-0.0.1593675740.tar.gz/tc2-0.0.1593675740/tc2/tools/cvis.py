import os
import json
import zstandard as zstd
import logging
import numpy as np
from typing import NamedTuple, List, Dict, Any, NewType, Optional, Callable, Union, Tuple
from collections import defaultdict
from tc2 import CommandType, FrameNum, UnitId
from tc2.constants import TCUnits, TCCommands


class CVisDrawCommand(NamedTuple):
    code: int
    args: List[int]
    str: str  # type: ignore
    cherrypi_ids_args_indices: List[int]


class CVisLog(NamedTuple):
    frame: int
    attachments: List[Any]
    file: str
    line: int
    message: str
    sev: int = 0  # Severity


class CVisUnitData(NamedTuple):
    last_seen_type: int = -1


class CVisUnitFirstSeen(NamedTuple):
    id: int
    type: int
    x: int  # pixel_x
    y: int  # pixel_y


def get_tensor_summary(name: str, tensor: np.ndarray) -> Dict[str, Any]:
    if tensor.size == 0:
        raise Exception(f"Cannot produce a summary for empty tensor {name}")
    HIST_NUM_BUCKETS = 10
    hist_count, bin_edges = np.histogram(tensor, HIST_NUM_BUCKETS)
    return {
        "shape": list(tensor.shape),
        "type": tensor.dtype.name,
        "min": tensor.min().item(),
        "max": tensor.max().item(),
        "mean": tensor.mean().item(),
        "std": tensor.std().item(),
        "median": np.median(tensor).item(),
        "absmedian": np.median(np.abs(tensor)).item(),
        "name": name,
        "hist": {
            "num_buckets": HIST_NUM_BUCKETS,
            "min": bin_edges[0].item(),
            "max": bin_edges[-1].item(),
            "values": [v.item() for v in hist_count],
        },
    }


class CVisDumper:
    def __init__(self, replay_file: str, suffix: str = ''):
        self._current_frame: FrameNum = FrameNum(0)
        self._replay_file: str = self.parse_replay_file(replay_file)
        self._suffix: str = '' if suffix == '' else f'.{suffix}'

        # Trace
        self._tasks: List[Any] = []  # Not implemented
        self._board_updates: List[Any] = []  # Not implemented
        self._draw_commands: Dict[int, List[CVisDrawCommand]] = defaultdict(
            list)
        self._game_values: Dict[FrameNum, Dict[str, float]] = defaultdict(dict)

        # Units
        self._units_info: Dict[UnitId, CVisUnitData] = defaultdict(
            CVisUnitData)
        self._units_updates: Dict[UnitId, Dict[FrameNum, dict]] = defaultdict(
            dict)
        self._units_first_seen: Dict[FrameNum, List[
            CVisUnitFirstSeen]] = defaultdict(list)

        # Logs
        self._logs: List[CVisLog] = []
        self._units_logs: Dict[int, List[CVisLog]] = defaultdict(list)

        self._cleanup_fn: List[Callable[[], None]] = []

        # Tensors
        self._tensor_summaries: Dict[FrameNum, List[dict]] = defaultdict(list)
        self._heatmaps_metadata: List[dict] = []
        self._heatmaps_writers: Dict[str, Any] = {}

    def step(self, tcstate) -> None:
        """
        Called right after we reach a new frame
        """
        frame = FrameNum(tcstate.frame_from_bwapi)
        self._current_frame = frame
        for listUnits in tcstate.units.values():
            for u in listUnits:
                updated = False
                if u.id not in self._units_info:
                    # New unit
                    self._units_info[u.id] = CVisUnitData(u.type)
                    self._units_first_seen[frame].append(
                        CVisUnitFirstSeen(
                            id=u.id, type=u.type, x=u.pixel_x, y=u.pixel_y))
                    updated = True
                elif u.type != self._units_info[u.id].last_seen_type:
                    updated = True
                if updated:
                    self._units_updates[u.id][frame] = {'type': u.type}

    def on_send(self, cmds: List[CommandType]) -> None:
        drawCmdToUnitIds: Dict[int, List[int]] = {
            TCCommands.draw_line: [],
            TCCommands.draw_unit_line: [0, 1],
            TCCommands.draw_unit_pos_line: [0],
            TCCommands.draw_unit_circle: [0],
            TCCommands.draw_circle: [],
            TCCommands.draw_text: [],
            TCCommands.draw_text_screen: [],
        }
        for cmd in cmds:
            if len(cmd) < 2 or cmd[0] not in drawCmdToUnitIds:
                continue
            self._draw_commands[self._current_frame].append(
                CVisDrawCommand(
                    code=cmd[0],
                    args=cmd[2:] if isinstance(cmd[1], str) else cmd[1:],
                    str=cmd[1] if isinstance(cmd[1], str) else '',
                    cherrypi_ids_args_indices=drawCmdToUnitIds[cmd[0]],
                ))

    def add_logger(self, logger: logging.Logger, unit_id: int,
                   level: Union[str, int]) -> None:
        class CVisLogHandler(logging.Handler):
            def __init__(self, cvis: 'CVisDumper', logs_list: List[CVisLog]):
                self.cvis = cvis
                self.logs_list = logs_list
                super().__init__()

            def emit(self, record: logging.LogRecord) -> None:
                self.logs_list.append(
                    CVisLog(
                        frame=self.cvis._current_frame,
                        attachments=[],
                        file=record.filename,
                        line=record.lineno,
                        message=record.getMessage(),
                        sev=record.levelno,
                    ))

        hdlr = CVisLogHandler(self, self._logs
                              if unit_id < 0 else self._units_logs[unit_id])
        hdlr.setLevel(level)
        logger.addHandler(hdlr)
        self._cleanup_fn.append(lambda: logger.removeHandler(hdlr))

    def dump_game_value(self, key: str, val: float,
                        frame: FrameNum = -1) -> None:
        if frame < 0:
            frame = self._current_frame
        self._game_values[frame][key] = val

    def write_trace(self) -> None:
        if self._replay_file == '':
            return

        def dump_list(l: list) -> list:
            return [x._asdict() for x in l]

        build_types_to_names: Dict[int, str] = {}
        for unit_name, unit_id in TCUnits.names.items():
            build_types_to_names[int(unit_id)] = unit_name

        trace = {
            "types_names": build_types_to_names,
            "tasks": self._tasks,
            "logs": dump_list(self._logs),
            "units_logs":
            {unit: dump_list(logs)
             for unit, logs in self._units_logs.items()},
            "units_updates": self._units_updates,
            "units_first_seen":
            {unit: dump_list(l)
             for unit, l in self._units_first_seen.items()},
            "board_updates": self._board_updates,
            "draw_commands":
            {frame: dump_list(c)
             for frame, c in self._draw_commands.items()},
            "trees": [],
            "heatmaps": self._heatmaps_metadata,
            "tensors_summaries": self._tensor_summaries,
            "game_values": self._game_values,
            "_version": 0
        }
        folder = f'{self._replay_file}.cvis{self._suffix}'

        # Cleanup first, because the IO might fail
        self._replay_file = ''
        for f in self._cleanup_fn:
            f()
        for w in self._heatmaps_writers.values():
            w.close()
        self._heatmaps_writers = {}
        self._cleanup_fn = []

        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, 'trace.json'), 'wb+') as fh:
            cctx = zstd.ZstdCompressor()
            with cctx.stream_writer(fh) as compressor:
                compressor.write(json.dumps(trace).encode('utf-8'))

    def parse_replay_file(self, file: str) -> str:
        # Function taken from OpenBW
        # See https://github.com/OpenBW/bwapi/blob/develop-openbw/bwapi/BWAPI/Source/BWAPI/GameEvents.cpp#L380
        def replace(cstr: str) -> str:
            if cstr == '\\':
                return '/'
            c = ord(cstr)
            if c >= 128:
                return cstr
            if c >= ord('a') and c <= ord('z'):
                return cstr
            if c >= ord('A') and c <= ord('Z'):
                return cstr
            if c >= ord('0') and c <= ord('9'):
                return cstr
            if cstr in ['-', '-', '_', '_', '.', '/', ' ']:
                return cstr
            return ''

        return ''.join([replace(c) for c in file])

    def dump_tensor_summary(self, name: str, tensor: np.ndarray) -> None:
        if tensor.size == 0:
            raise Exception(f"Empty tensor {name}")
        self._tensor_summaries[self._current_frame].append(
            get_tensor_summary(name, tensor))

    def dump_terrain_heatmap(
            self,
            name: str,
            tensor: np.ndarray,
            top_left_pixel: Tuple[int, int] = (0, 0),
            scaling_to_pixels: Tuple[float, float] = (8, 8)) -> None:
        if len(tensor.shape) != 2:
            raise Exception(
                f"Tensor {name} should be 2d, but has shape {tensor.shape}")
        if tensor.size == 0:
            raise Exception(f"Empty tensor {name}")

        if name not in self._heatmaps_writers:
            dump_directory = f'{self._replay_file}.cvis{self._suffix}'
            os.makedirs(dump_directory, exist_ok=True)
            filename = f'{dump_directory}/tensor__{len(self._heatmaps_writers)}__f{self._current_frame}.json.zstd.stream'

            # Open file to write tensor values in streaming
            fh = open(filename, 'wb+')
            cctx = zstd.ZstdCompressor()
            self._heatmaps_writers[name] = cctx.stream_writer(fh)

            # Write initial metadata
            self._heatmaps_metadata.append({
                "name": name,
                "filename": filename,
                "first_frame": self._current_frame,
            })

        summary = get_tensor_summary(name, tensor)
        cvis_tensor = {
            "top_left_pixel": top_left_pixel,
            "scaling": scaling_to_pixels,
            "dimension": tensor.shape,
            "data": tensor.flatten('C').tolist(),
            "summary": summary,
        }
        self._heatmaps_writers[name].write(
            json.dumps({
                "key": self._current_frame,
                "value": cvis_tensor,
            }).encode('utf-8'))
