from .deck_logic import GenericDeck
from .card_logic import Card, Rank
from typing import List, Callable
from enum import Enum, auto


class GameResult(Enum):
    HOUSE_BUST = auto(),
    HOUSE_21 = auto(),
    HOUSE_OPPONENT_BUST = auto(),
    HOUSE_OPPONENT_21 = auto(),
    HOUSE_CLOSER_TO_21 = auto(),
    HOUSE_OPPONENT_CLOSER_TO_21 = auto(),
    DRAW = auto()


class BlackjackPlayer:
    def __init__(self, hand: List[Card]) -> None:
        self.hand: List[Card] = hand
        self.score: int = 0

    def update_score(self) -> None:
        self.score = 0
        number_of_aces = 0
        for card in self.hand:
            if card.rank == Rank.ACE:
                number_of_aces += 1
                self.score += 13
            elif card.rank in [Rank.VALET, Rank.QUEEN, Rank.KING]:
                self.score += 10
            else:
                self.score += card.rank.value
        while number_of_aces and self.score > 21:
            self.score -= 12
            number_of_aces -= 1


class BlackjackManager:
    def __init__(self, deck: GenericDeck[Card], house_strategy: Callable[[int, int, List[Card], List[Card]], bool]) -> None:
        """You may inject any house strategy:
           the first argument is the current house hand score, the second is the current opponent score,
           the third is the the house current hand
           and the fourth is the player current hand. Return True if you want to draw another card
           and False otherwise
           I believe the only real two strategies is either if you stop once you have the same score
           as the house opponent or not but I wanted to try implementing dependency injection of sorts"""
        self.deck = deck
        self.house_opponent = BlackjackPlayer([])
        self.house = BlackjackPlayer([])
        self.players = [self.house_opponent, self.house]
        self.house_strategy = house_strategy

    def deal_new_card_to_players(self, number_of_cards=1) -> None:
        for player in self.players:
            player.hand += self.deck.draw(number_of_cards)

    def update_player_scores(self) -> None:
        for player in self.players:
            player.update_score()

    def is_game_over(self) -> bool:
        return any([player.score >= 21 for player in self.players])

    def call_house_strategy(self) -> None:
        while self.house.score < 21:
            if self.house_strategy(self.house.score, self.house_opponent.score,
                                   self.house.hand, self.house_opponent.hand):
                self.house.hand += self.deck.draw()
                self.update_player_scores()
            else:
                break

    def get_game_result(self) -> GameResult:
        if self.house_opponent.score > 21:
            return GameResult.HOUSE_OPPONENT_BUST
        if self.house_opponent.score == 21:
            return GameResult.HOUSE_OPPONENT_21
        if self.house.score > 21:
            return GameResult.HOUSE_BUST
        if self.house.score == 21:
            return GameResult.HOUSE_21
        if self.house_opponent.score > self.house.score:
            return GameResult.HOUSE_OPPONENT_CLOSER_TO_21
        if self.house_opponent.score < self.house.score:
            return GameResult.HOUSE_CLOSER_TO_21
        return GameResult.DRAW

    def display_game_result(self) -> None:
        match self.get_game_result():
            case GameResult.HOUSE_OPPONENT_BUST:
                print("YOU HAVE LOST: YOU HAVE BUSTED\n")
            case GameResult.HOUSE_OPPONENT_21:
                print("YOU HAVE WON: YOU GOT 21\n")
            case GameResult.HOUSE_BUST:
                print("YOU HAVE WON: HOUSE HAS BUSTED\n")
            case GameResult.HOUSE_21:
                print("YOU HAVE LOST: HOUSE GOT 21\n")
            case GameResult.HOUSE_OPPONENT_CLOSER_TO_21:
                print("YOU HAVE WON: YOU GOT CLOSER TO 21\n")
            case GameResult.HOUSE_CLOSER_TO_21:
                print("YOU HAVE LOST: HOUSE GOT CLOSER TO 21\n")
            case GameResult.DRAW:
                print("IT'S A DRAW\n")
        print(f"Sua mão: {self.house_opponent.hand}\n"
              f"Seu Score: {self.house_opponent.score}\n"
              f"Mão da casa: {self.house.hand}\n"
              f"Score da casa: {self.house.score}")

    def play(self) -> None:
        self.deck.shuffle()
        self.house_opponent.hand += self.deck.draw()
        player_decision: str = ''
        while player_decision != 'n':
            self.deal_new_card_to_players()
            self.update_player_scores()
            if self.is_game_over():
                break
            print(f'sua mão: {self.house_opponent.hand}')
            print(f'sua soma: {self.house_opponent.score}')
            print(f'mão da casa: {self.house.hand}')
            print(f'soma da casa: {self.house.score}')
            player_decision = input(
                "Gostaria de mais uma carta?\ny para sim e n para não\n")
            if player_decision.lower() not in ['y', 'n']:
                continue
        if self.house_opponent.score >= 21:
            pass
        else:
            self.call_house_strategy()
        self.display_game_result()
