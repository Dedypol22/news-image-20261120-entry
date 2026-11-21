#!/usr/bin/env python3
"""The World in One Day - Friday 20 November 2026: 35 stories, 7 regions.

Entry for the make.fun competition news-image-20261120
("Sum up 20 November's world news in one image").

The bundled image is a broadsheet front page for Friday 20 November 2026.
Its three lead stories are the overnight Russian missile barrage that hit
three bridges in Kyiv, Cyclone Akvan coming ashore near Gopalpur in Odisha
after more than 300,000 people were moved to shelters, and the AI sell-off
that sank Asia's stock markets (Taiwan -6.2%, Seoul -5.2%, Tokyo -5.1%).
Ten more illustrated stories follow - the UK-EU reset deal, COP31's last
day without a deal, a Russian cruise missile landing in eastern Poland,
the Iraqi army entering Jurf al-Sakhar, Italy's general strike, Japan's
2.3% inflation, Korea's move to impeach its top judge, Kenya drilling its
first oil well, Bukele filing for a third term, and Glenn Phillips' 118
against India - plus a numbered world map and 22 one-line briefs, for 35
dated stories across 7 regions in total. A DATE CHECK box lists the big
Thursday 19 November stories that were deliberately left out.

This script does one thing: it copies the bundled PNG
(assets/entry.png, next to this file) to the output path, byte for byte,
after validating that it is a real, complete PNG of exactly 1024x1024
pixels and at most 1 MiB. Standard library only; no network access;
fully deterministic - running it twice produces identical bytes.

Usage:
    python3 main.py [OUTPUT_PATH]

The output defaults to <repo>/output/entry.png, or to $MAKEFUN_OUTPUT
when that is set. When a directory /output exists it is used instead,
so the grader's /output/entry.png convention also works.
"""

import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "assets", "entry.png")
MAX_BYTES = 1048576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IEND_SUFFIX = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def default_output():
    """Pick the output path: explicit env var, /output, else repo output."""
    env = os.environ.get("MAKEFUN_OUTPUT")
    if env:
        return env
    if os.path.isdir("/output"):
        return "/output/entry.png"
    return os.path.join(HERE, "output", "entry.png")


def validate_png(data):
    """Check the bytes are a complete PNG of exactly 1024x1024."""
    if len(data) > MAX_BYTES:
        raise ValueError("PNG is %d bytes, over the 1 MiB limit" % len(data))
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG file (bad signature)")
    if not data.endswith(IEND_SUFFIX):
        raise ValueError("PNG is truncated (no complete IEND chunk)")
    if len(data) < 33:
        raise ValueError("PNG too short to hold an IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            "PNG is %dx%d, expected %dx%d"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    # Walk the chunks and confirm their CRCs, so a corrupt file is
    # caught here instead of being handed to the grader.
    pos = 8
    seen_ihdr = False
    seen_iend = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            raise ValueError("chunk %r overruns the file" % ctype)
        stored_crc = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        actual_crc = zlib.crc32(data[pos + 4:pos + 8 + length]) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            raise ValueError("chunk %r has a bad CRC" % ctype)
        if ctype == b"IHDR":
            seen_ihdr = True
        if ctype == b"IEND":
            seen_iend = True
            break
        pos = end
    if not seen_ihdr or not seen_iend:
        raise ValueError("PNG is missing IHDR or IEND")
    return width, height


def main(argv):
    if len(argv) > 2:
        print("usage: python3 main.py [OUTPUT_PATH]", file=sys.stderr)
        return 2
    output = argv[1] if len(argv) == 2 else default_output()
    with open(SOURCE, "rb") as handle:
        data = handle.read()
    width, height = validate_png(data)
    directory = os.path.dirname(os.path.abspath(output))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output, "wb") as handle:
        handle.write(data)
    print("wrote %s (%dx%d, %d bytes)" % (output, width, height, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
