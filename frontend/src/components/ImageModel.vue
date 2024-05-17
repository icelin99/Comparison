<template>
<div>
    <div v-if="isShow" style="display: flex; flex-direction: row; width: 100%; max-height: calc(100% - 90px); overflow-y: auto; position:fixed; top: 45px">
        <div :style="{width: '40%', height: '100%'}">
            <div style="display: flex; flex-direction: column; width: '100%'; height: '100%'; align-items: center;">
                <div class="image-container"><img :src="img_path" alt="Can't find image"></div>
                <div class="text-container"><div class="text-text">Image Path:</div><div class="image-path" @mouseover="startScroll" @mouseleave="stopScroll" >{{pageInfo[0].image_path}}</div></div>
                <div class="text-container"><div class="text-text">Question: </div><div class="text-border"> {{pageInfo[0].question}}</div></div>
                <div class="text-container"><div class="text-text">Category: </div>
                    <div class="tag-container">
                        <div v-for="(item, index) in category" :key="index" class="tag-list">
                            <Tag severity="success" :style="{backgroundColor:colorScale(item),color:'#696969'}"> {{ item }}</Tag>
                        </div>
                    </div>
                </div>
                <div class="text-container"><div class="text-text">Tag:</div>
                    <div class="tag-container">
                        <div v-for="(item, index) in tag" :key="index" class="tag-list">
                            <Tag severity="success" :style="{backgroundColor:colorScale(item),color:'#696969'}"> {{ item }}</Tag>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div :style="{width: '60%', height: '100%'}">
            <div style="display: flex; flex-direction: row; width: '100%'; height: '100%'">
                <DataTable :value="modelList" stripedRows tableStyle="min-width: 50rem; overflow: scroll; white-space: normal; word-wrap: break-word;" >
                    <Column field="model_name" header="Model" style="max-width: 10rem"></Column>
                    <Column field="answer" header="Answer" style="min-width: 25rem; max-width:35rem">
                        <template #body="{ data }">
                            <div v-html="renderMarkdown(data.answer)"></div>
                        </template>
                    </Column>
                    <Column  header="Score" >
                        <template #body="slotProps">
                            <!-- <Rating v-model="slotProps.data.standardScore" :stars="ratingStandard-1" @update:modelValue="value => onRatingChange(value,slotProps.index)">
                                <template #cancelicon>
                                    <img src="/assets/cancel.png" width="24" height="24"/>
                                </template>
                                <template #onicon>
                                    <img src="/assets/smiley.png" width="24" height="24" />
                                </template>
                                <template #officon>
                                    <img src="/assets/pensive.png" width="24" height="24" />
                                </template>
                            </Rating> -->
                            <div class="rating">
                                <span v-for="i in ratingStandard" :key="i" @click="onRatingChange(i,slotProps.index)" :class="{ active: slotProps.data.score !== null && slotProps.data.score !== undefined && i == reverseScaleScore(slotProps.data.score) }">{{ scaleScore(i) }}</span>
                            </div>
                        </template>
                    </Column>
                </DataTable>
               
            </div>
        </div>
    </div>
    <div v-if="isShow" class="page-change" style="display: flex; flex-direction: column; width: '100%';">
        <div class="save-button">
            <!-- <Button style="margin-right: 20px; background-color: cornflowerblue;" v-if="!saveOneClick" label="Save this page"  @click="saveOnePage"  /> -->
            <!-- <Button style="margin-right: 20px; background-color: cornflowerblue;" v-if="saveOneClick" label="This page saved ✔️" disabled="true" /> -->
            <Button style="margin-left: 10px; background-color: cornflowerblue;" v-if="!saveAllClick && currentPage == pageCount" label="Save All"     @click="saveAllPage" />
            <Button style="margin-left: 10px; background-color: cornflowerblue;" v-if="saveAllClick && currentPage == pageCount" label="All saved ✔️" disabled="true" />
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
import api from '@/utils/api'
import MarkdownIt from 'markdown-it'



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
        Column,
    },
    computed: {
        ...mapGetters(["selectSubmitted","currentData", "pageCount", "currentPage","ratingStandard", "pageInfo"]),
        parsedAnswers() {
            const result = {};
            this.modelList.forEach(model => {
                result[model._id] == this.markdown(model.answer);
            })
            return result;
        }
    },
    mounted() {
        this.$store.dispatch('updateIsLoading', false); // 挂载完成，隐藏loading
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
        pageInfo(newVal) {
            console.log("pageInfo",newVal);
            this.img_path = newVal[0].image_code;
            this.tag = newVal[0].tag;
            this.category = newVal[0].categories;
            this.modelList = newVal.map(item => item.modelList[0]);
            // this.modelList.forEach(element => {
            //     // element.standardScore = this.reverseScaleScore(element.score);
            //     // element.standardScore = element.score;
            //     element.answer = "Here is a [link](http://example.com). This is **bold** text and this is _italic_."
            // });
            this.data_info_id = newVal[0].data_info_id;
        },
        currentPage(newVal) {
            console.log("current page",newVal)
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
            // ["好", "图片", "经典", "景点", "任务", "人物", "场景", "风景", "美食", "娱乐", "智能"],
            category: null,
            jumpPage: null,
            leftHover: false,
            rightHover: false,
            colorScale: d3.scaleOrdinal(d3.schemePastel1),
            saveOneClick: false,
            saveAllClick: false,
            img_path: "",
            data_info_id: null,
            scrollInterval: null,
            markdown: new MarkdownIt()
        }
    },
    methods: {
        ...mapMutations(['nextItem','prevItem','setPage']),
        startScroll(event) {
            const target = event.target;
            if (target.scrollWidth > target.clientWidth) {
                // 如果内容宽度大于容器宽度，则开始滚动
                this.scrollInterval = setInterval(() => {
                if (target.scrollLeft < target.scrollWidth - target.clientWidth) {
                    target.scrollLeft++;
                } else {
                    target.scrollLeft = 0; // 重新开始滚动
                }
                }, 20);
            }
        },
        stopScroll() {
            clearInterval(this.scrollInterval); // 停止滚动
        },
        renderMarkdown(content) {
            if(content == null){
                return null;
            }
            return this.markdown.render(content);
        },
        async nextPage() {
            // 获取下一页数据
            const model_l = this.modelList;
            const page = this.currentPage + 1;
            this.saveAndGet(model_l, page);
        },
        async prevPage() {
            // 获取上一页数据
            const page = this.currentPage - 1;
            const model_l = this.modelList;
            this.saveAndGet(model_l, page);
        },
        async jump() {
            console.log("jump page",this.jumpPage);
            const model_l = this.modelList;
            this.saveAndGet(model_l, this.jumpPage,true);
        },
        scaleScore(standardScore) {
            let scale = null;
            if(this.ratingStandard == 3) {
                scale = d3.scaleOrdinal().domain([1,2,3]).range([0,0.5,1])
            } else {
                // else = 5
                scale = d3.scaleOrdinal().domain([1,2,3,4,5]).range([0,1,2,3,4])
            }
            return scale(standardScore);
        },
        reverseScaleScore(score) {
            let scale = null;
            if(this.ratingStandard == 3) {
                scale = d3.scaleOrdinal().domain([0,0.5,1]).range([1,2,3])
            } else {
                // else = 5
                scale = d3.scaleOrdinal().domain([0,0.25,0.5,0.75,1]).range([1,2,3,4,5])
            }
            return scale(score);
        },
        onRatingChange(score, index) {
            console.log('model list index', index)
            // 映射到相应的分数段
            if(this.ratingStandard == 3) 
            this.modelList[index].score = this.scaleScore(score);
            console.log("new score",this.modelList[index].score)
            // // this.modelList[index].score = this.scaleScore(value)

            // this.saveOneClick = false;
            // this.saveAllClick = false;
        },
        saveOnePage() {
            this.saveOneClick = true;
            //  save to databse
        },
        saveAllPage() {
            this.saveAllClick = true;
            // save all to database
        },
        saveAndGet(model_l,nextPage,isJump=false) {
            // 保存本页数据
            model_l.forEach(async model => {
                try {
                    const score = model.score;
                    console.log("sdcore", score)
                    const res = await api.saveById(this.currentPage,this.data_info_id, model.model_id,score);
                    console.log("save",res.data.message);
                    // 保存成功后 获取下一页数据
                    if(nextPage >= 1 && nextPage <= this.pageCount) {
                        this.$store.dispatch("updateCurrentPage", nextPage);
                        this.$store.dispatch("updateIsLoading", true);
                        try {
                            const response = await api.getPageById(nextPage);
                            console.log(" page info",response.data);
                            this.$store.dispatch("updateIsLoading", false);
                            this.$store.dispatch("updatePageInfo", response.data["page_info"])
                            if(isJump) {
                                this.jumpPage = null;
                            }
                        }
                        catch (error) {
                            console.error('Error getting page:', error)
                        }
                    }
                }
                catch (error) {
                    console.error('Error save this page:', nextPage, error)
                }
            })
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
    width: 450px;
    overflow: hidden;
}
.image-container  img {
    width: 98%;
    object-fit: contain;
}
.text-container {
    width: 98%;
    display: flex;
    flex-direction: row;
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 5px;
    padding-bottom: 5px;
    overflow: hidden;
    position: relative;
}
.text-border {
    border: 1px solid skyblue;
    border-radius: 5px;
    padding: 5px;
    margin-left: 20px;
    background-color: rgba(135,206,250,0.6);
    position: absolute;
    left: 75px;
}
.page-change {
    bottom: 0;
    padding: 15px 0 10px 5px;
    align-items: center;
    margin: auto;
    justify-content: center;
    position: fixed;
    width: 100%;
    height: 65px;
    margin-bottom: 8px;
}
.page-change p {
    margin-left:50px;
}
.tag-container {
    display: flex;
    flex-wrap: wrap; /* 允许元素在需要时换行 */
    left: 75px; /* 从左侧70px处开始显示标签 */
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
.rating {
    display: inline-flex;
}

.rating span {
    cursor: pointer;
    margin: 0 2px 0 2px;
    font-size: 20px;
    color: #9e9e9e;
    min-width: 24px;
    border: none;
    border-radius: 5px;
    background-color: rgb(255, 255, 255);
    justify-items: center;
    align-items: center;
    padding: 0 3px;
}

.rating span.active {
    color: #f44336;
    background-color: rgb(233, 243, 251);
    font-weight: bold;
    border: 1px solid #b4b4b4;
}

.image-path {
    white-space: nowrap;
    cursor: pointer;
    border: 1px solid #b9d4e6;
    background-color: rgba(135,206,250,0.6);
    border-radius: 5px;
    padding: 5px;
    margin-left: 20px;
    left: 70px;
    position: absolute;
}
.text-text {
    width: 75px;
    font-weight: bold;
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
::v-deep .p-datatable .p-datatable-thead > tr > th:nth-child(1) {
    width: 200px;
    word-wrap: break-word;
}
::v-deep .p-datatable .p-datatable-tbody > tr > td:nth-child(1) {
    width: 200px;
    word-wrap: break-word;
}

</style>
    