<template>
  <v-fade-transition appear>
    <v-card>
      <v-card-text>
        <v-form @submit="joinGame">
          <!-- <v-text-field label="Username" v-model="username" required></v-text-field> -->
          <v-alert type="error" :value="showInputError" transition="slide-y-reverse-transition">
            Room ID required to join.
          </v-alert>
          <v-text-field label="Enter Room ID" v-model="room_num" :rules="[rules.required]" mask="AAAAA" solo light hide-details></v-text-field>
          <v-btn block color="primary" large @click.stop="joinGame">Join</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-fade-transition>
</template>

<script>
export default {
  name: "create-form",
  data() {
    return {
      // username: '',
      room_num: null,
      showInputError: false,
      rules: {
        required: value => !!value || "Required."
      }
    };
  },
  computed: {
    room_id() {
      return this.room_num.toUpperCase();
    }
  },
  methods: {
    joinGame() {
      this.showInputError = false;
      if (this.room_num) {
        this.$emit("join-game", { room_id: this.room_id })
      } else {
        this.showInputError = true;
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
