<template>
  <div class="map-component">
    <!-- 地图容器 -->
    <div id="map" class="map-container"></div>

    <!-- 搜索框容器 -->
    <div class="search-container">
      <input
        type="text"
        placeholder="请输入地名"
        v-model="searchQuery"
        @keyup.enter="searchLocation"
      />
      <button @click="searchLocation">搜索</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import L from 'leaflet';

// 引入Leaflet CSS
import 'leaflet/dist/leaflet.css';

export default {
  name: 'MapComponent',
  data() {
    return {
      searchQuery: '', // 用户输入的地名查询
      map: null, // 叶子地图实例
    };
  },
  mounted() {
    // 确保DOM元素已加载后再初始化地图
    this.$nextTick(() => {
      this.initMap();
    });
  },
  methods: {
    /**
     * 初始化地图
     */
    initMap() {
      // 创建地图实例
      this.map = L.map('map', {
        zoomSnap: 0.1, // 地图的有效缩放级别
        maxZoom: 18,
        zoomControl: true,
      }).setView([39.961554, 116.358103], 15); // 设置初始视图为北京邮电大学的经纬度

      // 添加基础瓦片图层
      const baseLayer = L.tileLayer(
        "http://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",
        {
          attribution: '&copy; 高德地图',
          maxZoom: 18,
          minZoom: 3,
          subdomains: "1234",
        }
      );
      baseLayer.addTo(this.map);

      // 监听地图点击事件，打印点击位置的经纬度
      this.map.on('click', function(event) {
        console.log(event.latlng); // 输出经纬度对象
      });

      // 监听地图缩放开始事件，打印当前缩放级别
      this.map.on('zoomstart', () => {
        const zoomLevel = this.map.getZoom();
        console.log(zoomLevel);
      });
    },

    /**
     * 根据用户输入的地名进行搜索并跳转地图视角
     */
     async searchLocation() {
      const query = this.searchQuery.trim();
      if (!query) return;
      try {
        // 如果你需要保留原来的地名解析功能，也可以调用后端接口
        // const response = await axios.post('http://localhost:3000/geocode', { query });
        // const result = response.data;
        // if (result && result.lat && result.lng) {
        //   this.map.setView([result.lat, result.lng], 15);
        // } else {
        //   alert('未找到该位置，请尝试其他关键词。');
        // }

        // 这里我们直接使用路由跳转到自制地图页面，并可通过 query 参数传递关键词
        this.$router.push({ name: 'CustomMap', query: { q: query } });
        console.log('路由切换到:CustomMap');
      } catch (error) {
        console.error('Error during geocoding:', error);
        alert('地名解析失败，请稍后重试。');
      }
    },
  },
};
</script>

<style scoped>
/* 让地图组件固定大小，无多余空白 */
.map-component {
  position: relative;
  width: 800px; /* 设置固定宽度 */
  height: 600px; /* 设置固定高度 */
  overflow: hidden;
}

/* 地图容器全屏填充 */
.map-container {
  width: 100%;
  height: 100%;
}

/* 搜索框固定在右下角 */
.search-container {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background-color: white;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.search-container input {
  padding: 8px;
  width: 200px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 10px;
}

.search-container button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-container button:hover {
  background-color: #0056b3;
}
</style>