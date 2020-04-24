<template>
    <v-container d-flex flex-column justify-center align-center>
        <h1>Spyfall - Lobby {{lobbyId}}</h1>
        <v-btn text large color="primary">Start Game</v-btn>
        <v-btn text large color="primary" @click="leaveLobby">Leave Game</v-btn>

    </v-container>
</template>

<script>
  import {mapState, mapGetters, mapMutations} from 'vuex';

  export default {
    name: "spyfall-lobby",
    data() {
      return {
      };
    },
    computed: {
      ...mapState(['lobbyId', 'username']),
    },
    watch: {
    },
    methods: {
      leaveLobby(){
        console.log(`${this.username} is leaving lobby ${this.lobbyId}`);
        const params = {
          username: this.username,
          lobbyId: this.lobbyId
        };
        this.$router.push({name: "SpyfallHome"});
        this.$socket.emit('leave_lobby', params);
      },
    }
  };
</script>