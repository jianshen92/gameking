<template>
  <v-container d-flex flex-column justify-center mx-md-10 fluid>
    <div class="display-1 font-weight-bold text-center">Spyfall</div>
    <div v-if="isGameEnd" class="title text-center">
      Time has ran out. Game Ends.
    </div>
    <div v-else class="title text-center">
      <CountdownTimer @timeout="onTimeout" :endTime="endTime"/>
    </div>
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
            <SpyfallCard :location="location"/>
          </v-col>
      </v-row>
    </div>
    <v-btn text large color="primary" @click="endGame">End Game</v-btn>
  </v-container>
</template>

<script>
  import {mapState, mapGetters, mapMutations} from 'vuex';
  import CountdownTimer from '@/components/common/CountdownTimer';
  import SpyfallCard from '@/components/spyfall/SpyfallCard'

  export default {
    name: "spyfall-game",
    components: {CountdownTimer, SpyfallCard},
    data: function() {
      return {
          locationList: [],
          isSpy: false,
          location: null,
          startTime: null,
          endTime: null,
          gameDurationMinutes: null,
          isLoading: true,
          isGameEnd: false,
      };
    },
    computed: {
      ...mapState(['lobbyId', 'username','lobbyPlayers'])
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
        this.endTime = message.game_end_time;
        this.gameDurationMinutes = message.game_time_minutes;
        this.isSpy = (playerRole == "SPY");
        this.isLoading = false;
      },
      spyfall_end_game(){
        this.end_game();
        this.$router.push({name: "SpyfallLobby"});
      }
    },
    methods: {
      ...mapMutations(["end_game"]),
      onTimeout(){
          this.isGameEnd = true
      },
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