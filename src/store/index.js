import { createStore } from 'vuex';

export default createStore({
    state: {
        selectSubmitted: false,
    },
    mutations: {
        set_selectSubmitted(state, data) {
            state.selectSubmitted = data;
        }
    },
    actions: {
        updateSelectSubmitted({commit}, selectSubmitted) {
            commit('set_selectSubmitted', selectSubmitted);
        }
    },
    getters: {
        selectSubmitted: state => state.selectSubmitted,
    }
})