  <!-- src/components/UserProfile.vue -->
  <template>
    <!-- <div class="profile-bg-container"></div> -->
    <div class="user-profile-container">
      <!-- 用户信息卡片 -->
      <div class="user-card glassmorphism-effect">
        <div class="avatar-container" @click="goToHomePage">
          <img
            :src="user.avatarPath"
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
        <div class="action-buttons">
          <button class="edit-btn" @click="showAvatarEditor = true">
            <i class="icon-camera"></i>
            更换头像
          </button>
          <button class="edit-btn" @click="showSignatureEditor = true">
            <i class="icon-edit"></i>
            编辑签名
          </button>
          <button class="edit-btn" @click="gotoInterestSelector">
            <i class="icon-tag"></i>
            修改兴趣
          </button>
        </div>
      </div>
      
      <!-- 头像编辑弹窗 -->
      <transition name="modal">
        <div v-if="showAvatarEditor" class="modal-mask">
          <div class="modal-wrapper">
            <div class="modal-container">
              <h3>更换头像</h3>
              <ImageUpload @uploaded="handleAvatarUpload"/>
              <button class="modal-close" @click="showAvatarEditor = false">
                ×
              </button>
            </div>
          </div>
        </div>
      </transition>

      <!-- 签名编辑弹窗 -->
      <transition name="modal">
        <div v-if="showSignatureEditor" class="modal-mask">
          <div class="modal-wrapper">
            <div class="modal-container">
              <h3>编辑个性签名</h3>
              <textarea v-model="editableSignature" rows="3"></textarea>
              <div class="modal-actions">
                <button @click="saveSignature">保存</button>
                <button @click="showSignatureEditor = false">取消</button>
              </div>
            </div>
          </div>
        </div>
      </transition>


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
  import { mapState } from 'vuex';
  import axios from 'axios';

  export default {
    name: 'UserProfile',
    data() {
      return {
        diaries: [],
        diariesLoading: true,
        showAvatarEditor: false,
        editableSignature: this.user?.signature || '',
        showSignatureEditor: false,
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
          console.log('avatar',this.user.avatarPath);
          const { data } = await axios.get(
            `http://localhost:8000/diaries/${this.user.username}?sort_key=data&sort_order=desc`
          )
          this.diaries = data.diaries
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
      },
      gotoInterestSelector() {
        this.$router.push({name: 'InterestSelector'});
      },
      async handleAvatarUpload(url) {
        try {
          const response = await axios.put(`http://localhost:8000/user/${this.user.username}/details`, {
            signature: this.user.signature,
            hobbies: this.user.hobbies,
            avatarPath: url
          })
          if (response.data.message === '用户信息更新成功') {
            alert('头像更新成功！');
            this.$store.commit('setUser', {
              ...response.data.user,
              isLoggedIn: true
            });
          } else {
            alert('头像更新失败，请重试！');
          }
        } catch (error) {
          console.error('头像上传失败:', error)
        } finally {
          this.showAvatarEditor = false
        }
      },
      async saveSignature() {
        try {
          const response = await axios.put(`http://localhost:8000/users/${this.user.username}/details`,{
            signature: this.editableSignature,
            hobbies: this.user.hobbies,
            avatarPath: this.user.avatarPath
          })
          if (response.data.message === '用户信息更新成功') {
            alert('个性签名更新成功！');
            this.$store.commit('setUser', {
              ...response.data.user,
              isLoggedIn: true
            });
          } else {
            alert('个性签名更新失败，请重试！');
          }
        } catch (error) {
          console.error('签名保存失败:', error)
        } finally {
          this.showSignatureEditor = false
        }
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
  max-width: 1400px;
  padding: 2rem 3rem;
}

.user-card {
  width: 80%;
  margin: 2rem auto;
  padding: 3rem;
  border-radius: 24px;
  background: linear-gradient(145deg, #ffffff, #f8faff);
  box-shadow: 0 12px 40px rgba(0, 40, 120, 0.1);
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
  width: 160px;
  height: 160px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f0f2f5;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
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
  margin-top: 3rem;
  padding: 3rem;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
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

.action-buttons {
  margin-top: 2rem;
  display: flex;
  gap: 1.5rem;
  justify-content: center;
}

.edit-btn {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #4a6fff, #6b4aff);
  color: white;
  border-radius: 50px;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.edit-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(74, 111, 255, 0.3);
}

.user-card::after {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #4a6fff, #6b4aff);
  z-index: -1;
  border-radius: 24px;
  animation: gradientBorder 6s ease infinite;
}

@keyframes gradientBorder {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* 弹窗样式 */
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s;
}

.modal-container {
  width: 400px;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  position: relative;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

.modal-actions {
  margin-top: 1.5rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* 弹窗动画 */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>