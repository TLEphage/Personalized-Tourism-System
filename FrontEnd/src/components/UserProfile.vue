<!-- src/components/UserProfile.vue  -->
<template>
    <div class="user-profile">
      <div class="avatar-container">
        <img
          :src="user.userAvatar"
          alt="User Avatar"
          class="avatar"
          @click="goToHomePage"
        />
      </div>
      <div class="user-info">
        <h2>{{ user.username }}</h2>
        <p v-if="user.signature">{{ user.signature }}</p>
        <h3>爱好:</h3>
        <ul v-if="user.hobbies">
          <li v-for="hobby in user.hobbies" :key="hobby">{{ hobby }}</li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex';
  export default {
    name: 'UserProfile',
    computed:{
        ...mapState(['user'])
    },
    created() {
        // if (!this.user.id) {
        //     this.$router.push({ name: 'LoginRegister' });
        // }
    },
    methods: {
      goToHomePage() {
        this.$router.push({ name: 'Recommend' });
      },
    },
  };
  </script>
  
  <style scoped>
  .user-profile {
    display: flex;
    align-items: center;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
  }
  
  .avatar-container {
    margin-right: 20px;
    cursor: pointer;
  }
  
  .avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .user-info {
    display: flex;
    flex-direction: column;
  }
  
  h2 {
    margin: 0;
    font-size: 1.5em;
  }
  
  p {
    color: #666;
  }
  
  h3 {
    margin: 10px 0;
    font-size: 1.2em;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin: 5px 0;
  }
  </style>