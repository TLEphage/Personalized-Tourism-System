<template>
  <div class="recommend-container">
    <h1 class="page-title">🌟 发现精彩目的地</h1>
    <swiper/>

    <div class="tabs-container">
      <div 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-item', { 'active': activeTab === tab.id }]"
        @click="switchTab(tab.id)"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        {{ tab.label }}
      </div>
    </div>

    <!-- 搜索和排序容器 -->
    <div class="search-sort-container">
      <div class="search-box">
        <div class="search-icon">🔍</div>
        <input
          type="text"
          v-model="currentSearchQuery"
          placeholder="输入关键词进行搜索"
          class="search-input"
          @input="handleSearchInput"
          @keyup.enter="fetchList"
        >
      </div>
      <div v-if="activeTab !== 'foods'" class="sort-selector">
        <select v-model="currentSortBy" @change="fetchList" class="sort-select">
          <option value="popularity">按人气排序</option>
          <option value="rating">按评分排序</option>
        </select>
        <span class="sort-icon">▼</span>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content-container">
      <!-- 景点/学校/推荐景点列表 -->
      <div v-if="activeTab !== 'foods'" class="spot-grid">
        <h2 class="section-title">
          <span class="icon">{{ currentTabIcon }}</span>
          {{ currentTabTitle }}
          <span v-if="activeTab === 'spots'" class="sub">(根据用户评分实时更新)</span>
        </h2>

        <div v-if="loading" class="loading">
          <div class="loader"></div>
          正在加载精彩内容...
        </div>

        <div v-else-if="error" class="error-message">{{ error }}</div>

        <div v-else-if="list.length === 0" class="no-results">
          未找到与 "{{ currentSearchQuery }}" 相关的内容
        </div>

        <!-- 普通景点/学校列表 -->
        <div v-if="!isRecommendTab" class="spot-grid-content">
          <div v-for="(item, index) in list"
              :key="item.id"
              class="spot-card"
              @click="gotoDetailPage(item.name, activeTab)">
            <div class="card-header">
              <img :src="item.url"
                  :alt="item.name"
                  class="spot-image">
              <div class="ranking-badge">TOP {{ index + 1 }}</div>
              <div class="rating">
                ⭐ {{ item.rating?.toFixed(2) }}
                <span class="reviews">(热度{{ item.popularity }})</span>
              </div>
            </div>

            <div class="card-body">
              <h3 class="spot-name">{{ item.name }}</h3>
              <p class="spot-location">📍 {{ item.location }}</p>
              <p class="spot-description">{{ truncateDescription(item.description) }}</p>

              <div class="tags">
                <span v-for="(tag, tagIndex) in item.tags"
                      :key="tagIndex"
                      class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>

            <div class="card-footer">
              <div class="price">
                {{ item.price_range || '免费参观' }}
              </div>
              <div class="open-time">
                🕒 {{ item.open_hours?.weekday }}
              </div>
            </div>
          </div>
        </div>

        <!-- 推荐景点/学校列表（特殊展示） -->
        <div v-else class="recommend-grid-content">
          <div v-for="(rec, index) in list"
              :key="rec.item.id"
              class="recommend-card"
              @click="gotoDetailPage(rec.item.name, activeTab)">
            <div class="card-header">
              <img :src="rec.item.url"
                  :alt="rec.item.name"
                  class="spot-image">
              <div class="recommend-badge">推荐 {{ index + 1 }}</div>
              <div class="rating">
                ⭐ {{ rec.item.rating?.toFixed(1) }}
                <span class="reviews">(热度{{ rec.item.popularity }})</span>
              </div>
            </div>

            <div class="card-body">
              <h3 class="spot-name">{{ rec.item.name }}</h3>
              <p class="spot-location">📍 {{ rec.item.location }}</p>
              <p class="spot-description">{{ truncateDescription(rec.item.description) }}</p>

              <div class="recommend-scores">
                <div class="score-item">
                  <span class="score-label">匹配度:</span>
                  <span class="score-value">{{ (rec.match_score).toFixed(1) }}%</span>
                </div>
                <div class="score-item">
                  <span class="score-label">推荐指数:</span>
                  <span class="score-value">{{ rec.final_score.toFixed(2) }}</span>
                </div>
              </div>

              <div class="tags">
                <span v-for="(tag, tagIndex) in rec.item.tags"
                      :key="tagIndex"
                      class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>

            <div class="card-footer">
              <div class="price">
                {{ rec.item.price_range || '免费参观' }}
              </div>
              <div class="open-time">
                🕒 {{ rec.item.open_hours?.weekday }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 美食列表 -->
      <div v-else class="food-section">
        <h2 class="section-title">
          <span class="icon">🍜</span> 发现美食
        </h2>
        
        <div v-if="foodLoading" class="loading">
          <div class="loader"></div>
          正在搜索美食...
        </div>
        
        <div v-else-if="foodError" class="error-message">{{ foodError }}</div>
        
        <div v-else-if="!foodList.length && currentSearchQuery && !foodInitialLoad" class="no-results">
          未找到与 "{{ currentSearchQuery }}" 相关的美食。
        </div>
        
        <div v-else-if="!foodList.length && !currentSearchQuery && !foodInitialLoad" class="no-results">
          请输入关键词搜索美食。
        </div>
        
        <div v-else class="food-grid">
          <div v-for="food in foodList" :key="food.restaurant_name + food.address" class="food-card">
            <h3 class="food-name">{{ food.restaurant_name }}</h3>
            <p class="food-address">📍 {{ food.address }}</p>
            <p class="food-description">{{ truncateDescription(food.description, 45) }}</p>
            <div class="food-details">
              <span class="food-rating">⭐ {{ food.rating.toFixed(2) }}</span>
              <span class="food-popularity">(热度{{ food.popularity }})</span>
            </div>
            <div class="tags">
              <span v-for="(tag, tagIndex) in food.tags"
                    :key="tagIndex"
                    class="tag food-tag">
                {{ tag }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
import swiper from '../components/swiper.vue';

export default {
  name: 'Recommend',
  components: { swiper },
  data() {
    return {
      tabs: [
        { id: 'spots', label: '热门景点', icon: '🏆', placeholder: '搜索景点名称...' },
        { id: 'schools', label: '热门学校', icon: '🎓', placeholder: '搜索学校名称...' },
        { id: 'foods', label: '发现美食', icon: '🍜', placeholder: '搜索美食/餐厅...' },
        { id: 'recommend_scenic_spots', label: '推荐景点', icon: '🌟', placeholder: '搜索景点名称...' },
        { id: 'recommend_schools', label: '推荐学校', icon: '🌟', placeholder: '搜索学校名称...' }
      ],
      activeTab: 'spots',
      currentSearchQuery: '',
      currentSortBy: 'popularity',
      currentPlaceholder: '搜索景点名称...',
      list: [],
      loading: true,
      error: null,
      foodList: [],
      foodLoading: false,
      foodError: null,
      foodInitialLoad: true
    }
  },
  computed: {
    currentTabTitle() {
      const tab = this.tabs.find(t => t.id === this.activeTab);
      return tab ? tab.label : '';
    },
    currentTabIcon() {
      const tab = this.tabs.find(t => t.id === this.activeTab);
      return tab ? tab.icon : '';
    },
    currentTabPlaceholder() {
      const tab = this.tabs.find(t => t.id === this.activeTab);
      return tab ? tab.placeholder : '';
    },
    isRecommendTab() {
      return this.activeTab === 'recommend_scenic_spots' || this.activeTab === 'recommend_schools';
    }
  },
  watch: {
    currentSearchQuery() {
      this.debouncedFetch();
    },
    currentSortBy() {
      this.fetchList();
    },
  },
  created() {
    // 防抖函数（500ms）
    this.debouncedFetch = this.debounce(() => {
      this.fetchList();
    }, 500);
  },
  mounted() {
    this.fetchList();
  },
  methods: {
    switchTab(tabId) {
      this.activeTab = tabId;
      this.currentSearchQuery = '';
      this.currentSortBy = 'popularity';
      this.fetchList();
    },
    async fetchList() {
      if (this.activeTab === 'foods') {
        this.fetchFoodList();
        return ;
      }
      try {
        this.loading = true;
        let searchQuery = this.currentSearchQuery ? this.currentSearchQuery.trim() : "__all__";
        console.log('请求的景点/学校关键词:', searchQuery);
        if(this.activeTab === 'spots') {
          // GET     /spots/scenic_spots/{name}?tag=...&sort_key=...&sort_order=...  -> 获取景点
          const response = await axios.get(`http://localhost:8000/spots/scenic_spots/${searchQuery}?sory_key=${this.currentSortBy}&sort_order=desc`);
          this.list = response.data;
        } else if(this.activeTab === 'schools') {
          // GET     /spots/schools/{name}?tag=...&sort_key=...&sort_order=...       -> 获取校园
          const response = await axios.get(`http://localhost:8000/spots/schools/${searchQuery}?sory_key=${this.currentSortBy}&sort_order=desc`);
          this.list = response.data;
        } else if(this.activeTab === 'recommend_scenic_spots') {
          // GET     /recommend/{username}                           -> 根据用户hobbies以及内容的评分和热度推荐相关内容，包括景点、校园、美食、日记
          const response = await axios.get(`http://localhost:8000/recommend/${this.$store.state.user.username}`);
          this.list = response.data.scenic_spots;
          console.log('推荐景点数据:', this.list);
          // console.log('test:', this.list[0].item.name);
        } else if(this.activeTab === 'recommend_schools') {
          // GET     /recommend/{username}                           -> 根据用户hobbies以及内容的评分和热度推荐相关内容，包括景点、校园、美食、日记
          const response = await axios.get(`http://localhost:8000/recommend/${this.$store.state.user.username}`);
          this.list = response.data.schools;
          console.log('推荐学校数据:', this.list);
        }
      } catch (error) {
        console.error('获取数据失败:', error);
        this.error = '无法加载数据，请稍后重试';
        this.list = [];
      } finally {
        this.loading = false;
      }
    },
    handleSearchInput() {
      clearTimeout(this.timeoutId);
    },
    debounce(fn, delay) {
      return (...args) => {
        clearTimeout(this.timeoutId);
        this.timeoutId = setTimeout(() => {
          fn.apply(this, args);
        }, delay);
      };
    },
    truncateDescription(desc) {
      return desc?.length > 60 ? desc.slice(0, 60) + '...' : desc;
    },
    gotoDetailPage(name, tab) {
      console.log('点击了卡片，跳转到详情页:', name);
      let type;
      if(tab === 'schools' || tab === 'recommend_schools') {
        type = 'schools';
      } else if(tab === 'spots' || tab === 'recommend_scenic_spots') {
        type = 'scenic_spots';
      } else {
        console.error('未知的tab类型:', tab);
        return;
      }
      this.$router.push({ name: 'SpotDetail', params: { name, type } });
    },
    async fetchFoodList() {
      try {
        this.foodLoading = true;
        this.foodError = null;
        console.log('请求的美食关键词:', this.currentSearchQuery);
        const response = await axios.post(
          `http://localhost:8000/foods/search`, {
            longitude: 116.36,
            latitude: 39.96,
            search_text: this.currentSearchQuery,
            tags: [""],
            sort_key: "distance"
          }
        );
        console.log('获取美食数据成功:', response.data);
        this.foodList = response.data;
      } catch (error) {
        console.error('获取美食数据失败:', error);
        this.foodError = "无法加载美食数据，请稍后再试";
        this.foodList = [];
      } finally {
        this.foodLoading = false;
      }
    }
  }
}
</script>
  
<style scoped>
.recommend-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.page-title {
  text-align: center;
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 1.5rem;
}

/* 标签导航样式 */
.tabs-container {
  display: flex;
  justify-content: center;
  margin: 2rem 0 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.tab-item {
  padding: 1rem 2rem;
  margin: 0 0.5rem;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 500;
  color: #718096;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.tab-item:hover {
  color: #4a6fff;
}

.tab-item.active {
  color: #4a6fff;
  border-bottom-color: #4a6fff;
}

.tab-icon {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

/* 搜索和排序容器 */
.search-sort-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0 1rem;
  padding: 0.5rem;
}

.search-box {
  flex-grow: 1;
  max-width: 500px;
  display: flex;
  align-items: center;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 25px;
  padding-left: 15px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.search-box:focus-within {
  border-color: #4a6fff;
  box-shadow: 0 0 0 3px rgba(74, 111, 255, 0.1);
}

.search-icon {
  color: #a0aec0;
  font-size: 1.1rem;
  margin-right: 8px;
}

.search-input {
  flex-grow: 1;
  padding: 12px 15px 12px 0;
  border: none;
  border-radius: 0 25px 25px 0;
  font-size: 16px;
  outline: none;
  background-color: transparent;
}

/* 排序选择器 */
.sort-selector {
  position: relative;
  display: flex;
  align-items: center;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 25px;
  padding-right: 10px;
}

.sort-select {
  padding: 10px 25px 10px 15px;
  border: none;
  border-radius: 25px;
  font-size: 15px;
  background-color: transparent;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  outline: none;
  cursor: pointer;
}

.sort-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
  pointer-events: none;
}

.sort-selector:focus-within, .sort-select:focus {
  border-color: #4a6fff;
  box-shadow: 0 0 0 3px rgba(74, 111, 255, 0.1);
}

/* 主内容区域 */
.main-content-container {
  margin-top: 2rem;
}

.section-title {
  font-size: 1.8rem;
  color: #4a5568;
  margin: 2rem 0 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.section-title .sub {
  font-size: 1rem;
  color: #718096;
}

/* 景点/学校/推荐景点网格 */
.spot-grid-content {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.spot-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  overflow: hidden;
}

.spot-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 12px rgba(0, 40, 120, 0.1);
}

.card-header {
  position: relative;
  height: 200px;
}

.spot-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px 12px 0 0;
}

.ranking-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: rgba(255, 215, 0, 0.9);
  color: #2d3748;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: bold;
}

.rating {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-weight: 600;
  color: #2d3748;
}

.rating .reviews {
  font-size: 0.8em;
  color: #718096;
}

.card-body {
  padding: 1.5rem;
}

.spot-name {
  font-size: 1.3rem;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.spot-location {
  color: #4a5568;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.spot-description {
  color: #718096;
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #f0f4ff;
  color: #4a6fff;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

.price {
  color: #38a169;
  font-weight: bold;
}

.open-time {
  color: #718096;
  font-size: 0.9rem;
}

/* 美食网格 */
.food-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 550px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.food-grid::-webkit-scrollbar {
  width: 6px;
}

.food-grid::-webkit-scrollbar-thumb {
  background-color: #cbd5e0;
  border-radius: 3px;
}

.food-grid::-webkit-scrollbar-track {
  background-color: #edf2f7;
}

.food-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.06);
  padding: 1rem 1.25rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.food-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 10px rgba(0,0,0,0.08);
}

.food-name {
  font-size: 1.15rem;
  color: #334155;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.food-address {
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 0.6rem;
  display: flex;
  align-items: center;
}

.food-address::before {
  content: '📍';
  margin-right: 0.3em;
}

.food-description {
  font-size: 0.9rem;
  color: #475569;
  line-height: 1.5;
  margin-bottom: 0.75rem;
}

.food-details {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  font-size: 0.85rem;
  color: #475569;
  margin-bottom: 0.75rem;
}

.food-rating {
  font-weight: 500;
  color: #f59e0b;
}

.food-popularity {
  color: #64748b;
  font-size: 0.8rem;
}

.food-tag {
  background: #e0f2fe;
  color: #0ea5e9;
  font-size: 0.8rem;
  font-weight: 500;
  padding: 0.25rem 0.75rem;
}

/* 加载和错误状态 */
.loading {
  text-align: center;
  padding: 2rem;
  color: #4a5568;
}

.loader {
  display: inline-block;
  width: 2rem;
  height: 2rem;
  border: 3px solid #e2e8f0;
  border-radius: 50%;
  border-top-color: #4a6fff;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

.error-message, .no-results {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error-message {
  color: #ef4444;
  font-weight: 500;
}

.no-results {
  color: #64748b;
  font-style: italic;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .tabs-container {
    flex-wrap: wrap;
  }
  
  .tab-item {
    padding: 0.8rem 1.2rem;
    margin: 0.3rem;
    font-size: 1rem;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .tabs-container {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  
  .tab-item {
    width: 100%;
    text-align: center;
    justify-content: center;
    border-bottom: none;
    border-left: 3px solid transparent;
  }
  
  .tab-item.active {
    border-left-color: #4a6fff;
    border-bottom: none;
  }
  
  .search-sort-container {
    flex-direction: column;
  }
  
  .search-box {
    width: 100%;
    max-width: none;
  }
  
  .sort-selector {
    width: 100%;
  }
  
  .spot-grid-content {
    grid-template-columns: 1fr;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
}

.recommend-grid-content {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.recommend-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  overflow: hidden;
  position: relative;
  border: 1px solid #e0f2fe;
}

.recommend-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 12px rgba(0, 40, 120, 0.1);
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
  border-bottom: 1px solid #e2e8f0;
  margin-top: 0.5rem;
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
  .recommend-grid-content,
  .spot-grid-content {
    grid-template-columns: 1fr;
  }
  
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