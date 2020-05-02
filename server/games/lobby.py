from enum import Enum

from datetime import datetime
import time
import random
import math
import string
import os


class GameName(Enum):
    CODEWORDS = 1
    SPYFALL = 2


class Lobby(object):
    def __init__(self):
        self.game_id = self.generate_room_id()
        self.players = set()
        self.date_created = datetime.now()
        self.date_modified = self.date_created

    def add_player(self, name):
        """Add playername to player array"""
        self.players.add(name)

    def remove_player(self, name):
        """Remove playername to player array"""
        self.players.remove(name)

    def generate_room_id(self):
        """Generate a random room ID"""
        id_length = 6
        return "".join(
            random.SystemRandom().choice(string.ascii_uppercase)
            for _ in range(id_length)
        )

    def lobby_info(self):
        return {
            "game_id": self.game_id,
            "players": list(self.players),
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
        }


class Game(object):
    def __init__(self):
        self.lobby = Lobby()
