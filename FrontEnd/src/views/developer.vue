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
      <div v-if="edgeData.start_node">
        <p>已选择起点: {{ getNodeName(edgeData.start_node) }} (ID: {{ edgeData.start_node }})</p>
      </div>
      <div v-if="edgeData.end_node">
        <p>已选择终点: {{ getNodeName(edgeData.end_node) }} (ID: {{ edgeData.end_node }})</p>
        <input v-model="edgeData.walk_speed" type="number" placeholder="步行速度" />
        <input v-model="edgeData.bike_speed" type="number" placeholder="骑行速度" />
        <input v-model="edgeData.ebike_speed" type="number" placeholder="电动车速度" />
        <button @click="addNewEdge">添加边</button>
        <button @click="cancelEdgeAdding">取消</button>
      </div>
    </div>
  </div>

  <!-- 新增对话框 -->
  <div v-if="newNodeDialogVisible" class="overlay">
    <div class="dialog">
      <h3>{{ mode === 'addNode' ? '添加新节点' : '确认边信息' }}</h3>
      <p v-if="mode === 'addNode'">坐标：{{ clickedPosition.lng.toFixed(6) }}, {{ clickedPosition.lat.toFixed(6) }}</p>
      <input v-if="mode === 'addNode'" v-model="newNodeData.name" placeholder="节点名称" />
      <input v-if="mode === 'addNode'" v-model="newNodeData.type" placeholder="节点类型" />
      <input v-if="mode === 'addNode'" v-model="newNodeData.popularity" type="number" placeholder="节点热度" />
      
      <button @click="mode === 'addNode' ? addNewNode() : addNewEdge()">提交</button>
      <button @click="mode === 'addNode' ? cancelNodeAdding() : cancelEdgeAdding()">取消</button>
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
    const newNodeData = ref({ name: "", type: null, popularity: null});
    const edgeData = ref({ start_node: -1, end_node: -1, walk_speed: null, bike_speed: null, ebike_speed: null});
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

    const getNodeName = (nodeId) => {
      const node = existingNodes.value.find(n => n.id === nodeId);
      return node ? node.name : "未知节点";
    };

    // 加载图数据
    async function loadGraphData() {
      try {
        const res = await axios.get("http://localhost:8000/map/get_graph");
        console.log("图数据:", res.data);
        existingNodes.value = res.data.nodes;
        existingEdges.value = res.data.edges;
        renderGraphElements();
      } catch (error) {
        console.error("加载图数据失败:", error);
      }
    }

    const cancelEdgeAdding = () => {
      edgeData.value = { start_node: -1, end_node: -1, walk_speed: null, bike_speed: null, ebike_speed: null };
      edgeStartPoint.value = null;
      if (edgeStartMarker) {
        edgeStartMarker.setMap(null);
        edgeStartMarker = null;
      }
      newNodeDialogVisible.value = false;
    };

    const cancelNodeAdding = () => {
      newNodeDialogVisible.value = false;
      newNodeData.value = { name: "", type: null, popularity: null };
      clickedPosition.value = { lng: 0, lat: 0 };
    };

    // 渲染节点和边
    const renderGraphElements = () => {
      // 清除旧覆盖物
      existingNodeMarkers.forEach(marker => marker.setMap(null));
      existingEdgePolylines.forEach(polyline => polyline.setMap(null));
      existingNodeMarkers = [];
      existingEdgePolylines = [];

      // 绘制节点
      existingNodes.value.forEach(node => {
        const marker = new AMapInstance.CircleMarker({
          center: [node.longitude, node.latitude],
          radius: 5, // 圆点半径
          strokeColor: 'red', // 边框颜色
          strokeWeight: 2, // 边框宽度
          fillColor: 'red', // 填充颜色
          fillOpacity: 1, // 填充透明度
          map: map.value,
          cursor: 'pointer'
        });

        // 为每个节点添加点击事件
        marker.on('click', () => {
          if (mode.value === 'addEdge') {
            if (!edgeStartPoint.value) {
              edgeData.value.start_node = node.id;
              edgeStartPoint.value = { lng: node.longitude, lat: node.latitude };

              if (edgeStartMarker) edgeStartMarker.setMap(null);
              edgeStartMarker = new AMapInstance.CircleMarker({
                center: [node.longitude, node.latitude],
                radius: 5, // 圆点半径
                strokeColor: 'blue', // 边框颜色
                strokeWeight: 2, // 边框宽度
                fillColor: 'blue', // 填充颜色
                fillOpacity: 1, // 填充透明度
                map: map.value,
                cursor: 'pointer'
              });
            } else {
              edgeData.value.end_node = node.id;
              handleEdgeComplete(node);
            }
          }
        });

        existingNodeMarkers.push(marker);
      });

      // 绘制边
      existingEdges.value.forEach(edge => {
        const startNode = existingNodes.value.find(n => n.id === edge.start_node);
        const endNode = existingNodes.value.find(n => n.id === edge.end_node);

        if (startNode && endNode) {
          const polyline = new AMapInstance.Polyline({
            path: [
              [startNode.longitude, startNode.latitude],
              [endNode.longitude, endNode.latitude]
            ],
            strokeColor: "#1890FF",
            strokeWeight: 3,
            map: map.value
          });
          existingEdgePolylines.push(polyline);
        } else {
          console.error(`无法渲染边 (${edge.start_node} -> ${edge.end_node})，因为起点或终点节点不存在`);
        }
      });

      console.log("节点和边渲染完成");
    };

    // 修改后的地图点击处理
    const handleMapClick = (e) => {
      const clickedLng = e.lnglat.getLng();
      const clickedLat = e.lnglat.getLat();

      if (mode.value === "addNode") {
        // 检查是否在现有节点附近（10米内）
        const isExisting = existingNodes.value.some(node =>
          AMapInstance.GeometryUtil.distance(
            [node.longitude, node.latitude],
            [clickedLng, clickedLat]
          ) < 5
        );

        if (!isExisting) {
          clickedPosition.value = { lng: clickedLng, lat: clickedLat };
          newNodeDialogVisible.value = true;
        }
      } else if (mode.value === "addEdge") {
        // 查找最近的节点
        let minDist = Infinity;
        let closestNode = null;
        existingNodes.value.forEach(node => {
          const dist = AMapInstance.GeometryUtil.distance(
            [node.longitude, node.latitude],
            [clickedLng, clickedLat]
          );
          if (dist < minDist) {
            minDist = dist;
            closestNode = node;
          }
        });

        if (minDist > 10) {
          alert("请点击已有节点！");
          return;
        }

        if (!edgeStartPoint.value) {
          edgeData.value.start_node = closestNode.id;
          edgeStartPoint.value = { lng: closestNode.longitude, lat: closestNode.latitude };

          if (edgeStartMarker) edgeStartMarker.setMap(null);
          edgeStartMarker = new AMapInstance.CircleMarker({
            center: [node.longitude, node.latitude],
            radius: 5, // 圆点半径
            strokeColor: 'blue', // 边框颜色
            strokeWeight: 2, // 边框宽度
            fillColor: 'blue', // 填充颜色
            fillOpacity: 1, // 填充透明度
            map: map.value,
            cursor: 'pointer'
          });
        } else {
          edgeData.value.end_node = closestNode.id;

          // 检查边是否已存在
          const existingEdge = existingEdges.value.find(edge =>
            (edge.start_node === edgeData.value.start_node && edge.end_node === edgeData.value.end_node) ||
            (edge.start_node === edgeData.value.end_node && edge.end_node === edgeData.value.start_node)
          );

          if (existingEdge) {
            alert("该边已存在！");
            cancelEdgeAdding();
            return;
          }

          newNodeDialogVisible.value = true;
        }
      }
    };    
    // 添加新节点
    async function addNewNode() {
      try {
        const nodeData = {
          name: newNodeData.value.name,
          latitude: clickedPosition.value.lat,
          longitude: clickedPosition.value.lng
        }
        if (newNodeData.value.type) {
          nodeData.type = newNodeData.value.type;
        }
        if (newNodeData.value.popularity) {
          nodeData.popularity = newNodeData.value.popularity;
        }
        await axios.post("http://localhost:8000/map/add_node", {
          nodeData
        });
        await loadGraphData();
        newNodeDialogVisible.value = false;
        newNodeData.value = { name: "", type: null, popularity: null };
      } catch (error) {
        console.error("添加节点失败:", error);
      }
    }

    // 添加新边
    async function addNewEdge() {
      try {
        const edgeDataToSend = {
          start_node: edgeData.value.start_node,
          end_node: edgeData.value.end_node
        }
        if (edgeData.value.walk_speed) {
          edgeDataToSend.walk_speed = edgeData.value.walk_speed;
        }
        if (edgeData.value.bike_speed) {
          edgeDataToSend.bike_speed = edgeData.value.bike_speed;
        }
        if (edgeData.value.ebike_speed) {
          edgeDataToSend.ebike_speed = edgeData.value.ebike_speed;
        }
        await axios.post("http://localhost:8000/map/add_edge", {
          edgeDataToSend
        });
        await loadGraphData();
        edgeData.value = { start_node: -1, end_node: -1, walk_speed: null, bike_speed: null, ebike_speed: null };
        edgeStartPoint.value = null;
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
      mode,
      getNodeName,
      cancelEdgeAdding,
      cancelNodeAdding,
      existingEdges
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

.dialog-buttons {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.dialog-buttons button {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.dialog-buttons button:first-child {
  background-color: #1890ff;
  color: white;
  border: none;
}

.dialog-buttons button:last-child {
  background-color: #fff;
  border: 1px solid #d9d9d9;
}

.control-panel {
  position: absolute;
  top: 20px;
  left: 20px;
  background: white;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  border: 1px solid #1890ff;
  z-index: 999;
}

.control-panel h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
}

.control-panel select, 
.control-panel input {
  margin: 5px 0;
  padding: 4px;
  width: 200px;
}
</style>