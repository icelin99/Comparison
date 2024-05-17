import axios from 'axios'

const API_URL = 'http://101.230.144.192:10069/api/'

export default {
    getDatasetList() {
        console.log("11111111")
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
    getCategoryList(datasetID = null, modelIDs = []) {
        return axios.get(API_URL + 'list/category/', {
            params: {
                datasetID: datasetID,
                modelIDs: modelIDs
            }
        })
    },
    getTagList(datasetID = null, modelIDs = [], categoryIDs = []) {
        console.log("api--",datasetID,modelIDs,categoryIDs)
        return axios.post(API_URL + 'list/tag/', {
                datasetID: datasetID,
                modelIDs: modelIDs,
                categoryIDs: categoryIDs
        })
    },
    getFilterList(datasetID = 1, modelIDs = [], tagIDs = [], categoryIDs = []) {
        tagIDs = tagIDs? tagIDs: [];
        categoryIDs = categoryIDs ? categoryIDs: [];
        console.log("get filter list post: ", datasetID, modelIDs, tagIDs, categoryIDs)
        return axios.post(API_URL + 'filter/', {
                datasetID: datasetID,
                modelIDs: modelIDs,
                tagIDs: tagIDs,
                categoryIDs: categoryIDs
        })
    },
    getPageById(pageId) {
        const datasetID = parseInt(localStorage.getItem("datasetID"))
        const modelIDs = JSON.parse(localStorage.getItem("modelIDs"))
        const tagIDs = JSON.parse(localStorage.getItem("tagIDs"))
        const categoryIDs = JSON.parse(localStorage.getItem("categoryIDs"))
        return axios.post(`${API_URL}page/${pageId}/`, {
            datasetID: datasetID,
            modelIDs: modelIDs,
            tagIDs: tagIDs,
            categoryIDs: categoryIDs
        })
    },
    saveById(pageId,data_info_id, model_id, score = 0) {
        const standard = parseInt(localStorage.getItem("standard"))
        const datasetID = parseInt(localStorage.getItem("datasetID"))
        const tagIDs = JSON.parse(localStorage.getItem("tagIDs"))
        const categoryIDs = JSON.parse(localStorage.getItem("categoryIDs"))
        console.log("api ",pageId, data_info_id,model_id, score, standard);
        pageId = parseInt(pageId,10)
        return axios.post(`${API_URL}save/${pageId}/`, {
            data_info_id: data_info_id,
            datasetID: datasetID,
            modelID: model_id,
            score: score,
            standard: standard,
            tagIDs: tagIDs,
            categoryIDs: categoryIDs
        })
    },
    uploadFile(file) {
        return axios.post(`${API_URL}upload-file/`, file, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    },
    uploadFilePath(file,type) {
        return axios.post(`${API_URL}upload-file-path/`, {
            file: file,
            type: type
        });
    }
}