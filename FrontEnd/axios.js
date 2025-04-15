// axios.js
// 在用户登录之后，会把token用Vuex 保存起来，每次请求的时候，把token放在请求头中，这样后端就可以验证用户是否登录了
// Vuex是全局的，在本文件中，全局配置axoisInstance，在请求头中添加token
// 这样就可以在任何地方使用axiosInstance了，且是带有token的
import axios from 'axios';
import store from './store';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = store.state.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;