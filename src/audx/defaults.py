from enum import Enum
from typing import Annotated

import typer


class AudioFormat(str, Enum):
    flac = "flac"
    mp3 = "mp3"
    wav = "wav"


VALID_FILE_FORMATS: set[str] = {f.value for f in AudioFormat}
VALID_FILE_FORMATS_STR = ", ".join(sorted(VALID_FILE_FORMATS))


PathArg = Annotated[str, typer.Argument(help="Path to the file to process.")]
ConvertFromArg = Annotated[
    AudioFormat, typer.Option(help="Audio file format to convert from.")
]
ConvertToArg = Annotated[
    AudioFormat, typer.Option(help="Audio file format to convert to.")
]
DeleteOriginalArg = Annotated[
    bool, typer.Option(help="Delete original files after successful conversion.")
]
RecursiveArg = Annotated[
    bool, typer.Option(help="Recursively search for files in subdirectories.")
]
BitrateArg = Annotated[str, typer.Option(help="Audio bitrate for CBR encodes.")]
