// store/index.js
import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      token: null, // 初始化 token 为 null
    };
  },
  mutations: {
    setToken(state, token) {
      state.token = token; // 设置 token 的 mutation
    },
  },
  actions: {
    saveToken({ commit }, token) {
      commit('setToken', token); // 提交 mutation 来保存 token
    },
  },
});

export default store;