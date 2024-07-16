<template>
    <div>
    <Stepper v-if="!selectSubmitted">
        <StepperPanel >
            <template #header="{ index }">
                <div class="header-container">
                    <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                        1
                    </span>
                    <!-- </button> -->
                    <div style="font-weight: bold; padding: 0.5em;">Datasets</div>
                    <Dropdown :options="datasets" optionLabel="name" optionValue="id" v-model="selectedDataset" placeholder="select a dataSet" filter showClear @change="onDatasetChange()"  />
                </div>
            </template>
        </StepperPanel>
        <StepperPanel >
            <template #header="{ index }">
                <div class="header-container">
                    <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                        2
                    </span>
                    <!-- </button> -->
                    <div style="font-weight: bold; padding: 0.5em;">Model</div>
                    <MultiSelect v-model="selectedModel" :options="models" optionValue="id" optionLabel="name" placeholder="select a model" filter showClear @change="onModelChange(index)" :style="{ maxWidth: '220px' }" />
                </div>
            </template>
        </StepperPanel>
        <StepperPanel >
            <template #header="{ index }">
                <div class="header-container">
                    <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                        3
                    </span>
                    <!-- </button> -->
                    <div style="font-weight: bold; padding: 0.5em;">Standard</div>
                    <Dropdown :options="standards" v-model="selectedStandard"  optionValue="id" optionLabel="name" placeholder="select standard" filter showClear @change="onStandardChange(index)"   />
                </div>
            </template>
        </StepperPanel>
    </Stepper>
    <Button label="Submit" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: mediumaquamarine;border-color: aliceblue;"   @click="submitData" />
    <Button label="Submit2Voice" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: mediumaquamarine;border-color: aliceblue;"   @click="submitData2" />
    </div>
    </template>
    
    <script>
    
    import Stepper from 'primevue/stepper';
    import StepperPanel from 'primevue/stepperpanel';
    import Button from 'primevue/button';
    import Dropdown from 'primevue/dropdown';
    import cls_info from '../../public/assets/cls_info.json';
    import MultiSelect from 'primevue/multiselect';
    import api from '@/utils/api';
    import {mapGetters} from "vuex"
    
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
          dataJson:  [],
          taskInfo: [],
          datasets: ["domain_dataset"],
          selectedDataset: null,
          models: ["wenwen_1_20b","model2","model3"],
          selectedModel: null,
          standards: ["3档","5档", "10档"],
          selectedStandard: null,
          
        };
      },
      mounted() {
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
        ...mapGetters(["selectSubmitted"])
      },
      watch: {
            selectSubmitted(newVal) {
                if(newVal == false) {
                    this.ClearStepper();
                }
            }
        },
      methods: {
        async submitData() {
            console.log("submit");
            this.canSubmit = false;
            // 存储数据到 local storage
            const dataset_ = this.datasets.find(item => item.id==this.selectedDataset)
            this.$store.dispatch("updateDatasetName",dataset_.name)
            localStorage.setItem("dataset",dataset_.name);
            localStorage.setItem("datasetID", this.selectedDataset.toString())
            localStorage.setItem("modelIDs", JSON.stringify(this.changeObject2List(this.selectedModel)))
            
            try {
                this.$store.dispatch('updateIsLoading', true);
                this.$store.dispatch("updateCurrentPage",1)
                const response = await api.getFilterList(parseInt(localStorage.getItem("datasetID"),10), JSON.parse(localStorage.getItem("modelIDs")));
                console.log("get li list and first page",response.data);
                this.$store.dispatch("updatePageCount",response.data["page_count"]);
                this.$store.dispatch("updatePageInfo",JSON.parse(JSON.stringify(response.data["page_info"])));
                this.$store.dispatch("updateSelectSubmitted", true);
                this.$store.dispatch('updateIsLoading', false);
                this.$store.dispatch('updateDataInfoList',response.data["data_info_list"]);
            }
            catch (error) {
                console.error('Error getting id list and first page error:', error)
            }
            
        },
        ClearStepper() {
            this.selectedDataset = null;
            this.selectedModel = null;
            this.selectedStandard = null;
            localStorage.removeItem("datasetID");
            localStorage.removeItem("dataset");
            localStorage.removeItem("modelIDs");
            localStorage.removeItem("standard");
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
            } else {
                this.getModelList(this.selectedDataset);
                this.canSubmit = this.checkCanSubmit()
            }
        },
        onModelChange() {
            this.canSubmit = this.checkCanSubmit()
            console.log("select model",this.selectedModel,this.canSubmit,this.selectedModel.length);
        },
        onStandardChange() {
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
            this.canSubmit = this.checkCanSubmit()
            
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
        changeObject2List(object) {
            console.log(object, Object.values(object))
            return Object.values(object);
        },
        checkCanSubmit() {
            if(this.selectedDataset && this.selectedModel!= null && this.selectedModel.length>0 && this.selectedStandard) {
                return true;
            }
            return false;
        },

    async submitData2() {
        this.canSubmit = false;
        // 存储数据到 local storage
        const dataset_ = this.datasets.find(item => item.id==this.selectedDataset)
        this.$store.dispatch("updateDatasetName",dataset_.name)
        localStorage.setItem("dataset",dataset_.name);
        localStorage.setItem("datasetID", this.selectedDataset.toString())
        localStorage.setItem("modelIDs", JSON.stringify(this.changeObject2List(this.selectedModel)))
        // get category and tag
        try {
            this.$store.dispatch('updateIsLoading', true);
            this.$store.dispatch("updateCurrentPage",1)
            const response = await api.getFilterList(parseInt(localStorage.getItem("datasetID"),10), JSON.parse(localStorage.getItem("modelIDs")));
            console.log("get li list and first page",response.data);
            this.$store.dispatch("updatePageCount",response.data["page_count"]);
            this.$store.dispatch("updatePageInfo",JSON.parse(JSON.stringify(response.data["page_info"])));
            this.$store.dispatch("updateSelectSubmitted", true);
            this.$store.dispatch('updateDataInfoList',response.data["data_info_list"]);
            this.$store.dispatch('updateIsLoading', false);
            this.$router.push({name:'ImageVoice'});
        }
        catch (error) {
            console.error('Error getting id list and first page error:', error)
        }
        
    },
    
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
    