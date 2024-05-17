<template>
    <div class="header">MLLM Evaluation - {{ dataset }}
        <Button icon="pi pi-spin pi-cog" @click="showSidebar = true" class="setting-btn" />
        <Sidebar v-model:visible="showSidebar" header="功能列表" position="right">
            <div class="sidebar-list">
                
                    <div  class="sidebar-item">
                        <Button @click="clearClick">清空所选项</Button></div>
                    <div  class="sidebar-item"><Button @click="fileShow = true">上传JSON文件</Button></div>
                    <div  class="sidebar-item"><Button >存取数据</Button></div>
                    <div  class="sidebar-item"><Button >准确率表格</Button></div>

            </div>
        </Sidebar>
        <Dialog v-model:visible="fileShow" modal header="上传json文件" :style="{ width: '25rem' }">
            <span class="p-text-secondary block mb-5">请选择上传形式</span>
            <div class="mt-3 mb-3 flex align-items-center">
                <RadioButton v-model="uploadMethod" inputId="uploadFile" name="uploadMethod" value="file" />
                <label for="ingredient1" class="ml-2">上传文件</label>
            </div>
            <div class="mt-3 mb-3 flex align-items-center">
                <RadioButton v-model="uploadMethod" inputId="uploadPath" name="uploadMethod" value="path" />
                <label for="ingredient2" class="ml-2">上传绝对地址</label>
            </div>
            <div v-if="uploadMethod === 'file'" class="mt-5 mb-5">
                <input type="file" name="file" accept=".json" @change="onFileUpload" />
                <div class="mt-3 mb-3">
                    <RadioButton v-model="fileType" inputId="type4" name="fileType" value="result" />
                    <label for="ingredient1" class="ml-2">result</label>
                    <RadioButton v-model="fileType" inputId="type5" name="fileType" value="score" />
                    <label for="ingredient1" class="ml-2">score</label>
                </div>
              </div>
              <div v-else-if="uploadMethod === 'path'" class="mt-5 mb-5">
                <InputText v-model="filePath" :style="{width: '18rem'}" placeholder="请输入绝对地址" />
                <div class="mt-3 mb-3">
                    <RadioButton v-model="pathType" inputId="type1" name="pathType" value="dataset" />
                    <label for="ingredient1" class="ml-2">dataset</label>
                    <RadioButton v-model="pathType" inputId="type2" name="pathType" value="result" />
                    <label for="ingredient1" class="ml-2">model result</label>
                    <RadioButton v-model="pathType" inputId="type3" name="pathType" value="score" />
                    <label for="ingredient1" class="ml-2">model score</label>
                </div>
                
              </div>
        
              <div class="mt-4 flex justify-content-end">
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="fileShow = false" />
                <Button label="提交" icon="pi pi-check" class="p-button-text" @click="submitFile" />
              </div>
        </Dialog>
        
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

export default {
    name: 'EvaHeader',
    components: {
        Button,
        Sidebar,
        Dialog,
        RadioButton,
        FileUpload,
        InputText,
    },
    computed: {
        ...mapGetters(["filterData","alreadySubmit","dataset"])
    },
    watch: {
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
        }
    },
    methods: {
        clearClick() {
            this.$store.dispatch("updateAlreadySubmit", false);
            console.log("click alrady submit state",this.alreadySubmit);
            this.showSidebar = false;
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
                            const formData = new FormData();
                            formData.append('file',this.uploadedFile);
                            const res = await api.uploadFile(formData);
                            console.log('上传成功:', res.data);
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
                        try {
                            const res = await api.uploadFilePath(this.filePath,this.pathType);
                            console.log("res",res);
                            this.fileShow = false;
                            this.pathType = null;
                        }
                        catch(error) {
                            alert('上传失败:', error)
                        }
                    } else {
                        alert('选择路径的类型！')
                    }
                }else {
                    alert('请填写文件路径');
                }
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
    width: 98.5%;
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
    