from typing import Hashable, Protocol, Any


class HashableSortable(Hashable, Protocol):
    def __lt__(self, __other: Any) -> bool: ...
