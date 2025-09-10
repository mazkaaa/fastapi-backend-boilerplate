from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ItemEntity:
    id: int
    name: str
    description: Optional[str] = None


@dataclass
class ItemStore:
    _items: Dict[int, ItemEntity] = field(default_factory=dict)
    _next_id: int = 1

    def list(self) -> List[ItemEntity]:
        return list(self._items.values())

    def get(self, item_id: int) -> Optional[ItemEntity]:
        return self._items.get(item_id)

    def create(self, name: str, description: Optional[str] = None) -> ItemEntity:
        item = ItemEntity(id=self._next_id, name=name, description=description)
        self._items[item.id] = item
        self._next_id += 1
        return item

    def update(
        self, item_id: int, *, name: Optional[str] = None, description: Optional[str] = None
    ) -> Optional[ItemEntity]:
        item = self._items.get(item_id)
        if not item:
            return None
        if name is not None:
            item.name = name
        if description is not None:
            item.description = description
        return item

    def delete(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None


# Global in-memory store instance for simplicity
store = ItemStore()
