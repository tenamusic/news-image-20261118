#!/usr/bin/env python3
"""Entry point for the news-image-20261118 make.fun entry.

The repository ships a finished 1024x1024 image, entry.png, that sums
up the world news of Wednesday 18 November 2026 in six panels. Judging
runs this program with no network access and afterwards reads exactly
one file, so the program's whole job is to place those bytes at
/output/entry.png, unchanged, and to confirm they arrived intact.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

OUTPUT_PATH = Path("/output/entry.png")
SOURCE_NAME = "entry.png"


def source_image() -> Path:
    """Return the bundled image that sits next to this script."""
    candidate = Path(__file__).resolve().parent / SOURCE_NAME
    if not candidate.is_file():
        raise FileNotFoundError(f"bundled image missing: {candidate}")
    return candidate


def publish() -> int:
    payload = source_image().read_bytes()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Write to a sibling temp file first, then rename, so the judged
    # path only ever holds a complete image, never a partial write.
    staging = OUTPUT_PATH.with_name(OUTPUT_PATH.name + ".part")
    staging.write_bytes(payload)
    staging.replace(OUTPUT_PATH)
    written = OUTPUT_PATH.read_bytes()
    if written != payload:
        print("error: output differs from the bundled image", file=sys.stderr)
        return 1
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {OUTPUT_PATH} ({len(written)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(publish())
