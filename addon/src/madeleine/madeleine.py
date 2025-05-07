# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from typing import Self
from .bond_types import BondType

__all__ = ["BondValue"]


class BondValue:
    id: int = 0
    type: BondType = BondType.Unavailable
    value: int | str | float | bool | list[Self] | dict[Self, Self] | None = None

    def __init__(
        self,
        id: int,
        type: BondType,
        value: int | str | float | bool | list[Self] | dict[Self, Self] | None,
    ) -> None:
        self.id = id
        self.type = type
        self.value = value

    def get_elements(self) -> list[Self]:
        if self.type == BondType.List or self.type == BondType.Set or self.type == BondType.Struct:
            if type(self.value) is list:
                return self.value
        return []

    def get_by_id(self, id: int) -> Self | None:
        elements = self.get_elements()
        for element in elements:
            if element.id == id:
                return element
        return None

    def traverse(self, *ids: int, index: int = 0) -> Self:
        elements = self.get_elements()
        for element in elements:
            if element.id == ids[index]:
                if index == len(ids) - 1:
                    return element
                return element.traverse(index + 1, *ids)
        return self

    def get_value(self, index: int) -> Self | None:
        elements = self.get_elements()
        if len(elements) > index:
            return elements[index]
        return
