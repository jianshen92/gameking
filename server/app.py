"""Flask server for Codenames"""
# pylint: disable=C0103
from games.spyfall.game import Spyfall
from games.lobby import GameName

import eventlet
import logging
import json
import os
import gc
from sys import getsizeof
from flask import Flask, render_template, jsonify, request
from flask_socketio import (
    SocketIO,
    join_room,
    leave_room,
    close_room,
    send,
    emit,
)
from datetime import datetime, timedelta
from functools import reduce
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv

load_dotenv()

# attempt a relative import
# try:
#     from .codenames import game
# except (ImportError, ValueError):
#     from codenames import game

# init sentry
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(dsn=sentry_dsn, integrations=[FlaskIntegration()])

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = os.getenv("SECRET_KEY", "")

# set up logging
if not app.debug:
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

ROOMS = {}

GAMES = {}

GAME_DICT = {
    GameName.SPYFALL: Spyfall,
}


@socketio.on("create_lobby")
def on_create_lobby(data):
    """Create a generic game lobby"""
    game_name = data["gameName"]
    username = data["username"]

    # Get Game Object based on game name
    game_obj = GAME_DICT[GameName[game_name]]

    # Instantiate New Game Class
    game = game_obj()
    game_lobby = game.lobby

    game_lobby.add_player(username)
    lobby_id = game_lobby.game_id

    GAMES[lobby_id] = game
    join_room(lobby_id)

    print("--create lobby--")
    print(game_lobby.lobby_info()["players"])
    emit(
        "join_lobby", {"lobby_id": lobby_id, "lobby_info": game_lobby.lobby_info()},
    )


@socketio.on("join_lobby")
def on_join_lobby(data):
    """Join a generic game lobby"""
    username = data["username"]
    lobby_id = data["joinLobbyId"]

    if lobby_id not in GAMES:
        emit("error", {"error": "Unable to join room. Room does not exist."})
        return

    join_room(lobby_id)
    game = GAMES[lobby_id]
    game_lobby = game.lobby

    game_lobby.add_player(username)
    print("--join lobby--")
    print(game_lobby.lobby_info()["players"])
    emit(
        "join_lobby",
        {"lobby_id": lobby_id, "lobby_info": game_lobby.lobby_info()},
        room=lobby_id,
    )


@socketio.on("leave_lobby")
def on_leave(data):
    print("leave")
    """Leave the game lobby"""
    username = data["username"]
    lobby_id = data["lobbyId"]

    game = GAMES[lobby_id]
    game_lobby = game.lobby

    # remove player and rebroadcast game object
    game_lobby.remove_player(username)
    leave_room(lobby_id)

    # Send to the user who left the lobby
    emit(
        "leave_lobby", {"lobby_id": lobby_id, "lobby_info": game_lobby.lobby_info()},
    )

    # Send to the users who are still in lobby
    emit(
        "someone_left_lobby",
        {"lobby_id": lobby_id, "lobby_info": game_lobby.lobby_info()},
        room=lobby_id,
    )


"""
-----------------------------
Spyfall specific endpoints
-----------------------------
"""


@socketio.on("spyfall_start_game")
def spyfall_start_game(data):
    """Start Game"""
    username = data["username"]
    lobby_id = data["lobbyId"]

    game: Spyfall = GAMES[lobby_id]
    game_lobby = game.lobby

    game.start_game()

    emit("game_start", {"message": "start game"}, room=lobby_id)


@socketio.on("spyfall_game_info")
def spyfall_game_info(data):
    """Get Spyfall Game Information"""
    username = data["username"]
    lobby_id = data["lobbyId"]
    game: Spyfall = GAMES[lobby_id]

    emit("spyfall_game_info", game.game_info())


@socketio.on("spyfall_end_game")
def spyfall_end_game(data):
    """End Spyfall Game"""
    username = data["username"]
    lobby_id = data["lobbyId"]
    game: Spyfall = GAMES[lobby_id]

    if game:
        emit("spyfall_end_game", room=lobby_id)


def prune():
    """Prune rooms stale for more than 6 hours"""

    def delete_room(gid):
        close_room(gid)
        del ROOMS[gid]

    def is_stale(room):
        """Stale rooms are older than 6 hours, or have gone 20 minutes less than 5 minutes of total playtime"""
        return (
            (datetime.now() - room.date_modified).total_seconds() >= (60 * 60 * 24)
        ) or (
            (datetime.now() - room.date_modified).total_seconds() >= (60 * 20)
            and room.playtime() <= 5
        )

    if ROOMS:
        rooms = ROOMS.copy()
        for key in rooms.keys():
            if is_stale(ROOMS[key]):
                delete_room(key)
        del rooms
        gc.collect()


@app.route("/debug-sentry")
def trigger_error():
    division_by_zero = 1 / 0


@app.route("/stats")
def stats():
    """display room stats"""
    resp = {
        "total": len(ROOMS.keys()),
        "total_games": len(GAMES.keys()),
        "bytes_used": getsizeof(GAMES),
    }
    if "rooms" in request.args:
        if ROOMS:
            resp["rooms"] = sorted(
                [v.to_json() for v in ROOMS.values()],
                key=lambda k: k.get("date_modified"),
                reverse=True,
            )
        else:
            resp["rooms"] = None
    return jsonify(resp)


@app.route("/prune")
def hard_reset():
    GAMES.clear()
    gc.collect()
    return jsonify({"message": "hard reset room"})


# @socketio.on("create")
# def on_create(data):
#     """Create a game lobby"""
#     # username = data['username']
#     # create the game
#     # handle custom wordbanks
#     # prune old rooms
#     if data["dictionaryOptions"]["useCustom"]:
#         gm = game.Info(
#             size=data["size"],
#             teams=data["teams"],
#             wordbank=data["dictionaryOptions"]["customWordbank"],
#         )
#     # dict mixer
#     elif data["dictionaryOptions"]["mix"]:
#         gm = game.Info(
#             size=data["size"],
#             teams=data["teams"],
#             mix=data["dictionaryOptions"]["mixPercentages"],
#         )

#     # handle standard single dictionary
#     else:
#         gm = game.Info(
#             size=data["size"],
#             teams=data["teams"],
#             dictionary=data["dictionaryOptions"]["dictionaries"],
#         )

#     room = gm.game_id
#     ROOMS[room] = gm
#     join_room(room)
#     # rooms[room].add_player(username)
#     emit("join_room", {"room": room})
#     prune()


# @socketio.on("join")
# def on_join(data):
#     """Join a game lobby"""
#     # username = data['username']
#     room = data["room"]
#     if room in ROOMS:
#         # add player and rebroadcast game object
#         # rooms[room].add_player(username)
#         join_room(room)
#         send(ROOMS[room].to_json(), room=room)
#     else:
#         emit("error", {"error": "Unable to join room. Room does not exist."})


# @socketio.on("leave")
# def on_leave(data):
#     """Leave the game lobby"""
#     # username = data['username']
#     room = data["room"]
#     # add player and rebroadcast game object
#     # rooms[room].remove_player(username)
#     leave_room(room)
#     send(ROOMS[room].to_json(), room=room)


# @socketio.on("flip_card")
# def on_flip_card(data):
#     """flip card and rebroadcast game object"""
#     ROOMS[data["room"]].flip_card(data["card"])
#     send(ROOMS[data["room"]].to_json(), room=data["room"])


# @socketio.on("regenerate")
# def on_regenerate(data):
#     """regenerate the words list"""
#     room = data["room"]
#     ROOMS[room].generate_board(data.get("newGame", False))
#     send(ROOMS[room].to_json(), room=room)


# @socketio.on("list_dictionaries")
# def list_dictionaries():
#     """send a list of dictionary names"""
#     # send dict list to client
#     emit("list_dictionaries", {"dictionaries": list(game.DICTIONARIES.keys())})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)
