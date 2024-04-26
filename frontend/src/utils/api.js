import axios from 'axios'

const API_URL = 'http://localhost:8002/'

export default {
    getDatasetList() {
        console.log("11111111")
        return axios.get(API_URL + 'list/dataset/')
    },
    getModelList() {
        return axios.get(API_URL + 'list/model/')
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
    getTagList(datasetID = null, modelIDs = []) {
        return axios.get(API_URL + 'list/tag/', {
            params: {
                datasetID: datasetID,
                modelIDs: modelIDs
            }
        })
    },
    getFilterList(datasetID = 1, modelIDs = [], tagIDs = [], categoryIDs = []) {
        return axios.get(API_URL + 'filter/', {
            params: {
                datasetID: datasetID,
                modelIDs: modelIDs,
                tagIDs: tagIDs,
                categoryIDs: categoryIDs
            }
        })
    },
    getPageById(pageId) {
        return axios.get(API_URL + 'page/{pageId}/'.format(pageId))
    },
    saveById(pageId, modelId, score, standard = null) {
        return axios.post(API_URL + 'save/{pageId}/{modelId}/'.format(pageId, modelId), {
            score: score,
            standard: standard
        })
    }
}