<template>
<div>
  <div class="header">MLLM Evaluation</div>
  <div :style="{height:'20%', width:'100%', top: '45px',position:'fixed'}"><DataSetProgress /></div>
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
  margin-top: 10px;
}
.header {
  background-color: aliceblue;
  border-bottom: 2px solid #d2e8ff;
  position: fixed;
  top: 0;
  width: 100%;
  height: 40px;
  text-align: left;
  justify-content: center;
  line-height: 40px;
  font-size: large;
  font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: bold;
}
</style>
