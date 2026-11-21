#!/usr/bin/env python3
"""The World Today: Friday 20 November 2026 — 19 stories, 19 drawn.

Entry for make.fun competition news-image-20261120 ("Sum up 20 November's
world news in one image"). The bundled image is a broadsheet front page
summarising the day's world news in 19 stories, every story with its own
drawn illustration and a source tag:

  * Lead: Trump, Xi and Putin hold their first three-way summit in
    Shenzhen and issue a four-point peace declaration.
  * Six features: Anthropic's record $81.3bn IPO (+17% on debut), the ICJ
    ruling that Myanmar committed genocide against the Rohingya, European
    allies in Berlin ready for talks with Russia on Ukraine, four ballistic
    missiles hitting Kyiv, a tanker ablaze after hitting a mine east of the
    Strait of Hormuz, and the S&P 500's fifth straight loss (Nikkei -4.68%).
  * Twelve medium stories: Houthi strikes on Saudi targets, COP31's $120bn
    draft deal, India's evacuation of 80,000 ahead of storm Dana, the
    US-Venezuela military deal, Congo's Ebola outbreak, Korea's Supreme
    Court clearing ex-PM Han Duck-soo, Taiwan's market measures,
    California's Nvidia chip probe, a migrant boat sinking off Senegal,
    drones halting Genoa airport, Fiji's drought disaster, and Voyager 1
    reaching one light-day from Earth — plus a UTC timeline strip.

This script validates the bundled image (a real PNG, at most 1024x1024,
at most 1 MiB, complete IEND chunk) and writes it byte-for-byte to the
output path. No network, fully deterministic.
"""

import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "assets", "entry.png")

MAX_W, MAX_H = 1024, 1024
MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def validate(data):
    if len(data) > MAX_BYTES:
        fail("image is %d bytes, over the 1 MiB limit" % len(data))
    if not data.startswith(PNG_MAGIC):
        fail("not a PNG file")
    if not data.endswith(b"IEND\xaeB`\x82"):
        fail("PNG is truncated (no complete IEND chunk)")
    pos = len(PNG_MAGIC)
    width = height = None
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if ctype == b"IHDR":
            width, height = struct.unpack(">II", data[pos + 8:pos + 16])
            break
        pos += 12 + length
    if width is None:
        fail("no IHDR chunk found")
    if width > MAX_W or height > MAX_H:
        fail("image is %dx%d, over the 1024x1024 limit" % (width, height))
    return width, height


def main():
    if len(sys.argv) > 1:
        out_path = sys.argv[1]
    elif os.environ.get("MAKEFUN_OUTPUT"):
        out_path = os.environ["MAKEFUN_OUTPUT"]
    elif os.path.isdir("/output"):
        out_path = "/output/entry.png"
    else:
        out_path = os.path.join(HERE, "output", "entry.png")

    with open(SOURCE, "rb") as f:
        data = f.read()
    width, height = validate(data)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)

    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (out_path, width, height, len(data),
             hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
