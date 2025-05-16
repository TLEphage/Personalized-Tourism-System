<template>
  <div class="interest-selector">
      <h3>📸 选择您的旅行兴趣</h3>
      <p class="subtitle">发现属于您的独特旅程</p>
      <div class="interest-options">
          <label v-for="(option, index) in options" 
                 :key="index"
                 class="option-card"
                 :class="{ selected: selectedInterests.includes(option.value) }">
              <input type="checkbox"
                     :value="option.value"
                     v-model="selectedInterests"
                     class="sr-only">
              <span class="checkmark">✓</span>
              {{ option.label }}
          </label>
      </div>
      <p class="selected-display">已选兴趣：<span>{{ selectedInterests.join(' · ') }}</span></p>
      <button @click="submitInterests" :disabled="selectedInterests.length === 0">
          {{ selectedInterests.length ? `开启旅程 (${selectedInterests.length})` : '请选择兴趣' }}
      </button>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router'; 

export default {
  name: 'InterestSelector',
  setup() {
      const store = useStore();
      const router = useRouter();
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
          axios.put(`http://localhost:8000/users/${store.state.user.username}`, {
              avatarPath: store.state.user.avatarPath,
              signature: store.state.user.signature,
              hobbies: selectedInterests.value
          })
          .then(response => {
              if (response.data.message === '用户信息更新成功') {
                  alert('兴趣选择已保存！');
                  store.commit('setUser',{
                      ...response.data.user,
                      isLoggedIn: true
                  });
                  router.push({ name: 'Recommend'});
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
  font-family: 'Segoe UI', system-ui, sans-serif;
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem 2.5rem;
  border-radius: 16px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  box-shadow: 0 8px 32px rgba(0, 40, 120, 0.1);
}

h3 {
  color: #2a3258;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  color: #6c757d;
  text-align: center;
  margin-bottom: 2rem;
}

.interest-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
  margin: 2rem 0;
}

.option-card {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  background: white;
  border: 2px solid #e0e7ff;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.option-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 40, 120, 0.1);
}

.option-card.selected {
  background: #4a6fff;
  border-color: #4a6fff;
  color: white;
  animation: selectBounce 0.4s ease;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid #e0e7ff;
  border-radius: 4px;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  color: transparent;
  transition: all 0.2s ease;
}

.selected .checkmark {
  border-color: rgba(255,255,255,0.5);
  background: rgba(255,255,255,0.1);
  color: white;
}

.sr-only {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.selected-display {
  text-align: center;
  color: #6c757d;
  margin: 1.5rem 0;
}

.selected-display span {
  color: #4a6fff;
  font-weight: 500;
}

button {
  display: block;
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #4a6fff 0%, #6b4aff 100%);
  color: white;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(74, 111, 255, 0.3);
}

button:disabled {
  background: #e0e7ff;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

@keyframes selectBounce {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@media (max-width: 640px) {
  .interest-selector {
    margin: 1rem;
    padding: 1.5rem;
  }
  
  .interest-options {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>