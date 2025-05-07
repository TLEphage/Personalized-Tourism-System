<template>
  <div class="poi-container">
    <div id="map-container" ></div>

    <div class="nav-panel">
      <!-- 模式选择 -->
      <div class="mode-toggle">
        <button
          :class="['mode-button', currentMode.value === 'start-end' ? 'active-mode' : '']"
          @click="currentMode.value = 'start-end'"
        >
          起点终点导航
        </button>
        <button
          :class="['mode-button', currentMode.value === 'search-places' ? 'active-mode' : '']"
          @click="currentMode.value = 'search-places'"
        >
          地点搜索导航
        </button>
      </div>

      <!-- 起点终点模式展示内容 -->
      <template v-if="currentMode.value === 'start-end'">
        <div class="nav-header">
          <h1 class="nav-title">北京邮电大学导航</h1>
          <p>请设置您的起点和终点</p>
        </div>

        <button class="developer-button" @click="goToDeveloper">开发者模式</button>

        <div class="input-group">
          <label>起点位置</label>
          <input
            type="text"
            class="input-field"
            v-model="startLocation"
          />
        </div>

        <div class="input-group">
          <label>终点位置</label>
          <input
            type="text"
            class="input-field"
            v-model="endLocation"
          />
        </div>

        <div class="input-group">
          <label>导航模式</label>
          <select name="input-field" v-model="selectedMode">
            <option value="1">步行</option>
            <option value="2">自行车</option>
            <option value="3">电动车</option>
          </select>
        </div>

        <button class="nav-button" @click="startNavigation">开始导航</button>

        <div class="route-info">
          <h3>推荐路线信息</h3>
          <p>🗺️ 总距离: {{ totalDistance }} m</p>
          <p>⏱️ 预计时间: {{ estimatedTime }} min</p>
          <p>🚩 途径: {{ points }}</p>
        </div>
      </template>

      <!-- 搜索选择地点模式展示内容 -->
      <template v-else>
        <div class="input-group">
          <label>点击地图选择当前位置</label>
          <p class="info-text">请在地图上点击一个位置来作为您的当前位置</p>
        </div>

        <div class="input-group">
          <label>服务类型</label>
          <input
            type="text"
            class="input-field"
            v-model="serviceType"
            placeholder="例如：超市、卫生间、餐厅"
          />
        </div>

        <!-- 展示搜索结果 -->
        <div class="search-results-container" v-if="searchResults.length > 0">
          <h3>搜索到的地点</h3>
          <ul class="search-results-list">
            <li
              class="search-result-item"
              v-for="(item, index) in searchResults"
              :key="index"
            >
              <div>
                <h4>{{ item.name }}</h4>
                <p>距离: {{ item.distance }} 米</p>
                <p>地址: {{ item.address }}</p>
              </div>
            </li>
          </ul>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";
import axios from 'axios';

export default {
  name: "MapComponent",
  setup() {
    const startLocation = ref("");
    const endLocation = ref("");
    const totalDistance = ref(0);
    const estimatedTime = ref(0);
    const points = ref("");
    const map = ref(null);
    const selectedMode = ref(1);
    const currentMode = ref('start-end'); // 'start-end' 为起点终点模式，'search-places' 为搜索地点模式
    const serviceType = ref(''); // 存储用户输入的服务类型
    const searchResults = ref([]); // 存储搜索到的地点数据

   // 用来存当前绘制到地图上的点和线
   let routeMarkers = [];
   let routePolyline = null;

    let AMapInstance = null;

    onMounted(() => {
      window._AMapSecurityConfig = { securityJsCode: "7ac63ea230a00cbb7a4d0f9f3b046a84" };
      AMapLoader.load({
        key: "82af44ada0b783b707679cdc4f0ff723",
        version: "2.0",
      })
      .then((AMap) => {
        AMapInstance = AMap;
        map.value = new AMap.Map("map-container", {
          center: [116.36, 39.96],
          zoom: 16,
        });
      })
      .catch((e) => {
        console.error("Failed to load AMap script", e);
        alert("加载高德地图API失败，请检查网络连接或API Key是否正确");
      });
      map.value.on('click', function(e) {
        if(currentMode.value === 'search-places') {
          const position = e.lnglat;
          console.log('用户点击的地图位置经纬度：', position);
          // 这里可以存储点击位置的经纬度，供后续调用API使用
          // 调用后台API服务，具体实现需根据实际接口设计调整
          axios.post('http://localhost:8000/map/search_places', {
            latitude: position.lat,
            longitude: position.lng,
            type: serviceType.value,
          })
          .then(response => {
            if(response.data && response.data.length > 0) {
              searchResults.value = response.data;
              // 在地图上绘制搜索结果相关的标记，如果你需要的话

            } else {
              alert('未找到符合条件的地点');
            }
          })
          .catch(error => {
            console.error('搜索地点API调用错误：', error);
            alert('搜索地点API调用失败，请稍后再试');
          });
        }
      });
    });

    async function startNavigation() {
      if (!startLocation.value || !endLocation.value) {
        alert("请填写起点和终点位置！");
        return;
      }

      axios.post('http://localhost:8000/map/path_plan', {
        start: startLocation.value,
        end: endLocation.value,
        mode: parseInt(selectedMode.value),
      })
      .then(res => {
        const data = res.data;
        if (data.path.length === 0) {
          alert("未找到路线");
          return;
        }

        const route = data.path;
        totalDistance.value = data.distance;
        estimatedTime.value = data.time;
        points.value = route.map(p => p.name).join(" → ");

        if (!AMapInstance) {
          alert("地图加载失败，请稍后再试！");
          return;
        }

       // —— 清除旧的覆盖物 —— 
       routeMarkers.forEach(m => m.setMap(null));
       routeMarkers = [];
       if (routePolyline) {
         routePolyline.setMap(null);
         routePolyline = null;
       }

       // —— 组装坐标数组 （注意：服务端给的字段名 latitude/longitude 在这里是反过来的）——
       const coords = route.map(p => [p.longitude, p.latitude]);

       // —— 按顺序打点 —— 
       route.forEach(p => {
         const marker = new AMapInstance.Marker({
           position: [p.longitude, p.latitude],
           map: map.value,
           title: p.name
         });
         // 用 Label 给点加个红色小标签
         marker.setLabel({
           offset: new AMapInstance.Pixel(-10, -28),
           content: `<div style="
             background: #f33;
             color: #fff;
             padding: 2px 4px;
             border-radius: 3px;
             font-size: 12px;
           ">${p.name}</div>`
         });
         routeMarkers.push(marker);
       });

       // —— 画连线 —— 
       routePolyline = new AMapInstance.Polyline({
         path: coords,
         strokeColor: "#FF0000",
         strokeWeight: 4,
         strokeOpacity: 0.8,
         lineJoin: "round",
         map: map.value
       });

       // —— 自动缩放视野到所有点和线 —— 
       map.value.setFitView();

        console.log("已绘制路径和标记");
      })
      .catch(err => {
        // ...原有错误处理...
      });
    }

    return { startLocation, endLocation, totalDistance, estimatedTime, points, startNavigation };
  },
  methods: {
    goToDeveloper() {
      this.$router.push({ name: "Developer" });
      console.log("route to developer page");
    },
  }
};
</script>


<style>
:root {
  --primary-color: #4caf50;
  --secondary-color: #2196f3;
}

body {
  margin: 0;
  padding: 20px;
  background: #f5f5f5;
}

.mode-toggle {
  display: flex;
  margin-bottom: 1.5rem;
}

.mode-button {
  flex: 1;
  padding: 0.8rem;
  margin-right: 0.5rem;
  background: #f5f5f5;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.mode-button:last-child {
  margin-right: 0;
}

.active-mode {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

/* 添加搜索结果样式 */
.search-results-container {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.search-results-list {
  list-style-type: none;
  padding: 0;
}

.search-result-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background: #f1f1f1;
}

.info-text {
  font-size: 0.9rem;
  color: #666;
}

.poi-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  height: 90vh;
}

.poi-header {
  border-bottom: 2px solid #eee;
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}

.poi-title {
  color: var(--primary-color);
  margin: 0;
  font-size: 2.2rem;
}

#map-container {
  height: 100vh;
  width: 800px;
  position: relative;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.nav-panel {
  background: #fff;
  padding: 1.5rem;
  border-radius: 15px;
  box-shadow: -4px 0 12px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.nav-header {
  margin-bottom: 2rem;
}

.nav-title {
  color: var(--primary-color);
  margin: 0;
  font-size: 2.2rem;
}

.input-group {
  margin-bottom: 1.5rem;
  margin-right: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.input-field {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.nav-button {
  width: 100%;
  padding: 1rem;
  background: #45a049;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.nav-button:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.route-info {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.developer-button {
  position: absolute;
  top: 40px;
  right: 20px;
  padding: 0.8rem;
  background: #2196f3;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.developer-button:hover {
  background: #1976d2;
  transform: translateY(-2px);
}
</style>