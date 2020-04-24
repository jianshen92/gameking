<template>
  <v-container d-flex flex-column justify-center align-center>
    <h1>Spyfall</h1>
    <v-btn text large color="primary" @click="createLobby">Create Game</v-btn>
    <v-text-field label="Lobby ID" v-model="joinLobbyId" required></v-text-field>
    <v-btn text large color="primary" @click="joinLobby">Join Game</v-btn>
    <v-form>
      <v-text-field label="Username" v-model="form_username" required></v-text-field>
      <v-btn text large color="primary" large @click="setUsername">Set Username</v-btn>
      <div>user name is - {{username}}</div>
    </v-form>
  </v-container>
</template>

<script>
  import {mapState, mapGetters, mapMutations, mapActions} from 'vuex';

  export default {
    name: "spyfall-home",
    data() {
      return {
        form_username: this.username,
        joinLobbyId:''
      };
    },
    mounted: function () {
      this.setGame({gameName: "SPYFALL"});
    },
    computed: {
      ...mapState(['lobbyId', 'username', 'gameName']),
      room_id() {
        return this.room_num.toUpperCase();
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
      setUsername(){
        this.set_username(this.form_username);
      },
      createLobby(){
        console.log("create lobby")
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