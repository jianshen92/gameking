from games.lobby import Game

from enum import Enum

import random
import time


class Roles(Enum):
    SPY = 1
    PLAYER = 2


class Spyfall(Game):
    game_name = "Spyfall"
    location_list = [
        "Beach",
        "Broadway Theater",
        "Casino",
        "Circus Tent",
        "Bank",
        "Day Spa",
        "Hotel",
        "Restaurant",
        "Supermarket",
        "Service Station",
        "Hospital",
        "Embassy",
        "Military Base",
        "Police Station",
        "School",
        "University",
        "Airplane",
        "Ocean Liner",
        "Passenger Train",
        "Submarine",
        "Cathedral",
        "Corporate Party",
        "Movie Studio",
        "Crusader Army",
        "Pirate Ship",
        "Polar Station",
        "Space Station",
    ]

    def __init__(self, number_of_spies: int = 1, game_time_minutes: int = 8):
        super().__init__()
        self.number_of_spies = number_of_spies
        self.game_time_minutes = game_time_minutes
        self.player_roles = None
        self.game_start_time = None
        self.location = None

    def start_game(self):
        print(f"Starting Spyfall Game {self.lobby.game_id}")
        self._assign_role()
        self._set_location()
        self._set_start_time()
        self._set_end_time()

    def game_info(self):
        return {
            "number_of_spies": self.number_of_spies,
            "game_time_minutes": self.game_time_minutes,
            "player_roles": self.player_roles,
            "game_start_time": self.game_start_time,
            "game_end_time": self.game_end_time,
            "location": self.location,
            "location_list": self.location_list,
        }

    def _assign_role(self):
        players = self.lobby.players
        spies = random.sample(players, self.number_of_spies)
        players_roles = {}
        for player in players:
            players_roles[player] = {
                "role": (Roles.SPY.name if player in spies else Roles.PLAYER.name)
            }

        self.player_roles = players_roles

    def _set_start_time(self):
        self.game_start_time = time.time()
        print(f"Start time : {self.game_start_time}")

    def _set_end_time(self):
        self.game_end_time = self.game_start_time + self.game_time_minutes * 60

    def _set_location(self):
        self.location = random.sample(self.location_list, 1)[0]
        print(f"Location : {self.location}")
