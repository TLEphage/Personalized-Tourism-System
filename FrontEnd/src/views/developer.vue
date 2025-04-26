<!-- src/views/developer.vue -->
<template>
  <div id="map-container" style="height: 600px;"></div>

  <!-- 模式选择器 -->
  <div class="control-panel">
    <div>
      <h3>操作模式</h3>
      <select v-model="mode">
        <option value="addNode">添加节点</option>
        <option value="addEdge">添加边</option>
      </select>
    </div>

    <div v-if="mode === 'addNode'">
      <h3>添加新节点</h3>
      <p>在地图上点击位置添加新节点</p>
    </div>

    <div v-if="mode === 'addEdge'">
      <h3>添加新边</h3>
      <p>在地图上依次点击起点和终点</p>
      <div v-if="edgeData.startId">
        <p>已选择起点: {{ edgeData.startId }}</p>
      </div>
      <div v-if="edgeData.endId">
        <p>已选择终点: {{ edgeData.endId }}</p>
        <input v-model="edgeData.distance" type="number" placeholder="距离" />
        <input v-model="edgeData.walk_speed" type="number" placeholder="步行速度" />
        <input v-model="edgeData.bike_speed" type="number" placeholder="骑行速度" />
        <input v-model="edgeData.ebike_speed" type="number" placeholder="电动车速度" />
        <button @click="addNewEdge">添加边</button>
      </div>
      <button v-else @click="cancelEdgeAdding">取消</button>
    </div>
  </div>

  <!-- 新增节点对话框 -->
  <div v-if="newNodeDialogVisible" class="overlay">
    <div class="dialog">
      <h3>{{ mode === 'addNode' ? '添加新节点' : '确认边信息' }}</h3>
      <p v-if="mode === 'addNode'">坐标：{{ clickedPosition.lng.toFixed(6) }}, {{ clickedPosition.lat.toFixed(6) }}</p>
      <input v-if="mode === 'addNode'" v-model="newNodeData.name" placeholder="节点名称" />
      <input v-if="mode === 'addNode'" v-model="newNodeData.type" placeholder="节点类型" />
      <input v-if="mode === 'addNode'" v-model="newNodeData.popularity" type="number" placeholder="节点热度" />
      
      <button @click="mode === 'addNode' ? addNewNode() : addNewEdge()">提交</button>
      <button @click="newNodeDialogVisible = false">取消</button>
    </div>
  </div>

</template>

<script>
import { ref, onMounted } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";
import axios from "axios";


export default {
  name: "Developer",
  setup() {
    const map = ref(null);
    const existingNodes = ref([]);
    const existingEdges = ref([]);
    const newNodeDialogVisible = ref(false);
    const clickedPosition = ref({ lng: 0, lat: 0 });
    const newNodeData = ref({ name: "", type: "", popularity: "", connected_edges: [] });
    const edgeData = ref({ startId: "", endId: "", distance: "", walk_speed: "", bike_speed: "", ebike_speed: "" });
    const mode = ref("add_node"); //add_node, add_edge
    const edgeStartPoint = ref(null);

    // 地图覆盖物引用
    let existingNodeMarkers = [];
    let existingEdgePolylines = [];
    let AMapInstance = null;
    let edgeStartMarker = null;

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
        const res = await axios.get("http://localhost:8000/map/get_graph");
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
          const polyline = new AMapInstance.Polyline({
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

      if (mode.value === "addNode") {
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
      } else if (mode.value === "addEdge") {
        if (!edgeStartPoint.value) {
          // 第一次点击，设置起点
          edgeStartPoint.value = { lng: clickedLng, lat: clickedLat };
          edgeData.value.startId = existingNodes.value.find(node => 
            AMapInstance.GeometryUtil.distance(
              [node.longitude, node.latitude],
              [clickedLng, clickedLat]
            ) < 50 // 50米内视为已有节点
          )?.id;

          // 清除旧的起点标记
          if (edgeStartMarker) {
            edgeStartMarker.setMap(null);
          }

          // 添加起点标记
          edgeStartMarker = new AMapInstance.Marker({
            position: [clickedLng, clickedLat],
            map: map.value,
            title: "边起点",
            icon: "https://a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-red.png"
          });
        } else {
          // 第二次点击，设置终点
          edgeData.value.endId = existingNodes.value.find(node => 
            AMapInstance.GeometryUtil.distance(
              [node.longitude, node.latitude],
              [clickedLng, clickedLat]
            ) < 50 // 50米内视为已有节点
          )?.id;

          if (edgeData.value.startId && edgeData.value.endId) {
            // 显示添加边的对话框
            newNodeDialogVisible.value = true;
            clickedPosition.value = { lng: clickedLng, lat: clickedLat };
          } else {
            alert("请选择有效的起点和终点！");
          }

          // 清除起点标记
          if (edgeStartMarker) {
            edgeStartMarker.setMap(null);
          }
          edgeStartPoint.value = null;
        }
      }
    }
    // 添加新节点
    async function addNewNode() {
      try {
        await axios.post("http://localhost:8000/map/add_node", {
          longitude: clickedPosition.value.lng,
          latitude: clickedPosition.value.lat,
          ...newNodeData.value
        });
        await loadGraphData();
        newNodeDialogVisible.value = false;
        newNodeData.value = { name: "", type: "", popularity: "", connected_edges: [] };
      } catch (error) {
        console.error("添加节点失败:", error);
      }
    }

    // 添加新边
    async function addNewEdge() {
      try {
        await axios.post("http://localhost:8000/map/add_edge", {
          start_id: edgeData.value.startId,
          end_id: edgeData.value.endId,
          distance: edgeData.value.distance,
          walk_speed: edgeData.value.walk_speed,
          bike_speed: edgeData.value.bike_speed,
          ebike_speed: edgeData.value.ebike_speed
        });
        await loadGraphData();
        edgeData.value = { startId: "", endId: "", distance: "", walk_speed: "", bike_speed: "", ebike_speed: "" };
      } catch (error) {
        console.error("添加边失败:", error);
      }
    }

    return {
      existingNodes,
      newNodeDialogVisible,
      clickedPosition,
      newNodeData,
      edgeData,
      addNewNode,
      addNewEdge,
      mode
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