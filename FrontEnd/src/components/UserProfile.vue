  <!-- src/components/UserProfile.vue -->
  <template>
    <!-- <div class="profile-bg-container"></div> -->
    <div class="user-profile-container">
      <!-- 用户信息卡片 -->
      <div class="user-card glassmorphism-effect">
        <div class="avatar-container" @click="goToHomePage">
          <img
            :src="user.userAvatar"
            alt="用户头像"
            class="avatar"
          />
        </div>
        <div class="user-meta">
          <h2 class="username">{{ user.username }}</h2>
          <p class="signature" v-if="user.signature">{{ user.signature }}</p>
          <div class="hobbies-section">
            <h3>兴趣爱好</h3>
            <ul v-if="user.hobbies && user.hobbies.length">
              <li v-for="hobby in user.hobbies" :key="hobby">{{ hobby }}</li>
            </ul>
            <p v-else class="no-hobbies">暂无爱好信息</p>
          </div>
        </div>
      </div>

      <!-- 日记列表 -->
      <div class="diaries-section glassmorphism-effect">
        <h2 class="section-title">我的日记</h2>
        <div v-if="diariesLoading" class="loading">✨ 加载中...</div>
        <div v-else>
          <transition-group name="diary-list" tag="div">
            <div 
              v-for="diary in diaries"
              :key="diary.id"
              class="diary-card"
            >
              <div class="diary-content">
                <h3 class="diary-title">{{ diary.title || "无标题日记" }}</h3>
                <p class="diary-text">{{ truncatedContent(diary.content) }}</p>
                <div v-if="diary.images || diary.videos" class="media-grid">
                  <div 
                    v-for="(img,index) in diary.images"
                    :key="'img-'+index"
                    class="media-item"
                  >
                    <img :src="img" alt="日记图片" class="media-image" @click="openLightbox(img)">
                  </div>
                  <div
                    v-for="(video,index) in diary.videos"
                    :key="'video-'+index"
                    class="media-item"
                  >
                    <video controls class="media-video" >
                      <source :src="video" type="video/mp4" />
                      您的浏览器不支持视频播放
                    </video>
                  </div>
                </div>
                
                <div class="diary-footer">
                  <div class="meta-info">
                    <span class="views">
                      <i class="icon-eye"></i> views: {{ diary.views || 0 }}
                    </span>
                    <span class="rating">
                      <i class="icon-star"></i> rating: {{ diary.rating?.toFixed(1) || 0.0 }}
                    </span>
                  </div>
                  <!-- <span class="post-time">{{ formatDate(diary.createdAt) }}</span> -->
                </div>
              </div>
            </div>
          </transition-group>
          <p v-if="!diaries.length" class="no-diaries">暂时还没有写过日记哦~</p>
        </div>
      </div>
    </div>
  </template>

  <script>
  import { mapState } from 'vuex'
  import axios from 'axios'

  export default {
    name: 'UserProfile',
    data() {
      return {
        diaries: [],
        diariesLoading: true,
      }
    },
    computed: {
      ...mapState(['user'])
    },
    watch: {
      'user.username': {
        immediate: true,
        handler(newVal) {
          if (newVal) this.fetchDiaries()
        }
      }
    },
    methods: {
      async fetchDiaries() {
        try {
          this.diariesLoading = true
          const { data } = await axios.get(
            `http://localhost:8000/diaries/${this.user.username}`
          )
          console.log('日记加载成功1:', data)
          this.diaries = data.diaries
          console.log('日记加载成功2:', this.diaries)
        } catch (error) {
          console.error('日记加载失败:', error)
          this.diaries = []
        } finally {
          this.diariesLoading = false
        }
      },
      truncatedContent(text) {
        return text?.length > 100 ? text.slice(0, 100) + '...' : text
      },
      formatDate(timestamp) {
        return new Date(timestamp).toLocaleDateString()
      },
      goToHomePage() {
        this.$router.push({ name: 'Recommend' })
      }
    }
  }
  </script>

  <style scoped>
  /* 背景样式 */
.profile-bg-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 2rem 0;
}

/* 毛玻璃效果 */
.glassmorphism-effect {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
}

/* 多媒体网格布局 */
.media-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  margin: 1.5rem 0;
}

.media-item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.media-item:hover {
  transform: translateY(-3px);
}

.media-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  cursor: zoom-in;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.media-video {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  background: #000;
}

  .user-profile-container {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
  }

  /* 用户卡片样式 */
  .user-card {
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    padding: 2rem;
    display: flex;
    gap: 2rem;
    margin-bottom: 3rem;
  }

  .avatar-container {
    flex-shrink: 0;
    cursor: pointer;
    transition: transform 0.2s ease;
  }

  .avatar-container:hover {
    transform: scale(1.05);
  }

  .avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #f0f2f5;
  }

  .user-meta {
    flex-grow: 1;
  }

  .username {
    font-size: 2rem;
    margin: 0 0 0.5rem;
    color: #1a1a1a;
  }

  .signature {
    font-size: 1rem;
    color: #666;
    margin-bottom: 1.5rem;
  }

  .hobbies-section h3 {
    font-size: 1.1rem;
    color: #333;
    margin-bottom: 0.5rem;
  }

  .hobbies-section ul {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .hobbies-section li {
    background: #f0f2f5;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.9rem;
  }

  /* 日记列表样式 */
  .diaries-section {
    background: #fff;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  }

  .section-title {
    font-size: 1.5rem;
    color: #1a1a1a;
    margin: 0 0 2rem;
  }

  .diary-card {
    background: #fafafa;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    transition: transform 0.2s ease;
  }

  .diary-card:hover {
    transform: translateY(-2px);
  }

  .diary-content {
    padding: 1.5rem;
  }

  .diary-title {
    font-size: 1.2rem;
    margin: 0 0 1rem;
    color: #2c3e50;
  }

  .diary-text {
    color: #666;
    line-height: 1.6;
    margin: 0 0 1.5rem;
  }

  /* 添加加载动画 */
.loading {
  position: relative;
  font-size: 1.2rem;
}

.loading::after {
  content: "";
  animation: loading 1s infinite;
  margin-left: 0.5rem;
}

@keyframes loading {
  0% { content: "·"; }
  33% { content: "··"; }
  66% { content: "···"; }
}


  .diary-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.9rem;
  }

  .meta-info {
    display: flex;
    gap: 1.5rem;
    color: #888;
  }

  .meta-info i {
    margin-right: 0.3rem;
  }

  .post-time {
    color: #999;
  }

  .loading,
  .no-diaries {
    text-align: center;
    padding: 2rem;
    color: #888;
  }

  /* 过渡动画 */
  .diary-list-enter-active,
  .diary-list-leave-active {
    transition: all 0.4s ease;
  }

  .diary-list-enter-from,
  .diary-list-leave-to {
    opacity: 0;
    transform: translateX(30px);
  }
  </style>