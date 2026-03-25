# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2026 The Halo Archive
__all__ = ["IncorrectStrideValue", "NodeInterfaceDoesNotExist"]


class IncorrectStrideValue(Exception):
    """
    Stride value is not a multiple of 2!
    """


class NodeInterfaceDoesNotExist(Exception):
    """
    The node interface does not exist!
    """
