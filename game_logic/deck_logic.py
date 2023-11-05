from typing import TypeVar, Generic, List
from abc import ABC, abstractmethod
import random
T = TypeVar('T')


class IDeck(ABC, Generic[T]):
    @abstractmethod
    def __init__(self, cards: List[T]): pass
    @abstractmethod
    def shuffle(self) -> None: pass
    @abstractmethod
    def draw(self, amount: int) -> List[T]: pass
    @abstractmethod 
    def insert(self, cards_to_insert: List[T]) -> None: pass


class GenericDeck(IDeck, Generic[T]):
    def __init__(self, cards: List[T]) -> None:
        self.cards = cards

    def __repr__(self) -> str:
        return str(self.cards)

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def remaining_items(self) -> int:
        return len(self.cards)

    def flip_items(self) -> None:
        self.cards = self.cards[::-1]

    def draw(self, amount: int = 1) -> List[T]:
        if self.remaining_items() < amount:
            amount = self.remaining_items()
        items_to_return = self.cards[:amount]
        self.cards = self.cards[amount:]
        return items_to_return
    
    def insert(self, cards_to_insert: List[T]) -> None:
        self.items = self.items + cards_to_insert
