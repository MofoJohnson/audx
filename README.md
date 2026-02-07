## Installation

Install and run with uv:

```bash
uv tool install audx
```

## Documentation

```bash
❯ audx --help

 Usage: audx [OPTIONS] PATH

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  Path to the file to process. [required]                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --convert-from                                  TEXT  Audio file format to convert from. [default: flac]                               │
│ --convert-to                                    TEXT  Audio file format to convert to. [default: mp3]                                  │
│ --delete-original       --no-delete-original          Delete original files after successful conversion. [default: no-delete-original] │
│ --recursive             --no-recursive                Recursively search for files in subdirectories. [default: recursive]             │
│ --bitrate                                       TEXT  Audio bitrate for CBR encodes. [default: 320k]                                   │
│ --install-completion                                  Install completion for the current shell.                                        │
│ --show-completion                                     Show completion for the current shell, to copy it or customize the installation. │
│ --help                                                Show this message and exit.                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Docker

You can also run with Docker:

```bash
docker pull mofojohnson/audx
docker run --rm -v $PWD:/audx mofojohnson/audx path/to/files
```
