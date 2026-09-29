from typing import Any


class IdempotencyCache:

    def __init__(self):
        self._storage = {}

    def get(self, key: str) -> Any:
        return self._storage.get(key)
    
    def set(self, key: str, value: Any) -> None:
        self._storage[key] = value
