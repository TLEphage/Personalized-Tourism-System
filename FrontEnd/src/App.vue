<!-- src/App.vue -->
<template>
  <div id="app">
    <NavBar 
      :isLoggedIn="isLoggedIn"
      :userAvatar="userAvatar"
      :username="username"
      @nav-click="handleRouteChange"
    />
    <div class="content-container">
      <router-view @user-login="handleUserLogin"></router-view>
      <!-- 其他页面组件 -->
    </div>
  </div>
</template>

<script>

import NavBar from './components/NavBar.vue';
import { mapState } from 'vuex';

export default {
  name: 'App',
  components: {
    NavBar,
  },
  data (){
    return {
      currentRoute: 'Recommend',
    }
  },
  computed:{
    ...mapState(['user']),
    isLoggedIn(){
      return this.user.isLoggedIn;
    },
    username(){
      return this.user.username;
    },
    userAvatar(){
      return this.user.userAvatar;
    },
  },
  methods:{
    handleRouteChange(route){
      this.$router.push(route);
      console.log('路由切换到: ', route);
    },
    handleUserLogin(userData){
      this.$store.commit('setUser', userData);
    }
  },
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-container {
  margin-top: 60px; /* 与导航栏高度一致 */
  padding: 20px;
  flex: 1;
}
</style>