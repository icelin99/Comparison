<template>
<div>

<Stepper v-if="!alreadySubmit">
    <StepperPanel >
        <template #header="{ index }">
            <div class="header-container">
                <!-- <button class="custom-button" @click="updateActive(index); clickCallback();"> -->
                <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                    1
                </span>
                <!-- </button> -->
                <div style="font-weight: bold; padding: 0.5em;">Datasets</div>
                <Dropdown :options="datasets" optionLabel="name" optionValue="id" v-model="selectedDataset" placeholder="select a dataSet" filter showClear @change="onDatasetChange()" :disabled="index != active"  />
            </div>
        </template>
        <template #content="{ index, nextCallback }">
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Submit" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: mediumaquamarine;border-color: aliceblue;"  @click="submitData" />
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right" :style="{marginLeft:'auto', backgroundColor: hover? 'rgba(100,150,237,0.5)':'#6495ed', color:hover?'#46566d': '#ffffff'}" @click="NextCallback(index,nextCallback)" @mouseover="hover = true" @mouseleave="hover = false" />
                
            </div>
        </template>
    </StepperPanel>
    <StepperPanel >
        <template #header="{ index }">
            <div class="header-container">
                <!-- <button class="custom-button" @click="updateActive(index); clickCallback();"> -->
                <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                    2
                </span>
                <!-- </button> -->
                <div style="font-weight: bold; padding: 0.5em;">Model</div>
                <MultiSelect v-model="selectedModel" :options="models" optionValue="id" optionLabel="name" placeholder="select a model" filter showClear @change="onModelChange(index)" :disabled="index != active" :style="{ maxWidth: '220px' }" />
            </div>
        </template>
        <template #content="{ index, prevCallback, nextCallback }">
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Back" severity="secondary" icon="pi pi-arrow-left" style="margin-right:auto;" @click="PrevCallback(index, prevCallback)" />
                <Button label="Submit" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: mediumaquamarine;border-color: aliceblue;"    @click="submitData" />
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right"  :style="{marginLeft:'auto', backgroundColor: hover? 'rgba(100,150,237,0.5)':'#6495ed', color:hover?'#46566d': '#ffffff'}" @click="NextCallback(index, nextCallback)"  @mouseover="hover = true" @mouseleave="hover = false" />
            </div>
        </template>
    </StepperPanel>
    <StepperPanel >
        <template #header="{ index }">
            <div class="header-container">
                <!-- <button class="custom-button" @click="updateActive(index); clickCallback();"> -->
                <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                    3
                </span>
                <!-- </button> -->
                <div style="font-weight: bold; padding: 0.5em;">Standard</div>
                <Dropdown :options="standards" v-model="selectedStandard"  optionValue="id" optionLabel="name" placeholder="select standard" filter showClear @change="onStandardChange(index)" :disabled="index != active"  />
            </div>
        </template>
        <template #content="{ index, prevCallback }">
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Back" severity="secondary" icon="pi pi-arrow-left" style="margin-right:auto; display: block;" @click="PrevCallback(index, prevCallback)" />
                <Button label="Submit" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: mediumaquamarine;border-color: aliceblue;"   @click="submitData" />
                <!-- <Button label="Next" :disabled="!canSubmit" icon="pi pi-arrow-right" iconPos="right" :style="{marginLeft:'auto', backgroundColor: hover? 'rgba(100,150,237,0.5)':'#6495ed', color:hover?'#46566d': '#ffffff'}"  @click="NextCallback(index, nextCallback)"  @mouseover="hover = true" @mouseleave="hover = false" /> -->
            </div>
        </template>
    </StepperPanel>
   
</Stepper>
</div>
</template>

<script>

import Stepper from 'primevue/stepper';
import StepperPanel from 'primevue/stepperpanel';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import cls_info from '../../public/assets/cls_info.json';
import MultiSelect from 'primevue/multiselect';
import Menubar from 'primevue/menubar';
import api from '@/utils/api';
import {mapGetters} from "vuex"

export default {
  name: 'App',
  components: {
    Stepper,
    StepperPanel,
    Button,
    Dropdown,
    MultiSelect,
    Menubar
  },
  data() {
    return {
      active: 0,
      canSubmit: false,
      stepLength: 3,
      dataJson:  [],
      taskInfo: [],
      tags: [],
      selectedTag: null,
      categories: [],
      selectedCategory: null,
      datasets: ["domain_dataset"],
      selectedDataset: null,
      models: ["wenwen_1_20b","model2","model3"],
      selectedModel: null,
      standards: ["3档","5档", "10档"],
      selectedStandard: null,
      questions: [],
      selectedQuestion: null,
      filteredData: null,
      filteredTag: null,
      hover: false,
      canCategoryNext: false,
      
    };
  },
  mounted() {
    localStorage.removeItem("categoryIDs");
    localStorage.removeItem("dataset");
    this.$store.dispatch('updateIsLoading', false); // 挂载完成，隐藏loading
    // this.fetchData();
    this.getDatasetList();
    this.getModelList();
    this.getStandardList();
  },
  create() {
    
  },
  computed: {
    ...mapGetters(["filterData","alreadySubmit"])
  },
  watch: {
        alreadySubmit(newVal) {
            if(newVal == false) {
                this.ClearStepper();
            }
        }
    },
  methods: {
    updateActive(index) {
        this.active = index;
        this.canSubmit = this.checkCanSubmit();
    },
    NextCallback(index, nextCallback) {
        this.active = index +1;
        this.canSubmit = this.checkCanSubmit();
        nextCallback();
    },
    PrevCallback(index, prevCallback) {
        this.active = index - 1;
        prevCallback();
    },
    async submitData() {
        console.log("submit");
        this.canSubmit = false;
        // 存储数据到 local storage
        const dataset_ = this.datasets.find(item => item.id==this.selectedDataset)
        this.$store.dispatch("updateDataset",dataset_.name)
        localStorage.setItem("dataset",dataset_.name);
        localStorage.setItem("datasetID", this.selectedDataset.toString())
        localStorage.setItem("modelIDs", JSON.stringify(this.changeObject2List(this.selectedModel)))
        // get category and tag
        try {
            const category = await api.getCategoryList(this.selectedDataset,this.changeObject2List(this.selectedModel))
            this.$store.dispatch("updateCategoryList", category.data);
        }catch (error) {
            console.error('Error getting category list:', error)
        }
        try {
            const tag = await api.getTagList(this.selectedDataset,this.changeObject2List(this.selectedModel))
            this.$store.dispatch("updateTagList", tag.data);
        }catch (error) {
            console.error('Error getting tag list:', error)
        }
        
        try {
            this.$store.dispatch('updateIsLoading', true);
            this.$store.dispatch("updateCurrentPage",1)
            const response = await api.getFilterList(parseInt(localStorage.getItem("datasetID"),10), JSON.parse(localStorage.getItem("modelIDs")));
            console.log("get li list and first page",response.data);
            this.$store.dispatch("updatePageCount",response.data["page_count"]);
            this.$store.dispatch("updatePageInfo",JSON.parse(JSON.stringify(response.data["page_info"])));
            this.$store.dispatch("updateSelectSubmitted", true);
            this.$store.dispatch("updateAlreadySubmit", true);
            this.$store.dispatch('updateIsLoading', false);
        }
        catch (error) {
            console.error('Error getting id list and first page error:', error)
        }
        
    },
    ClearStepper() {
        this.selectedDataset = null;
        this.selectedModel = null;
        this.selectedStandard = null;
        this.selectedCategory = null;
        this.selectedTag = null;
        localStorage.removeItem("datasetID");
        localStorage.removeItem("dataset");
        localStorage.removeItem("modelIDs");
        localStorage.removeItem("standard");
        localStorage.removeItem("tagIDs");
        localStorage.removeItem("categoryIDs");
        this.active = 0;
        this.canSubmit = false;
        this.$store.dispatch("updateSelectSubmitted", false);
        this.$store.dispatch("updateCurrentPage",1)
    },
    onDatasetChange() {
        if(!this.selectedDataset) {
            this.models = [];
            this.tags = [];
            this.categories = [];
            this.canSubmit = this.checkCanSubmit();
        } else {
            this.getModelList(this.selectedDataset);
            this.canSubmit = this.checkCanSubmit();
        }
    },
    onModelChange() {
        this.canSubmit = this.checkCanSubmit();
        if(!this.selectedModel) {
            this.tags = null;
            this.categories = null;
        }
    },
    onStandardChange() {
        this.canSubmit = this.checkCanSubmit();
        //默认3档和5档，name值只有3和5
        const item = this.standards.find(item => item.id == this.selectedStandard);
        const name = item? item.name: undefined;
        console.log("select standard",name);
        if(String(name) == "3") {
            this.$store.dispatch("updateRatingStandard",3);
        } else if(String(name) == "5") {
            this.$store.dispatch("updateRatingStandard",5);
        } else {
            this.$store.dispatch("updateRatingStandard",10);
        }
        
    },

    async fetchData() {
        const response = await fetch('./assets/domain-standard1-0319_wenwen_1+20b.json')
        const text = await response.text();
        const lines = text.split('\n');
        this.dataJson = lines.filter(line => line.trim()).map(line => JSON.parse(line));
        this.filteredData = this.dataJson;
        // console.log("josn", this.dataJson);
        this.getQuestionsList(this.dataJson);
        
        this.taskInfo = cls_info[0].task_info;
        // console.log("cls info",this.taskInfo);
        this.initTagAndCategory();

    },
    getQuestionsList(data) {
        data.forEach((da,index) => {
            this.questions.push({"index":index,"question":da.question});
        })
    },
    initTagAndCategory() {
        const tagSet = new Set();
        const categorySet = new Set();

        this.taskInfo.forEach(info => {
            categorySet.add(info.category);
            info.tag.forEach(tag => tagSet.add(tag))
        });
        this.categories = Array.from(categorySet);
        this.tags = Array.from(tagSet);
        this.filteredTag = this.tags;
    },
    filterQuestionID() {
        const id_list = this.taskInfo.filter(info => {
            return (!this.selectedCategory  || this.selectedCategory.length === 0 || this.selectedCategory.includes(info.category)) && (!this.selectedTag || this.selectedTag.length === 0 || info.tag.some(tt => this.selectedTag.includes(tt)));
        })
        // .map(info => {return info.question_id});
        this.getFilterData(id_list);
    },
    filterTags() {
        if(!this.selectedCategory || this.selectedCategory.length === 0) {
            return this.tags;
        }
        let filtered = this.taskInfo.filter(info => this.selectedCategory.includes(info.category))
            .flatMap(info => info.tag);
        this.filteredTag = Array.from(new Set(filtered));
    },
    getFilterData(id_list) {
        // get filter data by question id
        this.filteredData = this.dataJson.filter((item,index) => {
            const info = id_list.find(item_ => item_.question_id == index);
            if(info) {
                item.tag = info.tag;
                return true;
            }
            return false;
        });
        this.$store.dispatch("updateFilterData",this.filteredData);
    },

    async getDatasetList() {
        try {
            const response = await api.getDatasetList();
            console.log("response",response.data);
            this.datasets = response.data;
        }
        catch (error) {
            console.error('Error getting dataset list:', error)
        }
    },
    async getModelList(datasetId = null) {
        try {
            const response = await api.getModelList(datasetId);
            console.log("response model",response.data);
            this.models = response.data;
            this.canSubmit = this.checkCanSubmit();
        }
        catch (error) {
            console.error('Error getting model list:', error)
        }
    },
    async getStandardList() {
        try {
            const response = await api.getStandardList();
            console.log("response standard",response.data);
            this.standards = response.data;
        }
        catch (error) {
            console.error('Error getting dtandard list:', error)
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
    async getCategoryList(datasetID, modelIds) {
        try {
            const response = await api.getCategoryList(datasetID, modelIds);
            console.log("response",response.data);
            this.categories = response.data;
        }
        catch (error) {
            console.error('Error getting category list:', error)
        }
    },
    changeObject2List(object) {
        console.log(object, Object.values(object))
        return Object.values(object);
    },
    checkCanSubmit() {
        if(this.models.length > 0) {
            if(this.selectedDataset && this.selectedModel && this.selectedStandard) {
                return true;
            }
        }else {
            if(this.selectedDataset && this.selectedStandard) {
                return true;
            }
        }
        return false;
    }

  }
}
</script>

<style>
.heading {
    padding: 0 0 45px 0;
}
.header-container {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center align items vertically in the container */
}

.custom-button {
  background: transparent;
  border: none;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.step-indicator {
  border-radius: 50%; /* Makes the border rounded */
  border: 2px solid;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgb(241, 248, 250);
}

.active {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.inactive {
  border-color: var(--surface-border-color);
}

/* Define custom CSS variables for colors */
:root {
  --primary-color: #4a97ea; /* Blue, example */
  --surface-border-color: #ccc; /* Grey, example */
}
</style>

<style scoped>
.stepper-line {
  transform: translateY(10px);
}
::v-deep .p-stepper-header {
    align-items: flex-start !important;
}
::v-deep .p-stepper-separator {
    margin-top: 20px;
    height: 3px !important;
}
::v-deep .p-button  {
    transition: background-color 0.3s !important; 
}
::v-deep .p-button .p-button-label {
  font-family: 'Arial', sans-serif; 
  /* font-size: 16px; */
  font-weight: bold;
}
::v-deep .p-button .pi {
  font-weight: bold;
}
::v-deeep .p-button:hover {
    background-color: #f1f5f9 !important;
}
</style>
