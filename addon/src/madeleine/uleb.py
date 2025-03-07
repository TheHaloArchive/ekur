# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader


def uleb128_decode(data: BufferedReader) -> int:
    result = 0
    shift = 0
    b = 0
    while True:
        b = data.read(1)[0]
        result |= (b & 0x7F) << shift
        if b & 0x80 == 0:
            break
        shift += 7
    return result


def sleb128_decode(data: BufferedReader) -> int:
    u = uleb128_decode(data)
    u = (u >> 1) ^ -(u & 1)
    return u
