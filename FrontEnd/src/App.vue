<!-- src/App.vue -->
<template>
  <div id="app">
    <NavBar 
      @nav-click="handleRouteChange"
    />
    <div class="content-container">
      <router-view></router-view>
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
    // isLoggedIn(){
    //   return this.user.isLoggedIn;
    // },
    // username(){
    //   return this.user.username;
    // },
    // userAvatar(){
    //   return this.user.userAvatar;
    // },
  },
  methods:{
    handleRouteChange(route){
      this.$router.push(route);
      console.log('路由切换到: ', route);
    },
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