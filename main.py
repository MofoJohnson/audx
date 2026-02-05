import os
import shutil
import subprocess
from pathlib import Path
from typing import Annotated

import click
import typer
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
)

VALID_FILE_FORMATS: set[str] = {"flac", "mp3", "wav"}
VALID_FILE_FORMATS_STR = ", ".join(sorted(VALID_FILE_FORMATS))

PathArg = Annotated[str, typer.Argument(help="Path to the file to process.")]
ConvertFromArg = Annotated[str, typer.Option(help="Audio file format to convert from.")]
ConvertToArg = Annotated[str, typer.Option(help="Audio file format to convert to.")]
DeleteOriginalArg = Annotated[
    bool, typer.Option(help="Delete original files after successful conversion.")
]
BitrateArg = Annotated[str, typer.Option(help="Audio bitrate for CBR encodes.")]


def die(msg: str, param_hint: str | None = None) -> None:
    if param_hint:
        raise typer.BadParameter(msg, param_hint=param_hint)

    raise click.ClickException(msg)


def discover(root_dir: Path, convert_from: str) -> list[Path]:
    results: list[Path] = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(f".{convert_from}"):
                results.append(Path(root) / file)

    return results


# no point trying to convert invalid audio files
def has_decodable_audio(path: Path) -> bool:
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-count_packets",
            "-show_entries",
            "stream=nb_read_packets",
            "-of",
            "default=nw=1",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return False

    for line in r.stdout.splitlines():
        if line.startswith("nb_read_packets="):
            try:
                return int(line.split("=", 1)[1]) > 0
            except ValueError:
                return False

    return False


# metadata and covert art is preserved
def convert_one(src: Path, dst: Path, convert_to: str, bitrate: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "quiet",
        "-y",
        "-i",
        str(src),
        "-map",
        "0:a:0",
        # preserve tags and chapters
        "-map_metadata",
        "0",
        "-map_chapters",
        "0",
    ]

    if convert_to == "mp3":
        cmd += [
            "-map",
            "0:v?",
            "-c:a",
            "libmp3lame",
            "-b:a",
            bitrate,
            "-id3v2_version",
            "3",
            "-c:v",
            "copy",
        ]

    elif convert_to == "flac":
        cmd += [
            "-c:a",
            "flac",
        ]

    elif convert_to == "wav":
        cmd += [
            "-c:a",
            "pcm_s16le",
        ]

    else:
        die(
            f"{convert_to}.\nValid formats: {VALID_FILE_FORMATS_STR}.",
            param_hint="--convert-to",
        )

    cmd += [str(dst)]
    _ = subprocess.run(cmd, check=True)


def main(
    path: PathArg,
    convert_from: ConvertFromArg = "flac",
    convert_to: ConvertToArg = "mp3",
    delete_original: DeleteOriginalArg = False,
    bitrate: BitrateArg = "320k",
):
    root_dir = Path(path)
    if not root_dir.is_dir():
        die(f"Provided path '{path}' is not a directory.", param_hint="PATH")

    if convert_from not in VALID_FILE_FORMATS:
        die(
            f"{convert_from}.\nValid formats: {VALID_FILE_FORMATS_STR}.",
            param_hint="--convert-from",
        )

    if convert_to not in VALID_FILE_FORMATS:
        die(
            f"{convert_to}.\nValid formats: {VALID_FILE_FORMATS_STR}.",
            param_hint="--convert-to",
        )

    if convert_from == convert_to:
        die("convert-from and convert-to must be different.")

    if shutil.which("ffmpeg") is None:
        die("ffmpeg not found on PATH. Install it and try again.")

    if shutil.which("ffprobe") is None:
        die(
            "ffprobe not found on PATH. It comes with ffmpeg by default; install a full ffmpeg build."
        )

    files = discover(root_dir, convert_from)
    total = len(files)

    if total == 0:
        typer.secho(f"No .{convert_from} files found in {root_dir}", fg="yellow")
        raise typer.Exit(code=0)

    converted = 0
    failed = 0
    skipped = 0
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TextColumn("• Converted: {task.fields[converted]}"),
        TextColumn("• Failed: {task.fields[failed]}"),
        TextColumn("• Skipped: {task.fields[skipped]}"),
        TextColumn("{task.fields[current]}"),
    ) as progress:
        task = progress.add_task(
            "Converting",
            total=total,
            converted=0,
            failed=0,
            skipped=0,
            current="",
        )

        for src in files:
            progress.update(task, current=f"• {src.name}")

            dst = src.with_suffix(f".{convert_to}")

            if dst.exists():
                skipped += 1
                progress.update(task, skipped=skipped)
                progress.advance(task)
                continue

            if not has_decodable_audio(src):
                failed += 1
                progress.update(task, failed=failed)
                progress.advance(task)
                continue

            try:
                convert_one(src, dst, convert_to, bitrate)
                converted += 1
                progress.update(task, converted=converted)
                if delete_original:
                    try:
                        src.unlink()
                    except OSError:
                        failed += 1
                        progress.update(task, failed=failed)

            except subprocess.CalledProcessError:
                failed += 1
                if dst.exists():
                    dst.unlink()
                progress.update(task, failed=failed)

            progress.advance(task)

        progress.update(task, description="[bold green]Completed", current="")


if __name__ == "__main__":
    typer.run(main)
