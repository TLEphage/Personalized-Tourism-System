<!-- EditDiary.vue -->
<template>
    <div class="edit-diary-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEdit ? '编辑日记' : '新建日记' }}</h2>
          <button class="close-btn" @click="$emit('close')">×</button>
        </div>
  
        <form @submit.prevent="handleSubmit" class="diary-form">
          <div class="form-group">
            <label for="title">标题</label>
            <input 
              type="text" 
              id="title" 
              v-model="formData.title" 
              placeholder="请输入日记标题"
              required
            >
          </div>
  
          <div class="form-group">
            <label for="content">内容</label>
            <textarea 
              id="content" 
              v-model="formData.content" 
              placeholder="写下你的旅行故事..."
              rows="8"
              required
            ></textarea>
          </div>
  
          <div class="form-group">
            <label>图片</label>
            
            <ImageUpload 
              @uploaded="handleImageUpload"
              @clear="handleImageClear"
              @error="handleUploadError"
            />
          </div>
  
          <div class="form-group">
            <label>标签</label>
            <div class="tags-input">
              <div class="tags-container">
                <span 
                  v-for="(tag, index) in formData.tags" 
                  :key="index"
                  class="tag"
                >
                  {{ tag }}
                  <button type="button" @click="removeTag(index)" class="tag-remove">×</button>
                </span>
              </div>
              <input 
                type="text" 
                v-model="newTag"
                @keydown.enter.prevent="addTag"
                placeholder="输入标签按回车添加"
              >
            </div>
          </div>

          <div class="video-generation-section">
            <h4>视频生成</h4>
            <div class="form-group">
              <div>
                <input type="checkbox" id="generateVideoToggle" v-model="videoParams.shouldGenerate">
                <label for="generateVideoToggle" style="margin-left: 5px;">为此日记生成视频</label>
              </div>
            </div>
            
            <div v-if="videoParams.shouldGenerate">
              <div class="form-group">
                <label>生成模式</label>
                <div>
                  <input type="radio" id="qualitySpeed" value="speed" v-model="videoParams.quality">
                  <label for="qualitySpeed" style="margin-left: 5px;">速度优先</label>
                </div>
                <div>
                  <input type="radio" id="qualityQuality" value="quality" v-model="videoParams.quality">
                  <label for="qualityQuality" style="margin-left: 5px;">质量优先</label>
                </div>
              </div>
              
              <div class="form-group">
                <label>生成方式</label>
                <div>
                  <input type="radio" id="genTypeText" value="text" v-model="videoParams.generationType">
                  <label for="genTypeText" style="margin-left: 5px;">文生视频（根据日记内容）</label>
                </div>
                <div>
                  <input type="radio" id="genTypeImage" value="image" v-model="videoParams.generationType">
                  <label for="genTypeImage" style="margin-left: 5px;">图生视频（根据日记图片）</label>
                </div>
              </div>
            </div>
          </div>
  
          <div class="form-actions">
            <button 
              type="button" 
              class="btn-cancel"
              @click="$emit('close')"
            >
              取消
            </button>
            <button 
              type="submit" 
              class="btn-submit"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? '保存中...' : (isEdit ? '保存修改' : '发布日记') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive } from 'vue';
  import axios from 'axios';
  import ImageUpload from './ImageUpload.vue';
  import { mapState } from 'vuex';
  import { useStore } from 'vuex';

  
  export default {
    name: 'EditDiary',
    components: {
      ImageUpload
    },
    computed: {
      ...mapState(['user'])
    },
    props: {
      diary: {
        type: Object,
        default: () => ({})
      },
      isEdit: {
        type: Boolean,
        default: false
      }
    },
    emits: ['close', 'submit'],
    
    setup(props, { emit }) {
      const store = useStore();

      const formData = reactive({
        title: props.diary?.title || '',
        content: props.diary?.content || '',
        images: props.diary?.images || [],
        tags: props.diary?.tags || []
      });

      const imageG = ref([]);
  
      const newTag = ref('');
      const isSubmitting = ref(false);
      const videoParams = reactive({
        shouldGenerate: false,
        quality: 'speed',
        generationType: 'text' // 默认为文生视频
      });
  
      const addTag = () => {
        const tag = newTag.value.trim();
        if (tag && !formData.tags.includes(tag)) {
          formData.tags.push(tag);
        }
        newTag.value = '';
      };
  
      const removeTag = (index) => {
        formData.tags.splice(index, 1);
      };
  
      const handleImageUpload = (data) => {
        const url = data.url;
        if(url && !formData.images.includes(url)) {
          console.log('EditDiary添加图片:', url);
          formData.images.push(url);
          imageG.value.push(data.file_path);
        } else {
          console.warn('图片已存在或无效:', url);
        }
      };
  
      const handleImageClear = (index) => {
        if (index !== undefined) {
          formData.images.splice(index, 1);
        } else {
          formData.images = [];
        }
      };
  
      const handleUploadError = (error) => {
        // 这里可以添加错误提示UI
        console.error(error);
      };

      const generateVideo = async (diary_id) => {
        try {
          if(videoParams.generationType === 'text') {
            console.log("开始文生视频");
            const response = await axios.post('http://localhost:8000/AIGen/text_generate_video', {
              username: store.state.user.username,
              diary_id: diary_id,
              prompt: formData.content,
              quality: videoParams.quality
            });
            console.log("文生视频结果： " + response.data.message);
          } else {
            console.log("开始图生视频");
            const response = await axios.post('http://localhost:8000/AIGen/image_generate_video', {
              username: store.state.user.username,
              diary_id: diary_id,
              quality: videoParams.quality,
              image_url: imageG.value[0],
              prompt: "让画面动起来"
            });
            console.log("图生视频结果： " + response.data.message);
          }
        } catch (error) {
          console.error('视频生成失败：' + error);
        }
      }
  
      const handleSubmit = async () => {
        try {
          if (!formData.title.trim()) {
            alert('请输入日记标题');
            return;
          }
          if (!formData.content.trim()) {
            alert('请输入日记内容');
            return;
          }

          isSubmitting.value = true;
          const payload = {
            ...formData,
            id: props.diary?.id,
            username: store.state.user.username
          };

          if (props.isEdit) {
            // 编辑模式
            await axios.post('http://localhost:8000/diaries/update', payload);
            if(videoParams.shouldGenerate) {
              generateVideo(props.diary.id);
            }
          } else {
            // 新建模式
            console.log("开始创建日记:", payload);
            const response = await axios.post('http://localhost:8000/diaries/add', payload);
            if(videoParams.shouldGenerate) {
              generateVideo(response.data.diary_id);
            }
          }
          emit('submit', payload);
          emit('close');
        } catch (error) {
          console.error('提交失败:', error);
          alert('保存失败，请重试');
        } finally {
          isSubmitting.value = false;
        }
      };
  
      return {
        formData,
        newTag,
        isSubmitting,
        videoParams,
        addTag,
        removeTag,
        handleImageUpload,
        handleImageClear,
        handleUploadError,
        handleSubmit
      };
    }
  };
  </script>
  
  <style scoped>
  .edit-diary-modal {
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
  
  .modal-header h2 {
    margin: 0;
    color: #2c3e50;
    font-size: 1.8rem;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 2rem;
    color: #666;
    cursor: pointer;
    transition: color 0.2s;
  }
  
  .close-btn:hover {
    color: #dc3545;
  }
  
  .diary-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .form-group label {
    font-weight: 600;
    color: #2c3e50;
  }
  
  input, textarea {
    padding: 0.8rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s;
  }
  
  input:focus, textarea:focus {
    border-color: #007bff;
    outline: none;
  }
  
  textarea {
    resize: vertical;
    min-height: 120px;
  }
  
  .tags-input {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .tag {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.8rem;
    background: #e9ecef;
    border-radius: 20px;
    font-size: 0.9rem;
  }
  
  .tag-remove {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    padding: 0;
    font-size: 1.2rem;
    line-height: 1;
  }
  
  .tag-remove:hover {
    color: #dc3545;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .btn-cancel, .btn-submit {
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .btn-cancel {
    background: #f8f9fa;
    border: none;
    color: #666;
  }
  
  .btn-cancel:hover {
    background: #e9ecef;
  }
  
  .btn-submit {
    background: #007bff;
    border: none;
    color: white;
  }
  
  .btn-submit:hover {
    background: #0056b3;
  }
  
  .btn-submit:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  /* 图片预览样式 */
  .image-previews {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 15px;
  }
  
  .image-preview-item {
    position: relative;
    width: 100px;
    height: 100px;
    border: 1px solid #eee;
    border-radius: 5px;
    overflow: hidden;
  }
  
  .preview-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .remove-image-btn {
    position: absolute;
    top: 5px;
    right: 5px;
    background: rgba(255, 0, 0, 0.7);
    color: white;
    border: none;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    line-height: 1;
  }
  </style>