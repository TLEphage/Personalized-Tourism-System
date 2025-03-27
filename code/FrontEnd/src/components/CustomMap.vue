<!-- src/components/CustomMap.vue -->
<template>
  <div id="custom-map" class="custom-map">
    <div id="custom-map-container" class="map-container">
    </div>
  </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import {graph} from '../data/graph';

export default{
    name:'CustomMap',
    data(){
      return{
        mapInstance:null
      }
    },
    beforeUnmount(){
      if(this.mapInstance){
        this.mapInstance.remove();
        this.mapInstance=null;
      }
    },
    mounted(){
        console.log('CustomMap mounted');
        console.log('Container dimensions:', document.getElementById('custom-map-container').getBoundingClientRect());
        this.initCustomMap();
    },
    methods: {
    initCustomMap() {
        // 创建自定义坐标系地图
        this.mapInstance = L.map('custom-map-container', {
            crs: L.CRS.Simple,
            attributionControl: false,
            zoomControl: false
        });

        // 计算坐标边界
        let coords = graph.V.map(node => [node.x, node.y]);
        let bounds = L.latLngBounds(coords);
    
        // 设置地图显示范围
        this.mapInstance.fitBounds(bounds);
        this.mapInstance.setMaxBounds(bounds.pad(0.1));

        // 绘制所有节点
        graph.V.forEach(node => {
            L.circleMarker([node.x, node.y], {
                radius: 6,
                color: '#3388ff',
                fillColor: '#3388ff',
                fillOpacity: 0.8
            }).bindTooltip(node.name).addTo(this.mapInstance);
        });

        // 绘制所有边
        graph.E.forEach(edge => {
            const start = graph.V[edge[0]];
            const end = graph.V[edge[1]];
            
            L.polyline(
                [[start.x, start.y], [end.x, end.y]],
                { color: '#ff7800', weight: 3 }
            ).addTo(this.mapInstance);
        });

        // 添加缩放控件
        L.control.zoom({ position: 'topright' }).addTo(this.mapInstance);

    }
}
}

</script>


<style scoped>
.custom-map {
  display:block;
  width: 800px;
  height: 600px;
  position: relative;
}
.map-container {
  width: 100% !important;
  height: 100% !important;
  background: #f0f0f0;
}
</style>