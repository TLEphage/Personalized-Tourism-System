<!-- src/views/developer.vue -->
<template>
  <div id="map-container" style="height: 600px;"></div>

  <!-- 新增节点对话框 -->
  <div v-if="newNodeDialogVisible" class="overlay">
    <div class="dialog">
      <h3>添加新节点</h3>
      <p>坐标：{{ clickedPosition.lng.toFixed(6) }}, {{ clickedPosition.lat.toFixed(6) }}</p>
      <input v-model="newNodeData.name" placeholder="节点名称" />
      <input v-model="newNodeData.type" placeholder="节点类型" />
      <button @click="addNewNode">提交</button>
      <button @click="newNodeDialogVisible = false">取消</button>
    </div>
  </div>

  <!-- 新增边表单 -->
  <div class="control-panel">
    <h3>添加新边</h3>
    <select v-model="edgeData.startId">
      <option value="">选择起点</option>
      <option v-for="node in existingNodes" :key="node.id" :value="node.id">
        {{ node.name }}
      </option>
    </select>
    <select v-model="edgeData.endId">
      <option value="">选择终点</option>
      <option v-for="node in existingNodes" :key="node.id" :value="node.id">
        {{ node.name }}
      </option>
    </select>
    <input v-model="edgeData.weight" type="number" placeholder="权重" />
    <button @click="addNewEdge">添加边</button>
  </div>

  <!-- 原有路径规划表单... -->
</template>

<script>
import { onMounted, ref } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";
import axios from 'axios';

export default {
  name: "MapComponent",
  setup() {
    // 原有状态
    const startLocation = ref("");
    const endLocation = ref("");
    const totalDistance = ref(0);
    const estimatedTime = ref(0);
    const points = ref("");
    const map = ref(null);
    const selectedMode = ref(1);

    // 新增开发者模式状态
    const existingNodes = ref([]);
    const existingEdges = ref([]);
    const newNodeDialogVisible = ref(false);
    const clickedPosition = ref({ lng: 0, lat: 0 });
    const newNodeData = ref({ name: "", type: "" });
    const edgeData = ref({ startId: "", endId: "", weight: "" });

    // 地图覆盖物引用
    let existingNodeMarkers = [];
    let existingEdgePolylines = [];
    let AMapInstance = null;

    // 初始化地图和加载数据
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

        // 添加地图点击监听
        map.value.on("click", handleMapClick);
        loadGraphData();
      });
    });

    // 加载图数据
    async function loadGraphData() {
      try {
        const res = await axios.get("http://localhost:8000/get_graph");
        existingNodes.value = res.data.nodes;
        existingEdges.value = res.data.edges;
        renderGraphElements();
      } catch (error) {
        console.error("加载图数据失败:", error);
      }
    }

    // 渲染节点和边
    function renderGraphElements() {
      // 清除旧覆盖物
      existingNodeMarkers.forEach(marker => marker.setMap(null));
      existingEdgePolylines.forEach(polyline => polyline.setMap(null));
      existingNodeMarkers = [];
      existingEdgePolylines = [];

      // 绘制节点
      existingNodes.value.forEach(node => {
        const marker = new AMapInstance.Marker({
          position: [node.longitude, node.latitude],
          map: map.value,
          title: node.name,
        });
        existingNodeMarkers.push(marker);
      });

      // 绘制边
      existingEdges.value.forEach(edge => {
        const startNode = existingNodes.value.find(n => n.id === edge.start_id);
        const endNode = existingNodes.value.find(n => n.id === edge.end_id);
        
        if (startNode && endNode) {
          const polyline = new AMAPInstance.Polyline({
            path: [
              [startNode.longitude, startNode.latitude],
              [endNode.longitude, endNode.latitude]
            ],
            strokeColor: "#0000FF",
            strokeWeight: 2,
            map: map.value
          });
          existingEdgePolylines.push(polyline);
        }
      });
    }

    // 地图点击处理
    function handleMapClick(e) {
      const clickedLng = e.lnglat.getLng();
      const clickedLat = e.lnglat.getLat();
      
      // 检查是否在现有节点附近
      const isExisting = existingNodes.value.some(node => 
        AMapInstance.GeometryUtil.distance(
          [node.longitude, node.latitude],
          [clickedLng, clickedLat]
        ) < 50 // 50米内视为已有节点
      );

      if (!isExisting) {
        clickedPosition.value = { lng: clickedLng, lat: clickedLat };
        newNodeDialogVisible.value = true;
      }
    }

    // 添加新节点
    async function addNewNode() {
      try {
        await axios.post("http://localhost:8000/add_node", {
          longitude: clickedPosition.value.lng,
          latitude: clickedPosition.value.lat,
          ...newNodeData.value
        });
        await loadGraphData();
        newNodeDialogVisible.value = false;
        newNodeData.value = { name: "", type: "" };
      } catch (error) {
        console.error("添加节点失败:", error);
      }
    }

    // 添加新边
    async function addNewEdge() {
      try {
        await axios.post("http://localhost:8000/add_edge", {
          start_id: edgeData.value.startId,
          end_id: edgeData.value.endId,
          weight: edgeData.value.weight
        });
        await loadGraphData();
        edgeData.value = { startId: "", endId: "", weight: "" };
      } catch (error) {
        console.error("添加边失败:", error);
      }
    }

    return {
      // 原有返回项
      startLocation,
      endLocation,
      totalDistance,
      estimatedTime,
      points,
      startNavigation,
      
      // 新增返回项
      existingNodes,
      newNodeDialogVisible,
      clickedPosition,
      newNodeData,
      edgeData,
      addNewNode,
      addNewEdge
    };
  }
};
</script>


<style>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog {
  background: white;
  padding: 20px;
  border-radius: 8px;
}

.control-panel {
  position: absolute;
  top: 20px;
  right: 20px;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>