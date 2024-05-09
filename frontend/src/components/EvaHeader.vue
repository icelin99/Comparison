<template>
    <div class="header">MLLM Evaluation
        <div class="clear-button" v-if="alreadySubmit"> Clear all your options
            <Button icon="pi pi-times" severity="danger" text raised rounded aria-label="Cancel" class="small-button"  @click="clearClick" />
        </div>
    </div>
</template>

<script>
import {mapGetters} from "vuex"
import Button from 'primevue/button';
export default {
    name: 'EvaHeader',
    components: {
        Button,
    },
    computed: {
        ...mapGetters(["filterData","alreadySubmit"])
    },
    watch: {
    },
    data() {
        return {
        
        }
    },
    methods: {
        clearClick() {
            this.$store.dispatch("updateAlreadySubmit", false);
            console.log("click alrady submit state",this.alreadySubmit);
        }

    }
}
</script>

<style>
.header {
    background-color: aliceblue;
    border-bottom: 2px solid #d2e8ff;
    position: fixed;
    top: 0;
    width: 98.5%;
    height: 40px;
    text-align: left;
    justify-content: space-between;
    align-items: center;
    line-height: 40px;
    font-size: large;
    font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: bold;
    padding-right: 3px;
    display: flex;
}
.clear-button {
    font-weight: 200;
    font-size: medium;
    justify-content: center;
    align-items: center;
    display: flex;
    padding: 0 10px;
}
.small-button {
    font-size: 12px;
    padding: 2px 5px;
    width: 28px;
    height: 28px;
    margin-left:5px;
}
</style>
    