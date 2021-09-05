<template>
  <div
    :class="['poker-cards', isSelected ? 'selected' : '']"
    v-on:click="toggleSelect"
  >
    <img
      v-if="flipped"
      class="poker-cards-image"
      src="@/assets/pokercards/back.png"
    />
    <img v-else class="poker-cards-image" :src="getCardAsset(suit, rank)" />
  </div>
</template>

<script>
export default {
  name: "PokerCard",
  props: {
    suit: Number,
    rank: Number,
    flipped: {
      type: Boolean,
      default: false,
    },
    clickable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isSelected: false,
    };
  },

  methods: {
    toggleSelect: function () {
      if (!this.clickable) {
        return;
      }
      this.isSelected = !this.isSelected;

      const action = this.isSelected ? "cardSelect" : "cardDeselect";
      this.$emit(action, this.suit, this.rank);
    },
    getCardAsset(suit, rank) {
      const suitMap = {
        1: "diamond",
        2: "clover",
        3: "hearts",
        4: "spade",
        999: "special",
      };

      const rankMap = {
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "J",
        12: "Q",
        13: "K",
        14: "A",
        15: "2",
        998: "black-joker",
        999: "red-joker",
      };

      return require(`@/assets/pokercards/${suitMap[suit]}/${rankMap[rank]}.png`);
    },
  },
};
</script>

<style>
.poker-cards {
  background: white;
  border-radius: 10px;
  border: #bdbdbd 1px solid;
  box-shadow: 0px 0px 10px 2px rgb(0 0 0 / 20%);
}

.poker-cards.stacked {
  margin-left: -6.5em;
}

.poker-cards.stacked.ddz-played-hand {
  margin-left: -3em;
}

.poker-cards.selected {
  margin-top: -1.5em;
}

.poker-cards.padded {
  margin: 0 0.2em;
}

.poker-cards.stacked.first,
.poker-cards.stacked.first.ddz-played-hand {
  margin-left: 0px;
}

.poker-cards-image {
  height: 100%;
  border-radius: 10px;
}
</style>