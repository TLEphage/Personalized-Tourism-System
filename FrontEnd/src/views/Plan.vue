<template>
  <div class="poi-container">
    <div id="map-container" ></div>

    <div class="nav-panel">
      <div class="nav-header">
        <h1 class="nav-title">北京邮电大学导航</h1>
        <p>请设置您的起点和终点</p>
      </div>

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
    });

    async function startNavigation() {
      if (!startLocation.value || !endLocation.value) {
        alert("请填写起点和终点位置！");
        return;
      }

      axios.post('http://localhost:8000/path_plan', {
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
       const coords = route.map(p => [p.latitude, p.longitude]);

       // —— 按顺序打点 —— 
       route.forEach(p => {
         const marker = new AMapInstance.Marker({
           position: [p.latitude, p.longitude],
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
</style>