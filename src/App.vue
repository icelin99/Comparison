<template>
<div>
  <div :style="{height:'20%', width:'100%'}"><DataSetProgress /></div>
  <div :style="{height:'80%', width:'100%'}"><ImageModel /></div>
</div>
</template>

<script>

import DataSetProgress from './components/DatasetProgress.vue'
import ImageModel from './components/ImageModel.vue'

export default {
  name: 'App',
  components: {
    DataSetProgress,
    ImageModel
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
  margin-top: 60px;
}
</style>
