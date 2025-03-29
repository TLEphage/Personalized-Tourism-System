<!-- src/components/CustomMap.vue -->
<template>
  <div id="custom-map" class="custom-map">
    <div id="custom-map-container" class="map-container"></div>
    <div class="search-container">
      <h2>路径搜索</h2>
      <form @submit.prevent="searchPath">
        <label for="start">起点</label>
        <input type="text" id="start" name="start" placeholder="请输入起点" required>
        <label for="end">终点</label>
        <input type="text" id="end" name="end" placeholder="请输入终点" required>
        <button type="submit">搜索</button>
      </form> 
      <div v-if="searchResult" class="search-result">
        <p v-if="searchResult.existed">路径存在:{{ searchResult.path.join(' -> ') }}</p>
        <p v-else>请输入存在的地点</p>
      </div>
    </div>
  </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import {graph} from '../data/graph';
import axios from 'axios';

export default{
    name:'CustomMap',
    data(){
      return{
        mapInstance:null,
        start:'',
        end:'',
        searchResult:null
      };
    },
    beforeUnmount(){
      if(this.mapInstance){
        this.mapInstance.remove();
        this.mapInstance=null;
      }
    },
    mounted(){
        console.log('CustomMap mounted');
        //console.log('Container dimensions:', document.getElementById('custom-map-container').getBoundingClientRect());
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

    },
    // 返回值数据结构
    // {
    //   existed: bool,
    //   path: [],
    //   distance:int,
    //   time:int,
    // }
    async searchPath(){
      try{
        const response = await axios.post('http://localhost:3000/api/searchPath',{
          start:this.start,
          end:this.end
        });
        this.searchResult = response.data;
        if(this.searchResult.existed){
          // 绘制最短路径
          this.drawPath(this.searchResult.path);
        }
      }catch(error){
        console.error('Error searching path:', error);
        this.searchResult = {existed:0, path:[]};
      }
    },
    drawPath(path){
      if(path.length < 2){
        console.warn("路径至少需要两个点才能绘制");
        return ;
      }
      for (let i=0;i<path.length-1;i++){
        const startId = path[i];
        const endId = path[i+1];
        const start = graph.V[startId];
        const end = graph.V[end];
        L.polyline(
          [[start.x, start.y],[end.x, end.y]],
          {color:'#ff3600', weitht:4}
        ).addTo(this.mapInstance);
      }
    }
}
}

</script>


<style scoped>
.custom-map {
  display:flex;
  width: 800px;
  height: 600px;
  position: relative;
}
.map-container {
  width: 100% !important;
  height: 100% !important;
  background: #f0f0f0;
}
.search-container {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 300px;
    text-align: center;
}

.search-container h2 {
    margin-bottom: 20px;
    color: #333;
}

.search-container form {
    display: flex;
    flex-direction: column;
}

.search-container label {
    margin-bottom: 5px;
    text-align: left;
    color: #555;
}

.search-container input[type="text"] {
    margin-bottom: 15px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    transition: border-color 0.3s ease;
}

.search-container input[type="text"]:focus {
    border-color: #007bff;
    outline: none;
}

.search-container button {
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.search-container button:hover {
    background-color: #0056b3;
}
</style>