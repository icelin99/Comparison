<template>
<div>
    <div v-if="isShow" class="ct-container">
        <div>Category<MultiSelect :options="categories" v-model="selectedCategory"  optionValue="id" optionLabel="name" filter showClear @change="onCategoryChange(index)" :style="{ minWidth: '150px' }" /></div>
        <div>Tag <MultiSelect :options="tags" v-model="selectedTag"  optionValue="id" optionLabel="name" filter showClear @change="onTagChange(index)" :style="{ minWidth: '150px' }"  />
        </div>
        <div class="select-btn-container">
            <Button  icon="pi pi-times" class="p-button-clear custom-clear-button" @click="clearData" />
            <Button icon="pi pi-search" class="p-button-query custom-query-button" @click="queryData" />
        </div>
    </div>
    <div v-if="isShow" style="display: flex; flex-direction: row; width: 100%; max-height: calc(100% - 90px); overflow-y: auto; position:fixed; top: 95px; bottom:40px;">
        <div :style="{width: '40%', height: '100%'}">
            <div style="display: flex; flex-direction: column; width: '100%'; height: '100%'; align-items: center;">
                <div class="image-container" @dblclick="openModal('image', img_path)">
                    <img :src="img_path" alt="Can't find image">
                  </div>
                  <div v-if="isModalOpen" class="modal" @click="closeModal">
                    <span class="close"  @click="closeModal" >&times;</span>
                    <div class="modal-content" @click.stop>
                        <template v-if="modalType === 'image'">
                          <img :src="modalContent" alt="Image preview" class="img-preview"
                          @wheel="zoomImage" 
                          @mousedown="startDragging"
                          @mouseleave="stopDragging"
                            :style="imageStyle">
                        </template>
                        <template v-else>
                          <div>{{ modalContent }}</div>
                        </template>
                      </div>
                  </div>

                <div class="text-container"><div class="text-text">Category</div>
                    <div class="tag-container">
                        <div v-for="(item, index) in category" :key="index" class="tag-list">
                            <Tag severity="success" :style="{backgroundColor:colorScale(item),color:'#696969'}"> {{ item }}</Tag>
                        </div>
                    </div>
                </div>
                <div class="text-container"><div class="text-text">Tag</div>
                    <div class="tag-container">
                        <div v-for="(item, index) in tag" :key="index" class="tag-list">
                            <Tag severity="success" :style="{backgroundColor:colorScale(item),color:'#696969'}"> {{ item }}</Tag>
                        </div>
                    </div>
                </div>
                <div class="text-container"><div class="text-text">图片地址</div><div class="image-path" @dblclick="openModal('text', pageInfo[0].image_path)" >{{pageInfo[0].image_path}}</div></div>
                <div class="text-container"><div class="text-text">问题</div><div class="text-border" @dblclick="openModal('text', pageInfo[0].question)"> {{pageInfo[0].question}}</div></div>
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
    <div v-if="isShow&&!isModalOpen" class="page-change" style="display: flex; flex-direction: column; width: '100%';">
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
import {mapGetters, mapMutations} from "vuex"
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import Tag from 'primevue/tag'
import Rating from 'primevue/rating'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import api from '@/utils/api'
import MarkdownIt from 'markdown-it'
import MultiSelect from 'primevue/multiselect'



export default {
    name: 'App',
    components: {
        Button,
        InputNumber,
        Tag,
        Rating,
        DataTable,
        Column,
        MultiSelect
    },
    computed: {
        ...mapGetters(["selectSubmitted","currentData", "pageCount", "currentPage","ratingStandard", "pageInfo", "categoryList", "tagList"]),
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
        },
        categoryList(newVal) {
            this.selectedCategory = null;
            console.log("getting new category list", newVal);
            this.categories = newVal;
            console.log(this.categories)
        },
        tagList(newVal) {
            this.selectedTag = null;
            console.log("getting new tag list", newVal);
            this.tags = newVal;
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
            markdown: new MarkdownIt(),
            isModalOpen: false,
            modalType: 'text', // 'text' or 'image'
            modalContent: '', // Content to display in modal
            selectedCategory: null,
            selectedTag: null,
            categories: [],
            tags: [],
            zoomLevel: 1,
            isDragging: false,
            startX: 0,
            startY: 0,
            translateX: 0,
            translateY: 0,
            imageStyle: {
                transform: 'scale(1)  translate(0px, 0px)',
                cursor: 'grab'
            },
            pageEdit: []
        }
    },
    methods: {
        ...mapMutations(['nextItem','prevItem','setPage']),
        startScroll(event) {
            console.log("event",event.target);
            event.target.classList.add('scrollable');
        },
        stopScroll(event) {
            console.log("event",event.target);
            event.target.classList.remove('scrollable');
            // clearInterval(this.scrollInterval); // 停止滚动
        },
        startDrag(event) {
            this.isDragging = true;
            this.startX = event.pageX - event.target.offsetLeft;
            this.scrollLeft = event.target.scrollLeft;
            event.target.style.cursor = 'grabbing'; // 改变鼠标指针为抓取状态
        },
        stopDrag(event) {
            this.isDragging = false;
            event.target.style.cursor = 'grab'; // 恢复鼠标指针为抓手状态
        },
        drag(event) {
            if (!this.isDragging) return;
            event.preventDefault();
            const x = event.pageX - event.target.offsetLeft;
            const walk = x - this.startX; // 计算鼠标移动距离
            event.target.scrollLeft = this.scrollLeft - walk; // 滚动内容
        },
        openModal(type, content) {
            this.modalType = type;
            this.modalContent = content;
            this.isModalOpen = true;
            this.zoomLevel = 1;
            this.translateX = 0;
            this.translateY = 0;
            this.updateImageStyle();
        },
        closeModal() {
        this.isModalOpen = false;
        },
        renderMarkdown(content) {
            if(content == null){
                return null;
            }
            // 去掉字符串中的\n
            const sanitizedInput = content.replace(/\\n/g, '\n').replace(/^```markdown/, '').replace(/```$/, '');
            return this.markdown.render(sanitizedInput);
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
            this.modelList[index].score = this.scaleScore(score);
            console.log("new score",this.modelList[index].score)
            // 记录修改的索引
            if (!this.pageEdit.includes(index)) {
                this.pageEdit.push(index);
            }
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
        async saveAndGet(model_l,nextPage,isJump=false) {
            if(this.pageEdit && this.pageEdit.length && this.pageEdit.length > 0) {
                // 保存本页数据
                const modelList = this.pageEdit.map(index => ({
                    "modelID": model_l[index].model_id,
                    "score": model_l[index].score,
                    "standard": parseInt(localStorage.getItem("standard"),10)
                }))
                console.log("修改了的model list",modelList)
                try {
                    const res = await api.saveById(this.currentPage,this.data_info_id, modelList);
                    console.log("save",res.data.message);
                }
                catch (error) {
                    console.error('Error save this page:', nextPage, error)
                }
            }
            if(nextPage >= 1 && nextPage <= this.pageCount) {
                this.$store.dispatch("updateCurrentPage", nextPage);
                this.$store.dispatch("updateIsLoading", true);
                try {
                    let category_list = null;
                    if(this.selectedCategory) {
                        category_list = this.changeObject2List(this.selectedCategory);
                    }
                    let tag_list = null;
                    if(this.selectedTag) {
                        tag_list = this.changeObject2List(this.selectedTag);
                    }
                    const response = await api.getPageById(nextPage,parseInt(localStorage.getItem("datasetID"),10),JSON.parse(localStorage.getItem("modelIDs")),tag_list,category_list);
                    console.log(" page info",response.data);
                    this.$store.dispatch("updateIsLoading", false);
                    this.$store.dispatch("updatePageInfo", response.data["page_info"])
                    if(isJump) {
                        this.jumpPage = null;
                    }
                    this.pageEdit = [];
                }
                catch (error) {
                    console.error('Error getting page:', error)
                }
            }
            
        },
        async getTagList(datasetID, modelIds=[], catregoryIds=[]) {
            try {
                const response = await api.getTagList(datasetID, modelIds,catregoryIds);
                console.log("response",response.data);
                this.tags = response.data;
            }
            catch (error) {
                console.error('Error getting tag list:', error)
            }
        },
        async getCategoryList(datasetID, modelIds, tagIds = []) {
            try {
                const response = await api.getCategoryList(datasetID, modelIds,tagIds);
                console.log("response",response.data);
                this.categories = response.data;
            }
            catch (error) {
                console.error('Error getting category list:', error)
            }
        },
        onTagChange() {
            console.log("select tag:",this.changeObject2List(this.selectedTag));
            if(this.selectedTag) {
                
                const tag_list = this.changeObject2List(this.selectedTag);
                console.log("!!!!!!!!!!!!!!!! xuan ze le", tag_list)
                this.getCategoryList(parseInt(localStorage.getItem("datasetID"),10),JSON.parse(localStorage.getItem("modelIDs")), tag_list);
            } else {
                this.getCategoryList(parseInt(localStorage.getItem("datasetID"),10),JSON.parse(localStorage.getItem("modelIDs")))
            }
        },
        onCategoryChange() {
            console.log("select:",this.changeObject2List(this.selectedCategory));
            if(this.selectedCategory) {
                const category_list = this.changeObject2List(this.selectedCategory);
                this.getTagList(parseInt(localStorage.getItem("datasetID"),10),JSON.parse(localStorage.getItem("modelIDs")), category_list);
            } else {
                this.getTagList(parseInt(localStorage.getItem("datasetID"),10),JSON.parse(localStorage.getItem("modelIDs")));
            }
        },
        changeObject2List(object) {
            console.log(object, Object.values(object))
            return Object.values(object);
        },
        zoomImage(event) {
            const scaleAmount = 0.1;
            if (event.deltaY < 0) {
                this.zoomLevel += scaleAmount;
            } else {
                this.zoomLevel -= scaleAmount;
                if (this.zoomLevel < 1) {
                    this.zoomLevel = 1;
                }
            }
            this.updateImageStyle();
        },
        startDragging(event) {
            console.log("start dragging",this.zoomLevel)
            event.preventDefault();
            if (this.zoomLevel > 1) {
                this.isDragging = true;
                this.startX = event.clientX - this.translateX;
                this.startY = event.clientY - this.translateY;
                this.imageStyle.cursor = 'grabbing';
                window.addEventListener('mousemove', this.dragImage);
                window.addEventListener('mouseup', this.stopDragging);
            }
        },
        dragImage(event) {
            
            if (this.isDragging) {
                console.log("dragImage",event)
                this.translateX = event.clientX - this.startX;
                this.translateY = event.clientY - this.startY;
                this.updateImageStyle();
            }
        },
        stopDragging() {
            if (this.isDragging) {
                this.isDragging = false;
                this.imageStyle.cursor = 'grab';
            }
        },
        updateImageStyle() {
            this.imageStyle.transform = `scale(${this.zoomLevel}) translate(${this.translateX}px, ${this.translateY}px)`;
        },
        clearData() {
            this.selectedCategory = null;
            this.selectedTag = null;
            this.categories = this.categoryList;
            this.tags = this.tagList;
            this.queryData();
        },
        async queryData() {
            let category_list = null;
            if(this.selectedCategory) {
                category_list = this.changeObject2List(this.selectedCategory);
            }
            let tag_list = null;
            if(this.selectedTag) {
                tag_list = this.changeObject2List(this.selectedTag);
            }
            try {
                this.$store.dispatch('updateIsLoading', true);
                this.$store.dispatch("updateCurrentPage",1);
                const res = await api.getFilterList(parseInt(localStorage.getItem("datasetID"),10),JSON.parse(localStorage.getItem("modelIDs")),tag_list,category_list);
                console.log("query data",res.data);
                this.$store.dispatch("updatePageCount",res.data["page_count"]);
                this.$store.dispatch("updatePageInfo",res.data["page_info"]);
                this.$store.dispatch('updateIsLoading', false);
            }
            catch (error) {
                console.error('Error getting filter list and first page:', error)
            }
            
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
    cursor: pointer;
}
.image-container  img {
    width: 98%;
    object-fit: contain;
    transition: transform 0.3s ease;
}
.modal {
    display: flex;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.9);
    align-items: center;
    justify-content: center;
}
.close {
    position: absolute;
    top: 15px;
    right: 35px;
    color: #fff;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
}
.modal-content {
    margin: auto;
    display: block;
    max-width: 80%;
    max-height: 80%;
}
.text-container {
    width: 98%;
    display: flex;
    flex-direction: row;
    margin-top: 10px;
    padding: 5px 0;
    overflow: hidden;
    align-items: center;
   /* position: relative; */
}
.text-border {
    border: 1px solid skyblue;
    border-radius: 5px;
    padding: 5px;
    /*margin-left: 20px; */
    background-color: rgba(135,206,250,0.6);
   /* position: absolute; */
    /* left: 75px; */
    cursor: pointer;
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
    /*margin-left: 20px;
    left: 70px; */
    overflow: hidden;
}
.scrollable {
    animation: scrollText 5s linear infinite; /* 设置滚动动画 */
}
.modal {
    display: flex;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(198, 198, 198, 0.9);
    align-items: center;
    justify-content: center;
}
.close {
    position: absolute;
    top: 15px;
    right: 35px;
    color: #fff;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
} 
.modal-content img {
    margin: auto;
    display: block;
    max-width: 90vw; /* 最大宽度为视口宽度的90% */
    max-height: 90vh; /* 最大高度为视口高度的90% */
    object-fit: contain; /* 保持纵横比并适应容器 */
}
.modal-content {
    margin: auto;
    display: block;
    max-width: 80%;
    max-height: 80%;
    color: white; /* 如果是文本内容，则设置文本颜色为白色 */
    background-color: rgba(255, 255, 255, 0); /* 设置背景颜色为黑色 */
    padding: 20px; /* 为文本内容添加一些内边距 */
    font-size: 3rem;
  }
@keyframes scrollText {
    0% {
        transform: translateX(100%);
    }
    100% {
        transform: translateX(-100%);
    }
}
.text-text {
    min-width: 75px;
    font-weight: bold;
    height: 20px;
    line-height: 15px;
    text-align: start;
}
.ct-container {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #ddd;
    height: 50px;
    top:45px;
    position:fixed;
    width: 100%;
    padding-left: 300px;
    padding-right: 300px;
    font-family: 'Arial', sans-serif; 
    font-weight: bold;
    padding-top:5px;
}

.select-btn-container {
    display: flex;
    gap:1rem;
    align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  padding-bottom:7px;
}
.custom-clear-button {
    background-color: #fbd6d6; 
    border-color: #e9d6d6;
    color: rgb(84, 84, 84);
}
  
.custom-clear-button:hover {
    background-color: #fff3f3; 
}
  
.custom-query-button {
    background-color: #dceeff; 
    border-color: #edf6ff;
    color: rgb(84, 84, 84);
}
  
.custom-query-button:hover {
    background-color: #f1f8ff; 
}
</style>
<style scoped>

::v-deep .p-dropdown {
  height: 25px !important; /* Set your desired item height */
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
::v-deep .p-tag {
    font-size: 0.9rem;
}

</style>
    