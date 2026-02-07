from typing import Annotated

import typer

VALID_FILE_FORMATS: set[str] = {"flac", "mp3", "wav"}
VALID_FILE_FORMATS_STR = ", ".join(sorted(VALID_FILE_FORMATS))


PathArg = Annotated[str, typer.Argument(help="Path to the file to process.")]
ConvertFromArg = Annotated[str, typer.Option(help="Audio file format to convert from.")]
ConvertToArg = Annotated[str, typer.Option(help="Audio file format to convert to.")]
DeleteOriginalArg = Annotated[
    bool, typer.Option(help="Delete original files after successful conversion.")
]
RecursiveArg = Annotated[
    bool, typer.Option(help="Recursively search for files in subdirectories.")
]
BitrateArg = Annotated[str, typer.Option(help="Audio bitrate for CBR encodes.")]
