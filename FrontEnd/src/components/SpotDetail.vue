<template>
    <div class="spot-detail-container">
      <!-- 返回按钮 -->
      <div class="back-button">
        <button @click="goBack">
          <span class="icon">⬅️</span> 返回
        </button>
      </div>
  
      <!-- 加载中状态 -->
      <div v-if="loading" class="loading">
        <div class="loader"></div>
        <p>正在加载景点详情...</p>
      </div>
  
      <!-- 错误状态 -->
      <div v-else-if="error" class="error">
        <p>❌ {{ error }}</p>
        <button @click="fetchSpotDetail(name)">重试</button>
      </div>
  
      <!-- 景点详情内容 -->
      <div v-else class="spot-detail-content">
        <!-- 景点主图和基本信息 -->
        <div class="spot-header">
          <img :src="spot.url" :alt="spot.name" class="spot-main-image">
          <div class="spot-basic-info">
            <h1 class="spot-name">{{ spot.name }}</h1>
            <div class="spot-rating">
              <span class="stars">
                <span v-for="i in 5" :key="i" class="star">
                  {{ i <= spot.rating ? '★' : '☆' }}
                </span>
              </span>
              <span class="rating-value">{{ spot.rating.toFixed(1) }}</span>
              <span class="rating-count">({{ spot.popularity }}人评价)</span>
            </div>
            <div class="spot-tags">
              <span v-for="(tag, index) in spot.tags" :key="index" class="tag">{{ tag }}</span>
            </div>
          </div>
        </div>
  
        <!-- 景点详情内容 -->
        <div class="spot-info-section">
          <h2 class="section-title">景点介绍</h2>
          <p class="spot-description">{{ spot.description }}</p>
        </div>
  
        <!-- 景点地址和开放时间 -->
        <div class="spot-info-section">
          <div class="info-item">
            <span class="info-label">📍 地址：</span>
            <span class="info-value">{{ spot.location }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">🕒 开放时间：</span>
            <span class="info-value">{{ spot.open_hours.weekday }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">💰 门票：</span>
            <span class="info-value">{{ spot.price_range || '免费参观' }}</span>
          </div>
        </div>
  
        <!-- 用户评论 -->
        <!-- <div class="spot-info-section">
          <h2 class="section-title">游客评论</h2>
          <div v-if="spot.reviews && spot.reviews.length > 0" class="reviews-container">
            <div v-for="(review, index) in spot.reviews" :key="index" class="review-card">
              <div class="review-header">
                <span class="reviewer-name">{{ review.user.name }}</span>
                <span class="review-date">{{ review.date }}</span>
              </div>
              <div class="review-rating">
                <span class="stars">
                  <span v-for="i in 5" :key="i" class="star">
                    {{ i <= review.rating ? '★' : '☆' }}
                  </span>
                </span>
                <span class="rating-value">{{ review.rating }}</span>
              </div>
              <p class="review-content">{{ review.content }}</p>
            </div>
          </div>
          <div v-else class="no-reviews">
            <p>暂无评论，快来抢沙发吧！</p>
          </div>
        </div> -->
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'SpotDetail',
    data() {
      return {
        spot: {},
        loading: true,
        error: null,
        name: ''
      };
    },
    created() {
      this.name = this.$route.params.name;
      this.fetchSpotDetail(this.name);
      console.log('获取景点详情的参数:', this.name);
    },
    methods: {
      async fetchSpotDetail(name) {
        try {
          this.loading = true;
          console.log('请求参数:', name);
          const response = await axios.get(`http://localhost:8000/spots/${name}`);
          console.log('获取景点详情成功:', response.data);
          this.spot = response.data[0];
          this.error = null;
        } catch (error) {
          console.error('获取景点详情失败:', error);
          this.error = '无法加载景点详情，请稍后重试';
        } finally {
          this.loading = false;
        }
      },
      goBack() {
        this.$router.go(-1);
      }
    }
  };
  </script>
  
  <style scoped>
  .spot-detail-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
    font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  }
  
  .back-button {
    margin-bottom: 1.5rem;
  }
  
  .back-button button {
    background: none;
    border: none;
    font-size: 1rem;
    cursor: pointer;
    color: #4a6fff;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .loading,
  .error {
    text-align: center;
    padding: 2rem;
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
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .error button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: #4a6fff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .spot-header {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .spot-main-image {
    width: 100%;
    height: 300px;
    object-fit: cover;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  .spot-basic-info {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .spot-name {
    font-size: 2rem;
    color: #2d3748;
    margin: 0;
  }
  
  .spot-rating {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .stars {
    color: #f9a826;
    font-size: 1.2rem;
  }
  
  .rating-value {
    font-size: 1.2rem;
    font-weight: bold;
    color: #2d3748;
  }
  
  .rating-count {
    font-size: 0.9rem;
    color: #718096;
  }
  
  .spot-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .tag {
    background-color: #f0f4ff;
    color: #4a6fff;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
  }
  
  .spot-info-section {
    background-color: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }
  
  .section-title {
    font-size: 1.5rem;
    color: #2d3748;
    margin-top: 0;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .spot-description {
    color: #4a5568;
    line-height: 1.6;
    font-size: 1rem;
  }
  
  .info-item {
    margin-bottom: 0.8rem;
  }
  
  .info-label {
    font-weight: bold;
    color: #2d3748;
    min-width: 100px;
    display: inline-block;
  }
  
  .info-value {
    color: #4a5568;
  }
  
  .spot-gallery {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .gallery-image {
    width: 100%;
    height: 150px;
    object-fit: cover;
    border-radius: 8px;
    transition: transform 0.3s ease;
    cursor: pointer;
  }
  
  .gallery-image:hover {
    transform: scale(1.05);
  }
  
  .reviews-container {
    margin-top: 1rem;
  }
  
  .review-card {
    background-color: #f8fafc;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
  }
  
  .review-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }
  
  .reviewer-name {
    font-weight: bold;
    color: #2d3748;
  }
  
  .review-date {
    color: #718096;
    font-size: 0.85rem;
  }
  
  .review-rating {
    margin-bottom: 0.5rem;
  }
  
  .review-content {
    color: #4a5568;
    line-height: 1.5;
    font-size: 0.95rem;
  }
  
  .no-reviews {
    text-align: center;
    padding: 2rem;
    color: #718096;
  }
  
  @media (max-width: 768px) {
    .spot-header {
      grid-template-columns: 1fr;
    }
    
    .spot-main-image {
      height: 200px;
    }
    
    .spot-gallery {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  </style>