#!/usr/bin/env python3
"""The World Today -- Thursday 19 November 2026.

Publishes the edition poster for the make.fun news-image bounty.

The poster artwork lives next to this file as ``poster.png``.  Running
this module copies that file, byte for byte, into the entry directory
so the grader receives exactly the image the edition was built with.
Nothing is re-encoded, resized, or otherwise touched: the copy is
verified with a SHA-256 digest before the program reports success.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

POSTER_NAME = "poster.png"
ENTRY_NAME = "entry.png"
DEFAULT_OUTPUT_ROOT = "/output"


def _poster_path() -> Path:
    """Return the poster file sitting beside this module."""
    return Path(__file__).resolve().parent / POSTER_NAME


def _output_root() -> Path:
    """Return the entry directory from the environment, or the default."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if configured:
        return Path(configured)
    return Path(DEFAULT_OUTPUT_ROOT)


def _digest(path: Path) -> str:
    """Compute the SHA-256 hex digest of a file, streaming it in chunks."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def _fail(message: str) -> "SystemExit":
    """Print an error to stderr and request a non-zero exit."""
    print(f"error: {message}", file=sys.stderr)
    return SystemExit(1)


def publish() -> int:
    """Copy the poster to the entry path and verify the copy."""
    source = _poster_path()
    if not source.is_file():
        raise SystemExit(_fail(f"poster not found: expected {POSTER_NAME} at {source}"))

    destination_dir = _output_root()
    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise SystemExit(_fail(f"cannot create output directory {destination_dir}: {exc}"))

    destination = destination_dir / ENTRY_NAME
    try:
        shutil.copyfile(source, destination)
    except OSError as exc:
        raise SystemExit(_fail(f"cannot write entry file {destination}: {exc}"))

    source_size = source.stat().st_size
    copied_size = destination.stat().st_size
    if copied_size != source_size:
        raise SystemExit(
            _fail(
                f"copy size mismatch: poster is {source_size} bytes "
                f"but entry is {copied_size} bytes"
            )
        )

    if _digest(source) != _digest(destination):
        raise SystemExit(_fail("copy hash mismatch: entry differs from poster"))

    print(f"Wrote {destination} ({copied_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(publish())
