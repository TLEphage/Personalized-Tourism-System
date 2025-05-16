<!-- ImageUpload.vue -->
<script lang="ts">
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'ImageUpload',
  emits: ['uploaded', 'clear'],
  setup(props, { emit }) {
    const file = ref<File | null>(null);
    const previewUrl = ref<string>('');
    const isUploading = ref(false);
    const fileInput = ref<HTMLInputElement | null>(null);

    const handleFileChange = (e: Event) => {
      const input = e.target as HTMLInputElement;
      if (input.files?.length) {
        file.value = input.files[0];
        previewUrl.value = URL.createObjectURL(file.value);
      }
    };

    const uploadFile = async () => {
      if (!file.value) return;
      isUploading.value = true;

      const formData = new FormData();
      formData.append('file', file.value);
      try {
        const response = await axios.post('http://localhost:8000/api/upload', formData);
        console.log('上传成功:', response.data);
        emit('uploaded', response.data);
      } catch (error) {
        console.error('上传失败:', error);
        emit('clear');
      } finally {
        isUploading.value = false;
      }
    };

    const clear = () => {
      if (fileInput.value) {
        fileInput.value.value = ''; // 清空文件选择框
      }
      file.value = null;
      previewUrl.value = '';
    };

    return {
      handleFileChange,
      uploadFile,
      previewUrl,
      file,
      isUploading,
      fileInput,
      clear
    };
  }
};
</script>

<template>
  <div class="image-upload">
    <input 
      type="file" 
      @change="handleFileChange" 
      accept="image/*"
      ref="fileInput" 
    />
    <img v-if="previewUrl" :src="previewUrl" alt="Preview" class="preview" />
    <button 
      v-if="file" 
      @click="uploadFile"
      :disabled="isUploading" 
    >
      {{ isUploading ? '上传中...' : '上传图片' }}
    </button>
  </div>
</template>

  
<style>
.preview {
  max-width: 200px;
  max-height: 200px;
  margin-top: 10px;
}
</style>