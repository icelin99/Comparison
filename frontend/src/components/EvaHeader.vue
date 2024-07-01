<template>
    <div class="header">MLLM Evaluation - {{ dataset }}
        <Button icon="pi pi-spin pi-cog" @click="showSidebar = true" class="setting-btn" />
        <Sidebar v-model:visible="showSidebar" header="功能列表" position="right">
            <div class="sidebar-list">
                
                    <div  class="sidebar-item">
                        <Button @click="clearClick">清空所选项并跳转到主页面</Button></div>
                    <div  class="sidebar-item"><Button @click="fileShow = true">上传JSON文件</Button></div>
                    <div  class="sidebar-item">
                        <Button @click="goDelete" >删除相关信息</Button>
                    </div>
                    <div  class="sidebar-item"><Button @click="saveShow = true">查看打分结果</Button></div>
                    <div  class="sidebar-item">
                        <Button @click="seeAccuracy" >准确率表格</Button>
                    </div>
                    <div  class="sidebar-item">
                        <Button @click="goMarkdown" >Markdown 编译</Button>
                    </div>
                    <!-- <div  class="sidebar-item">
                        <Button @click="goMarkdownShow" >Markdown 编译显示</Button>
                    </div> -->

            </div>
        </Sidebar>
        <Dialog v-model:visible="fileShow" modal header="上传json文件" :style="{ width: '25rem' }">
           
            <span class="p-text-secondary block mb-5">请选择上传形式</span>
            <div class="mt-3 mb-3 flex align-items-center">
                <RadioButton v-model="uploadMethod" inputId="uploadFile" name="uploadMethod" value="file" :disabled="true" />
                <label for="ingredient1" class="ml-2">上传文件</label>
            </div>
            <div class="mt-3 mb-3 flex align-items-center">
                <RadioButton v-model="uploadMethod" inputId="uploadPath" name="uploadMethod" value="path" />
                <label for="ingredient2" class="ml-2">上传绝对地址</label>
            </div>
            <div v-if="uploadMethod === 'file'" class="mt-5 mb-5">
                <input type="file" name="file" accept=".json,.jsonl" @change="onFileUpload" />
                <p>文件大小请不要超过10M</p>
                <div class="mt-3 mb-3">
                    <RadioButton v-model="fileType" inputId="type4" name="fileType" value="result" />
                    <label for="ingredient1" class="ml-2">result</label>
                    <RadioButton v-model="fileType" inputId="type5" name="fileType" value="score" />
                    <label for="ingredient1" class="ml-2">score</label>
                </div>
              </div>
              <div v-else-if="uploadMethod === 'path'" class="mt-5 mb-5">
                <InputText v-model="filePath" :style="{width: '18rem'}" placeholder="请输入绝对地址" @blur="validatePath"/>
                <p v-if="pathType == 'dataset'">请输入dataset目录的绝对地址</p>
                <p v-if="pathType == 'result' || pathType == 'score'">请输入文件的绝对地址</p>
                <div class="mt-3 mb-3">
                    <RadioButton v-model="pathType" inputId="type1" name="pathType" value="dataset" />
                    <label for="ingredient1" class="ml-2">dataset</label>
                    <RadioButton v-model="pathType" inputId="type2" name="pathType" value="result" />
                    <label for="ingredient1" class="ml-2">model result</label>
                    <RadioButton v-model="pathType" inputId="type3" name="pathType" value="score" />
                    <label for="ingredient1" class="ml-2">model score</label>
                </div>
                <p v-if="!isPathValid" style="color: red;">请输入一个有效的绝对地址</p>
              </div>
              
              <div class="mt-4 flex justify-content-end">
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="fileShow = false" />
                <Button label="提交" icon="pi pi-check" class="p-button-text" @click="submitFile" />
              </div>
        </Dialog>
        <Dialog v-model:visible="saveShow" modal header="请选择需要下载的参数" :style="{ width: '50rem' }">
            <div class="p-fluid">
                <div>
                    <div style="font-weight: bold; padding: 0.5em;">Dataset</div>
                    <Dropdown :options="datasets" optionLabel="name" optionValue="id" v-model="selectedDataset" placeholder="select a dataSet" filter showClear @change="onDatasetChange()" />
                </div>
                <div>
                    <div style="font-weight: bold; padding: 0.5em;">Model</div>
                    <Dropdown v-model="selectedModel" :options="models" optionLabel="name" optionValue="id" placeholder="Select a model"  filter showClear @change="onModelChange()"/>
                </div>
                <div>
                    <div style="font-weight: bold; padding: 0.5em;">Standard</div>
                    <Dropdown v-model="selectedStandard" :options="standards" optionLabel="name" optionValue="name" placeholder="Select a model"  filter showClear @change="onStandardChange()"/>
                </div>
                <Button label="Submit" @click="fetchSaveData" />
            </div>
        </Dialog>
        <Dialog v-model:visible="showMarkdown" modal header="Markdown编辑器" :style="{ width: '80rem' }" >
            <MardownEditor />
        </Dialog>
        <Dialog v-model:visible="compileMarkdown" modal header="Markdown" :style="{ width: '60rem' }" >
            <CodeBlockRenderer/>
        </Dialog>
        <Dialog v-model:visible="showDelete" modal header="输入待删除的dataset名字或者result地址" :style="{ width: '30rem' }" >
            <InputText v-model="delete_dataset" :style="{width: '20rem'}"   />
            <p v-if="deleteType == 'dataset'">请输入dataset名字</p>
            <p v-if="deleteType == 'result'">请输入result的绝对地址</p>
            <div class="mt-3 mb-3">
                <RadioButton v-model="deleteType" inputId="type8" name="deleteType" value="dataset" />
                <label for="ingredient1" class="ml-2">dataset</label>
                <RadioButton v-model="deleteType" inputId="type9" name="deleteType" value="result" />
                <label for="ingredient1" class="ml-2">model result</label>
            </div>
            <div class="mt-4 flex justify-content-end">
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="fileShow = false" />
                <Button label="提交" icon="pi pi-check" class="p-button-text" @click="submitDelete" />
            </div>
        </Dialog>
        <Toast ref="toast" />
    </div>
</template>

<script>
import {mapGetters} from "vuex"
import Button from 'primevue/button';
import Sidebar from "primevue/sidebar";
import Dialog from "primevue/dialog";
import RadioButton from "primevue/radiobutton";
import FileUpload from "primevue/fileupload";
import InputText from "primevue/inputtext";
import api from '@/utils/api';
import Dropdown from "primevue/dropdown";
import Message from "primevue/message";
import Toast from "primevue/toast";
import MardownEditor from "./MardownEditor.vue";
import CodeBlockRenderer from "./CodeBlockRenderer.vue";

// import { download } from "@/utils/download";

export default {
    name: 'EvaHeader',
    components: {
        Button,
        Sidebar,
        Dialog,
        RadioButton,
        FileUpload,
        InputText,
        Dropdown,
        Message,
        Toast,
        MardownEditor,
        CodeBlockRenderer
    },
    computed: {
        ...mapGetters(["filterData","alreadySubmit","dataset"])
    },
    watch: {
    },
    mounted() {
        this.getDatasetList();
        this.getModelList();
        this.getStandardList();
    },
    data() {
        return {
            showSidebar: false,
            fileShow: false,
            uploadMethod: null,
            filePath: null,
            uploadedFile: null,
            pathType: null,
            fileType: null,
            saveShow: false,
            selectedDataset: null,
            selectedModel: null,
            selectedStandard: null,
            datasets: null,
            models: null,
            standards: null,
            isPathValid: true,
            messageVisible: false,
            messageSeverity: null,
            messageText: null,
            showMarkdown: false,
            compileMarkdown: false,
            showDelete:false,
            delete_dataset: "",
            deleteType: null,
        }
    },
    methods: {
        clearClick() {
            this.$store.dispatch("updateAlreadySubmit", false);
            console.log("click alrady submit state",this.alreadySubmit);
            this.showSidebar = false;
            this.$router.push({name: 'Home'})
        },
        onFileUpload(event) {
            console.log("ervent",event);
            this.uploadedFile = event.target.files[0];
        },
        async submitFile() {
            console.log("submit",this.uploadMethod,this.uploadedFile,this.filePath);
            if(this.uploadMethod == 'file')  {
                if(this.uploadedFile) {
                    if(this.fileType) {
                        try {
                            const res = await api.uploadFile(this.uploadedFile,this.fileType);
                            if(res.data.error){
                                alert("上传失败")
                            }else{
                                console.log('上传成功:', res.data);
                            }
                            this.fileShow = false;
                            this.uploadedFile = null;
                        }
                        catch(error) {
                            alert('上传失败:', error)
                        }
                    }
                    else {
                        alert('选择文件的类型！')
                    }
                } else {
                    alert('请选择一个文件');
                }
            } else {
                if(this.filePath) {
                    console.log('上传绝对地址:', this.filePath);
                    if(this.pathType) {
                        const res = await api.uploadFilePath(this.filePath,this.pathType);
                        console.log("res",res);
                        if(res.data["success"]) {
                            window.location.reload();
                            this.showToast('success','Success',res.data["success"])
                        } else if(res.data["error"]) {
                            this.showToast('error','Error', res.data["error"])
                        }
                        this.fileShow = false;
                        this.pathType = null;
                        this.filePath = null;
                    
                    } else {
                        alert('选择路径的类型！')
                    }
                }else {
                    alert('请填写文件路径');
                }
            }
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
                console.log("response",response.data);
                this.standards = response.data;
            }
            catch (error) {
                console.error('Error getting dtandard list:', error)
            }
        },
        onDatasetChange() {
            if(!this.selectedDataset) {
                this.models = [];
            } else {
                this.getModelList(this.selectedDataset);
            }
        },
        onModelChange() {
            console.log(this.selectedModel)
        },
        onStandardChange() {
            console.log(this.selectedStandard)
        },
        async fetchSaveData() {
            try {
                const res = await api.fetchSaveData(this.selectedDataset,this.selectedModel,this.selectedStandard);
                console.log("response",res.data,res.headers);
                if(res.data.error) {
                    alert(res.data.error)
                } else {
                    const { file_content, file_name } = res.data;
                    const type = 'application/json';

                    const blob = new Blob([file_content], { type });
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = file_name;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);

                    this.selectedDataset = null;
                    this.selectedModel = null;
                    this.selectedStandard = null;
                }
                
            }catch (error) {
                console.error('Error fetching save data:', error)
            }
        },
        validatePath() {
            const absolutePathPattern = /^(?:\/|(?:[a-zA-Z]:)?\\|\\\\)/;
            this.isPathValid = absolutePathPattern.test(this.filePath);
        },
        seeAccuracy() {
            this.showSidebar = false;
            this.$router.push({
                name:"AccuracyTable"
            })
        },
        showToast(severity,summary,detail){
            this.$refs.toast.add({ severity: severity, summary: summary, detail: detail, life: 2000 })
        },
        goMarkdown() {
            this.showMarkdown = true;
        },
        goMarkdownShow() {
            this.compileMarkdown = true;
        },
        goDelete() {
            this.showDelete = true;
        },
        async submitDelete() {
            if(this.deleteType){
                if(this.deleteType == "dataset") {
                    const res = await api.deleteDataset(this.delete_dataset);
                    console.log("res",res.data);
                    if(res.data["error"]) {
                        this.showToast('error','Error', res.data["error"])
                    }
                    if(res.data["success"]) {
                        window.location.reload();
                        this.showToast('success','Success', res.data["success"])
                    }
                } else if(this.deleteType == "result") {
                    const res = await api.deleteResult(this.delete_dataset);
                    console.log("res",res.data);
                    if(res.data["error"]) {
                        this.showToast('error','Error', res.data["error"])
                    }
                    if(res.data["success"]) {
                        window.location.reload();
                        this.showToast('success','Success', res.data["success"])
                    }
                }
            } else {
                alert("请选择要删除的类型！")
            }
            
        }
        

    }
}
</script>

<style scoped>
.header {
    background-color: aliceblue;
    border-bottom: 2px solid #d2e8ff;
    position: fixed;
    top: 0;
    width: 100%;
    height: 40px;
    text-align: left;
    justify-content: space-between;
    align-items: center;
    line-height: 40px;
    font-size: large;
    font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: bold;
    padding-right: 3px;
    display: flex;
}
.clear-button {
    font-weight: 200;
    font-size: medium;
    justify-content: center;
    align-items: center;
    display: flex;
    padding: 0 10px;
}
.small-button {
    font-size: 12px;
    padding: 2px 5px;
    width: 28px;
    height: 28px;
    margin-left:5px;
}
::v-deep .setting-btn {
    width: 4rem;
    background-color: #4a97ea;
    color:aliceblue;
}
.sidebar-list {
    padding: 5px 10px;
    justify-content: center;
    align-items: center;
}
.sidebar-item {
    padding: 2px 5px;
    width: 300px;
    align-items: flex-start;
}
::v-deep .p-button {
    background-color: #FFFFFF !important;
    border: none;
    color:#4a97ea;
    height: 35px;
}
::v-deep .p-button:hover {
    background-color: #F1F5F9 !important;
}
.mt-3 {
    margin-top: 1rem;
}
.mb-3 {
    margin-bottom: 1rem;
}
.mt-5 {
    margin-top: 1.5rem;
}
.mb-5 {
    margin-bottom: 1.5rem;
}
</style>
    