<template>
  <v-container>
    <v-row>
      <!--card -->

      <!--<v-col-->
      <!--cols="12"-->
      <!--sm="4"-->
      <!--&gt;-->
      <!--<v-card class="mx-auto"-->
      <!--shaped-->
      <!--:elevation="10"-->
      <!--:to="{ name: 'CodewordsHome' }"-->
      <!--&gt;-->
      <!--<v-card-title>-->
      <!--Codewords-->
      <!--</v-card-title>-->
      <!--<v-card-subtitle>-->
      <!--Multiplayer | 2 Teams-->
      <!--</v-card-subtitle>-->
      <!--<v-card-text>-->
      <!--Two teams of player guessing word-->
      <!--</v-card-text>-->
      <!--</v-card>-->
      <!--</v-col>-->

      <!--card end-->
      <!--card -->
      <v-col cols="12" sm="4">
        <v-card
          class="mx-auto"
          shaped
          :elevation="10"
          :to="{ name: 'SpyfallHome' }"
        >
          <v-card-title> Spyfall </v-card-title>
          <v-card-subtitle> Multiplayer </v-card-subtitle>
          <v-card-text> Identify the Spy among the Agents </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card
          class="mx-auto"
          shaped
          :elevation="10"
          :to="{ name: 'DouDiZhuHome' }"
        >
          <v-card-title> Dou Di Zhu </v-card-title>
          <v-card-subtitle> 3 Player </v-card-subtitle>
          <v-card-text>
            Peasants team up and raise against the landlord!
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<<script>
  import {mapState, mapGetters, mapMutations, mapActions} from 'vuex';

  export default {
    name: "home",
    data() {
      return {
      };
    },
    mounted: function () {
      this.setGame({gameName: ""});
    },
    methods: {
      ...mapActions([
        'setGame',
      ]),
    }
  };
</script>