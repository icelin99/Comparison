<template>
    <div>
      <div :style="{height:'20%', width:'98%', top: '45px',position:'fixed'}"><DataSetProgress /></div>
      <div :style="{height:'80%', width:'98%'}"><ImageModel /></div>
    </div>
</template>

<script>

import DataSetProgress from './DatasetProgress.vue'
import ImageModel from './ImageModel.vue'

export default {
    name: 'App',
    components: {
        DataSetProgress,
        ImageModel
    },
    mounted() {
    this.$store.dispatch('updateIsLoading', false); // 挂载完成，隐藏loading
    }
}
</script>

<style>

</style>
