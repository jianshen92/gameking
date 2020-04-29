<template>
  <v-layout flex-row align-start justify-center text-xs-center row wrap>
    <v-flex lg4 md5 sm6 xs12>
      <slot name="game-logo">
      </slot>
      <h1 class="cn-text">{{name}}</h1>
      <v-alert
        :value="false"
        type="warning"
      >
        If you experience issues, please try refreshing the page.
      </v-alert>
      <v-btn block color="secondary" large :to="createRoute" id="create-btn">Create Game</v-btn>
      <join-form @join-game="$emit('join-game', $event)"></join-form>
      <v-card class="mt-2 text-xs-left">
        <v-card-title>
          <span class="title font-weight-light">Enjoying {{name}}?</span>
        </v-card-title>
        <v-card-text class="ma-0 py-1">
          Consider donating to keep this website running and to support future development!
        </v-card-text>
        <v-card-actions class="text-xs-left">
          <coffee-button></coffee-button>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import JoinForm from '@/components/JoinForm';
import CoffeeButton from '@/components/CoffeeButton';

export default {
  name: 'Lobby',
  props: {
    name: {
      type: String,
      required: true
    },
    createRoute: {
      type: String,
      default: "create"
    }
  },
  components: {
    JoinForm,
    CoffeeButton
  }
};
</script>
