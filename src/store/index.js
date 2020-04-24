import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate'
import * as Cookies from 'js-cookie'

Vue.use(Vuex);
const inFifteenMinutes = new Date(new Date().getTime() + 15 * 60 * 1000);

export default new Vuex.Store({
  plugins: [createPersistedState({
    storage: {
      getItem: key => Cookies.get(key),
      // Please see https://github.com/js-cookie/js-cookie#json, on how to handle JSON.
      setItem: (key, value) => Cookies.set(key, value, { expires: inFifteenMinutes }),
      removeItem: key => Cookies.remove(key)
    }
  })],
  state: {
    // By jian shen
    lobbyId: '',
    gameName: '',

    // end
    connected: false,
    dictionaries: [],
    game: {},
    room: '',
    username: '',
    error: null,
    turn: '',
    spymasterReveal: false,
    popupHides: 0
  },
  getters: {
    words(state) {
      if (state.game.solution) {
        return Object.keys(state.game.solution);
      }
      return [];
    },
    tileCounts(state) {
      if (state.game.solution) {
        const flippedCounts = {};
        const totalCounts = {
          R: 0,
          B: 0,
          G: 0,
          X: 0,
        };
        // compile the counts for each team + assassin
        Object.keys(state.game.solution).forEach((word) => {
          if (state.game.solution[word] !== 'O') {
            flippedCounts[state.game.solution[word]] = flippedCounts[state.game.solution[word]] || 0;
            if (state.game.board[word]) {
              flippedCounts[state.game.board[word]] += 1;
            }
            totalCounts[state.game.solution[word]] = totalCounts[state.game.solution[word]] || 0;
            totalCounts[state.game.solution[word]] += 1;
          }
        });
        return {
          total: totalCounts,
          flipped: flippedCounts,
        };
      }
      return false;
    },
    gameWon(state, getters) {
      if (getters.tileCounts) {
        return getters.tileCounts.flipped.X > 0 ||
          getters.tileCounts.flipped.R === getters.tileCounts.total.R ||
          getters.tileCounts.flipped.B === getters.tileCounts.total.B ||
          getters.tileCounts.flipped.G === getters.tileCounts.total.G;
      }
      return false;
    },
  },
  actions: {
    setGame({commit}, payload) {
      commit('SET_GAME', {
        gameName: payload.gameName
      })
    }
  },
  mutations: {
    // By jian shen
    SOCKET_JOIN_LOBBY(state, message){
      state.lobbyId = message.lobby_id;
      console.log("user " + state.username + " has joined lobby:" + state.lobbyId)
      console.log(message.lobby_info.players)
    },

    SET_GAME(state, payload){
      state.gameName = payload.gameName
    },

    SOCKET_LEAVE_LOBBY(state, message){
      state.lobbyId = ""
      console.log(`user ${state.username} has left ${message.lobby_info.game_name} lobby ${message.lobby_info.game_id}`)
      console.log(message.lobby_info.players)
    },
    // end

    SOCKET_CONNECT(state) {
      state.connected = true;
    },
    SOCKET_DISCONNECT(state) {
      state.connected = false;
    },
    SOCKET_MESSAGE(state, message) {
      state.game = message;
      state.turn = message.starting_color;
      state.room = message.game_id;
      state.error = null;
    },
    SOCKET_JOIN_ROOM(state, message) {
      state.error = null;
      state.room = message.room;
    },
    SOCKET_LIST_DICTIONARIES: (state, message) => {
      state.dictionaries = message.dictionaries;
    },
    SOCKET_ERROR(state, message) {
      state.error = message.error;
    },
    set_turn(state, team) {
      state.turn = team;
    },
    set_game(state, game) {
      state.game = game;
    },
    set_room(state, room) {
      state.room = room;
    },
    set_username(state, username) {
      state.username = username;
    },
    reset_error(state) {
      state.room = null;
      state.error = null;
    },
    reveal_spymaster(state) {
      state.spymasterReveal = true;
    },
    reset_room(state) {
      state.game = {};
      state.spymasterReveal = false;
    },
    incrementPopupHides(state) {
      state.popupHides++
    },
  },
});
