<!-- 旅游日记总界面，能按评分和热度进行排序 -->
<!--
日记数据结构
diary
{
    username:string,
    id: int,
    title:string,
    content:string,
    image:jpg/png/...,
    video:mp4,
    views:int,
    rating:float,
}
-->
<template>
    <div class="diary-list-container">
        <h2>所有日记</h2>
        <input type="text" v-model="searchQuery" placeholder="搜索日记标题或关键词">
        <select v-model="sortBy">
            <option value="hot">按热度排序</option>
            <option value="rating">按评分排序</option>
        </select>
        <div class="diary-list">
            <div
                v-for="diary in filteredDiaries" 
                :key="diary.id"
                class="diary-item"
            >
                <h3>{{ diary.title }}</h3>
                <p>{{ diary.content }}</p>
                <img :src="diary.image" alt="旅行照片" class="diary-image">
                <video controls v-if="diary.video" class="diary-video">
                    <source :src="diary.video" type="video/mp4"></source>
                </video>
                <div class="meta-info">
                    <span>浏览量: {{ diary.views }}</span>
                    <span>评分: {{ diary.rating.toFixed(1) }}</span>
                </div>
                <button @click="showEditForm(diary.id)">编辑</button>
                <button @click="deleteDiary(diary.id)">删除</button>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
import EditDiary from '../components/EditDiary.vue';
export default{
    components:{
      EditDiary
    },
    data(){
      return {
        diaries: [],
        searchQuery: '',
        sortBy: 'hot',
        editingDiaryId:null,
      }
    },
    created(){
      this.fetchDiaries();
    },
    methods:{
      fetchDiaries(){
        axios.get('/api/diaries')
          .then(response => {
            this.diaries = response.data;
          })
          .catch(error => {
            console.error('Error fetching diaries:', error);
          });
      },
      showEditForm(diaryId){
        this.editingDiaryId = diaryId;
      },
      closeEditForm(){
        this.editingDiaryId = null;
      },
      deleteDiary(diaryId){
        axios.delete(`/api/diaries/${diaryId}`)
          .then(() => {
            this.fetchDiaries();
          })
          .catch(error => {
            console.error('Error deleting diary:', error);
          });
      }
    }
}
</script>

<style scoped>
.diary-list-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.diary-list {
  display: grid;
  gap: 20px;
}

.diary-item {
  border: 1px solid #ccc;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.diary-image {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
}

.diary-video {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
}

.meta-info {
  margin-top: 10px;
  color: #666;
}

button {
  margin-top: 10px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>