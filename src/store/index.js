import { createStore } from 'vuex';

export default createStore({
    state: {
        selectSubmitted: false,
        filterData: [],
        currentPage: 1,
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
        }
    },
    actions: {
        updateSelectSubmitted({commit}, selectSubmitted) {
            commit('set_selectSubmitted', selectSubmitted);
        },
        updateFilterData({commit}, filterData) {
            commit('set_filterData',filterData);
        }
    },
    getters: {
        selectSubmitted: state => state.selectSubmitted,
        filterData: state => state.filterData,
        currentData: state => state.filterData[state.currentPage-1]
    }
})