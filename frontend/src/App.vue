<template>
<div>
  <EvaHeader />
  <div :style="{height:'20%', width:'98%', top: '45px',position:'fixed'}"><DataSetProgress /></div>
  <div :style="{height:'80%', width:'98%'}"><ImageModel /></div>
</div>
</template>

<script>

import DataSetProgress from './components/DatasetProgress.vue'
import ImageModel from './components/ImageModel.vue'
import EvaHeader from './components/EvaHeader.vue'

export default {
  name: 'App',
  components: {
    DataSetProgress,
    ImageModel,
    EvaHeader
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
  margin-right:10px;
  padding: 0 20px 10px 0;
}

</style>
