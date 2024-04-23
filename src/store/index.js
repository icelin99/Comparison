import { createStore } from 'vuex';

export default createStore({
    state: {
        selectSubmitted: false,
        filterData: [],
    },
    mutations: {
        set_selectSubmitted(state, data) {
            state.selectSubmitted = data;
        },
        set_filterData(state, data) {
            state.filterData = data;
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
    }
})