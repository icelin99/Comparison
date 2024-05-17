import { createStore } from 'vuex';

export default createStore({
    state: {
        selectSubmitted: false,
        filterData: [],
        currentPage: 1,
        ratingStandard: parseInt(localStorage.getItem("standard")),
        pageInfo: localStorage.getItem("pageInfo"),
        pageCount: parseInt(localStorage.getItem("pageCount")),
        alreadySubmit: false,
        isLoading: true,
        dataset: null,
    },
    mutations: {
        set_selectSubmitted(state, data) {
            state.selectSubmitted = data;
        },
        set_filterData(state, data) {
            state.filterData = data;
        },
        prevItem(state) {
            if(state.currentPage > 1) {
                state.currentPage--;
            }
        },
        nextItem(state) {
            if(state.currentPage < state.pageCount) {
                state.currentPage++;
            }
        },
        setPage(state, page) {
            console.log("--------------- new ppagt", page, typeof page);
            if(page >= 1 && page <= state.pageCount) {
                state.currentPage = page;
                localStorage.setItem("currentPage",page.toString());
            }
        },
        set_ratingStandard(state, rating) {
            state.ratingStandard = rating;
            localStorage.setItem("standard",rating.toString());
        },
        set_pageInfo(state, info) {
            state.pageInfo = info;
            localStorage.setItem("pageInfo",info);
        },
        set_pageCount(state, count) {
            state.pageCount = count;
            localStorage.setItem("pageCount",count.toString());
        },
        set_alreadySubmit(state, alreadySubmit) {
            state.alreadySubmit = alreadySubmit;
        },
        set_loading(state, loading) {
            state.isLoading = loading;
        },
        set_dataset(state,dataset) {
            console.log("store dataset",dataset)
            state.dataset = dataset;
        }
    },
    actions: {
        updateSelectSubmitted({commit}, selectSubmitted) {
            commit('set_selectSubmitted', selectSubmitted);
        },
        updateFilterData({commit}, filterData) {
            commit('set_filterData',filterData);
        },
        updateCurrentPage({commit}, currentPage) {
            commit('setPage',currentPage);
        },
        updateRatingStandard({commit}, standard) {
            commit('set_ratingStandard',standard);
        },
        updatePageInfo({commit}, info) {
            commit('set_pageInfo',info);
        },
        updatePageCount({commit}, count) {
            commit('set_pageCount',count);
        },
        updateAlreadySubmit({commit}, alreadySubmit) {
            commit('set_alreadySubmit',alreadySubmit);
        },
        updateIsLoading({commit}, loading) {
            commit('set_loading', loading);
        },
        updateDataset({commit},name) {
            commit('set_dataset',name);
        }
    },
    getters: {
        selectSubmitted: state => state.selectSubmitted,
        filterData: state => state.filterData,
        currentData: state => state.filterData[state.currentPage-1],
        pageCount: state => state.pageCount,
        currentPage: state => state.currentPage,
        ratingStandard: state => state.ratingStandard,
        pageInfo: state => state.pageInfo,
        alreadySubmit: state => state.alreadySubmit,
        loading: state => state.isLoading,
        dataset: state => state.dataset,
    }
})