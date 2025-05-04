# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia

__all__ = [
    "version",
    "version_string",
    "EMPTY_TEXTURES",
    "EMPTY_CONTROL",
    "MP_VISOR",
    "ANY_REGION",
    "TRANSPARENT_INTENTIONS",
    "INCORRECT_RTGOS",
]

version = (1, 1, 5)
version_string = ".".join(str(v) for v in version)
EMPTY_TEXTURES = [10098, 580203186, 92914]
EMPTY_CONTROL: int = 11617
MP_VISOR: int = 1420626520
ANY_REGION: str = "192819851"
TRANSPARENT_INTENTIONS: list[int] = [-783606968, -1010104944]
INCORRECT_RTGOS: list[int] = [
    1143017283,
    -453665744,
    -1400519942,
    947954639,
    1208611533,
    -223934709,
    -280090707,
    -416461967,
    -2048057069,
    -453665744,
    1100028612,
]
