<!-- ImageUpload.vue -->
<template>
  <div class="image-upload-container">
    <div class="upload-area" @click="triggerFileInput" @drop.prevent="handleDrop" @dragover.prevent>
      <input 
        type="file" 
        @change="handleFileChange" 
        accept="image/*"
        ref="fileInput"
        multiple
        class="file-input"
      />
      <div v-if="!previewUrls.length" class="upload-placeholder">
        <i class="fas fa-cloud-upload-alt"></i>
        <p>点击或拖拽图片到此处上传</p>
        <p class="upload-hint">支持 jpg、png、gif 格式</p>
      </div>
    </div>

    <div v-if="previewUrls.length" class="preview-container">
      <div v-for="(url, index) in previewUrls" :key="index" class="preview-item">
        <img :src="url" alt="Preview" class="preview-image" />
        <div class="preview-overlay">
          <button class="delete-btn" @click.stop="removeImage(index)">
            <i class="fas fa-trash"></i>
          </button>
        </div>
        <div class="upload-progress" v-if="uploadingIndex === index">
          <div class="progress-bar" :style="{ width: uploadProgress + '%' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import axios from 'axios';

export default {
  name: 'ImageUpload',
  emits: ['uploaded', 'clear', 'error'],
  
  setup(props, { emit }) {
    const fileInput = ref(null);
    const files = ref([]);
    const previewUrls = ref([]);
    const uploadingIndex = ref(-1);
    const uploadProgress = ref(0);

    const triggerFileInput = () => {
      fileInput.value?.click();
    };

    const handleFileChange = (e) => {
      const newFiles = Array.from(e.target.files);
      addFiles(newFiles);
    };

    const handleDrop = (e) => {
      const newFiles = Array.from(e.dataTransfer.files).filter(file => file.type.startsWith('image/'));
      addFiles(newFiles);
    };

    const addFiles = (newFiles) => {
      for (const file of newFiles) {
        if (file.type.startsWith('image/')) {
          files.value.push(file);
          previewUrls.value.push(URL.createObjectURL(file));
        }
      }
      uploadImages();
    };

    const removeImage = (index) => {
      if (uploadingIndex.value === index) return;
      
      URL.revokeObjectURL(previewUrls.value[index]);
      files.value.splice(index, 1);
      previewUrls.value.splice(index, 1);
      emit('clear', index);
    };

    const uploadImages = async () => {
      for (let i = 0; i < files.value.length; i++) {
        if (uploadingIndex.value !== -1) continue;
        
        const file = files.value[i];
        const formData = new FormData();
        formData.append('file', file);
        
        uploadingIndex.value = i;
        uploadProgress.value = 0;
        
        try {
          const response = await axios.post('http://localhost:8000/upload/images', formData, {
            onUploadProgress: (progressEvent) => {
              uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            }
          });
          // response.data有三个值filename,file_path(绝对路径),url(图床路径)
          emit('uploaded', response.data);
          console.log("上传成功：", response.data);
        } catch (error) {
          console.error('上传失败:', error);
          emit('error', `图片 ${file.name} 上传失败`);
        } finally {
          uploadingIndex.value = -1;
        }
      }
    };

    watch(files, () => {
      if (files.value.length === 0) {
        emit('clear');
      }
    });

    return {
      fileInput,
      previewUrls,
      uploadingIndex,
      uploadProgress,
      triggerFileInput,
      handleFileChange,
      handleDrop,
      removeImage
    };
  }
};
</script>

<style scoped>
.image-upload-container {
  width: 100%;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.upload-area:hover {
  border-color: #007bff;
  background: #f1f8ff;
}

.file-input {
  display: none;
}

.upload-placeholder {
  color: #666;
}

.upload-placeholder i {
  font-size: 3rem;
  color: #007bff;
  margin-bottom: 1rem;
}

.upload-hint {
  font-size: 0.9rem;
  color: #999;
  margin-top: 0.5rem;
}

.preview-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.preview-item {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 1;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.preview-item:hover .preview-overlay {
  opacity: 1;
}

.delete-btn {
  background: #dc3545;
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
}

.delete-btn:hover {
  transform: scale(1.1);
}

.upload-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: rgba(0, 0, 0, 0.2);
}

.progress-bar {
  height: 100%;
  background: #007bff;
  transition: width 0.3s ease;
}
</style>