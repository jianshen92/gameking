<template>
  <v-container d-flex flex-column justify-center mx-10>
    <div class="display-1 font-weight-bold text-center">Spyfall</div>
    <v-progress-circular
      indeterminate
      color="primary"
      v-if="isLoading"
    ></v-progress-circular>
    <div v-else>
      <div class="subtitle-1 font-weight-bold text-center" v-if="isSpy">You are a Spy</div>
      <div class="subtitle-1 font-weight-bold text-center" v-else>{{location}}</div>

      <div class="title font-weight-light text-center">Locations</div>
      <v-row no-gutters>
          <v-col
            v-for="location in locationList"
            v-bind:key="location"
            cols="12"
            sm="6"
          >
            <v-card shaped class="mx-2 my-1 px-3 py-1">
              {{location}}
            </v-card>
          </v-col>
      </v-row>
    </div>
    <v-btn text large color="primary" @click="endGame">End Game</v-btn>
  </v-container>
</template>
<script>
  import {mapState, mapGetters, mapMutations} from 'vuex';

  export default {
    name: "spyfall-game",
    data: function() {
      return {
          locationList: [],
          isSpy: false,
          location: null,
          startTime: null,
          gameDurationMinutes: null,
          isLoading: true,
      };
    },
    computed: {
      ...mapState(['lobbyId', 'username','lobbyPlayers']),
    },
    created: function() {
      const params = {
        username: this.username,
        lobbyId: this.lobbyId
      };
      this.$socket.emit('spyfall_game_info', params);
    },
    sockets: {
      spyfall_game_info(message) {
        const playerRole = message.player_roles[this.username].role;
        this.locationList = message.location_list;
        this.location = message.location;
        this.startTime = message.game_start_time;
        this.gameDurationMinutes = message.game_time_minutes;
        this.isSpy = (playerRole == "SPY");
        this.isLoading = false
      },
      spyfall_end_game(){
        this.end_game();
        this.$router.push({name: "SpyfallLobby"});
      }
    },
    methods: {
      ...mapMutations(["end_game"]),
      endGame(){
        const params = {
          username: this.username,
          lobbyId: this.lobbyId
        };
        this.$socket.emit('spyfall_end_game', params);
      }
    }
  };
</script>