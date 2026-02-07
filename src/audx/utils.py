import os
from pathlib import Path

import click
import typer


def die(msg: str, param_hint: str | None = None) -> None:
    if param_hint:
        raise typer.BadParameter(msg, param_hint=param_hint)

    raise click.ClickException(msg)


def discover(root_dir: Path, convert_from: str, recursive: bool = True) -> list[Path]:
    results: list[Path] = []
    if not recursive:
        for file in root_dir.iterdir():
            if file.is_file() and file.name.lower().endswith(f".{convert_from}"):
                results.append(file)
    else:
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith(f".{convert_from}"):
                    results.append(Path(root) / file)

    return results
