<template>
    <div class="interest-selector">
        <h3>请选择您的兴趣指标</h3>
        <div class="interest-options">
            <label v-for="(option,index) in options" :key="index">
                <input type="checkbox"
                       :value="option.value"
                       v-model="selectedInterests">
                {{ option.label }}
            </label>
        </div>
        <p>您选择的兴趣:{{ selectInterests.join(',') }}</p>
    </div>
</template>

<script>
import { ref } from 'vue';
const options = [
  { value: '暴走', label: '暴走' },
  { value: '烧香拜佛', label: '烧香拜佛' },
  { value: '历史文化', label: '历史文化' },
  { value: '自然风光', label: '自然风光' },
  { value: '美食探索', label: '美食探索' },
]

const selectInterests = ref([]);

</script>

<style scoped>
.interest-selector {
  font-family: Arial, sans-serif;
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.interest-options {
  margin-top: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="checkbox"] {
  margin-right: 5px;
}
</style>