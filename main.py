"""news-23 b58 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
DST = os.path.join(DST_DIR, "entry.png")


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    if not DST_DIR or not os.path.isabs(DST_DIR):
        fail("MAKEFUN_OUTPUT_DIR must be an absolute path")
    src_abs = os.path.abspath(SRC)
    dst_abs = os.path.abspath(DST)
    if dst_abs == src_abs or dst_abs.startswith(os.path.dirname(src_abs) + os.sep):
        fail("refusing to write inside the source repo (MAKEFUN_OUTPUT_DIR must be outside it)")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > 1024 * 1024:
        fail("entry.png exceeds 1 MiB")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("not a PNG file")
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (1024, 1024):
        fail("entry.png is not 1024x1024")
    if data[12:16] != b"IHDR":
        fail("missing IHDR chunk")
    if data[-12:] != struct.pack(">I", 0) + b"IEND" + struct.pack(">I", 0xAE426082):
        fail("missing well-formed IEND trailer")
    os.makedirs(DST_DIR, exist_ok=True)
    with open(DST, "wb") as f:
        f.write(data)
    with open(DST, "rb") as f:
        out = f.read()
    if out != data:
        fail("output differs from source")
    print("source", SRC, len(data), "bytes,", w, "x", h)
    print("wrote", DST, len(data), "bytes, sha256",
          hashlib.sha256(data).hexdigest(), "1024x1024")


if __name__ == "__main__":
    main()
