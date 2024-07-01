import axios from 'axios'

const API_URL = 'http://101.230.144.192:10069/api/'
// 'http://localhost:8003/'
// 'http://101.230.144.192:10069/api/'

export default {
    getDatasetList() {
        console.log("11111111",API_URL + 'list/dataset/')
        return axios.get(API_URL + 'list/dataset/')
    },
    getModelList(datasetID) {
        return axios.get(API_URL + 'list/model/', {
            params: {
                datasetID: datasetID
            }
        })
    },
    getStandardList() {
        return axios.get(API_URL + 'list/standard/')
    },
    getCategoryList(datasetID = null, modelIDs = [], tagIDs = []) {
        console.log("get category api---", datasetID, modelIDs, tagIDs, typeof modelIDs, typeof tagIDs);
        return axios.post(API_URL + 'list/category/', {
            datasetID: datasetID,
            modelIDs: modelIDs,
            tagIDs: tagIDs
        })
    },
    getTagList(datasetID = null, modelIDs = [], categoryIDs = []) {
        console.log("get tag api--",datasetID,modelIDs,categoryIDs, typeof modelIDs, typeof categoryIDs)
        return axios.post(API_URL + 'list/tag/', {
                datasetID: datasetID,
                modelIDs: modelIDs,
                categoryIDs: categoryIDs
        })
    },
    getFilterList(datasetID = 1, modelIDs, tagIDs = [], categoryIDs = []) {
        tagIDs = tagIDs? tagIDs: [];
        categoryIDs = categoryIDs ? categoryIDs: [];
        const standard = parseInt(localStorage.getItem("standard"),10)
        console.log("get filter list post: ", datasetID, modelIDs, standard, tagIDs, categoryIDs)
        return axios.post(API_URL + 'filter/', {
                datasetID: datasetID,
                modelIDs: modelIDs,
                standard: standard,
                tagIDs: tagIDs,
                categoryIDs: categoryIDs
        })
    },
    getPageById(pageId,datasetID,modelIDs,tagIDs = [], categoryIDs = []) {
        const standard = parseInt(localStorage.getItem("standard"),10)
        return axios.post(`${API_URL}page/${pageId}/`, {
            datasetID: datasetID,
            modelIDs: modelIDs,
            standard: standard,
            tagIDs: tagIDs,
            categoryIDs: categoryIDs
        })
    },
    saveById(pageId,data_info_id, modelList) {
        console.log("save score",modelList)
        const datasetID = parseInt(localStorage.getItem("datasetID"),10)
        pageId = parseInt(pageId,10)
        return axios.post(`${API_URL}save/${pageId}/`, {
            data_info_id: data_info_id,
            datasetID: datasetID,
            modelList: modelList,
        })
    },
    uploadFile(file, filetype) {
        console.log("----", filetype)
        const formData = new FormData();
        formData.append('file', file);
        formData.append('filetype', filetype);
        console.log(formData)
        console.log("form data -----");
        for (const pair of formData.entries()) {
            console.log(`${pair[0]}: ${pair[1]}`);
        }
        return axios.post(`${API_URL}upload-file/`, {
            file: file,
            filetype: filetype
        }, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
        })
    },
    uploadFilePath(file,type) {
        return axios.post(`${API_URL}upload-file-path/`, {
            file: file,
            type: type
        });
    },
    fetchSaveData(datasetID, modelID,standard) {
        return axios.get(API_URL + 'fetch/file/', {
            params: {
                datasetID: datasetID,
                modelID: modelID,
                standard: standard
            }
        }, {
            responseType: 'blob'  // 设置响应类型为 blob
        })
    },
    fetchDatasetInfo(datasetID) {
        console.log("dataset id",datasetID)
        return axios.get(API_URL + 'fetch/dataset/', {
            params: {
                datasetID: datasetID
            }
        }, {
            responseType: 'blob'  // 设置响应类型为 blob
        })
    },
    getFileURL(filename) {
        return `${API_URL}download/${filename}/`
    },
    editAnswer(data_info_id, answer) {
        return axios.post(`${API_URL}edit-answer/`,{
            datainfoID: data_info_id,
            ref_answer: answer
        })
    },
    deleteDataset(dataset_name) {
        return axios.post(`${API_URL}delete-dataset/`, {
                dataset_name: dataset_name
            
        })
    },
    deleteResult(path) {
        return axios.post(`${API_URL}delete-result/`, {
            path: path
        })
    },
    getAccuracy(datasetID, modelIDs,standard) {
        return axios.post(`${API_URL}accuracy/`, {
            datasetID: datasetID,
            modelIDs: modelIDs,
            standard: standard
            
        })
    },
    changeModelName(datasetID,modelID,name) {
        return axios.post(API_URL+ 'edit-modelname/',{
            datasetID: datasetID,
            modelID: modelID,
            modelname: name
        })
    }
}