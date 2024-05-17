<template>
    <div>
        <div class="card flex justify-content-center">
            <Sidebar v-model:visible="visible" header="Sidebar">
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
            </Sidebar>
            <Button icon="pi pi-arrow-right" @click="visible = true" />
        </div>
    </div>
</template>

<script>
import {mapGetters} from "vuex"

import Sidebar from 'primevue/sidebar';

export default {
    name: 'MenuBar',
    components: {
        Sidebar
    },
    computed: {
        ...mapGetters(["dataset"])
    },
    watch: {
        dataset(newVal) {
            console.log("4444",newVal)
        }
    },
    data() {
        return {
            menubarItem: [{
                    label: "user",
                    icon: 'pi pi-fw pi-user',
                    items:[{
                        label: 'clear dataset and model',
                        icon: 'pi pi-fw pi-user-edit',
                        command: () => { window.location.href = './DatasetProgress.vue'}
                    }]
            }],
            li: this.dataset,
        }
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
</style>
    