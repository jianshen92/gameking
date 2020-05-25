<template>
  <v-card shaped @click="toggleCard" class="mx-2 my-1 px-3 py-1" v-bind:class="[isCrossOut ? 'blue-grey darken-4 cross-out' : '']">
    {{location}}
  </v-card>
</template>

<script>
export default {
  name: "SpyfallCard",
  props: {
    location : String,
  },
  data () {
    return {
      isCrossOut: false
    }
  },
  methods : {
    toggleCard(){
      this.isCrossOut = !this.isCrossOut
    }
  },
}
</script>

<style>
.v-card.cross-out {
  text-decoration: line-through;
  color: #757575;
}
</style>