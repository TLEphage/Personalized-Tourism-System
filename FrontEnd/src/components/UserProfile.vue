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
      <div class="diaries-container">
        <h2>日记列表</h2>
        <div v-if="diaries.length > 0">
          <div
          v-for="diary in diaries"
          :key="diary.id"
          class="diary-item"
          >
            <div class="diary-content">
              <h3>{{ diary.title }}</h3>
              <p>{{ diary.content }}</p>
              <!-- <div v-if="diary.image" class="diary-media">
                <img src="diary.image" alt="Diary Image">
              </div>
              <div v-if="diary.video" class="diary-media">
                <video controls>
                  <source :src="diary.video" type="video/mp4">
                </video>
              </div> -->
              <div class="diary-stats">
                <p>浏览量: {{ diary.views }}</p>
                <p>评分: {{ diary.rating }}</p>
              </div>
            </div>
          </div>
        </div>
        <div v-else>暂无日记</div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex';
  import axios from 'axios';
  export default {
    name: 'UserProfile',
    computed:{
        ...mapState(['user'])
    },
    data() {
      return {
        diaries: [],
      };
    },
    created() {
        this.fetchDiaries();
    },
    methods: {
      goToHomePage() {
        this.$router.push({ name: 'Recommend' });
      },
      async fetchDiaries() {
        try {
          const response = await axios.get(`http://localhost:8000/diaries/${this.user.username}`);
          this.diaries = response.data;
        } catch (error) {
          console.error('Error fetching diaries:', error);
        }
      }
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

  .diaries-container {
  margin-top: 20px;
}

.diary-item {
  margin-bottom: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
}

.diary-content {
  display: flex;
  flex-direction: column;
}

.diary-media img,
.diary-media video {
  max-width: 100%;
  height: auto;
}

.diary-stats {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
  </style>