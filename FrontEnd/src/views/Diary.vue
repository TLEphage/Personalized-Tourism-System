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
    <div class="diary-grid">
      <transition-group name="diary-fade">
        <article 
          v-for="diary in normalDiaries"
          :key="diary.id"
          class="diary-card"
          @click="viewDetail(diary.id)"
        >
          <!-- 封面图 -->
          <div class="diary-cover">
            <img 
              :src="diary.images[0]"
              :alt="diary.title"
              class="cover-image"
            >
            <div class="diary-meta">
              <span class="meta-item">
                <i class="fas fa-eye"></i>
                {{ formatNumber(diary.views) }}
              </span>
              <span class="meta-item">
                <i class="fas fa-star"></i>
                {{ diary.rating.toFixed(1) }}
              </span>
            </div>
          </div>

          <!-- 内容预览 -->
          <div class="diary-preview">
            <h3 class="diary-title">{{ diary.title }}</h3>
            <p class="diary-excerpt">{{ truncateContent(diary.content, 100) }}</p>
            
            <!-- 标签 -->
            <div class="diary-tags" v-if="diary.tags && diary.tags.length">
              <span 
                v-for="(tag, index) in diary.tags.slice(0, 3)" 
                :key="index"
                class="tag"
              >
                {{ tag }}
              </span>
              <span v-if="diary.tags.length > 3" class="tag more-tag">
                +{{ diary.tags.length - 3 }}
              </span>
            </div>

            <!-- 作者信息 -->
            <div class="diary-footer">
              <div class="author-info">
                <img :src="diary.avatar || '/default-avatar.jpg'" class="author-avatar">
                <span class="author-name">{{ diary.username }}</span>
              </div>
            </div>
          </div>
        </article>
      </transition-group>
    </div>

    <!-- 推荐日记卡片 -->
    <article 
      v-for="recommendDiary in recommendDiaries"
      :key="recommendDiary.item.id"
      class="recommend-diary-card"
      @click="viewDetail(recommendDiary.item.id)"
    >
      <div class="recommend-badge">推荐</div>
      
      <!-- 封面图 -->
      <div class="diary-cover">
        <img 
          :src="recommendDiary.item.images[0]"
          :alt="recommendDiary.item.title"
          class="cover-image"
        >
        <div class="diary-meta">
          <span class="meta-item">
            <i class="fas fa-eye"></i>
            {{ formatNumber(recommendDiary.item.views) }}
          </span>
          <span class="meta-item">
            <i class="fas fa-star"></i>
            {{ recommendDiary.item.rating.toFixed(1) }}
          </span>
        </div>
      </div>

      <!-- 内容预览 -->
      <div class="diary-preview">
        <h3 class="diary-title">{{ recommendDiary.item.title }}</h3>
        <p class="diary-excerpt">{{ truncateContent(recommendDiary.item.content, 100) }}</p>
        
        <!-- 推荐分数 -->
        <div class="recommend-scores">
          <div class="score-item">
            <span class="score-label">匹配度:</span>
            <span class="score-value">{{ (recommendDiary.match_score * 100).toFixed(1) }}%</span>
          </div>
          <div class="score-item">
            <span class="score-label">推荐指数:</span>
            <span class="score-value">{{ recommendDiary.final_score.toFixed(2) }}</span>
          </div>
        </div>
        
        <!-- 标签 -->
        <div class="diary-tags" v-if="recommendDiary.item.tags && recommendDiary.item.tags.length">
          <span 
            v-for="(tag, index) in recommendDiary.item.tags.slice(0, 3)" 
            :key="index"
            class="tag"
          >
            {{ tag }}
          </span>
          <span v-if="recommendDiary.item.tags.length > 3" class="tag more-tag">
            +{{ recommendDiary.item.tags.length - 3 }}
          </span>
        </div>

        <!-- 作者信息 -->
        <div class="diary-footer">
          <div class="author-info">
            <img :src="recommendDiary.item.avatar || '/default-avatar.jpg'" class="author-avatar">
            <span class="author-name">{{ recommendDiary.item.username }}</span>
          </div>
        </div>
      </div>
    </article>

    <button class="create-diary-btn" @click="showEditor = true">
      <i class="icon-plus"></i>
      新建日记
    </button>
    
    <EditDiary
      v-if="showEditor"
      :diary="editingDiary"
      :isEdit="!!editingDiary"
      @close="closeEditor"
      
    />
  </div>
</template>

<script>
import axios from 'axios';
import EditDiary from '../components/EditDiary.vue';
import ImageUpload from '../components/ImageUpload.vue';

export default{
    components:{
      EditDiary,
      ImageUpload
    },
    data(){
      return {
        diaries: [],
        searchQuery: '',
        sortBy: 'views',
        isLoading: false,
        showEditor: false,
        editingDiary: null
      }
    },
    created(){
      this.fetchDiaries();
    },
    computed:{
      // 普通日记（非推荐）
      normalDiaries() {
        return this.diaries.filter(diary => !diary.hasOwnProperty('item'));
      },
      
      // 推荐日记（带推荐分数的）
      recommendDiaries() {
        return this.diaries.filter(diary => diary.hasOwnProperty('item'));
      },
      
      filteredDiaries(){
        let filtered = this.diaries.filter(diary => {
          const diaryItem = diary.item || diary; // 统一处理普通日记和推荐日记
          const search = this.searchQuery.toLowerCase();
          return diaryItem.title.toLowerCase().includes(search) || 
                 diaryItem.content.toLowerCase().includes(search);
        });

        return filtered.sort((a, b) => {
          // 对于推荐日记，使用final_score排序
          if (a.final_score && b.final_score) {
            return b.final_score - a.final_score;
          }
          
          // 普通日记按原逻辑排序
          if(this.sortBy === 'views') return (b.item?.views || b.views) - (a.item?.views || a.views);
          if(this.sortBy === 'rating') return (b.item?.rating || b.rating) - (a.item?.rating || a.rating);
          return 0;
        });
      }
    },
    methods:{
      async fetchDiaries() {
        try {
          this.isLoading = true
          if(this.$store.state.user.username) {
            const response = await axios.get(`http://localhost:8000/recommend/${this.$store.state.user.username}`);
            this.diaries = response.data.diaries || [];
          } else {
            const { data } = await axios.get(`http://localhost:8000/diaries/__all__?sort_key=${this.sortBy}&sort_order=desc`)
            this.diaries = data.diaries
          }
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
      handleImageUpload(url) {
        this.newDiary.images.push(url);
      },
      async handleDiarySubmit(diaryData) {
        try {
          const response = await axios.post('http://localhost:8000/diaries/add', {
            ...diaryData,
            username: this.$store.state.user.username
          });
          
          if (response.data.message === '日记添加成功') {
            this.closeEditor();
            this.fetchDiaries();
          }
        } catch (error) {
          console.error('提交失败:', error);
        }
      },
      closeEditor() {
        this.showEditor = false;
        this.editingDiary = null;
      },
      handleSort() {
        this.fetchDiaries();
      },
      handleSearch() {
        this.fetchDiaries();
      },
      viewDetail(id) {
        console.log('查看日记详情id:', id)
        this.$router.push({name: 'DiaryDetail', params: {id}});
      },
      formatNumber(num) {
        if (num >= 1000000) {
          return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
          return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
      }
    }
}
</script>

<style scoped>
.diary-list-container {
  max-width: 1440px;
  margin: 2rem auto;
  padding: 0 2rem;
}

/* 搜索区域 */
.search-control {
  margin-bottom: 3rem;
  padding: 2rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.search-group {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.search-wrapper {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.search-input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
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
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
}

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

.content-section {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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

.float-btn {
  position: fixed;
  right: 40px;
  bottom: 40px;
  padding: 16px 24px;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  border: none;
  border-radius: 30px;
  font-size: 1.1rem;
  box-shadow: 0 8px 20px rgba(0, 123, 255, 0.3);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s;
}

.float-btn:hover {
  transform: translateY(-2px);
}

.diary-editor-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  width: 800px;
  max-height: 90vh;
  border-radius: 16px;
  padding: 2rem;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.close-btn {
  font-size: 2rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

input, textarea {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
}

textarea {
  resize: vertical;
}

.upload-preview {
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-cancel {
  padding: 0.8rem 1.5rem;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  color: #666;
}

.btn-submit {
  padding: 0.8rem 1.5rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.diary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin: 2rem auto;
  max-width: 1200px;
}

.diary-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.diary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

/* 封面样式 */
.diary-cover {
  position: relative;
  height: 250px;
  overflow: hidden;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.diary-card:hover .cover-image {
  transform: scale(1.05);
}

.diary-meta {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  display: flex;
  gap: 0.8rem;
  z-index: 2;
}

.meta-item {
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-item i {
  font-size: 1rem;
}

/* 内容预览 */
.diary-preview {
  flex: 1;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.diary-title {
  font-size: 1.6rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #2c3e50;
  line-height: 1.3;
}

.diary-excerpt {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #666;
  margin-bottom: 1.5rem;
  flex: 1;
}

/* 标签样式 */
.diary-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1rem 0;
}

.tag {
  background: #f0f2f5;
  color: #666;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.tag:hover {
  background: #e4e7eb;
  transform: translateY(-1px);
}

/* 底部信息 */
.diary-footer {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.author-name {
  font-weight: 500;
  color: #2c3e50;
}

.publish-date {
  color: #999;
  font-size: 0.9rem;
}

.create-diary-btn {
  position: fixed;
  right: 2rem;
  bottom: 2rem;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  border: none;
  border-radius: 30px;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  cursor: pointer;
  box-shadow: 0 8px 16px rgba(0, 123, 255, 0.2);
  transition: all 0.3s ease;
}

.create-diary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0, 123, 255, 0.3);
}

/* 动画效果 */
.diary-fade-enter-active,
.diary-fade-leave-active {
  transition: all 0.5s ease;
}

.diary-fade-enter-from,
.diary-fade-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* 响应式布局优化 */
@media (max-width: 1200px) {
  .diary-grid {
    grid-template-columns: repeat(2, 1fr);
    padding: 0 1rem;
  }
  
  .search-control {
    margin: 2rem 1rem;
  }
  
  .search-group {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .diary-grid {
    grid-template-columns: 1fr;
  }
  
  .diary-card {
    margin-bottom: 2rem;
  }
  
  .search-wrapper {
    flex-direction: column;
  }
}

.recommend-diary-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  border: 1px solid #e0f2fe;
}

.recommend-diary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.recommend-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: linear-gradient(135deg, #4a6fff, #8a2be2);
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  z-index: 2;
}

.recommend-scores {
  display: flex;
  justify-content: space-around;
  padding: 0.8rem;
  background: #f8fafc;
  border-radius: 8px;
  margin: 0.5rem 0;
  border: 1px solid #e2e8f0;
}

.score-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.score-label {
  font-size: 0.85rem;
  color: #718096;
  margin-bottom: 0.3rem;
}

.score-value {
  font-size: 1.1rem;
  font-weight: bold;
  color: #4a6fff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .recommend-scores {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .score-item {
    flex-direction: row;
    justify-content: space-between;
  }
}
</style>