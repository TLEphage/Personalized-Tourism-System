<template>
    <div class="recommend-container">
      <h1 class="page-title">🌟 发现精彩目的地</h1>
      <swiper/>

      <!-- 搜索和排序容器 -->
      <div class="search-sort-container">
        <div class="search-box">
          <div class="search-icon">🔍</div>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="搜索景点名称..."
            class="search-input"
            @input="handleSearchInput"
          >
        </div>
        <div class="sort-selector">
          <select v-model="sortBy" @change="fetchRankingList" class="sort-select">
            <option value="popularity">按人气排序</option>
            <option value="rating">按评分排序</option>
          </select>
          <span class="sort-icon">▼</span>
        </div>
      </div>

      <div class="main-content-container">
        <!-- Spots Section Wrapper (70%) -->
        <div class="spots-section-wrapper">
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
                   @click="gotoDetailPage(spot.name)"
                  >
                <div class="card-header">
                  <img :src="spot.url"
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

        <!-- Food Section Wrapper (30%) -->
        <div class="food-section-wrapper">
          <div class="food-section">
            <h2 class="section-title">
              <span class="icon">🍜</span> 发现美食
            </h2>
            <div class="food-search-box">
              <div class="search-icon">🔍</div>
              <input
                type="text"
                v-model="foodSearchQuery"
                placeholder="搜索美食/餐厅..."
                class="search-input"
              >
            </div>

            <div v-if="foodLoading" class="loading">
              <div class="loader"></div>
              正在搜索美食...
            </div>
            <div v-else-if="foodError" class="error-message">{{ foodError }}</div>
            <div v-else-if="!foodList.length && foodSearchQuery && !foodInitialLoad" class="no-results">
              未找到与 "{{ foodSearchQuery }}" 相关的美食。
            </div>
             <div v-else-if="!foodList.length && !foodSearchQuery && !foodInitialLoad" class="no-results">
              请输入关键词搜索美食。
            </div>
            <div v-else class="food-grid">
              <div v-for="food in foodList" :key="food.restaurant_name + food.address" class="food-card">
                <h3 class="food-name">{{ food.restaurant_name }}</h3>
                <p class="food-address">📍 {{ food.address }}</p>
                <p class="food-description">{{ truncateDescription(food.description, 45) }}</p>
                <div class="food-details">
                  <span class="food-rating">⭐ {{ food.rating.toFixed(1) }}</span>
                  <span class="food-popularity">({{ food.popularity }}人气)</span>
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
        sortBy: 'popularity',
        // timeoutId: null,
        rankingList: [],
        loading: true,
        error: null,
        foodSearchQuery: '',
        foodList: [],
        foodLoading: false,
        foodError: null,
        foodInitialLoad: true
      }
    },
    watch: {
      searchQuery() {
        this.debouncedFetch();
      },
      sortBy() {
        this.fetchRankingList();
      },
      foodSearchQuery() {
        this.foodInitialLoad = false;
        this.debouncedFetchFoodList();
      }
    },
    created() {
      // 防抖函数（500ms）
      this.debouncedFetch = this.debounce(() => {
        this.fetchRankingList();
      }, 500);
      this.debouncedFetchFoodList = this.debounce(() => {
        this.fetchFoodList();
      }, 500);
    },
    mounted() {
      this.fetchRankingList();
      this.fetchFoodList();
    },
    methods: {
      async fetchRankingList() {
        try {
          this.loading = true;
          let name;
          if(this.searchQuery) name = encodeURIComponent(this.searchQuery);
          else name = '__all__';
          console.log('请求的景点名称:', name);
          const response = await axios.get(`http://localhost:8000/spots/${name}?sort_key=${this.sortBy}&sort_order=desc`);
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
      gotoDetailPage(name) {
        console.log('点击了景点卡片，跳转到详情页:', name);
        this.$router.push({ name: 'SpotDetail', params: { name } });
      },
      async fetchFoodList() {
        // if(!this.foodSeatchQuery) {
        //   this.foodList = [];
        //   this.foodLoading = false;
        //   this.foodError = null;
        //   return ;
        // }
        try {
          this.foodLoading = true;
          this.foodError = null;
          const response = await axios.post(
            `http://localhost:8000/foods/search`, {
              longitude: 116.36,
              latitude: 39.96,
              search_text: this.foodSearchQuery,
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

  .sort-select {
    transition: all 0.3s ease;
  }
  .sort-select:focus {
    border-color: #4a6fff;
    box-shadow: 0 0 8px rgba(74, 111, 255, 0.2);
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

  .main-content-containter {
    display: flex;
    gap: 2rem;
    margin-top: 2.5rem;
  }

  .spots-section-wrapper {
  flex: 7; /* 70% width */
  min-width: 0; /* For flexbox item proper sizing */
}

.food-section-wrapper {
  flex: 3; /* 30% width */
  min-width: 0; /* For flexbox item proper sizing */
  background-color: #fdfdff; /* Slightly off-white background for distinction */
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  height: fit-content; /* Adjust height to content or set a max-height */
}

.food-section .section-title {
  margin-top: 0; /* Adjust title margin for food section */
  margin-bottom: 1.5rem;
  font-size: 1.6rem; /* Slightly smaller title for food section */
}
.food-section .section-title .icon {
  font-size: 1.5rem; /* Adjust icon size */
}

.food-search-box {
  display: flex; /* Align icon and input */
  align-items: center;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 25px; /* More rounded */
  padding-left: 12px;
  margin-bottom: 1.5rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.food-search-box:focus-within { /* Style when input inside is focused */
  border-color: #4a6fff;
  box-shadow: 0 0 0 3px rgba(74, 111, 255, 0.1);
}
.food-search-box .search-icon {
  color: #a0aec0;
  font-size: 1rem; /* Adjust icon size */
  padding-right: 8px;
}
.food-search-box .search-input {
  /* Remove individual styling for search-input if it conflicts */
  /* The general .search-input style might be sufficient */
  width: 100%;
  padding: 10px 12px 10px 0; /* Adjust padding */
  border: none; /* Remove border from input itself, parent has it */
  border-radius: 0 25px 25px 0;
  font-size: 15px;
  outline: none;
  background-color: transparent;
}


/* General search input class (used by both spots and food if desired) */
.search-box { /* Container for icon and input */
  display: flex;
  align-items: center;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 25px;
  padding-left: 15px; /* Space for icon */
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
  padding: 12px 15px 12px 0; /* Adjusted padding */
  border: none;
  border-radius: 0 25px 25px 0;
  font-size: 16px;
  outline: none;
  background-color: transparent;
}
/* Adjust .search-input:focus as it's now handled by .search-box:focus-within */
/* Remove .search-input:focus if you prefer the parent's focus style */
.search-input:focus {
   /* border-color: #4a6fff; */ /* Handled by parent */
   /* box-shadow: 0 2px 8px rgba(74, 111, 255, 0.1); */ /* Handled by parent */
}

.food-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 550px; /* Example max height */
  overflow-y: auto;
  padding-right: 0.5rem; /* Space for scrollbar, if any */
}
/* Custom scrollbar for food-grid (optional) */
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
  color: #334155; /* Darker text */
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.food-address {
  font-size: 0.8rem;
  color: #64748b; /* Softer color */
  margin-bottom: 0.6rem;
  display: flex;
  align-items: center;
}
.food-address::before { /* Use pseudo-element for icon if preferred */
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
  color: #f59e0b; /* Amber color for rating */
}
.food-popularity {
  color: #64748b;
  font-size: 0.8rem;
}

.food-section .tags { /* Ensure tags in food section are also styled */
  margin-top: 0.5rem; /* Add some space above tags */
}
.food-tag {
  background: #e0f2fe; /* Light blue */
  color: #0ea5e9;    /* Sky blue */
  font-size: 0.8rem;
  font-weight: 500;
  padding: 0.25rem 0.75rem;
}

.no-results, .error-message {
  text-align: center;
  color: #64748b;
  padding: 2rem 1rem;
  font-style: italic;
}
.error-message {
  color: #ef4444; /* Red for errors */
  font-style: normal;
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 1024px) { /* Adjust breakpoint for stacking */
  .main-content-container {
    flex-direction: column;
  }
  .food-section-wrapper {
    margin-top: 2rem;
  }
  .food-grid {
    max-height: none; /* Or a different max-height for smaller screens */
  }
}

@media (max-width: 768px) {
  .spot-grid {
    grid-template-columns: 1fr;
  }
  .page-title {
    font-size: 2rem;
  }
  .section-title {
    font-size: 1.5rem; /* Smaller section titles on mobile */
  }
  .food-section .section-title {
    font-size: 1.4rem;
  }
}

/* Adjust existing search-sort-container for consistency */
.search-sort-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem; /* Add gap between search and sort */
  margin: 2rem 0 1rem; /* Adjust margins */
  padding: 0.5rem; /* Add some padding */
  /* background-color: #f8fafc; /* Optional: light bg */
  /* border-radius: 8px; */
}
.search-sort-container .search-box {
  flex-grow: 1; /* Allow search box to take available space */
  max-width: 500px; /* Max width for search box */
}
.sort-selector {
  position: relative; /* For custom icon positioning */
  display: flex;
  align-items: center;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 25px;
  padding-right: 10px; /* Space for icon */
}
.sort-select {
  padding: 10px 25px 10px 15px; /* Adjust padding for icon */
  border: none;
  border-radius: 25px;
  font-size: 15px;
  background-color: transparent;
  appearance: none; /* Remove default arrow */
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
  pointer-events: none; /* Icon doesn't interfere with select */
}
.sort-selector:focus-within, .sort-select:focus {
  border-color: #4a6fff;
  box-shadow: 0 0 0 3px rgba(74, 111, 255, 0.1);
}
  </style>