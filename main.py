"""Entry point for the news-image-20261118 bounty.

Copies the bundled entry.png (a 1024x1024 infographic summing up the world
news of Wednesday 18 November 2026) into the output directory, after checking
that the bundled file is a whole PNG or JPEG within the 1 MiB cap.
"""

import os
import shutil
import sys

MAX_BYTES = 1024 * 1024  # the bounty caps the entry image at 1 MiB
# The image is a JPEG in a file named entry.png: the gate tells PNG from
# JPEG by the first bytes, and the rules keep the name entry.png either way.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def looks_like_image(path):
    """True when the file at path starts with a PNG or JPEG signature."""
    with open(path, "rb") as fh:
        head = fh.read(8)
    return head.startswith(PNG_MAGIC) or head.startswith(JPEG_MAGIC)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png is missing beside main.py", file=sys.stderr)
        return 1
    if os.path.getsize(src) > MAX_BYTES:
        print("entry.png exceeds the 1 MiB cap", file=sys.stderr)
        return 1
    if not looks_like_image(src):
        print("entry.png is not a PNG or JPEG image", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Verify the copy landed whole: a truncated write must fail loudly
    # rather than hand the judge a broken image.
    with open(src, "rb") as fh:
        want = fh.read()
    with open(dst, "rb") as fh:
        got = fh.read()
    if got != want:
        print("copied entry.png does not match the bundled file", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(got)} bytes, verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
