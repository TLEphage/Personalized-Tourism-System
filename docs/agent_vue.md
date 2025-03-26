以下是使用Vue 3 + TypeScript + Leaflet实现的完整前端代码：

```html
<!-- src/App.vue -->
<template>
  <div class="container">
    <!-- 导航控制面板 -->
    <div class="control-panel">
      <h1>北邮校园导航</h1>
      <div class="input-group">
        <label>起点：</label>
        <select v-model="selectedStart">
          <option v-for="node in buildingNodes" :key="node.id" :value="node">
            {{ node.name }}
          </option>
        </select>
      </div>
      <div class="input-group">
        <label>终点：</label>
        <select v-model="selectedEnd">
          <option v-for="node in buildingNodes" :key="node.id" :value="node">
            {{ node.name }}
          </option>
        </select>
      </div>
      <button @click="calculateRoute" :disabled="!isFormValid">开始导航</button>
    </div>

    <!-- 地图容器 -->
    <div class="map-container">
      <l-map
        ref="map"
        :zoom="17"
        :center="center"
        :options="{ attributionControl: false }"
      >
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          layer-type="base"
        />

        <!-- 原始地图数据 -->
        <l-geo-json
          v-if="mapData"
          :geojson="mapData"
          :options-style="geoJsonStyle"
        />

        <!-- 导航路径 -->
        <l-polyline
          v-if="currentPath.length > 0"
          :lat-lngs="currentPath"
          color="blue"
          :weight="3"
        />
      </l-map>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { LMap, LTileLayer, LGeoJson, LPolyline } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import axios from 'axios'

// 类型定义
interface BuildingNode {
  id: string
  name: string
  coordinates: [number, number]  // [lng, lat]
}

interface GeoJsonFeature {
  type: string
  geometry: {
    type: string
    coordinates: any
  }
  properties: Record<string, any>
}

// 地图初始中心点（北邮主楼坐标）
const center = ref<[number, number]>([39.96648, 116.35923])
const mapData = ref<GeoJsonFeature[]>([])
const buildingNodes = ref<BuildingNode[]>([])
const selectedStart = ref<BuildingNode|null>(null)
const selectedEnd = ref<BuildingNode|null>(null)
const currentPath = ref<[number, number][]>([])

// 表单验证
const isFormValid = computed(() => 
  selectedStart.value && selectedEnd.value && selectedStart.value !== selectedEnd.value
)

// 获取初始数据
onMounted(async () => {
  try {
    // 获取地图数据
    const response = await axios.get('/data/bupt.geojson')
    mapData.value = response.data.features
    
    // 提取建筑物节点
    buildingNodes.value = mapData.value
      .filter(f => f.geometry.type === 'Point' && f.properties.type === 'building')
      .map(f => ({
        id: f.properties.id,
        name: f.properties.name,
        coordinates: f.geometry.coordinates
      }))
  } catch (error) {
    console.error('数据加载失败:', error)
  }
})

// 路径计算
const calculateRoute = async () => {
  if (!selectedStart.value || !selectedEnd.value) return

  try {
    const response = await axios.post('/api/route', {
      start: selectedStart.value.coordinates,
      end: selectedEnd.value.coordinates
    })
    
    // 转换坐标格式 [lng, lat] => [lat, lng]
    currentPath.value = response.data.path.map((point: number[]) => 
      [point[1], point[0]]
    )
  } catch (error) {
    console.error('路径计算失败:', error)
    currentPath.value = []
  }
}

// GeoJSON样式配置
const geoJsonStyle = () => ({
  color: '#4a4a4a',
  weight: 2,
  opacity: 0.8
})
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
}

.control-panel {
  width: 300px;
  padding: 20px;
  background: #f5f5f5;
  border-right: 1px solid #ddd;
}

.map-container {
  flex: 1;
  height: 100vh;
}

.input-group {
  margin: 15px 0;
}

label {
  display: block;
  margin-bottom: 5px;
}

select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
```

需要安装的依赖：
```bash
npm install vue @vue-leaflet/vue-leaflet leaflet axios
```

代码说明：

1. 项目结构：
```
src/
├── App.vue
├── main.ts
├── assets/
└── types/
public/
└── data/
    └── bupt.geojson  # 地图数据文件
```

2. 核心功能模块：
- 地图渲染：使用`@vue-leaflet/vue-leaflet`集成Leaflet地图
- 数据加载：从本地加载GeoJSON地图数据（开发时可放在public目录）
- 建筑选择：通过下拉菜单选择起点/终点建筑物
- 路径请求：通过axios向后端发送路径计算请求
- 路径显示：将返回的路径坐标转换为Leaflet需要的[lat,lng]格式

3. 运行准备：
```typescript
// main.ts
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.mount('#app')
```

4. 需要补充的配置：
```javascript
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  optimizeDeps: {
    exclude: ['@vue-leaflet/vue-leaflet']
  }
})
```

该实现包含以下关键特性：
- 响应式布局：左侧控制面板+右侧地图布局
- 数据验证：确保起点终点有效后才能提交
- 错误处理：捕获数据加载和路径计算异常
- 坐标转换：处理GeoJSON的[lng,lat]与Leaflet的[lat,lng]差异
- 样式隔离：使用scoped样式防止污染全局

与后端的交互规范：
```typescript
// 请求体
interface RouteRequest {
  start: [number, number]  // [lng, lat]
  end: [number, number]
}

// 响应体
interface RouteResponse {
  path: [number, number][]  // [lng, lat]数组
  distance: number
  time: number
}
```

注意：实际部署时需要：
1. 配置代理解决跨域问题（开发环境）
2. 生产环境部署时配置Nginx反向代理
3. Leaflet的CSS文件需要单独引入
4. 需要真实的地图数据文件（GeoJSON格式）

可以通过以下方式增强功能：
1. 添加加载状态提示
2. 增加地图标记点显示
3. 支持路径切换（最短/最优）
4. 添加导航指引面板
5. 实现GPS实时定位功能
