from functional.transformations import name
from games.lobby import Game
from games.card.cards import DouDiZhuDeck
from games.card.cards import Hand
from games.card.cards import Card
from games.card.cards import DouDiZhuPlayer
from games.card.cards import DouDiZhuGameState
from games.card.cards import DouDiZhuPhase
from games.card.cards import DouDiZhuBidValue
from games.card.cards import DouDiZhuBidState
from typing import List
from typing import Dict

from functional import seq


class DouDiZhu(Game):
    game_name = "Dou Di Zhu"
    min_player = 3
    max_player = 3

    def __init__(self):
        super().__init__(min_player=self.min_player, max_player=self.max_player)
        self.game_player: List[DouDiZhuPlayer] = None
        self._set_starting_game_state()

    def _set_starting_game_state(self):
        self.deck: DouDiZhuDeck = DouDiZhuDeck()
        self.current_turn_id: int = 0
        self.phase = DouDiZhuPhase.BIDDING
        self.bid_value = DouDiZhuBidValue.ZERO
        self.last_bid_by: DouDiZhuPlayer = None
        self.bid_pass_counter: int = 0
        self.last_played_hand: Hand = None
        self.pass_counter: int = 0
        self.dizhu: DouDiZhuPlayer = DouDiZhuPlayer(name="")
        self.river: List[Card] = []

    def restart_game(self):
        self._set_starting_game_state()
        self._distribute_cards()

    def game_info(self):
        return {"game_name": self.game_name, "game_state": self.get_game_state()}

    def _generate_player(self) -> None:
        self.game_player = [
            DouDiZhuPlayer(name=player) for player in self.lobby.players
        ]

    def _distribute_cards(self) -> List[Hand]:
        current_ptr = 0
        cards_per_player = 17
        for game_player in self.game_player:
            player_cards = self.deck.cards[current_ptr : current_ptr + cards_per_player]
            game_player.assign_hand(player_cards)
            current_ptr += cards_per_player

        self.river = self.deck.cards[-3:]

    def start_game(self):
        print(f"Starting DouDiZhu Game {self.lobby.game_id}")
        self._generate_player()
        self._distribute_cards()

    def get_game_state(self):
        game_state = DouDiZhuGameState(
            game_player=self.game_player,
            current_turn=self.game_player[self.current_turn_id],
            river=self.river,
            phase=self.phase,
            bid_state=self._get_bid_state(),
            dizhu=self.dizhu,
        )

        return game_state.dict()

    def _get_bid_state(self):
        bid_value = self.bid_value
        remaining_bid = (
            seq([value for value in DouDiZhuBidValue])
            .filter(lambda x: x > bid_value)
            .list()
        )
        return DouDiZhuBidState(
            bid_value=bid_value, remaining_bid=remaining_bid, bid_by=self.last_bid_by
        )

    def bid(self, player_name: str, bid: int):
        """
        Bid for Dizhu
        """
        self.last_bid_by = self._get_player(player_name=player_name)
        self.bid_value = DouDiZhuBidValue(bid)

        if self.bid_value == DouDiZhuBidValue.THREE:
            self._assign_dizhu()
            # Dizhu will start
            return

        # Next Player
        self._increase_turn_counter()

        # Reset Pass Counter
        self.bid_pass_counter = 0

    def bid_pass(self, player_name: str):
        """
        Passing a Bid
        """
        # Next Player
        self._increase_turn_counter()
        self.bid_pass_counter += 1

        if self.bid_pass_counter == 2 and self.bid_value != DouDiZhuBidValue.ZERO:
            self._assign_dizhu()

    def _assign_dizhu(self):
        """
        Assign last bid player as dizhu
        """
        self.dizhu = self.last_bid_by
        print(f"{self.dizhu.name} assigned as Dizhu")

        # Dizhu gets extra cards
        self.dizhu.add_cards(cards=self.river)

        # Change Game Phase
        self._change_to_game_phase()

    def _change_to_game_phase(self):
        self.phase = DouDiZhuPhase.GAME

    def play_cards(self, player_name: str, raw_cards: List[str]) -> bool:
        """
        Play Cards
        """
        played_hand: Hand = Hand.hand_parser(raw_hand=raw_cards)
        player: DouDiZhuPlayer = self._get_player(player_name=player_name)

        if self._validate_played_hand(played_hand=played_hand):
            # Play Hand
            player.play(played_hand=played_hand)

            # Next Player
            self._increase_turn_counter()

            # Reset Pass Counter
            self.pass_counter = 0

            # Record Last Played hand for validation
            self.last_played_hand = played_hand
            return True

        return False

    def player_pass(self, player_name: str):
        """
        Player Pass Their Turn
        """
        player: DouDiZhuPlayer = self._get_player(player_name=player_name)
        if self._validate_pass():
            player.play(played_hand=Hand(cards=[]))
            self._increase_turn_counter()
            self.pass_counter += 1

    def _get_player(self, player_name: str) -> DouDiZhuPlayer:
        """
        Get Player by Name
        """
        # TODO, use dictionary to access player.
        for player in self.game_player:
            if player.name == player_name:
                return player

        raise Exception(f"Player {player_name} not found in this game")

    def _validate_played_hand(self, played_hand: Hand) -> bool:
        """
        Check if current played hand is valid
        """
        # TODO, Fill in validation logic

        return True

    def _validate_pass(self) -> bool:
        """
        Check if passing is valid
        """
        if self.pass_counter >= 2:
            return False

        return True

    def _increase_turn_counter(self):
        """
        Increase turn counter and pass to next player
        """
        self.current_turn_id = (self.current_turn_id + 1) % self.max_player
