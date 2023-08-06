# __main__.py
import sys
import typing
import os
import functools
import argparse
import logging
import json

import tqdm # type: ignore
import toml

from .pipeline import (
    Pipeline,
    get_formatted_output_dir,
    get_most_recent_dir,
    process_pipeline_stages,
    convert,
    wav2png,
    post_wav2png,
    primitive,
    post_primitive)
from .color import (
    interpolate_colors_fn_lookup,
    COLOR_SCHEMES,
    DEFAULT_COLOR_SCHEME_KEY)
from . import __version__

module_logger = logging.getLogger(__name__)

gemscapes_dir = os.path.dirname(os.path.abspath(__file__))


def create_parser():
    interpolate_colors_fn_names = ", ".join([f"'{name}'" for name in interpolate_colors_fn_lookup])
    color_scheme_names = ["'{}'".format(key) for key in COLOR_SCHEMES.keys()]
    color_scheme_str = ", ".join(color_scheme_names)

    pipeline_stage_names_str = ", ".join(Pipeline.fn_names)
    pipeline_stage_count = len(Pipeline.fn_names)

    parser = argparse.ArgumentParser(description="Create gemscapes from audio files")

    parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                        help="Files from which to create gemscapes")
    parser.add_argument("-d", "--outdir", action="store", dest="output_dir",
                        help="Put output files in this directory")
    parser.add_argument("-c", "--config", action="store",
                        help="Configuration file to use to modify output gemscapes")
    parser.add_argument("-r", "--report", nargs="+", dest="report",
                        help="Name or path of TOML or JSON (or any combination thereof) report file")
    parser.add_argument("-l", "--log", action="store",
                        help="Name or path of log file")
    parser.add_argument("--wav2png.width", dest="image_width", type=int,
                        help="image width in pixels")
    parser.add_argument("--wav2png.height",  dest="image_height", type=int,
                        help="image height in pixels")
    parser.add_argument("--wav2png.fft", dest="fft_size", type=int,
                        help="fft size, power of 2 for increased performance")
    parser.add_argument("--wav2png.peak-width", dest="peak_width", type=int,
                        help="Peak width in resulting images")
    parser.add_argument("--wav2png.color-scheme-file", action="store",
                        dest="color_scheme_file_path", type=str,
                        help="path to file containing color scheme configurations")
    parser.add_argument("--wav2png.color-scheme", action="store", dest="color_scheme", type=str,
                        help="name of the color scheme to use (one of: {})".format(color_scheme_str))
    parser.add_argument("--wav2png.color-space", dest="color_space", type=str,
                        help=("Color space in which to do interpolation. "
                              f"Available values are {interpolate_colors_fn_names}."))
    parser.add_argument("--wav2png.color-range", dest="color_range", type=float,
                        help="Percentage of color palette to use")
    parser.add_argument("--wav2png.mu-cut", dest="mu_cut", type=float,
                        help=("Don't consider spectral centroid values above this when "
                              "interpolating between spectral centroid and color palette"))
    parser.add_argument("--post-wav2png.v-scale",  dest="v_wssf", type=float,
                        help="Vertical white space scaling factor")
    parser.add_argument("--post-wav2png.h-scale",  dest="h_wssf", type=float,
                        help="Horizontal white space scaling factor")
    parser.add_argument("--primitive.primitive-exec", action="store", dest="primitive_exec", type=str,
                        help="Specify path to primitive executable.")
    parser.add_argument("--primitive.primitive-args", action="store", dest="primitive_args", type=str,
                        help="Specify arguments to pass to primitive executable. Must include '-n <int>' argument")
    parser.add_argument("--post-primitive.black-thresh", action="store", dest="thresh", type=float,
                        help="Specify a RGB distance threshold below which to set a shape's color to transparent")

    parser.add_argument("--pipeline-range", action="store", dest="pipeline_stage", type=str,
                        default="0:", help=("Specify which range of pipeline stages to compute. "
                                            "Uses Python range/slice syntax, eg if 1:3 is specified, then the second and third stage are done. "
                                            "If a single number is specified, the pipeline will do up to specified number, ie :{number}. "
                                             f"Total number of stages is {pipeline_stage_count}. "
                                             f"Pipeline stages are {pipeline_stage_names_str}. "
                                             "(default %(default)s)"))
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")

    parser.add_argument('--version', action='version', version=f"{__version__}")

    return parser


def load_config(file_path: str) -> typing.MutableMapping[str, typing.Any]:
    with open(file_path, "r") as fd:
        config = toml.load(fd)
    return config


def save_report(
    report: dict,
    file_paths: typing.Union[str, typing.List[str]],
    output_dir: str
) -> None:
    """
    Utility for saving report files.
    Right now this supports TOML and JSON formats.


    Example:
        >>> save_report({"key": value}, ["report.toml", "report.json"])
        >>> save_report({"key": value}, "report.toml")

    Args:
        report: dictionary report to save to disk
        file_paths: Can either be a single string or a list of strings.
    """

    if isinstance(file_paths, str):
        file_paths = [file_paths]

    module_logger.debug(f"main: file_paths: {file_paths}")
    for report_file_path in file_paths:
        if not os.path.isabs(report_file_path):
            if output_dir is not None:
                report_file_path = os.path.join(output_dir, report_file_path)

        with open(report_file_path, "w") as fd:
            if report_file_path.endswith(".toml"):
                toml.dump(report, fd)
            elif report_file_path.endswith(".json"):
                json.dump(report, fd)


def setup_logging(verbose: bool, log_file_path: str = None, output_dir: str = None):
    log_level = logging.ERROR
    if verbose:
        log_level = logging.DEBUG
    if log_file_path is None:
        logging.basicConfig(level=log_level)
    else:
        if not os.path.isabs(log_file_path):
            if output_dir is not None:
                log_file_path = os.path.join(output_dir, log_file_path)
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s', "%Y-%m-%d %H:%M:%S")
        fh.setFormatter(formatter)
        sh = logging.StreamHandler()
        sh.setLevel(log_level)
        formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
        sh.setFormatter(formatter)

        # we have to specify a level for the root logger, or else nothing gets output
        logging.basicConfig(level=logging.DEBUG, handlers=[sh, fh])

    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    logging.getLogger("eyed3").setLevel(logging.ERROR)
    logging.getLogger("PIL").setLevel(logging.ERROR)


def get_config(default_config: dict, vars_parsed: dict, config_file_path: str = None) -> dict:
    """
    Get pipeline configuration. CLI configurations are prioritized over configurations from a file.

    Args:
        default_config: This is the default configuration
        vars_parsed: configuration dictionary from CLI
        config_file_path: file path to configuration TOML file.

    Returns:
        dict: Configuration dictionary for gemscape pipeline.
    """

    non_pipeline_keys = ["output_dir", "report"]

    config = default_config.copy()

    if config_file_path is not None:
        loaded_config = load_config(config_file_path)
        for func_key in default_config:
            if not hasattr(default_config[func_key], "keys"):
                continue
            func_config = loaded_config.get(func_key, {})
            func_config = {key: func_config[key] for
                           key in func_config if key in default_config[func_key]}
            config[func_key].update(func_config)

        for key in non_pipeline_keys:
            if key in loaded_config:
                config[key] = loaded_config[key]

    for key in non_pipeline_keys:
        if vars_parsed[key] is not None:
            config[key] = vars_parsed[key]

    for func_key in default_config:
        if not hasattr(default_config[func_key], "keys"):
            continue
        for key in default_config[func_key]:
            if vars_parsed[key] is not None:
                config[func_key][key] = vars_parsed[key]

    return config


def main(args):

    parser = create_parser()
    parsed = parser.parse_args(args)

    default_color_scheme_file_path = os.path.join(
        os.path.dirname(gemscapes_dir),
        "blue_dot_sessions.color.toml"
    )

    default_config = {
        "convert": {},
        "wav2png": {
            "fft_size": 32768,
            "image_width": 1000,
            "image_height": 301,
            "peak_width": 2,
            "color_scheme": "blue_dot_sessions",
            "color_scheme_file_path": default_color_scheme_file_path,
            "color_space": "snap_to",
            "color_range": 0.7,
            "mu_cut": 2.5
        },
        "post_wav2png": {
            "v_wssf": 1.0,
            "h_wssf": 1.1
        },
        "primitive": {
            "primitive_args": "-n 30 -m 8 -bg #ffffff00 -kt 0.35 -at 0.015,0.3",
            "primitive_exec": "primitive"
        },
        "post_primitive": {
            "thresh": 0.35
        },
        "output_dir": None,
        "report": "report.toml"
    }


    vars_parsed = vars(parsed)
    configs = get_config(default_config, vars_parsed, parsed.config)

    if "h_wssf" in configs["post_wav2png"]:
        configs["post_primitive"]["h_wssf"] = 1.0/configs["post_wav2png"]["h_wssf"]

    if "v_wssf" in configs["post_wav2png"]:
        configs["post_primitive"]["v_wssf"] = 1.0/configs["post_wav2png"]["v_wssf"]

    pipeline_stages = process_pipeline_stages(parsed.pipeline_stage)
    pipeline_stages = list(range(len(Pipeline.fn_names))[pipeline_stages])
    output_dir = configs["output_dir"]

    if output_dir is not None:
        init_dry_run = pipeline_stages[0] > 0
        if init_dry_run:
            output_dir = get_most_recent_dir(output_dir)
        else:
            output_dir = get_formatted_output_dir(output_dir)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

    setup_logging(parsed.verbose, parsed.log, output_dir)

    gemscape_gen = Pipeline(
        lambda file_path, **kwargs: convert(
            file_path, output_dir=output_dir, **configs["convert"], **kwargs),
        lambda file_path, **kwargs: wav2png(
            file_path, normalize=True, **configs["wav2png"], **kwargs),
        functools.partial(post_wav2png, **configs["post_wav2png"]),
        lambda file_path, **kwargs: primitive(
            file_path, **configs["primitive"], **kwargs
        ),
        functools.partial(post_primitive, **configs["post_primitive"])
    )

    def progress(iterable):
        if len(iterable) > 1 and not parsed.verbose:
            return tqdm.tqdm(iterable)
        else:
            return iterable

    total_report = {
        "pipeline config": configs,
        "targets": []
    }

    for file_path in progress(parsed.file_paths):
        for i, res in enumerate(gemscape_gen(file_path, stages=pipeline_stages)):
            pass
        res = res[-1]
        res["input_file_path"] = os.path.abspath(file_path)
        res["input_file_name"] = os.path.basename(file_path)
        total_report["targets"].append(res)

    save_report(total_report, configs["report"], output_dir)

if __name__ == "__main__":
    main(sys.argv[1:])
