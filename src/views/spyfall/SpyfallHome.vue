<template>
  <v-container d-flex flex-column justify-center align-center>
    <h1>Spyfall</h1>
    <v-text-field label="Username" v-model="formUsername" required></v-text-field>
    <v-btn text large color="primary" @click="createLobby">Create Game</v-btn>
    <v-text-field label="Lobby ID" v-model="joinLobbyId" required></v-text-field>
    <v-btn text large color="primary" @click="joinLobby">Join Game</v-btn>
  </v-container>
</template>

<script>
  import {mapState, mapGetters, mapMutations, mapActions} from 'vuex';

  export default {
    name: "spyfall-home",
    data() {
      return {
        joinLobbyId:''
      };
    },
    mounted: function () {
      console.log("hello")
      this.setGame({gameName: "SPYFALL"});
    },
    computed: {
      ...mapState(['lobbyId', 'username', 'gameName']),
      room_id() {
        return this.room_num.toUpperCase();
      },
      formUsername: {
        get () {
          return this.username
        },
        set (value) {
          this.set_username(value)
        }
      }
    },
    watch: {
      username(newValue){
        console.log("username has changed to " + newValue)
      },
      lobbyId(lobbyId){
        if (this.lobbyId != ""){
          console.log("going to lobby " + lobbyId);
          this.$router.push({ name: 'SpyfallLobby'});
        }
      }
    },
    methods: {
      ...mapActions([
        'setGame',
      ]),
      ...mapMutations(["set_username", "set_room"]),
      createLobby(){
        console.log("create lobby")
        console.log(this.gameName)
        const params = {
          gameName: this.gameName,
          username: this.username
        };
        this.$socket.emit('create_lobby', params);
      },
      joinLobby(){
        console.log("join lobby " + this.joinLobbyId);
        const params = {
          gameName: this.gameName,
          username: this.username,
          joinLobbyId: this.joinLobbyId
        };
        this.$socket.emit('join_lobby', params)
      },
      joinGame() {
        // this.set_username(this.username);
        this.showInputError = false;
        if (this.room_num) {
          this.set_room(this.room_id);
          this.$router.push({name: "Player", params: {room: this.room_id}});
        } else {
          this.showInputError = true;
        }
      }
    }
  };
</script>