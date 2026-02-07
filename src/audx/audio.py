import subprocess
from pathlib import Path

from audx.defaults import VALID_FILE_FORMATS_STR
from audx.utils import die


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
