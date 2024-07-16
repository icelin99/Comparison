<template>
<div class="hide-scrollbar">
  <LoadingComponent />
  <EvaHeader class="header" />
  <div class="content">
    <router-view />
  </div>
</div>
</template>

<script>
import EvaHeader from './components/EvaHeader.vue'
import LoadingComponent from './components/LoadingComponent.vue'

export default {
  name: 'App',
  components: {
    EvaHeader,
    LoadingComponent
  },
  mounted() {
    this.$store.dispatch('updateIsLoading', false); // 挂载完成，隐藏loading
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
  padding: 0 20px 10px 0;
}
body::-webkit-scrollbar {
  width: 0;
  background: transparent;
}


</style>
