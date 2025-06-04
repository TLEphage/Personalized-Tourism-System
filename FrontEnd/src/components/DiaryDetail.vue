<template>
  <div class="diary-detail-container">
    <button @click="goBack" class="btn-back">« 返回列表</button>

    <div v-if="isLoading" class="loading-state">
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>错误: {{ error }}</p>
    </div>

    <div v-else-if="!diary" class="not-found-state">
      <p>日记未找到。</p>
    </div>

    <div v-else class="diary-content-wrapper">
      <h1>{{ diary.title }}</h1>
      <div class="meta-info">
        <span>作者: {{ diary.username }}</span>
      </div>

      <button
        @click="editDiary"
        style="
          padding: 0.6em 1.2em;
          background-color: #28a745;
          color: white;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          font-size: 0.9em;
          white-space: nowrap;
        "
      >
        编辑日记
      </button>

      <div class="main-content section">
        <h3>内容详情</h3>
        <div class="ql-snow"><div class="ql-editor" v-html="diary.content"></div></div>
      </div>
      
      <div v-if="diary.images && diary.images.length > 0" class="image-gallery section">
        <h3>图片集</h3>
        <div class="gallery-grid">
          <img v-for="(image, index) in diary.images" 
               :key="`img-${index}`" 
               :src="image" 
               :alt="`日记图片 ${index + 1}`" 
               class="diary-image"/>
        </div>
      </div>
      <div v-else class="section"><p>暂无图片。</p></div>

      <div class="video-section section">
        <h3>视频</h3>
        <div v-if="diary.videos && diary.videos.length > 0" class="video-gallery">
          <div v-for="(videoUrl, index) in diary.videos" :key="`vid-${index}`" class="video-player-wrapper">
            <video controls :src="videoUrl" class="diary-video">
              您的浏览器不支持 HTML5 video 标签。
            </video>
          </div>
        </div>
        <div v-else-if="isVideoGenerating" class="video-status">
          <p>AI 视频正在生成中... <span class="spinner"></span></p>
          <small>(页面会自动检查更新，或稍后刷新查看)</small>
        </div>
        <div v-else class="video-status">
          <p>暂无视频。</p>
        </div>
      </div>

      <div v-if="diary.tags && diary.tags.length > 0" class="tags-section section">
        <h3>标签</h3>
        <span v-for="tag in diary.tags" :key="tag" class="tag-item">{{ tag }}</span>
      </div>
      <div v-else class="section"><p>暂无标签。</p></div>

    </div>

    <!-- 评分部分 -->
    <div class="rating-section section" v-if="!isLoading && !error && diary">
      <h3>评分</h3>
      <div class="rating-container">
        <!-- 当前用户评分 -->
        <div class="user-rating" v-if="$store.state.user.isLoggedIn">
          <p>您的评分：</p>
          <div class="star-rating">
            <span v-for="star in 5" :key="star" 
                  @click="rate(star)" 
                  :class="['star', { 'active': star <= userRating }]"
                  :title="`${star}星`">
              ★
            </span>
          </div>
        </div>
        <div v-else class="login-prompt">
          <p>请<a href="/login">登录</a>后参与评分</p>
        </div>
        
        <!-- 平均评分 -->
        <div class="average-rating">
          <p>
            平均评分：<strong>{{ diary.rating?.toFixed(1) || '暂无' }}</strong>
          </p>
        </div>
      </div>
    </div>

    <EditDiary
      v-if="showEditor"
      :diary="editingDiary"
      :isEdit="!!editingDiary"
      @close="closeEditor"
      @submit="handleDiarySubmit"
    />
  </div>
</template>

<script>
import axios from 'axios';
import EditDiary from './EditDiary.vue';

export default {
  name: 'DiaryDetail',
  components: {
    EditDiary
  },
  data() {
    return {
      diary: null,
      isLoading: true,
      error: null,
      isVideoGenerating: false,
      pollingInterval: null,
      pollingAttempts: 0,
      maxPollingAttempts: 20,
      showEditor: false,
      editingDiary: null,
      userRating: 0,
    };
  },
  methods: {
    async fetchDiaryDetail() {
      this.id = this.$route.params.id;
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.post(`http://localhost:8000/diaries/details/${this.id}`);
        console.log(response);
        const data = response.data;
        console.log( '日记', this.id,'详情:', response.data); 
        this.diary = data;

        this.checkVideoStatus();

      } catch (err) {
        console.error('Error fetching diary details:', err);
        this.error = err.message;
        this.diary = null;
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
      } finally {
        this.isLoading = false;
      }
    },

    async checkVideoStatus() {
      try {
        const response = await axios.post('http://localhost:8000/AIGen/check_video_status');
        if(response.data.message) {
          console.log(response.data.message + "，剩余" + response.data.remaining_tasks + "个任务");
        }
      } catch (err) {
        console.error('Error checking video status:', err);
      }
    },

    goBack() {
      this.$router.go(-1);
    },
    editDiary() {
      this.editingDiary = { ...this.diary };
      this.showEditor = true;
    },
    
    handleDiarySubmit(updatedDiary) {
      this.diary = updatedDiary;
      this.closeEditor();
      alert('日记已更新！');
    },
    
    // 新增关闭编辑器方法
    closeEditor() {
      this.showEditor = false;
      this.editingDiary = null;
    },
    async rate(rating) {
      if(!this.$store.state.user.isLoggedIn) {
        alert('请先登录！');
        return;
      }
      try {
        this.userRating = rating;
        const response = await axios.post(`http://localhost:8000/diaries/rate`, {
          id: this.diary.id,
          rate: rating
        });
        if(response.data.message) {
          console.log(response.data.message);
          this.diary = response.data.diary;
        }
      } catch (err) {
        console.error('Error submitting rating:', err);
        alert('评分失败，请稍后再试。');
      }
    }
  },
  created() {
    this.fetchDiaryDetail();
  },
  beforeUnmount() {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
      this.pollingInterval = null;
    }
  },
  watch: {
    id(newId, oldId) {
      if (newId !== oldId) {
        console.log(`Diary ID changed from ${oldId} to ${newId}. Re-fetching details.`);
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
        this.diary = null; // Reset diary before fetching new one
        this.fetchDiaryDetail();
      }
    }
  }
};
</script>

<style scoped>
.diary-detail-container {
  padding: 20px;
  max-width: 900px;
  margin: 20px auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.btn-back {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 25px;
  font-size: 0.95em;
  transition: background-color 0.2s ease;
}
.btn-back:hover {
  background-color: #545b62;
}

.loading-state, .error-state, .not-found-state {
  text-align: center;
  padding: 50px 20px;
  font-size: 1.2em;
  color: #555;
}
.error-state {
  color: #d9534f;
}

.diary-content-wrapper h1 {
  font-size: 2.2em;
  margin-bottom: 10px;
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}

.meta-info {
  font-size: 0.9em;
  color: #7f8c8d;
  margin-bottom: 25px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px 20px; /* row-gap column-gap */
}
.meta-info span {
  margin-right: 20px;
}

.section {
  background-color: #fff;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 25px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.section h3 {
  font-size: 1.4em;
  margin-top: 0;
  margin-bottom: 15px;
  color: #34495e;
  border-bottom: 1px solid #ecf0f1;
  padding-bottom: 8px;
}

.main-content .ql-editor {
  line-height: 1.7;
  color: #333;
  font-size: 1.05em;
  padding: 0; /* Reset padding if ql-editor itself has it */
  min-height: auto; /* Override Quill's min-height if not desired */
}
.main-content.section { /* Apply section styles to main content area */
  padding: 20px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
}
.diary-image {
  width: 100%;
  height: auto;
  border-radius: 5px;
  object-fit: cover;
  border: 1px solid #ddd;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.diary-image:hover {
    transform: scale(1.03);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.video-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}
.video-player-wrapper {
  position: relative;
  /* padding-bottom: 56.25%; 16:9, not always needed if video has intrinsic ratio */
  height: auto; /* Let video define its height */
  overflow: hidden;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.diary-video {
  display: block; /* Fixes extra space below video */
  width: 100%;
  height: auto; /* Maintain aspect ratio */
  border-radius: 5px;
  background-color: #000;
}

.video-status p {
  color: #3498db;
  font-weight: 500;
}
.video-status small {
  color: #7f8c8d;
  font-size: 0.85em;
  display: block;
  margin-top: 5px;
}
.spinner {
  display: inline-block;
  width: 1em;
  height: 1em;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner-border .75s linear infinite;
  vertical-align: text-bottom;
  margin-left: 8px;
}
@keyframes spinner-border {
  to { transform: rotate(360deg); }
}

.tags-section .tag-item {
  display: inline-block;
  background-color: #3498db;
  color: white;
  padding: 6px 14px;
  border-radius: 15px;
  margin-right: 8px;
  margin-bottom: 8px;
  font-size: 0.9em;
  transition: background-color 0.2s ease;
}
.tags-section .tag-item:hover {
  background-color: #2980b9;
}

.rating-section {
  margin-top: 30px;
  padding: 25px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}

.rating-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.user-rating, .average-rating {
  flex: 1;
  min-width: 250px;
}

.star-rating, .stars-display {
  font-size: 28px;
  line-height: 1;
  margin-top: 8px;
}

.star-rating .star {
  color: #ccc;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-right: 5px;
}

.star-rating .star:hover,
.star-rating .star.active {
  color: #FFC107;
  transform: scale(1.2);
}

.star-rating .star.active:hover {
  transform: scale(1.25);
}

.stars-display .star {
  color: #e0e0e0;
  margin-right: 3px;
}

.stars-display .star.filled {
  color: #FFC107;
}

.login-prompt a {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
}

.login-prompt a:hover {
  text-decoration: underline;
}

.rating-count {
  color: #7f8c8d;
  font-size: 0.9em;
  margin-left: 8px;
}

@media (max-width: 600px) {
  .rating-container {
    flex-direction: column;
    align-items: flex-start;
  }
}

/* Basic Quill CSS for v-html content if not globally included */
/* Consider importing 'quill/dist/quill.snow.css' in your main.js or App.vue */
.ql-snow { box-sizing: border-box; font-family: Helvetica, Arial, sans-serif; font-size: 13px; height: 100%; margin: 0px; position: relative; }
.ql-editor { box-sizing: border-box; line-height: 1.42; height: 100%; outline: none; overflow-y: auto; padding: 12px 15px; tab-size: 4; -moz-tab-size: 4; text-align: left; white-space: pre-wrap; word-wrap: break-word; }
.ql-editor p, .ql-editor ol, .ql-editor ul, .ql-editor pre, .ql-editor blockquote, .ql-editor h1, .ql-editor h2, .ql-editor h3, .ql-editor h4, .ql-editor h5, .ql-editor h6 { margin: 0; padding: 0; counter-reset: list-1 list-2 list-3 list-4 list-5 list-6 list-7 list-8 list-9; }
.ql-editor ol, .ql-editor ul { padding-left: 1.5em; }
.ql-editor ol > li, .ql-editor ul > li { list-style-type: none; }
.ql-editor ul > li::before { content: '\2022'; } /* Basic bullet */
.ql-editor blockquote { border-left: 4px solid #ccc; margin-bottom: 5px; margin-top: 5px; padding-left: 16px; }
.ql-editor pre { background-color: #f0f0f0; border-radius: 3px; white-space: pre-wrap; margin-bottom: 5px; margin-top: 5px; padding: 5px 10px; }
/* Add more Quill styles as needed, or import the full theme */
</style>