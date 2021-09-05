from enum import Enum
from pydantic import BaseModel
from typing import Union, List, Dict
import random

from functional import seq


class CardSuit(int, Enum):
    SPADE = 4
    HEARTS = 3
    CLOVER = 2
    DIAMOND = 1


class CardRank(int, Enum):
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    TWO = 15


class SpecialSuit(int, Enum):
    JOKER = 999


class SpecialRank(int, Enum):
    RED_JOKER = 999
    BLACK_JOKER = 998


def suit_decider(suit_value: int) -> Union[CardSuit, SpecialSuit]:
    if suit_value < 100:
        return CardSuit(suit_value)
    else:
        return SpecialSuit(suit_value)


def rank_decider(rank_value: int) -> Union[CardRank, SpecialRank]:
    if rank_value < 100:
        return CardRank(rank_value)
    else:
        return SpecialRank(rank_value)


class Card(BaseModel):
    suit: Union[CardSuit, SpecialSuit]
    rank: Union[CardRank, SpecialRank]

    @property
    def value(self):
        return (self.rank.value << 2) + self.suit.value

    def __hash__(self):
        return hash((self.suit, self.rank))

    class Config:
        allow_mutation = False


class Hand(BaseModel):
    cards: List[Card]

    def __init__(self, **data):
        super().__init__(**data)
        self._sort()

    def _sort(self):
        self.cards = sorted(self.cards, key=lambda x: x.value)

    def add_cards(self, cards: List[Card]):
        self.cards.extend(cards)
        self._sort()

    def play(self, cards_to_play: List[Card]):
        remaining_cards = set(self.cards) - set(cards_to_play)
        self.cards = list(remaining_cards)
        self._sort()

    @property
    def hand_count(self):
        return len(self.cards)

    @classmethod
    def hand_parser(cls, raw_hand: List[str]):
        hand = (
            seq(raw_hand)
            .map(lambda x: x.split("-"))
            .map(
                lambda x: Card(
                    suit=suit_decider(int(x[0])), rank=rank_decider(int(x[1]))
                )
            )
            .list()
        )

        return cls(cards=hand)


class DouDiZhuDeck:
    def __init__(self):
        self.cards: List[Card] = self.generate_ddz_deck()

    @staticmethod
    def generate_ddz_deck(shuffle: bool = True) -> List[Card]:
        cards = []
        normal_cards = [
            Card(rank=rank, suit=suit) for rank in CardRank for suit in CardSuit
        ]
        special_cards = [
            Card(rank=SpecialRank.RED_JOKER, suit=SpecialSuit.JOKER),
            Card(rank=SpecialRank.BLACK_JOKER, suit=SpecialSuit.JOKER),
        ]
        cards.extend(normal_cards)
        cards.extend(special_cards)

        if shuffle:
            random.shuffle(cards)
        return cards

    def shuffle(self) -> None:
        random.shuffle(self.cards)


class DouDiZhuPlayer(BaseModel):
    name: str
    hand: Hand = None
    last_played: Hand = Hand(cards=[])

    def assign_hand(self, cards: List[Card]):
        self.hand = Hand(cards=cards)
        self.last_played = Hand(cards=[])

    def add_cards(self, cards: List[Card]):
        self.hand.add_cards(cards)

    def play(self, played_hand: Hand):
        # Set Last played Hand
        self.last_played = played_hand

        # Play cards
        self.hand.play(cards_to_play=played_hand.cards)


class DouDiZhuPhase(str, Enum):
    BIDDING = "bid"
    GAME = "game"


class DouDiZhuBidValue(int, Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3


class DouDiZhuBidState(BaseModel):
    bid_value: DouDiZhuBidValue
    remaining_bid: List[DouDiZhuBidValue]
    bid_by: DouDiZhuPlayer = None


class DouDiZhuGameState(BaseModel):
    game_player: List[DouDiZhuPlayer]
    current_turn: DouDiZhuPlayer
    river: List[Card]
    phase: DouDiZhuPhase
    bid_state: DouDiZhuBidState
    dizhu: DouDiZhuPlayer = None


# def doudizhu_deck():
#     for
# class DouDiZhu:
#     def __init__():
#         pass

#     def generate_deck(self):
