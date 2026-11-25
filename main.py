#!/usr/bin/env python3
"""Entry point for news-image-20261124 (stdlib only).

The front page is pre-rendered by render.py (PIL, local only) and vendored
as entry.png. This program only copies that file to $MAKEFUN_OUTPUT_DIR
and verifies size, format and dimensions. No network, no third-party
imports, fully deterministic.
"""
import hashlib
import os
import shutil
import struct
import sys

EXPECTED_MD5 = "ee599eb965815110c14257a0892f55ad"


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is not set")
    if not os.path.isfile(src):
        return fail("entry.png missing from repo")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > 1048576:
        return fail("entry.png exceeds 1 MiB (%d bytes)" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("entry.png is not a PNG")
    if not data.endswith(b"IEND\xaeB`\x82"):
        return fail("entry.png is truncated (no IEND chunk)")
    if len(data) < 1000:
        return fail("entry.png suspiciously small (%d bytes)" % len(data))
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        return fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    md5 = hashlib.md5(data).hexdigest()
    if EXPECTED_MD5 != "PLACEHOLDER" and md5 != EXPECTED_MD5:
        return fail("entry.png md5 mismatch: got %s" % md5)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        out = f.read()
    if hashlib.md5(out).hexdigest() != md5:
        return fail("copied output md5 mismatch")
    print("ok: entry.png %d bytes md5=%s" % (len(data), md5))
    return 0


if __name__ == "__main__":
    sys.exit(main())
