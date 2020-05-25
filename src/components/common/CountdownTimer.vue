<template>
  <span>
    {{ minuteSecond }}
  </span>
</template>

<script>
export default {
  name: "CountdownTimer",
  props: {
    endTime : Number,
  },
  data () {
    return {
      timerCount: null,
      minuteSecond: "00:00",
      timerEnd: false,
    }
  },
  methods : {
    timeout(){
      this.$emit('timeout');
      this.timerEnd = true;
    }
  },
  watch: {
    endTime : {
      immediate: true,
      handler (value) {
        this.timerCount = Math.round(value - ( Date.now() / 1000 ))
      }
    },
    timerCount: {
      handler(value) {
          if (value > 0) {
              setTimeout(() => {
                  this.timerCount--;
                  this.minuteSecond = new Date(this.timerCount * 1000).toISOString().substr(14, 5);
              }, 1000);
          } else if (value == 0) {
              this.timeout()
          }
      },
      immediate: true // This ensures the watcher is triggered upon creation
    }
  }
}
</script>