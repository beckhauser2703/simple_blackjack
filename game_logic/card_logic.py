from typing import TypeVar, Generic, List
from enum import Enum, auto
T = TypeVar('T')


class Suit(Enum):
    DIAMONDS = auto(),
    HEARTS = auto(),
    CLUBS = auto(),
    SPADES = auto()


class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    VALET = 11
    QUEEN = 12
    KING = 13


class Card():
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
    def __repr__(self) -> str:
        return f'({self.rank.name}, {self.suit.name})'
