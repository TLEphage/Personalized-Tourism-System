<!-- 旅游日记总界面，能按评分和热度进行排序 -->
<!--
日记数据结构
diary
{
    username:string,
    id: int,
    title:string,
    content:string,
    images:jpg/png/...,
    videos:mp4,
    views:int,
    rating:float,
}
-->
<template>
  <div class="diary-list-container">
    <!-- 搜索控制区 -->
    <div class="search-control glassmorphism-effect">
      <div class="search-group">
        <div class="search-wrapper">
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="输入关键词搜索旅行日记..."
            class="search-input"
            @keyup.enter="handleSearch"
          >
          <button class="search-btn" @click="handleSearch">
            <i class="icon-search"></i>
            搜索
          </button>
        </div>
        <div class="sort-wrapper">
          <label>排序方式：</label>
          <select v-model="sortBy" class="sort-select">
            <option value="views">🔥 热门优先</option>
            <option value="rating">⭐ 高评分优先</option>
            <option value="latest">🕒 最新发布</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 日记列表 -->
    <div class="diary-list">
      <transition-group name="diary-fade">
        <article 
          v-for="diary in filteredDiaries"
          :key="diary.id"
          class="diary-card"
        >
          <!-- 媒体区 -->
          <div class="media-section">
            <div class="image-gallery">
              <img 
                v-for="(img, index) in diary.images.slice(0, 3)"
                :key="index"
                :src="img"
                :alt="`旅行图片 ${index + 1}`"
                class="gallery-image"
                :class="{ 'main-image': index === 0 }"
              >
            </div>
            <div v-if="diary.videos.length" class="video-container">
              <video controls :poster="diary.images[0]">
                <source :src="diary.videos[0]" type="video/mp4">
              </video>
            </div>
          </div>

          <!-- 内容区 -->
          <div class="content-section">
            <h2 class="diary-title">{{ diary.title }}</h2>
            <div class="author-meta">
              <span class="author">✍️ {{ diary.username }}</span>
              <time class="post-date">📅 {{ diary.createdAt?formatDate(diary.createdAt):'暂无时间信息' }}</time>
            </div>
            <p class="diary-content">{{ diary.content }}</p>
            
            <!-- 数据指标 -->
            <div class="metrics-grid">
              <div class="metric-item">
                <i class="icon-eye"></i>
                <div>
                  <span class="metric-value">{{ diary.views }}</span>
                  <span class="metric-label">浏览量</span>
                </div>
              </div>
              <div class="metric-item">
                <i class="icon-star"></i>
                <div>
                  <span class="metric-value">{{ diary.rating.toFixed(1) }}</span>
                  <span class="metric-label">平均评分</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="action-section">
            <button class="btn-detail" @click="viewDetail(diary.id)">
              <i class="icon-arrow-right"></i>
              查看详情
            </button>
          </div>
        </article>
      </transition-group>
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
        sortBy: 'views',
        isLoading: false,
      }
    },
    created(){
      this.fetchDiaries();
    },
    computed:{
      filteredDiaries(){
        let filtered = this.diaries.filter(diary => {
        const search = this.searchQuery.toLowerCase()
        return diary.title.toLowerCase().includes(search) || 
               diary.content.toLowerCase().includes(search)
        })

        // 排序逻辑
        return filtered.sort((a, b) => {
          if(this.sortBy === 'views') return b.views - a.views
          if(this.sortBy === 'rating') return b.rating - a.rating
          return 0
        })
      }
    },
    methods:{
      async fetchDiaries() {
        try {
          this.isLoading = true
          const { data } = await axios.get(`http://localhost:8000/diaries/__all__?sort_key=${this.sortBy}&sort_order=desc`)
          this.diaries = data.diaries
        } catch (error) {
          console.error('日记加载失败:', error)
        } finally {
          this.isLoading = false
        }
      },
      truncateContent(text, maxLength) {
        return text.length > maxLength ? text.slice(0, maxLength) + '...' : text
      },
      formatNumber(num) {
        return num > 1000 ? (num/1000).toFixed(1) + 'k' : num
      },
      formatDate(timestamp) {
        if (!timestamp) return '未知时间'
        const date = new Date(timestamp)
        return date.toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        })
      },
    }
}
</script>

<style scoped>
/* 容器布局 */
.diary-list-container {
  max-width: 1280px;
  margin: 2rem auto;
  padding: 0 2rem;
}

/* 搜索控制区 */
.search-control {
  margin-bottom: 3rem;
  padding: 2rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
}

.search-group {
  display: grid;
  gap: 2rem;
}

.search-wrapper {
  display: flex;
  gap: 1rem;
  width: 100%;
}

.search-input {
  flex: 1;
  padding: 1.2rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 4px rgba(0, 123, 255, 0.1);
}

.search-btn {
  padding: 0 2rem;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.search-btn:hover {
  transform: translateY(-2px);
}

/* 排序控件 */
.sort-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sort-select {
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
  background: white;
}

/* 日记卡片 */
.diary-list {
  display: grid;
  gap: 3rem;
}

.diary-card {
  background: white;
  border-radius: 24px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  min-height: 480px;
}

.media-section {
  position: relative;
  overflow: hidden;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  padding: 0.5rem;
}

.main-image {
  grid-column: 1 / -1;
  height: 280px;
}

.gallery-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 12px;
  transition: transform 0.3s ease;
}

.gallery-image:hover {
  transform: scale(1.03);
}

.video-container {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  width: 240px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 内容区 */
.content-section {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.diary-title {
  font-size: 2rem;
  margin: 0;
  color: #1a1a1a;
  line-height: 1.3;
}

.author-meta {
  display: flex;
  gap: 1.5rem;
  color: #666;
  font-size: 0.95rem;
}

.diary-content {
  flex: 1;
  color: #444;
  font-size: 1.1rem;
  line-height: 1.8;
}

/* 数据指标 */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-item i {
  font-size: 1.8rem;
  color: #007bff;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.metric-label {
  display: block;
  color: #666;
  font-size: 0.9rem;
}

/* 操作按钮 */
.action-section {
  border-top: 1px solid #eee;
  padding: 1.5rem 2.5rem;
}

.btn-detail {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 1rem 2rem;
  background: transparent;
  border: 2px solid #007bff;
  border-radius: 8px;
  color: #007bff;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-detail:hover {
  background: #007bff;
  color: white;
}

/* 过渡动画 */
.diary-fade-enter-active,
.diary-fade-leave-active {
  transition: all 0.5s ease;
}

.diary-fade-enter-from,
.diary-fade-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

@media (max-width: 1024px) {
  .diary-card {
    grid-template-columns: 1fr;
    min-height: auto;
  }
  
  .media-section {
    height: 400px;
  }
  
  .content-section {
    padding: 2rem;
  }
}
</style>