<template>
<div>
    <div v-if="isShow" style="display: flex; flex-direction: row; width: '100%'; height: '100%'">
        <div :style="{width: '40%', height: '100%'}">
            <div style="display: flex; flex-direction: column; width: '100%'; height: '100%'; align-items: center;">
                <div class="image-container"><img :src="currentData.image" alt="Can't find image"></div>
                <div class="text-container"><div>Question: </div><div class="text-border"> {{currentData.question}}</div></div>
                <div class="text-container"><div>Tag: </div><div class="text-border"> {{ currentData.tag }}</div></div>
            </div>
        </div>
        <div :style="{width: '60%', height: '100%'}">
            <div style="display: flex; flex-direction: column; width: '100%'; height: '100%'">
                <div class="model-container" v-for="(item, index) in modelList" :key="index" >
                    <div class="model-name">{{ item.model }}</div>
                    <div class="model-answer">{{ item.answer }}</div>
                    <div class="model-score">
                        <Dropdown style=" width: 150px; line-height: 30px;"  placeholder="scoring for this model performance" v-model="selectedScore" :options="scoreList" />
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-if="isShow" class="page-change" style="display: flex; flex-direction: row; width: '100%'; height: '30px'">
        <Button label="" icon="pi pi-angle-left" iconPos="right" style="background-color: lightsteelblue;border-color: aliceblue; margin-right:15px;"   @click="prevPage" />
        <Button label=""  icon="pi pi-angle-right"  style="background-color: cornflowerblue;border-color: aliceblue;"   @click="nextPage" />
    </div>
</div>
</template>

<script>
import Image from './Image.vue'
import Model from './Model.vue'
import Dropdown from 'primevue/dropdown'
import {mapGetters, mapMutations} from "vuex"
import Button from 'primevue/button'
export default {
    name: 'App',
    components: {
        Image,
        Model,
        Dropdown,
        Button
    },
    computed: {
        ...mapGetters(["selectSubmitted","currentData"])
    },
    watch: {
        selectSubmitted(newVal) {
            console.log("submittted and show!");
            if(newVal == true) {
                this.isShow = true;
            } else {
                this.isShow = false;
            }
        },
        currentData(newVal) {
            console.log("current data",newVal);
            // todo: modify modelList when I get multiple models data.
            this.modelList = [{
                "model": "model1",
                "answer": newVal.answer,
                "socre":null,
            }]
        }
    },
    data() {
        return {
            isShow: false,
            data: null,
            modelList: [{
                "model": "model 1",
                "answer": "The view in this picture is serene, with the calm, clear waters reflecting the tranquility of nature. The boat glides gently, offering a peaceful respite from the hustle of daily life.",
                "score": 0
            }, {
                "model": "model 2",
                "answer": "This image captures the stunning clarity of the water, a testament to the pristine environment. The vivid greenery and the cascading waterfall in the background create a picturesque scene of natural beauty.",
                "score": 0.5
            }, {
                "model": "model 3",
                "answer": "It's a breathtaking view that showcases the harmony between humans and nature. The traditional boat and the person's attire suggest a cultural depth, adding a layer of richness to the already visually captivating landscape.",
                "score": 0
            }, {
                "model": "model 4",
                "answer": "The photograph offers a glimpse into a world that appears untouched by time, where the purity of the water and the lushness of the surrounding foliage speak of a hidden paradise.",
                "score": 1
            }, {
                "model": "model 5",
                "answer": "This view is like a painting come to life, where every element conspires to evoke a sense of wonder. The waterfall adds a sense of grandeur to the scene, making it not just a picture, but an experience for the viewer.",
                "score": 0.5
            }],
            scoreList: [0,0.5,1],
            selectedScore: 0,
            imagePath: "/assets/scenery.jpeg",
            question: "How is the view in this picture?",
            tag: "tag of the dataset",
        }
    },
    methods: {
        ...mapMutations(['nextItem','prevItem']),
        nextPage() {
            this.nextItem();
        },
        prevPage() {
            this.prevItem();
        }
    }
}
</script>

<style>
.model-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}
.model-container div {
    flex: 1;
    text-align: center;
    padding: 10px;
}
.model-score {
    max-height: 40px;
    align-items: center;
}
.image-container {
    width: 400px;
    height: 400px;
    overflow: hidden;
}
.image-container  img {
    width: 98%;
    height: 98%;
    object-fit: cover;
}
.text-container {
    width: 98%;
    display: flex;
    flex-direction: row;
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 5px;
    padding-bottom: 5px;
    align-items: center;
}
.text-border {
    border: 1px solid skyblue;
    border-radius: 5px;
    padding: 5px;
    margin-left: 20px;
}
.page-change {
    bottom: 0;
    padding: 15px 0 10px 0;
    align-items: center;
    margin: auto;
    justify-content: center;
}
</style>
<style scoped>

::v-deep .p-dropdown {
  height: 50px !important; /* Set your desired item height */
  align-items: center;
}
</style>
    