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

      <button class="nav-button" @click="startNavigation">开始导航</button>

      <div class="route-info">
        <h3>推荐路线信息</h3>
        <p>🗺️ 总距离: {{ totalDistance }} km</p>
        <p>⏱️ 预计时间: {{ estimatedTime }} min</p>
        <p>🚩 途径: {{ points }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";

export default {
  name: "MapComponent",
  setup() {
    const startLocation = ref("");
    const endLocation = ref("");
    const totalDistance = ref(0);
    const estimatedTime = ref(0);
    const points = ref("");
    const map = ref(null);

    let AMapInstance = null;

    onMounted(() => {
      // 配置安全密钥
      window._AMapSecurityConfig = {
        securityJsCode: "7ac63ea230a00cbb7a4d0f9f3b046a84", // 替换为你的安全密钥
      };

      // 使用 AMapLoader 加载高德地图 API
      AMapLoader.load({
        key: "82af44ada0b783b707679cdc4f0ff723", // 替换为你的API Key
        version: "2.0", // 指定要加载的 JSAPI 的版本
      })
      .then((AMap) => {
        // 初始化地图
        AMapInstance = AMap;
        map.value = new AMap.Map("map-container", {
          center: [116.36, 39.96], // 北京邮电大学的经纬度
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

      // const response = await axios.post('http://localhost:8080/plan', {
      //   startLocation: startLocation.value,
      //   endLocation: endLocation.value,
      // });

      const data = {
        existed: true,
        distance: 8,
        time: 10,
        route: [
          { name: "北京邮电大学北门", polyline: "116.36101,39.96241;116.36000,39.96200" },
          { name: "时光广场", polyline: "116.36100,39.96200;116.35900,39.96100" },
          { name: "北京邮电大学东门", polyline: "116.35900,39.96100;116.35706,39.96500" }
        ]
      };

      if (data.existed === true && data.route.length > 0) {
        const route = data.route;
        totalDistance.value = data.distance;
        estimatedTime.value = data.time;
        points.value = route.map(step => step.name).join(" -> ");

        if(!AMapInstance){
          alert("地图加载失败，请稍后再试！");
          return;
        }
        // 绘制导航路径
        const routePath = route.flatMap(step => step.polyline.split(";").map(coord => {
          const [lng, lat] = coord.split(",");
          return new AMapInstance.LngLat(lng, lat);
        }));

        const polyline = new AMapInstance.Polyline({
          path: routePath,
          strokeColor: "#4CAF50",
          strokeWeight: 6,
          strokeOpacity: 0.7,
        });
        map.value.add(polyline);

        // 添加起点终点标记
        const markers = [
          new AMapInstance.Marker({
            position: routePath[0],
            icon: new AMapInstance.Icon({
              size: new AMapInstance.Size(34, 34),
              image: "https://mapapi.qq.com/web/lbs/javascriptGL/demo/img/markerDefault.png",
            }),
            title: "起点",
          }),
          new AMapInstance.Marker({
            position: routePath[routePath.length - 1],
            icon: new AMapInstance.Icon({
              size: new AMapInstance.Size(34, 34),
              image: "https://mapapi.qq.com/web/lbs/javascriptGL/demo/img/markerRed.png",
            }),
            title: "终点",
          }),
        ];
        map.value.add(markers);
      } else {
        alert("未找到路线");
      }
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