<template>
    <div>
      <div :style="{height:'20%', width:'98%', top: '45px',position:'fixed'}"><HomePage/></div>
      <div :style="{height:'80%', width:'98%'}"><ImageModel /></div>
    </div>
</template>

<script>

import HomePage from './HomePage.vue'
import ImageModel from './ImageModel.vue'

export default {
    name: 'App',
    components: {
        HomePage,
        ImageModel
    },
    mounted() {
    this.$store.dispatch('updateIsLoading', false); // 挂载完成，隐藏loading
    }
}
</script>

<style>

</style>
