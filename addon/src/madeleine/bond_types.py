# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from enum import IntEnum


class BondType(IntEnum):
    Stop = 0
    StopBase = 1
    Bool = 2
    Uint8 = 3
    Uint16 = 4
    Uint32 = 5
    Uint64 = 6
    Float = 7
    Double = 8
    String = 9
    Struct = 10
    List = 11
    Set = 12
    Map = 13
    Int8 = 14
    Int16 = 15
    Int32 = 16
    Int64 = 17
    Wstring = 18
    Unavailable = 127
