<template>
  <div class="interest-selector">
      <h3>请选择您的旅游兴趣</h3>
      <div class="interest-options">
          <label v-for="(option, index) in options" :key="index">
              <input type="checkbox"
                     :value="option.value"
                     v-model="selectedInterests">
              {{ option.label }}
          </label>
      </div>
      <p>您选择的兴趣: {{ selectedInterests.join(',') }}</p>
      <button @click="submitInterests">提交</button>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'InterestSelector',
  setup() {
      const selectedInterests = ref([]);
      const options = [
          { value: '名人故居', label: '名人故居' },
          { value: '自然风光', label: '自然风光' },
          { value: '历史文化', label: '历史文化' },
          { value: '美食探索', label: '美食探索' },
          { value: '现代建筑', label: '现代建筑' },
          { value: '博物馆', label: '博物馆' },
          { value: '公园', label: '公园' },
          { value: '宗教场所', label: '宗教场所' },
          { value: '购物', label: '购物' },
          { value: '夜生活', label: '夜生活' },
      ];

      const submitInterests = () => {
          if (selectedInterests.value.length === 0) {
              alert('请至少选择一个兴趣！');
              return;
          }

          // 向后端发送用户选择的兴趣
          axios.post('http://localhost:8000/save-interests', {
              interests: selectedInterests.value
          })
          .then(response => {
              if (response.data.success) {
                  alert('兴趣选择已保存！');
                  // 跳转到旅游推荐页面
                  window.location.href = '/recommend';
              } else {
                  alert('保存兴趣失败，请重试！');
              }
          })
          .catch(error => {
              console.error('保存兴趣失败：', error);
              alert('保存兴趣失败，请重试！');
          });
      };

      return {
          selectedInterests,
          options,
          submitInterests
      };
  }
};
</script>

<style scoped>
.interest-selector {
  font-family: Arial, sans-serif;
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.interest-options {
  margin-top: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="checkbox"] {
  margin-right: 5px;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>