<template> 
  <div class="accuracy-container">
    <div class="ctn-container">
      <div class="select-container">
        <div>Dataset</div>
        <Dropdown :options="datasets" v-model="selectedDataset"  optionValue="id" optionLabel="name" filter showClear @change="onDatasetChange(index)" :style="{ width: '200px' }" />
    </div>
      <div class="select-container">
        <div>Model</div><MultiSelect :options="models" v-model="selectedModel"  optionValue="id" optionLabel="name" filter showClear @change="onModelChange(index)" :style="{ width: '250px' }"  />
      </div>
      <div class="select-container">
        <div>Standard</div><Dropdown :options="standards" v-model="selecteStandard"  optionValue="name" optionLabel="name" filter showClear @change="onStandardChange(index)" :style="{ width: '100px' }" /></div>
      <div class="select-container select-btn-container">
          <Button  icon="pi pi-times" class="p-button-clear custom-clear-button" @click="clearData" />
          <Button icon="pi pi-search" class="p-button-query custom-query-button" @click="queryData" />
      </div>
    </div>
    <div class="accuracy-table" >
      
      <table class="custom-table">
        <thead>
          <tr>
            <th class="dataset-header">Dataset Name</th>
            <th class="fixed-header">Category</th>
            <th class="fixed-header">Tag</th>
            <th class="fixed-header">Count</th>
            <th class="model-header" v-for="model in modelNames" :key="model">{{ model }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in tableData" :key="rowIndex" :class="getRowClass(rowIndex)">
            <td v-if="isFirstRowspan('dataset', rowIndex)" :rowspan="computeRowspan('dataset', rowIndex)">{{ row.dataset }}</td>
            <td v-if="isFirstRowspan('category', rowIndex)" :rowspan="computeRowspan('category', rowIndex)">{{ row.category }}</td>
            <td>{{ row.tag }}</td>
            <td>{{ row.count }}</td>
            <td v-for="model in modelNames" :key="model">{{ row[model] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <Toast ref="toast" />
  </div>

   
</template>
  
<script>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import MultiSelect from 'primevue/multiselect'
import Dropdown from 'primevue/dropdown';
import api from '@/utils/api';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
  
export default {
    components: {
        DataTable,
        Column,
        MultiSelect,
        Dropdown,
        Button,
        Toast
    },
    data() {
        return {
        // jsonData: 
        // {'common_ability': {'ocr': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '41.67%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '41.67%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '66.67%'}],'Test': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '41.67%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '41.67%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '66.67%'}]}, '长图理解': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '66.67%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '83.33%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '83.33%'}]}, 'UI理解': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '0.00%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '25.00%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '41.67%'}]}, '推理能力': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '28.57%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '50.00%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '28.57%'}]}, '指令跟随能力': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '58.33%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '66.67%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '66.67%'}]}, '翻译': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '30.00%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '0.00%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '35.00%'}]}, '表格提取': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '0.00%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '0.00%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '0.00%'}]}, '幽默理解': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '0.00%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '0.00%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '0.00%'}]}, 'region caption': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': 'None'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': 'None'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': 'None'}]}, 'grounding': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': 'None'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': 'None'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': 'None'}]}, '数数': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '16.67%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '33.33%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '16.67%'}]}, '文案诗歌': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '90.00%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '100.00%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '80.00%'}]}, 'Zero-shot能力': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': '50.00%'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': '33.33%'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': '66.67%'}]}, '复杂图表': {'None': [{'model_id': 1, 'model_name': 'd240319_common_ability_vit1b_internlm2chat20b', 'accuracy': 'None'}, {'model_id': 2, 'model_name': 'd240415_common_ability_vit1b_internlm2chat20b', 'accuracy': 'None'}, {'model_id': 3, 'model_name': 'd240424_common_ability', 'accuracy': 'None'}]}}},
        jsonData: {'Drive_AGI_testset_0625': {'万物感知': {'动物': {'count': 30, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '80.00%'}]}, '建筑识别': {'count': 12, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '41.67%'}]}, '品牌': {'count': 20, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '75.00%'}]}, '车型': {'count': 19, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '63.16%'}]}, '植物': {'count': 30, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '43.33%'}]}, '二维码': {'count': 30, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '0.00%'}]}, '交通标识': {'count': 34, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '36.76%'}]}}, '车辆感知': {'品牌': {'count': 9, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '55.56%'}]}, '车型': {'count': 11, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '54.55%'}]}, 'color': {'count': 20, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '30.00%'}]}, 'lane': {'count': 18, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '61.11%'}]}, 'orientation': {'count': 20, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '42.11%'}]}, '价格询问': {'count': 28, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '71.43%'}]}}, '全局感知': {'模糊描述': {'count': 20, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '65.00%'}]}, 'poem': {'count': 11, 'models': [{'model_id': 122, 'model_name': 'gpt4o_Drive_AGI_testset_0625', 'accuracy': 'None'}, {'model_id': 128, 'model_name': '0522v2car_Drive_AGI_testset_0625', 'accuracy': '35.00%'}]}}}},
        tableData: [],
        modelNames: [],
        rowspans: {
            dataset: [],
            category: []
        },
        selectedDataset: null,
        datasets: null,
        selectedModel: null,
        models: null,
        selecteStandard: null,
        standards: null,
        };
    },
    created() {
        this.processData();
    },
    mounted() {
      this.getDatasetList();
      this.getModelList();
      this.getStandardList();
    },
    methods: {
        processData() {
          const data = this.jsonData;
          const result = [];
          const modelNamesSet = new Set();
          const rowspans = {
            dataset: [],
            category: []
          };

          for (const dataset in data) {
            let datasetRowspan = 0;
            for (const category in data[dataset]) {
              let categoryRowspan = 0;
              console.log("111",data[dataset][category]);
              for (const tag in data[dataset][category]) {
                const entry = {
                  dataset: dataset,
                  category: category,
                  tag: tag,
                  count: data[dataset][category][tag]["count"]
                };
                console.log("0000",tag,data[dataset][category]);
                const models = data[dataset][category][tag]["models"];
                models.forEach(model => {
                  entry[model.model_name] = model.accuracy;
                  modelNamesSet.add(model.model_name);
                });
                console.log("entry",entry)
                result.push(entry);
                categoryRowspan++;
              }
              rowspans.category.push(categoryRowspan);
              datasetRowspan += categoryRowspan;
            }
            rowspans.dataset.push(datasetRowspan);
          }

          this.tableData = result;
          this.modelNames = Array.from(modelNamesSet);
          this.rowspans = rowspans;
          console.log(rowspans);
          console.log(result);
        },
        isFirstRowspan(field, rowIndex) {
          if (rowIndex === 0) return true;
          return this.tableData[rowIndex][field] !== this.tableData[rowIndex - 1][field];
        },
        computeRowspan(field, rowIndex) {
          let count = 1;
          for (let i = rowIndex + 1; i < this.tableData.length; i++) {
            if (this.tableData[rowIndex][field] === this.tableData[i][field]) {
              count++;
            } else {
              break;
            }
          }
          return count;
        },
        getRowClass(rowIndex) {
          return rowIndex % 2 === 0 ? 'even-row': 'odd-row';
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
        onDatasetChange() {
          console.log(this.selectedDataset)
            if(!this.selectedDataset) {
                this.models = [];
            } else {
                this.getModelList(this.selectedDataset);
            }
            this.selectedModel = null;
        },
        onModelChange() {
          console.log(this.selectedModel)
        },
        onStandardChange() {
          // '3', '5','10'
            console.log(this.selecteStandard); 
        },
        clearData() {
          this.selecteStandard = null;
          this.selectedDataset = null;
          this.selectedModel = null;
        },
        async queryData() {
          console.log(parseInt(this.selectedDataset),JSON.parse(JSON.stringify(this.selectedModel)),parseInt(this.selecteStandard));
          if(this.selectedDataset && this.selectedModel && this.selecteStandard) {
            try {
              this.$store.dispatch('updateIsLoading', true);
              const res = await api.getAccuracy(parseInt(this.selectedDataset),JSON.parse(JSON.stringify(this.selectedModel)),parseInt(this.selecteStandard));
              console.log("query data",res.data);
              this.jsonData = res.data;
              this.processData();
              console.log("process data finished");
              this.$store.dispatch('updateIsLoading', false);
            }
            catch(e) {
              console.log(e)
            }
          }
          else {
            this.showToast('error','Error', "请选择所有项")
          }
        },
        showToast(severity,summary,detail){
            this.$refs.toast.add({ severity: severity, summary: summary, detail: detail, life: 2000 })
        },
    }
};
</script>

<style scoped>
.accuracy-container {
  display: flex;
  flex-direction: column;
  top: 45px;
  position: fixed;
  width: 100%;
}
.accuracy-table {
   /* top: 90px; 
    position: fixed; */
    flex: 1;
    bottom: 0; 
    width: 100%; 
    overflow-y: auto;
    max-height: calc(100% -45px);
}
.ctn-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  height: 50px;
 /* top:45px;
  position:fixed; */
  width: 100%;
  margin: auto;
  padding-left: 100px;
  padding-right: 100px;
  font-family: 'Arial', sans-serif; 
  font-weight: bold;
  z-index: 1;
}
.select-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 0 10px;
}
.custom-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.custom-table th,
.custom-table td {
  border: 1px solid #ddd;
  padding: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.custom-table th.fixed-header {
  background-color: rgb(238, 243, 248);
  text-align: center;
  width: 50px;
  white-space: normal; 
  word-wrap: break-word;
}
.custom-table th.dataset-header {
  background-color: rgb(238, 243, 248);
  text-align: center;
  width: 80px;
}
.custom-table th.model-header{
  background-color: rgb(238, 243, 248);
  text-align: center;
  width: 100px;
  white-space: normal; 
  word-wrap: break-word;

}

.custom-table td {
  white-space: nowrap;
}

.even-row {
  background-color: rgb(251, 253, 255);
}

.odd-row {
  background-color: #ffffff;
}

</style>
