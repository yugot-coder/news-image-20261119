#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261119.

The entry image is poster.png: a one-page newspaper front page,
"THE WORLD TODAY", summing up the world news of Thursday 19 November
2026. It was drawn at build time by build_poster.py; the grading
sandbox has no Pillow and no network, so this program only has to put
the finished image where the grader reads it.

It reads poster.png, which ships in this repository beside this file,
checks that it is a PNG inside the gate's size limits, and writes it
byte for byte to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png
when the variable is unset, the grader's container layout). Two runs
therefore always write the same bytes.
"""

import os
import struct
from pathlib import Path

POSTER_NAME = "poster.png"
ENTRY_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # the gate's 1 MiB cap
MAX_SIDE = 1024  # the gate's pixel cap


def poster_file() -> Path:
    """The poster, stored in this repository next to this program."""
    return Path(__file__).resolve().parent / POSTER_NAME


def output_folder() -> Path:
    """Where the grader reads the entry image from."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def check_poster(blob: bytes) -> None:
    """Refuse to hand the grader an image its gate would reject.

    Only the PNG magic and the IHDR width/height are read; the image
    bytes themselves pass through untouched.
    """
    if not blob.startswith(PNG_MAGIC):
        raise ValueError("poster.png is not a PNG file")
    width, height = struct.unpack(">II", blob[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(
            f"poster is {width}x{height}, over the {MAX_SIDE}px cap"
        )
    if len(blob) > MAX_BYTES:
        raise ValueError(f"poster is {len(blob)} bytes, over the cap")


def main() -> None:
    blob = poster_file().read_bytes()
    check_poster(blob)
    folder = output_folder()
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ENTRY_NAME).write_bytes(blob)


if __name__ == "__main__":
    main()
