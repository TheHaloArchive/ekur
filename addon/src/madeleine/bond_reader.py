# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader
import struct
import logging
from typing import cast

from .madeleine import BondValue
from .uleb import uleb128_decode, sleb128_decode
from .bond_types import BondType


def type_and_id(data: BufferedReader) -> tuple[int, BondType]:
    id_and_type = data.read(1)[0]
    bond_type = BondType(id_and_type & 0x1F)
    id = id_and_type >> 5
    if id == 6:
        id = data.read(1)[0]
    elif id == 7:
        id = int.from_bytes(data.read(2), byteorder="little")
    return id, bond_type


def get_type_count(data: BufferedReader) -> tuple[BondType, int]:
    len_and_type = data.read(1)[0]
    bond_type = BondType(len_and_type & 0x1F)
    length = len_and_type >> 5
    if length == 0:
        length = uleb128_decode(data)
    else:
        length -= 1
    return bond_type, length


def read_blobs(data: BufferedReader, count: int) -> None:
    _ = data.read(count)


def read_list(data: BufferedReader, type: BondType) -> list[BondValue]:
    type, count = get_type_count(data)
    values: list[BondValue] = []
    if type == BondType.List or type == BondType.Int8 or type == BondType.Uint8:
        read_blobs(data, count)
    else:
        for _ in range(count):
            val = read_value(0, type, data)
            values.append(val)
    return values


def read_map(data: BufferedReader) -> dict[BondValue, BondValue]:
    key_type = BondType(data.read(1)[0] & 0x1F)
    value_type = BondType(data.read(1)[0] & 0x1F)
    count = uleb128_decode(data)
    values: dict[BondValue, BondValue] = {}
    for _ in range(count):
        key = read_value(0, key_type, data)
        value = read_value(0, value_type, data)
        values[key] = value
    return values


def read_wstring(data: BufferedReader) -> str:
    length = uleb128_decode(data)
    try:
        dat = data.read(length * 2).decode("utf-16")
        return dat
    except UnicodeDecodeError:
        logging.error("UnicodeDecodeError while reading wstring!")
        return ""


def read_string(data: BufferedReader) -> str:
    length = uleb128_decode(data)
    try:
        dat = data.read(length).decode("utf-8")
        return dat
    except UnicodeDecodeError:
        logging.error("UnicodeDecodeError while reading string!")
        return ""


def read_value(id: int, type: BondType, data: BufferedReader) -> BondValue:
    val = BondValue(id, type, None)
    match type:
        case BondType.Struct:
            val.value = read_struct(data)
        case BondType.Int32 | BondType.Int64 | BondType.Int16:
            val.value = sleb128_decode(data)
        case BondType.Uint16 | BondType.Uint32 | BondType.Uint64:
            val.value = uleb128_decode(data)
        case BondType.Uint8:
            val.value = data.read(1)[0]
        case BondType.Int8:
            val.value = cast(int, struct.unpack("b", data.read(1))[0])
        case BondType.Bool:
            val.value = bool(data.read(1)[0])
        case BondType.Float:
            val.value = cast(float, struct.unpack("f", data.read(4))[0])
        case BondType.Double:
            val.value = cast(float, struct.unpack("d", data.read(8))[0])
        case BondType.Set | BondType.List:
            val.value = read_list(data, type)
        case BondType.Map:
            val.value = read_map(data)
        case BondType.Wstring:
            val.value = read_wstring(data)
        case BondType.String:
            val.value = read_string(data)
        case BondType.Stop | BondType.StopBase | BondType.Unavailable:
            ...
    return val


def read_field(data: BufferedReader) -> BondValue:
    id, type = type_and_id(data)
    val = read_value(id, type, data)
    return val


def read_struct(data: BufferedReader) -> list[BondValue]:
    _length = uleb128_decode(data)
    values: list[BondValue] = []
    while True:
        val = read_field(data)
        match val.type:
            case BondType.Stop:
                break
            case BondType.StopBase:
                ...
            case _:
                values.append(val)
    return values


def get_base_struct(data: BufferedReader) -> BondValue:
    return BondValue(0, BondType.Struct, read_struct(data))
