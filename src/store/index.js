import { createStore } from 'vuex';

export default createStore({
    state: {
        selectSubmitted: false,
        filterData: [],
        currentPage: 1,
        ratingStandard: 0,
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
            if(state.currentPage < state.filterData.length) {
                state.currentPage++;
            }
        },
        setPage(state, page) {
            if(page >= 1 && page <= state.filterData.length) {
                state.currentPage = page;
            }
        },
        set_ratingStandard(state, rating) {
            state.ratingStandard = rating;
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
        }
    },
    getters: {
        selectSubmitted: state => state.selectSubmitted,
        filterData: state => state.filterData,
        currentData: state => state.filterData[state.currentPage-1],
        pageCount: state => state.filterData.length,
        currentPage: state => state.currentPage,
        ratingStandard: state => state.ratingStandard,
    }
})