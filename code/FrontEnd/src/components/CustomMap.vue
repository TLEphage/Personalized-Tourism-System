<!-- src/components/CustomMap.vue -->
<template>
  <div id="custom-map">
    <div id="custom-map-container" class="map-container">
    </div>
  </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import {points} from '../data/points.js';

export default{
    name:'CustomMap',
    mounted(){
        console.log('CustomMap mounted');
        this.initCustomMap();
    },
    methods:{
        initCustomMap(){
            // 创建地图实例（初始中心和缩放可随意设置，后面会fitBounds调整）
            const map = L.map('custom-map-container').setView([39.962, 116.350], 16);

            // 添加高德地图瓦片
            L.tileLayer("http://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}", {
                attribution: '© 高德地图',
                maxZoom: 18,
                minZoom: 3,
                subdomains: "1234",
            }).addTo(map);

            // 根据坐标数据创建标记
            const markers = points.map(point => {
                return L.marker([point.lat, point.lng]).bindPopup(`<b>${point.name}</b><br>${point.type}`);
            });

            // 将所有标记放入一个 featureGroup，并调整地图视图以包含所有标记
            const group = L.featureGroup(markers).addTo(map);
            map.fitBounds(group.getBounds().pad(0.1)); // 加点内边距

            // 如果需要，也可以单独添加每个标记到地图上（featureGroup 已经包含了）
            markers.forEach(marker => marker.addTo(map));
        }
    }
}

</script>


<style scoped>
.custom-map {
  width: 800px;
  height: 600px;
  position: relative;
}
.map-container {
  width: 100%;
  height: 100%;
}
</style>