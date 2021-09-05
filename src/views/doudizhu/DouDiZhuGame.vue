<template>
  <div class="ddz-container">
    <!-- <v-container flex-column justify-center fill-height> -->
    <!-- <div class="display-1 font-weight-bold text-center">Dou Di Zhu Game</div> -->
    <v-btn v-on:click="restartGame" color="error"> Restart Game</v-btn>
    <div class="ddz-river">
      <PokerCard
        v-for="card in river"
        :key="card.suit + '-' + card.rank"
        :suit="card.suit"
        :rank="card.rank"
        :class="'padded ddz-river-cards'"
      />
    </div>
    Bid : {{ currentBid }} DiZhu : {{ dizhu }}
    <div class="ddz-centre-field">
      <div class="ddz-left-player-panel ddz-side-panel">
        <div class="ddz-player-name">{{ leftPlayerName }}</div>
        <div class="ddz-side-player-hand">
          <PokerCard :flipped="true" :class="'ddz-side-hand'" />
        </div>
        <div class="ddz-player-card-left">{{ leftPlayerCards.length }}</div>
      </div>
      <div class="ddz-left-player-play ddz-side-player-play">
        <PokerCard
          v-for="(card, index) in leftPlayerLastPlayedCards"
          :key="card.suit + '-' + card.rank"
          :suit="card.suit"
          :rank="card.rank"
          :class="['stacked ddz-played-hand', index === 0 ? 'first' : '']"
        />
      </div>
      <div class="ddz-placeholder-space"></div>
      <div class="ddz-right-player-play ddz-side-player-play">
        <PokerCard
          v-for="(card, index) in rightPlayerLastPlayedCards"
          :key="card.suit + '-' + card.rank"
          :suit="card.suit"
          :rank="card.rank"
          :class="['stacked ddz-played-hand', index === 0 ? 'first' : '']"
        />
      </div>
      <div class="ddz-right-player-panel ddz-side-panel">
        <div class="ddz-player-name">{{ rightPlayerName }}</div>
        <div class="ddz-side-player-hand">
          <PokerCard :flipped="true" :class="'ddz-side-hand'" />
        </div>
        <div class="ddz-player-card-left">{{ rightPlayerCards.length }}</div>
      </div>
    </div>
    <div class="ddz-player-played-hand">
      <PokerCard
        v-for="(card, index) in myLastPlayedCards"
        :key="card.suit + '-' + card.rank"
        :suit="card.suit"
        :rank="card.rank"
        :class="['stacked ddz-played-hand', index === 0 ? 'first' : '']"
      />
    </div>

    <div class="ddz-action-panel">
      <template v-if="isMyTurn">
        <template v-if="phase == 'bid'">
          <v-btn
            v-on:click="bid(bidValue)"
            v-for="bidValue in remainingBids"
            :key="bidValue"
            >{{ bidValue }}
          </v-btn>
          <v-btn v-on:click="bidPass" color="error"> Pass</v-btn>
        </template>
        <template v-else>
          <v-btn
            v-on:click="playCards"
            :disabled="selectedCards.length == 0 ? true : false"
            >Play Cards</v-btn
          >
          <v-btn v-on:click="passTurn" color="error"> Pass</v-btn>
        </template>
      </template>
      <v-btn v-else :disabled="true">Waiting for Other Players</v-btn>
    </div>
    <!-- <div>{{ [...selectedCards] }}</div> -->
    <div class="ddz-player-hand">
      <PokerCard
        v-for="(card, index) in myCards"
        :key="card.suit + '-' + card.rank"
        :suit="card.suit"
        :rank="card.rank"
        :class="['stacked ddz-hand', index === 0 ? 'first' : '']"
        :clickable="true"
        @cardSelect="onSelectCard"
        @cardDeselect="onDeselectCard"
      />
    </div>
  </div>
  <!-- </v-container> -->
</template>

<script>
import { mapState, mapGetters, mapMutations } from "vuex";
import PokerCard from "@/components/pokercard/PokerCard";

const mod = (a, n) => ((a % n) + n) % n;

export default {
  name: "doudizhu-game",
  components: { PokerCard },
  data: function () {
    return {
      phase: "",

      river: null,

      isMyTurn: false,

      myCards: [],
      myLastPlayedCards: [],

      leftPlayerCards: [],
      leftPlayerName: null,
      leftPlayerLastPlayedCards: [],

      rightPlayerCards: [],
      rightPlayerName: null,
      rightPlayerLastPlayedCards: [],

      selectedCards: [],

      // bid related
      currentBid: 0,
      remainingBids: [],
      dizhu: "",
    };
  },
  // watch: {
  //   selectedCards: function (newCards) {
  //     console.log("current card :", newCards);
  //   },
  // },
  computed: {
    ...mapState(["lobbyId", "username", "lobbyPlayers"]),
  },
  created: function () {
    const params = {
      username: this.username,
      lobbyId: this.lobbyId,
    };
    this.$socket.emit("ddz_game_info", params);
  },
  sockets: {
    ddz_game_info(message) {
      // Setting all players position
      const { myself, leftPlayer, rightPlayer } = this.getAllPlayers(
        message.game_state.game_player
      );

      // Turn
      this.isMyTurn = message.game_state.current_turn.name == this.username;

      // Myself
      this.myCards = myself.hand.cards;
      this.myLastPlayedCards = myself.last_played.cards;

      // Left Player
      this.leftPlayerCards = leftPlayer.hand.cards;
      this.leftPlayerName = leftPlayer.name;
      this.leftPlayerLastPlayedCards = leftPlayer.last_played.cards;

      // Right Player
      this.rightPlayerCards = rightPlayer.hand.cards;
      this.rightPlayerName = rightPlayer.name;
      this.rightPlayerLastPlayedCards = rightPlayer.last_played.cards;

      this.river = message.game_state.river;

      // Phase
      this.phase = message.game_state.phase;

      // Bid
      this.currentBid = message.game_state.bid_state.bid_value;
      this.remainingBids = message.game_state.bid_state.remaining_bid;

      this.dizhu = message.game_state.dizhu;
    },
    ddz_played_successful(message) {
      /**
       * If played successful, empty selected cards state
       */
      console.log(message);
      if (message.player === this.username) {
        this.selectedCards = [];
      }
    },
    spyfall_end_game() {
      this.end_game();
      this.$router.push({ name: "SpyfallLobby" });
    },
  },
  methods: {
    ...mapMutations(["end_game"]),
    getAllPlayers(gamePlayers) {
      const myIndex = gamePlayers.findIndex(
        (element) => element.name == this.username
      );
      const leftPlayerIndex = mod(myIndex - 1, 3);
      const rightPlayerIndex = mod(myIndex + 1, 3);

      const myself = gamePlayers[myIndex];
      const leftPlayer = gamePlayers[leftPlayerIndex];
      const rightPlayer = gamePlayers[rightPlayerIndex];

      return { myself, leftPlayer, rightPlayer };
    },
    getMyCards(gamePlayers) {
      const myself = gamePlayers.find(
        (element) => element.name == this.username
      );
      return myself.hand.cards;
    },
    onSelectCard(suit, rank) {
      console.log(`selected - suit : ${suit}, rank ${rank} `);
      this.selectedCards.push(`${suit}-${rank}`);
    },
    onDeselectCard(suit, rank) {
      console.log(`deselected - suit : ${suit}, rank ${rank} `);
      this.selectedCards = this.selectedCards.filter(
        (card) => card !== `${suit}-${rank}`
      );
    },

    bid: function (bidValue) {
      const params = {
        username: this.username,
        lobbyId: this.lobbyId,
        bidValue: bidValue,
      };
      this.$socket.emit("ddz_bid", params);
    },

    bidPass: function () {
      const params = {
        username: this.username,
        lobbyId: this.lobbyId,
      };
      this.$socket.emit("ddz_bid_pass", params);
    },

    playCards: function () {
      const params = {
        username: this.username,
        lobbyId: this.lobbyId,
        cardsPlayed: this.selectedCards,
      };
      this.$socket.emit("ddz_play_card", params);
    },
    passTurn: function () {
      const params = {
        username: this.username,
        lobbyId: this.lobbyId,
      };
      this.$socket.emit("ddz_pass", params);
    },
    restartGame: function () {
      const params = {
        username: this.username,
        lobbyId: this.lobbyId,
      };
      this.$socket.emit("ddz_restart", params);
    },
    endGame() {
      const params = {
        username: this.username,
        lobbyId: this.lobbyId,
      };
      this.$socket.emit("spyfall_end_game", params);
    },
  },
};
</script>

<style>
.ddz-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  height: 100%;
}

.ddz-river {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.ddz-centre-field {
  flex: 1;
  display: flex;
  flex-direction: row;
}

.ddz-player-hand {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-top: 2.5em;
}

.ddz-hand {
  height: 12em;
}

.ddz-player-played-hand {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-bottom: 1em;
}

.ddz-played-hand {
  height: 6em;
}

.ddz-side-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ddz-side-hand {
  height: 10rem;
}

.ddz-river-cards {
  height: 6rem;
}

.ddz-placeholder-space {
  flex: 1;
}

.ddz-action-panel {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.ddz-action-panel button {
  margin: 0 0.5em;
}
.ddz-side-player-play {
  display: flex;
  flex-direction: row;
  margin: 3em 1em;
}
</style>