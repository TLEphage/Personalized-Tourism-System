<template>
    <div class="recommend-container">
      <h1 class="page-title">🌟 发现精彩目的地</h1>
      <swiper/>

      <!-- 搜索框 -->
      <div class="search-container">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="请输入景点名称..."
          class="search-input"
          @input="handleSearchInput"
        >
      </div>

      <!-- 热门景点排行 -->
      <div class="spots-section">
        <h2 class="section-title">
          <span class="icon">🏆</span> 
          热门景点排行榜
          <span class="sub">(根据用户评分实时更新)</span>
        </h2>
        
        <div v-if="loading" class="loading">
          <div class="loader"></div>
          正在加载精彩内容...
        </div>
  
        <div v-else class="spot-grid">
          <div v-for="(spot, index) in rankingList" 
               :key="spot.id"
               class="spot-card"
               
              >
            <div class="card-header">
              <img :src="spot.image" 
                   :alt="spot.name"
                   class="spot-image">
              <div class="ranking-badge">TOP {{ index + 1 }}</div>
              <div class="rating">
                ⭐ {{ spot.rating.toFixed(1) }}
                <span class="reviews">({{ spot.popularity }}人评价)</span>
              </div>
            </div>
            
            <div class="card-body">
              <h3 class="spot-name">{{ spot.name }}</h3>
              <p class="spot-location">📍 {{ spot.location }}</p>
              <p class="spot-description">{{ truncateDescription(spot.description) }}</p>
              
              <div class="tags">
                <span v-for="(tag, tagIndex) in spot.tags" 
                      :key="tagIndex"
                      class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
  
            <div class="card-footer">
              <div class="price">
                {{ spot.price_range || '免费参观' }}
              </div>
              <div class="open-time">
                🕒 {{ spot.open_hours.weekday }}
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
        searchQuery: '',
        timeoutId: null,
        rankingList: [],
        loading: true,
        error: null
      }
    },
    watch: {
      searchQuery(newVal) {
        this.debouncedFetch(newVal);
      }
    },
    created() {
      // 防抖函数（500ms）
      this.debouncedFetch = this.debounce((name) => {
        this.fetchRankingList(name);
      }, 500);
    },
    mounted() {
      this.fetchRankingList();
    },
    methods: {
      async fetchRankingList(name = '') {
        try {
          this.loading = true;
          const response = await axios.get(`http://localhost:8000/spots/${name}`);
          console.log('请求参数:', name);
          console.log('获取景点数据成功:', response.data);
          this.rankingList = response.data;
          this.error = null;
        } catch (error) {
          console.error('获取景点数据失败:', error);
          this.error = '无法加载景点数据，请稍后重试';
          this.rankingList = [];
        } finally {
          this.loading = false;
        }
      },
      handleSearchInput() {
        // 清除之前的定时器
        clearTimeout(this.timeoutId);
        // 显示实时清除按钮的逻辑可以在此扩展
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
        return desc.length > 60 ? desc.slice(0, 60) + '...' : desc;
      },
      gotoDetailPage(spotId) {
        this.$router.push({ name: 'Detail', params: { spotId } });
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

  .search-container {
  margin: 2rem 0;
  text-align: center;
}

.search-input {
  width: 80%;
  max-width: 500px;
  padding: 12px 24px;
  border: 2px solid #e2e8f0;
  border-radius: 30px;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
}

.search-input:focus {
  border-color: #4a6fff;
  box-shadow: 0 2px 8px rgba(74, 111, 255, 0.1);
}
  
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
  
  .spot-grid {
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
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  @media (max-width: 768px) {
    .spot-grid {
      grid-template-columns: 1fr;
    }
    
    .page-title {
      font-size: 2rem;
    }
  }
  </style>