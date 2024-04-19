<template>
<div>
    <div v-if="isShow" style="display: flex; flex-direction: row; width: '100%'; height: '100%'">
        <div :style="{width: '40%', height: '100%', background: 'azure'}"><Image /></div>
        <div :style="{width: '60%', height: '100%'}"><Model /></div>
    </div>
</div>
</template>

<script>
import Image from './Image.vue'
import Model from './Model.vue'
import {mapGetters} from "vuex"
export default {
    name: 'App',
    components: {
        Image,
        Model
    },
    computed: {
        ...mapGetters(["selectSubmitted"])
    },
    watch: {
        selectSubmitted(newVal) {
            console.log("submittted and show!");
            if(newVal == true) {
                this.isShow = true;
            } else {
                this.isShow = false;
            }
        }
    },
    data() {
        return {
            isShow: false
        }
    }
}
</script>

<style>

</style>
    