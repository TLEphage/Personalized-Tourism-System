<!-- 编辑日记
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
    <div class="edit-diary-model">
        <h3>编辑日记</h3>
        <form @submit.prevent="updateDiary">
            <label for="title">标题:</label>
            <input type="text" id="title" v-model="diary.title" required>
            <label for="content">内容:</label>
            <textarea id="content" v-model="diary.content" required></textarea>
            <label for="image">图片 URL:</label>
            <input type="text" id="image" v-model="diary.image">
            <label for="video">视频 URL:</label>
            <input type="text" id="video" v-model="diary.video">
            <button type="submit">保存</button>
            <button type="button" @click="$emit('close')">取消</button>
        </form>
    </div>
</template>


<script>
    import axios from 'axios';
    export default {
        name:'EditDiary',
        props: {
            diaryId: {
                type: Number,
                required: true
            }
        },
        data(){
            return{
                diary:{
                    title:'',
                    content:'',
                    image:'',
                    video:''
                }
            }
        },
        created(){
            this.fetchDiary();
        },
        methods:{
            fetchDiary() {
            axios.get(`/api/diaries/${this.diaryId}`)
                .then(response => {
                    this.diary = response.data;
                })
                .catch(error => {
                    console.error('Error fetching diary:', error);
                });
        },
        updateDiary() {
            axios.put(`/api/diaries/${this.diaryId}`, this.diary)
                .then(() => {
                    this.$emit('update-diary');
                    this.$emit('close');
                })
                .catch(error => {
                    console.error('Error updating diary:', error);
                });
        }
        }
    }
</script>


<style>
.edit-diary-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-top: 10px;
}

input, textarea {
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  margin-top: 20px;
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