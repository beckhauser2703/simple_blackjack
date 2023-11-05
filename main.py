from game_logic import GenericDeck, Card, Rank, Suit, BlackjackManager
from typing import List

def house_strategy(current_score: int, player_score: int, house_hand: List[Card], player_hand: List[Card]) -> bool:
    if current_score < player_score:
        return True
    return False
    
def main():
    deck = GenericDeck([Card(rank, suit)\
                        for rank in Rank \
                        for suit in Suit])
    blackjack_manager = BlackjackManager(deck, house_strategy)
    blackjack_manager.play()

if __name__ == '__main__':
    main()