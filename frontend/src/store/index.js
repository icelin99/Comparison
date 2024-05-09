import { createStore } from 'vuex';

export default createStore({
    state: {
        selectSubmitted: false,
        filterData: [],
        currentPage: parseInt(localStorage.getItem("currentPage")),
        ratingStandard: parseInt(localStorage.getItem("standard")),
        pageInfo: localStorage.getItem("pageInfo"),
        pageCount: parseInt(localStorage.getItem("pageCount")),
        alreadySubmit: false,
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
    }
})