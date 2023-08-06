import typing
import logging
import inspect
import time
import os
import datetime

from ..metadata import get_blue_dot_sessions_metadata
from .convert import convert
from .wav2png import wav2png
from .compute_stats import compute_stats
from .post_wav2png import post_wav2png
from .primitive import primitive
from .post_primitive import post_primitive
from .pipeline_types import (
    PipelineFnReturnType,
    PipelineFnType,
    ComputeStatsPipelineFnType,
    ComputeStatsPipelineEndFnType
)


__all__ = [
    "convert",
    "wav2png",
    "post_wav2png",
    "primitive",
    "post_primitive",
    "get_formatted_output_dir",
    "get_most_recent_dir",
    "process_pipeline_stages",
    "Pipeline"
    # "pipeline_sig",
    # "pipeline_stage_count",
    # "pipeline_stage_names",
]


module_logger = logging.getLogger(__name__)


def get_formatted_output_dir(output_dir):
    output_dir_dir = os.path.dirname(output_dir)
    endpoint = os.path.basename(output_dir)
    if "%" in endpoint:
        module_logger.debug(f"get_formatted_output_dir: detected datetime output dir")
        now = datetime.datetime.now()
        endpoint = now.strftime(endpoint)
        module_logger.debug(f"get_formatted_output_dir: endpoint={endpoint}")
    output_dir = os.path.join(output_dir_dir, endpoint)
    return output_dir


def get_most_recent_dir(output_dir):
    output_dir_dir = os.path.dirname(output_dir)
    module_logger.debug(f"get_most_recent_dir: "
                        f"output_dir parent dir {output_dir_dir}")
    sub_dirs = []
    for path in os.listdir(output_dir_dir):
        path = os.path.join(output_dir_dir, path)
        if os.path.isdir(path):
            sub_dirs.append([os.path.getmtime(path), path])

    sorted_sub_dirs = sorted(sub_dirs, key=lambda val: val[0])
    most_recent = sorted_sub_dirs[-1][1]
    module_logger.debug((f"get_most_recent_dir: most recently "
                         f"modified dir in parent dir {most_recent}"))

    return most_recent



def process_pipeline_stages(stages_str: str) -> slice:
    module_logger.debug(f"process_pipeline_stages: stages_str={stages_str}")
    if ":" in stages_str:
        stages_list: typing.List[typing.Optional[int]] = []
        split = stages_str.split(":")
        for val in split:
            try:
                stages_list.append(int(val))
            except ValueError:
                stages_list.append(None)
        stages = slice(*stages_list)
    else:
        stages = slice(int(stages_str))
    module_logger.debug(f"process_pipeline_stages: stages={stages}")
    return stages

def _time(fn, *args, **kwargs):
    t0 = time.time()
    res = fn(*args, **kwargs)
    delta = time.time() - t0
    return res, delta


class Pipeline:

    fn_names = [
        "convert_fn",
        "wav2png_fn",
        "post_wav2png_fn",
        "primitive_fn",
        "post_primitive_fn"
    ]

    def __init__(self,
        convert_fn: PipelineFnType,
        wav2png_fn: PipelineFnType,
        post_wav2png_fn: PipelineFnType,
        primitive_fn: PipelineFnType,
        post_primitive_fn: PipelineFnType
    ):
        """
        Run gemscape pipeline consisting of the following stages:

        conversion: Convert .mp3 input to .wav
        wav2png: Create a visual representation of .wav file
        post wav2png: Modify wav2png output before passing to primitive
        primtive: Call `primitive`, creating SVG from PNG
        post primitive: Modify primitive output

        Returns:
            function that takes as input .mp3 file.
        """
        self.convert_fn = convert_fn
        self.wav2png_fn = wav2png_fn
        self.post_wav2png_fn = post_wav2png_fn
        self.primitive_fn = primitive_fn
        self.post_primitive_fn = post_primitive_fn

        self.fns = [
            self.convert_fn,
            self.wav2png_fn,
            self.post_wav2png_fn,
            self.primitive_fn,
            self.post_primitive_fn
        ]


    def __len__(self):
        return len(self.fns)

    def __call__(self, file_path: str, stages: list = None) -> typing.Generator[typing.Any, None, None]:

        track_metadata = get_blue_dot_sessions_metadata(file_path)
        module_logger.debug(f"pipeline._pipeline: track_metadata={track_metadata}")

        if stages is None:
            stages = list(range(len(self.fns)))

        module_logger.debug(f"pipeline._pipeline: stages={stages}")

        total_report = {
            "metadata": track_metadata
        }

        for idx, fn in enumerate(self.fns):
            # module_logger.debug(f"pipeline._pipeline: idx={idx}, stages[-1]={stages[-1]}")
            if idx == stages[-1] + 1:
                break
            if idx < stages[0]:
                module_logger.debug(f"pipeline: stage {idx}, calling {self.fn_names[idx]}({file_path}, dry_run=True) ")
                (file_path, report), delta = _time(fn, file_path, dry_run=True, track_metadata=track_metadata)
            else:
                module_logger.debug(f"pipeline: stage {idx}, calling {self.fn_names[idx]}({file_path})")
                (file_path, report), delta = _time(fn, file_path, track_metadata=track_metadata)
            module_logger.debug(f"pipeline: stage {idx}, {self.fn_names[idx]} took {delta:.2f} sec")
            total_report[self.fn_names[idx]] = report
            yield file_path, report, total_report


def compute_stats_pipeline(
    convert_fn: ComputeStatsPipelineFnType,
    compute_stats_fn: ComputeStatsPipelineEndFnType
):

    def _pipeline(file_path: str) -> typing.Generator[typing.Union[str, dict], None, None]:

        module_logger.debug(f"pipeline: calling convert_fn({file_path}) ")
        file_path, delta = _time(convert_fn, file_path)
        module_logger.debug(f"pipeline: convert_fn took {delta:.2f} sec")
        yield file_path
        module_logger.debug(f"pipeline: calling compute_stats_fn({file_path}) ")
        res, delta = _time(compute_stats_fn, file_path)
        module_logger.debug(f"pipeline: compute_stats_fn took {delta:.2f} sec")
        yield res

    return _pipeline


compute_stats_pipeline_sig = inspect.signature(compute_stats_pipeline)
compute_stats_pipeline_stage_count = len(compute_stats_pipeline_sig.parameters)
compute_stats_pipeline_stage_names = [param for param in compute_stats_pipeline_sig.parameters]
