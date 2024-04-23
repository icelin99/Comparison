<template>
<div>
    <div class="heading" v-if="alreadySubmit">
        <Button label="Clear selected items" severity="secondary" icon="pi pi-times" iconPos="left" @click="ClearStepper" />
    </div>
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
                <Dropdown :options="datasets" v-model="selectedDataset" placeholder="select a dataSet" filter showClear @change="onDatasetChange()" :disabled="index != active"  />
            </div>
        </template>
        <template #content="{ index, nextCallback }">
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right" style="margin-left:auto; background-color: cornflowerblue;" @click="NextCallback(index,nextCallback)" />
                <Button label="Submit" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: mediumaquamarine;border-color: aliceblue;"   @click="submitData" />
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
                <MultiSelect v-model="selectedModel" :options="models" placeholder="select a model" filter showClear @change="onModelChange(index)" :disabled="index != active" />
            </div>
        </template>
        <template #content="{ index, prevCallback, nextCallback }">
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Back" severity="secondary" icon="pi pi-arrow-left" style="margin-right:auto;" @click="PrevCallback(index, prevCallback)" />
                <Button label="Submit" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: mediumaquamarine;border-color: aliceblue;"   @click="submitData" />
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right"  style="margin-left:auto; background-color: cornflowerblue;" @click="NextCallback(index, nextCallback)" />
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
                <Dropdown :options="standards" v-model="selectedStandard" placeholder="select standard" filter showClear @change="onStandardChange(index)" :disabled="index != active"  />
            </div>
        </template>
        <template #content="{ index, prevCallback,nextCallback }">
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Back" severity="secondary" icon="pi pi-arrow-left" style="margin-right:auto; display: block;" @click="PrevCallback(index, prevCallback)" />
                <Button label="Submit" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: mediumaquamarine;border-color: aliceblue;"   @click="submitData" />
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right" style="margin-left:auto; background-color: cornflowerblue;"  @click="NextCallback(index, nextCallback)" />
            </div>
        </template>
    </StepperPanel>
    <StepperPanel>
        <template #header="{ index }">
            <div class="header-container">
                <!-- <button class="custom-button" @click="updateActive(index); clickCallback();"> -->
                <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                    4
                </span>
                <!-- </button> -->
                <div style="font-weight: bold; padding: 0.5em;">Category</div>
                <MultiSelect :options="categories" v-model="selectedCategory" placeholder="select category" filter showClear @change="onCategoryChange(index)" :disabled="index != active" />
            </div>
        </template>
        <template #content="{ index, prevCallback, nextCallback }" >
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Back" severity="secondary" icon="pi pi-arrow-left" style="margin-right:auto;" @click="PrevCallback(index, prevCallback)" />
                <Button label="Submit" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: mediumaquamarine;border-color: aliceblue;"   @click="submitData" />
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right" style="margin-left:auto; background-color: cornflowerblue;" @click="NextCallback(index, nextCallback)" />
            </div>
        </template>
    </StepperPanel>
    <StepperPanel>
        <template #header="{ index }">
            <div class="header-container">
                <!-- <button class="custom-button" @click="updateActive(index); clickCallback();"> -->
                <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                    5
                </span>
                <!-- </button> -->
                <div style="font-weight: bold; padding: 0.5em;">Tag</div>
                <MultiSelect :options="filteredTag" v-model="selectedTag" placeholder="select a tag" filter showClear @change="onTagChange(index)" :disabled="index != active" />
            </div>
        </template>
        <template #content="{ index, prevCallback, nextCallback }" >
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Back" severity="secondary" icon="pi pi-arrow-left" style="margin-right:auto;" @click="PrevCallback(index, prevCallback)" />
                <Button label="Submit" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: mediumaquamarine;border-color: aliceblue;"   @click="submitData" />
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right" style="margin-left:auto; background-color: cornflowerblue;" @click="NextCallback(index, nextCallback)" />
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

export default {
  name: 'App',
  components: {
    Stepper,
    StepperPanel,
    Button,
    Dropdown,
    MultiSelect
  },
  data() {
    return {
      active: 0,
      canSubmit: false,
      stepLength: 5,
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
      standards: ["3档","5档"],
      selectedStandard: null,
      questions: [],
      selectedQuestion: null,
      alreadySubmit: false,
      filteredData: null,
      filteredTag: null,
    };
  },
  mounted() {
    this.fetchData();
  },
  create() {
    
  },
  computed: {
    filteredQuestions() {
      return this.questions.filter(question => {
        const categoryMatch = this.selectedCategory ? question.category === this.selectedCategory : true;
        const tagMatch = this.selectedTag ? question.tag.includes(this.selectedTag) : true;
        return categoryMatch && tagMatch;
      });
    }
  },
  methods: {
    updateActive(index) {
        this.active = index;
        console.log("active", this.active);
        if(this.selectedDataset && this.selectedModel && this.selectedStandard) {
            this.canSubmit = true;
        }
    },
    NextCallback(index, nextCallback) {
        this.active = index +1;
        console.log("active", this.active);
        if(this.selectedDataset && this.selectedModel && this.selectedStandard) {
            this.canSubmit = true;
        }
        nextCallback();
    },
    PrevCallback(index, prevCallback) {
        this.active = index - 1;
        console.log("active", this.active);
        prevCallback();
    },
    submitData() {
        console.log("submit");
        this.canSubmit = false;
        // filter questions
        this.filterQuestionID();
        this.$store.dispatch("updateSelectSubmitted", true);
        this.alreadySubmit = true;
    },
    ClearStepper() {
        this.alreadySubmit = false;
        this.selectedDataset = null;
        this.selectedModel = null;
        this.selectedStandard = null;
        this.selectedCategory = null;
        this.selectedTag = null;
        this.active = 0;
        this.canSubmit = false;
        this.$store.dispatch("updateSelectSubmitted", false);
    },
    onDatasetChange() {
        if(this.selectedDataset && this.selectedModel && this.selectedStandard) {
            this.canSubmit = true;
        }
        console.log(typeof nextCallback)
    },
    onModelChange() {
      
        if(this.selectedDataset && this.selectedModel && this.selectedStandard) {
            this.canSubmit = true;
        }
        console.log("multi select",this.selectedModel);
    },
    onTagChange() {
        
        if(this.selectedDataset && this.selectedModel && this.selectedStandard) {
            this.canSubmit = true;
        }
        console.log(this.selectedTag);
    },
    onCategoryChange() {
        
        if(this.selectedDataset && this.selectedModel && this.selectedStandard) {
            this.canSubmit = true;
        }
        console.log(this.selectedCategory);
        this.filterTags();
    },
    onStandardChange() {
       
        if(this.selectedDataset && this.selectedModel && this.selectedStandard) {
            this.canSubmit = true;
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
        console.log("questions" , this.questions)
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
        console.log("tags and cate", this.tags, this.categories);
        this.filteredTag = this.tags;
    },
    filterQuestionID() {
        const id_list = this.taskInfo.filter(info => {
            return (!this.selectedCategory  || this.selectedCategory.length === 0 || this.selectedCategory.includes(info.category)) && (!this.selectedTag || this.selectedTag.length === 0 || info.tag.some(tt => this.selectedTag.includes(tt)));
        })
        // .map(info => {return info.question_id});
        console.log("filter id list",id_list);
        this.getFilterData(id_list);
    },
    filterTags() {
        if(!this.selectedCategory || this.selectedCategory.length === 0) {
            return this.tags;
        }
        let filtered = this.taskInfo.filter(info => this.selectedCategory.includes(info.category))
            .flatMap(info => info.tag);
        this.filteredTag = Array.from(new Set(filtered));
        console.log("original tags",this.tags);
        console.log("filter tag",this.filteredTag);
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
        console.log("filtered data",this.filteredData);
        this.$store.dispatch("updateFilterData",this.filteredData);
    }

  }
}
</script>

<style>
.heading {
    padding: 0 0 15px 0;
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
</style>
