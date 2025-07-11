// src/store/index.js
import { createStore } from 'vuex';

export default createStore({
    state: {
        user: {
            isLoggedIn: false,
            id: -1,
            username: '',
            avatarPath: '',
            role: '',
            signature: '',
            hobbies: []
        }
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        logout(state) {
            state.user.isLoggedIn = false;
            state.user.id = -1;
            state.user.username = '';
            state.user.avatarPath = '';
            state.user.role = '';
            state.user.signature = '';
            state.user.hobbies = [];
        }
    },
});