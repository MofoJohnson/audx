import shutil
import subprocess
from pathlib import Path

import typer
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
)

from audx.audio import convert_one, has_decodable_audio
from audx.defaults import (
    VALID_FILE_FORMATS,
    VALID_FILE_FORMATS_STR,
    BitrateArg,
    ConvertFromArg,
    ConvertToArg,
    DeleteOriginalArg,
    PathArg,
    RecursiveArg,
)
from audx.utils import die, discover

app = typer.Typer()


@app.command()
def main(
    path: PathArg,
    convert_from: ConvertFromArg = "flac",
    convert_to: ConvertToArg = "mp3",
    delete_original: DeleteOriginalArg = False,
    recursive: RecursiveArg = True,
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

    files = discover(root_dir, convert_from, recursive=recursive)
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


def cli() -> None:
    app()


if __name__ == "__main__":
    cli()
