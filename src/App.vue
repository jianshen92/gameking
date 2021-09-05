<template>
  <v-app dark id="codenames">
    <v-navigation-drawer temporary right app v-model="drawer">
      <v-list class="pa-1">
        <v-list-item tag="div">
          <v-list-item-action>
            <v-btn
              icon
              @click.stop="drawer = !drawer"
              aria-label="Close drawer"
            >
              <v-icon>chevron_right</v-icon>
            </v-btn>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Help</v-list-item-title>
          </v-list-item-content>
          <v-list-item-avatar>
            <img src="@/assets/logo-64x64.png" alt="codenames logo" />
          </v-list-item-avatar>
        </v-list-item>
      </v-list>
      <v-list class="pt-0" dense>
        <v-divider></v-divider>
        <v-list-item
          v-for="item in helpMenu"
          :key="item.title"
          router
          :to="item.path"
          :href="item.href"
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-list dense two-line>
        <v-divider></v-divider>
        <v-list-item>
          <v-list-item-action>
            <v-icon>wifi</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              Socket Status: {{ connected ? "Connected" : "Not Connected" }}
            </v-list-item-title>
            <v-list-item-subtitle v-if="connected">
              Connection Type: {{ this.$socket.io.engine.transport.name }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-subheader>Support Gameking!</v-subheader>
        <v-list-item>
          <coffee-button></coffee-button>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar app fixed :color="getColor" v-if="!error && room">
      <v-toolbar-title class="cn-text headline">{{ room }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-title v-if="isFirstTurn" class="cn-text">{{
        getTurn
      }}</v-toolbar-title>
      <!-- Scoreboard -->
      <v-toolbar-title v-else class="cn-text headline" id="scoreboard">
        <span class="red--text text--darken-1">{{ tileCounts.flipped.R }}</span>
        <span style="padding: 0 10px" v-if="!'G' in tileCounts.flipped">
          <v-avatar size="32">
            <img src="@/assets/logo-64x64.png" alt="codenames logo" />
          </v-avatar>
        </span>
        <span v-else> - </span>
        <span class="blue--text text--darken-1">{{
          tileCounts.flipped.B
        }}</span>
        <template v-if="'G' in tileCounts.flipped">
          <span> - </span>
          <span class="green--text text--lighten-1">{{
            tileCounts.flipped.G
          }}</span>
        </template>
      </v-toolbar-title>
    </v-toolbar>

    <v-content>
      <v-alert
        color="error"
        :value="errorAlert"
        dismissible
        fixed
        @input="onAlertClose"
      >
        {{ error }}
      </v-alert>
      <ApplePopup />
      <!-- <v-container v-if="error">
        <router-view></router-view>
      </v-container> -->
      <v-container grey darken-4 fill-height fluid pa-2>
        <router-view></router-view>
      </v-container>
    </v-content>
    <v-bottom-navigation value="true" app>
      <v-btn text replace :to="{ name: 'Home' }">
        <v-icon medium>home</v-icon> Home
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn text v-if="!connected" value="false">
        <v-icon medium>warning</v-icon> Not Connected
      </v-btn>
      <v-btn
        text
        replace
        :to="{ name: 'Player', params: { room: room } }"
        v-if="room && connected && !error"
      >
        <v-icon medium>person</v-icon> Agent
      </v-btn>
      <v-btn
        text
        replace
        :to="{ name: 'Spymaster', params: { room: room } }"
        v-if="room && connected && !error"
      >
        <v-icon medium>local_library</v-icon> Spymaster
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn text @click.stop="drawer = !drawer" to="#">
        <v-icon medium>help_outline</v-icon> Help
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>

<script>
import { mapGetters, mapState, mapMutations } from "vuex";
import ApplePopup from "@/components/ApplePopup";
import CoffeeButton from "@/components/CoffeeButton";

export default {
  name: "app",
  components: { ApplePopup, CoffeeButton },
  created() {
    // Code to leave any existing lobbies if user refresh or close browser
    window.addEventListener(
      "beforeunload",
      () => {
        //I CAN ACCESS TO this VARIABLE
        console.log(this.gameName);
        const params = {
          gameName: this.gameName,
          username: this.username,
          lobbyId: this.lobbyId,
        };
        this.$socket.emit("leave_lobby", params);
      },
      false
    );
  },
  data() {
    return {
      drawer: false,
      showSidebar: false,
      showError: false,
      showInstallMessage: true,
      helpMenu: [
        //        {
        //          title: "How to Play",
        //          icon: "import_contacts",
        //          path: "/help"
        //        },
        {
          title: "Contact",
          icon: "email",
          href: "mailto:jianshen92@gmail.com?subject=Gameking Support",
        },
        {
          title: "Contribute",
          icon: "code",
          href: "https://github.com/jianshen92/gameking",
        },
        {
          title: "Report a Bug",
          icon: "bug_report",
          href: "https://github.com/jianshen92/gameking/issues/new",
        },
      ],
    };
  },
  computed: {
    ...mapState([
      "connected",
      "room",
      "error",
      "errorAlert",
      "game",
      "turn",
      "lobbyId",
      "username",
      "gameName",
    ]),
    ...mapGetters(["gameWon", "tileCounts"]),
    isFirstTurn() {
      if (!this.connected) {
        return true;
      }
      if (this.game.board) {
        return Object.values(this.game.board).every((e) => e === false);
      }
      return true;
    },
    getColor() {
      // override bar color if ws not connected
      if (!this.connected) {
        return "red darken-3";
      }
      if (this.isFirstTurn) {
        switch (this.turn) {
          case "R":
            return "red darken-3";
          case "G":
            return "green lighten-1";
          case "B":
            return "blue darken-2";
          default:
            return "secondary";
        }
      }
      return "secondary";
    },
    getTurn() {
      // override starting team text if ws is not connected
      if (!this.connected) {
        return "Unable to connect to server.";
      }
      switch (this.turn) {
        case "R":
          return "Red Team Starts";
        case "G":
          return "Green Team Starts";
        case "B":
          return "Blue Team Starts";
        default:
          return "";
      }
    },
  },
  mounted() {
    this.$socket.emit("list_dictionaries");
  },
  methods: {
    ...mapMutations(["set_turn", "reset_error"]),
    browserClose(e) {
      e.preventDefault();
      console.log("hi");
    },
    onAlertClose(e) {
      console.log("dismiss alert");
      this.reset_error();
    },
  },
};
</script>

<style lang="scss">
html,
body {
  background: #303030;
}
.cn-text {
  font-family: "Courier New", Courier, "Lucida Sans Typewriter",
    "Lucida Typewriter", monospace !important;
  letter-spacing: 1px !important;
  &--upcase {
    text-transform: uppercase;
  }
  &--caps {
    text-transform: capitalize;
  }
}
#scoreboard {
  font-weight: bold;
}
</style>
