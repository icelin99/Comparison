<template>
<div>

    <div v-if="isShow" style="display: flex; flex-direction: row; width: '100%'; height: '100%'">
        <div :style="{width: '40%', height: '100%'}">
            <div style="display: flex; flex-direction: column; width: '100%'; height: '100%'; align-items: center;">
                <div class="image-container"><img :src="currentData.image" alt="Can't find image"></div>
                <div class="text-container"><div>Question: </div><div class="text-border"> {{currentData.question}}</div></div>
                <div class="text-container"><div>Tag:</div>
                    <div v-for="(item, index) in currentData.tag" :key="index" class="tag-list">
                        <Tag severity="success" :style="{backgroundColor:colorScale(item),color:'#696969'}"> {{ item }}</Tag>
                    </div>
                </div>
            </div>
        </div>
        <div :style="{width: '60%', height: '100%'}">
            <div style="display: flex; flex-direction: row; width: '100%'; height: '100%'">
                <DataTable :value="modelList" stripedRows tableStyle="min-width: 50rem">
                    <Column field="model" header="Model"></Column>
                    <Column field="answer" header="Answer"></Column>
                    <Column  header="Score">
                        <template #body="slotProps">
                            <Rating v-model="slotProps.data.standardScore" :stars="ratingStandard-1" @update:modelValue="onRatingChange">
                                <template #cancelicon>
                                    <img src="/assets/cancel.png" width="24" height="24"/>
                                </template>
                                <template #onicon>
                                    <img src="/assets/smiley.png" width="24" height="24" />
                                </template>
                                <template #officon>
                                    <img src="/assets/pensive.png" width="24" height="24" />
                                </template>
                            </Rating>
                        </template>
                    </Column>
                </DataTable>
               
            </div>
        </div>
    </div>
    <div v-if="isShow" class="page-change" style="display: flex; flex-direction: column; width: '100%';">
        <div class="save-button">
            <Button style="margin-right: 20px; background-color: cornflowerblue;" v-if="!saveOneClick" label="Save this page"  @click="saveOnePage"  />
            <Button style="margin-right: 20px; background-color: cornflowerblue;" v-if="saveOneClick" label="This page saved ✔️" disabled="true" />
            <Button style="margin-left: 10px; background-color: cornflowerblue;" v-if="!saveAllClick" label="Save All"     @click="saveAllPage" />
            <Button style="margin-left: 10px; background-color: cornflowerblue;" v-if="saveAllClick" label="All saved ✔️" disabled="true" />
        </div>
        <div style="display: flex; flex-direction: row; width: '100%'; height: 30px; line-height: 25px; justify-content: center;align-items: center;">
            <Button label="" icon="pi pi-angle-left" iconPos="right" :style="{backgroundColor: leftHover?'rgba(176,196,222,0.5)': 'lightsteelblue',borderColor: 'aliceblue',marginRight:'15px'}"   @click="prevPage" @mouseover="leftHover = true" @mouseleave="leftHover = false" />
            Page {{ currentPage }} of {{ pageCount }}
            <Button label=""  icon="pi pi-angle-right"  :style="{backgroundColor: rightHover? 'rgba(100,149,237,0.5)':'cornflowerblue',borderColor: 'aliceblue'}"   @click="nextPage" @mouseover="rightHover = true" @mouseleave="rightHover = false" />
            <p> jump to a specific page</p>
            <InputNumber v-model="jumpPage" inputId="minmax-buttons" mode="decimal" :min="1" :max="pageCount" @keyup.enter="jump" autofocus />
        </div>
        
    </div>
</div>
</template>

<script>
import * as d3 from 'd3'
import Image from './Image.vue'
import Model from './Model.vue'
import Dropdown from 'primevue/dropdown'
import {mapGetters, mapMutations} from "vuex"
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import Tag from 'primevue/tag'
import Rating from 'primevue/rating'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

export default {
    name: 'App',
    components: {
        Image,
        Model,
        Dropdown,
        Button,
        InputNumber,
        Tag,
        Rating,
        DataTable,
        Column
    },
    computed: {
        ...mapGetters(["selectSubmitted","currentData", "pageCount", "currentPage","ratingStandard"]),
    },
    mounted() {
        this.$store.dispatch("updateCurrentPage",1);
        // this.tag = this.currentData.tag;
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
                "score":0,
                "standardScore": 0,
            }]
        }
    },
    data() {
        return {
            isShow: false,
            data: null,
            modelList: [],
            scoreList: [0,0.5,1],
            selectedScore: null,
            imagePath: "/assets/scenery.jpeg",
            question: "How is the view in this picture?",
            tag: null,
            jumpPage: null,
            leftHover: false,
            rightHover: false,
            colorScale: d3.scaleOrdinal(d3.schemePastel1),
            saveOneClick: false,
            saveAllClick: false,
        }
    },
    methods: {
        ...mapMutations(['nextItem','prevItem','setPage']),
        nextPage() {
            this.nextItem();
        },
        prevPage() {
            this.prevItem();
        },
        jump() {
            console.log("jump page",this.jumpPage);
            if(this.jumpPage >= 1 && this.jumpPage <= this.pageCount) {
                this.$store.dispatch("updateCurrentPage",this.jumpPage)
                this.jumpPage = null;
            }
        },
        onRatingChange() {
            // 映射到相应的分数段
            let scale = null;
            if(this.ratingStandard == 3) {
                scale = d3.scaleOrdinal().domain([0,1,2]).range([0,0.5,1])
            } else {
                scale = d3.scaleOrdinal().domain([0,1,2,3,4]).range([0,0.25,0.5,0.75,1])
            }
            this.modelList[0].score = scale(this.modelList[0].standardScore)
            this.saveOneClick = false;
            this.saveAllClick = false;
        },
        saveOnePage() {
            this.saveOneClick = true;
            //  save to databse
        },
        saveAllPage() {
            this.saveAllClick = true;
            // save all to database
        }
    }
}
</script>

<style>
.model-container {
    display: flex;
    justify-content: center;
    /* margin-bottom: 10px; */
}
.mode-name {
    width: 20%;
}
.model-answer {
    width: 60%;
}
.model-score {
    max-height: 40px;
    align-items: center;
    padding: 1px 2px 1px 2px;
    width: 20%;
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
    background-color: rgba(135,206,250,0.6);
}
.page-change {
    bottom: 0;
    padding: 15px 0 10px 0;
    align-items: center;
    margin: auto;
    justify-content: center;
    position: fixed;
    width: 100%;
}
.page-change p {
    margin-left:50px;
}
.tag-list {
    /* margin-left: 15px; */
    padding-left: 5px;
}
.rating-img {
    width: 24px;
    height: 24px;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
}
.rating-img img {
    width: 100%;
    height: 100%;
}
.save-button {
    padding-bottom: 30px;
    padding-right: 20px;
    padding-left: 20px;
}
</style>
<style scoped>

::v-deep .p-dropdown {
  height: 50px !important; /* Set your desired item height */
  align-items: center;
}
::v-deep .p-button {
    transition: background-color 0.3s !important; 

}
::v-deeep .p-button:hover {
    background-color: #f1f5f9 !important;
}
::v-deep .p-inputtext {
    margin-left:10px;
    width: 50px;
}
::v-deep .p-rating {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
::v-deep .p-rating-item{
    margin-right: 2px;
    padding: 0;
    width: 24px;
    height: 24px;
    box-sizing: border-box;
    flex-basis: 24px;
}
</style>
    