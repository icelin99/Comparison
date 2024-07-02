<template>
    <div v-if="isLoading" class="loading-overlay">
      <img src="/assets/loading.gif" alt="Loading" class="loading-image"/>
      <div class="load_txt">{{txt}}</div>
    </div>
</template>

<script>
export default {
  name: 'LoadingComponent',
  computed: {
    isLoading() {
      return this.$store.state.isLoading
    }
  },
  data() {
    return {
      txt: "MLLM Evaluation Loading...",
    }
  }
}
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(255, 255, 255, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  flex-direction: column;
}
.loading-image {
  width: 100px;
}
.load_txt {
  color: rgb(99, 99, 99); /* 白色字体 */
  font-size: 1em; /* 字体大小 */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* 文字阴影 */
  font-family: 'Arial', sans-serif; /* 使用Arial字体 */
  animation: pulse 2s infinite; /* 使用pulse动画，无限循环 */
}
</style>