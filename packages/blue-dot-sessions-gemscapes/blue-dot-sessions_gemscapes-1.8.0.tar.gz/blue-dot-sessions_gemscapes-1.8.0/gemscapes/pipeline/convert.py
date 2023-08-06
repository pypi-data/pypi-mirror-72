import os
import logging

from ..conversion import convert_to_wav
from ..metadata import BDSMetaDataType
from .pipeline_types import PipelineFnReturnType


module_logger = logging.getLogger(__name__)


def convert(
    file_path: str,
    output_dir: str = None,
    track_metadata: BDSMetaDataType = None,
    dry_run: bool = False
) -> PipelineFnReturnType:
    """
    Convert mp3 files to wav.

    Args:
        file_path: Input .mp3 file path
        dry_run: Run without modifying anything

    Returns:
        output file path

    """
    if output_dir is None:
        output_dir = os.path.dirname(file_path)

    file_name = os.path.basename(file_path)
    output_file_path = os.path.splitext(os.path.join(output_dir, file_name))[0] + ".wav"

    if not dry_run:
        if file_path.endswith(".mp3"):
            output_file_path = convert_to_wav(file_path, output_file_path=output_file_path)
        elif file_path.endswith(".wav"):
            output_file_path = file_path

    report = {
        "file_path": file_path,
        "output_file_path": output_file_path,
        "dry_run": dry_run
    }

    return output_file_path, report
