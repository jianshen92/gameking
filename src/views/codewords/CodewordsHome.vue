<template>
<lobby @join-game="joinGame" name="Codewords" create-route="create">
  <template slot="game-logo">
    <v-avatar tile size="128">
      <img src="@/assets/logo-256x256.png" alt="codenames logo">
    </v-avatar>
  </template>
</lobby>
</template>

<script>
import { mapMutations } from 'vuex';
import JoinForm from '@/components/JoinForm';
import Lobby from '@/components/layout/Lobby';

export default {
  name: 'CodewordsHome',
  components: {
    JoinForm,
    Lobby
  },
  mounted() {
    this.reset_error();
  },
  methods: {
    ...mapMutations(["set_username", "set_room", "reset_error"]),
    joinGame(event){
      this.set_room(event.room_id);
      this.$router.push({ name: "Player", params: { room: event.room_id } });
    }
  },
};
</script>
