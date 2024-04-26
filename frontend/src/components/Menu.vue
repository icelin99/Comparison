<template>
    <div>
        <Menubar>
        <template #start>
            <p>MLLM Evaluation</p>
        </template>   
        <template #end>

        </template>
    </Menubar>
    </div>
</template>

<script>

import Menubar from 'primevue/menubar';

export default {
    name: 'App',
    components: {
        Menubar
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
            }]
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
    