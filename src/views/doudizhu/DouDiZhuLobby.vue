<template>
  <v-container d-flex flex-column justify-center mx-md-10 fluid>
    <div class="display-2 font-weight-bold text-center">Dou Di Zhu</div>
    <div class="display-1 font-weight-light text-center">{{ lobbyId }}</div>
    <v-btn text large color="primary" @click="startGame">Start Game</v-btn>
    <v-btn text large color="primary" @click="leaveLobby">Leave Game</v-btn>

    <v-container>
      <div class="title font-weight-light text-center">Players</div>
      <v-list>
        <v-list-item-group dark>
          <v-list-item v-for="player in lobbyPlayers" v-bind:key="player">
            <v-list-item-content>
              <v-list-item-title v-text="player"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-container>
  </v-container>
</template>

<script>
import { mapState, mapGetters, mapMutations } from "vuex";

export default {
  name: "doudizhu-lobby",
  data() {
    return {};
  },
  computed: {
    ...mapState(["lobbyId", "username", "lobbyPlayers"]),
  },
  sockets: {
    game_start() {
      this.start_game();
      this.$router.push({ name: "DouDiZhuGame" });
    },
  },
  methods: {
    ...mapMutations(["start_game"]),
    startGame() {
      const params = {
        username: this.username,
        lobbyId: this.lobbyId,
      };
      this.$socket.emit("ddz_start_game", params);
    },
    leaveLobby() {
      console.log(`${this.username} is leaving lobby ${this.lobbyId}`);
      const params = {
        username: this.username,
        lobbyId: this.lobbyId,
      };
      this.$router.push({ name: "DouDiZhuHome" });
      this.$socket.emit("leave_lobby", params);
    },
  },
};
</script>