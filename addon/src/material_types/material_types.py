from abc import ABC, abstractmethod


class MaterialType(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def _create_nodes(self) -> None:
        pass
