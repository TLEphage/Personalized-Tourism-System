<template>
  <div class="poi-container">
    <div id="map-container" v-show="currentMode !== 'indoor'" ></div>
    <div id="indoor-map-container" v-show="currentMode === 'indoor'"></div>

    <button class="developer-button" @click="goToDeveloper">开发者模式</button>

    <div class="nav-panel">
      <div class="mode-switch">
        <button 
          @click="switchMode('navigation')"
          :class="{ active: currentMode === 'navigation' }"
        >两点导航</button>
        <button
          @click="switchMode('multi')"
          :class="{ active: currentMode === 'multi'}"  
        >多点导航</button>
        <button
          @click="switchMode('search')"
          :class="{ active: currentMode === 'search' }"
        >附近搜索</button>
        <button
          @click="switchMode('indoor')"
          :class="{ active: currentMode === 'indoor' }"
        >室内导航</button>
      </div>

      <!-- 两点导航模式 -->
      <div v-if="currentMode === 'navigation'" class="mode-content">
        <div class="input-group">
          <label>区域模式</label>
          <div class="mode-buttons">
            <button @click="areaMode = 'campus'" :class="{ active: areaMode === 'campus' }">校园</button>
            <button @click="areaMode = 'scenic'" :class="{ active: areaMode === 'scenic' }">景区</button>
          </div>
        </div>
        <div class="nav-header">
          <h1 class="nav-title">北京邮电大学导航</h1>
          <p>请设置您的起点和终点</p>
        </div>

        <div class="input-group">
          <label>路径策略</label>
          <div class="strategy-buttons">
            <button @click="strategy = 'shortest_path'" :class="{ active: strategy === 'shortest_path' }">最短路径</button>
            <button @click="strategy = 'shortest_time'" :class="{ active: strategy === 'shortest_time' }">最短时间</button>
          </div>
        </div>

        <div class="input-group">
          <label>交通方式</label>
          <select name="input-field" v-model="selectedMode">
            <option v-for="option in modeOptions" :key="option.value" :value="option.value">
              {{ option.text }}
            </option>
          </select>
        </div>

        <div class="input-group">
          <label>起点位置</label>
          <div class="suggestion-container">
            <input
              type="text"
              class="input-field"
              v-model="startLocation"
              @input="handleStartInput"
              @focus="showStartSuggestions = true"
              @blur="onInputBlur('start')"
            />
            <div v-if="showStartSuggestions && startSuggestions.length" class="suggestion-box">
              <div 
                v-for="(suggestion, index) in startSuggestions" 
                :key="index"
                class="suggestion-item"
                @click="selectStartSuggestion(suggestion)"
              >
                {{ suggestion }}
              </div>
            </div>
          </div>
        </div>

        <div class="input-group">
          <label>终点位置</label>
          <div class="suggestion-container">
            <input
              type="text"
              class="input-field"
              v-model="endLocation"
              @input="handleEndInput"
              @focus="showEndSuggestions = true"
              @blur="onInputBlur('end')"
            />
            <div v-if="showEndSuggestions && endSuggestions.length" class="suggestion-box">
              <div 
                v-for="(suggestion, index) in endSuggestions" 
                :key="index"
                class="suggestion-item"
                @click="selectEndSuggestion(suggestion)"
              >
                {{ suggestion }}
              </div>
            </div>
          </div>
        </div>

        <button class="nav-button" @click="startNavigation">开始导航</button>

        <div class="route-info">
          <h3>推荐路线信息</h3>
          <p>🗺️ 总距离: {{ totalDistance }} m</p>
          <p>⏱️ 预计时间: {{ estimatedTime }} s</p>
          <p>🚩 途径: {{ points }}</p>
        </div>
      </div>

      <!-- 多点导航模式 -->
      <div v-if="currentMode === 'multi'" class="mode-content">
        <div class="input-group">
          <label>区域模式</label>
          <div class="mode-buttons">
            <button @click="multiAreaMode = 'campus'" :class="{ active: multiAreaMode === 'campus' }">校园</button>
            <button @click="multiAreaMode = 'scenic'" :class="{ active: multiAreaMode === 'scenic' }">景区</button>
          </div>
        </div>
        <div class="nav-header">
          <h1 class="nav-title">多点路径规划</h1>
          <p>请按顺序添加多个景点</p>
        </div>

        <div class="input-group">
          <label>交通方式</label>
          <select name="input-field" v-model="selectedMode">
            <option v-for="option in modeOptions" :key="option.value" :value="option.value">
              {{ option.text }}
            </option>
          </select>
        </div>

        <div class="multi-points-container">
          <div class="point-item" v-for="(point, index) in multiPoints" :key="index">
            <div class="point-header">
              <span class="point-number">地点 {{ index + 1 }}</span>
              <div class="point-actions">
                <button @click="movePointUp(index)" :disabled="index === 0">↑</button>
                <button @click="movePointDown(index)" :disabled="index === multiPoints.length - 1">↓</button>
                <button @click="removePoint(index)">×</button>
              </div>
            </div>
            <div class="suggestion-container">
              <input
                type="text"
                class="input-field"
                v-model="multiPoints[index].name"
                @input="handleMultiInput(index, $event)"
                @focus="setActiveSuggestionIndex(index)"
                @blur="onMultiInputBlur(index)"
              />
              <div 
                v-if="activeSuggestionIndex === index && multiSuggestions[index] && multiSuggestions[index].length" 
                class="suggestion-box"
                @mouseleave="activeSuggestionIndex = null"
              >
                <div 
                  v-for="(suggestion, sIndex) in multiSuggestions[index]" 
                  :key="sIndex"
                  class="suggestion-item"
                  @click="selectMultiSuggestion(index, suggestion)"
                >
                  {{ suggestion }}
                </div>
              </div>
            </div>
          </div>

          <button class="add-point-btn" @click="addPoint">
            + 添加地点
          </button>
        </div>

        <button class="nav-button" @click="startMultiNavigation" :disabled="multiPoints.length < 2">
          {{ multiPoints.length < 2 ? '请至少添加两个地点' : '开始多点导航' }}
        </button>

        <div class="route-info">
          <h3>多点路线信息</h3>
          <p>🗺️ 总距离: {{ multiTotalDistance }} m</p>
          <p>⏱️ 预计时间: {{ multiEstimatedTime }} min</p>
          <p>🚩 途径: {{ multiPoints.join(" → ") }}</p>
        </div>
      </div>

      <!-- 搜索模式 -->
      <div v-if="currentMode === 'search'" class="mode-content">
        <div class="input-group">
          <label>当前位置</label>
          <input
            type="text"
            class="input-field"
            :value="currentPositionText"
            readonly
          />
          <p class="hint">点击地图选择位置</p>
        </div>

        <div class="input-group">
          <label>服务类型</label>
          <select class="input-field" v-model="selectedServiceType">
            <option value="超市">超市</option>
            <option value="洗手间">洗手间</option>
            <option value="食堂">食堂</option>
            <option value="商店">商店</option>
            <option value="图书馆">图书馆</option>
            <option value="饭店">饭店</option>
            <option value="咖啡馆">咖啡馆</option>
          </select>
        </div>

        <div class="input-group">
          <label>最大结果数量</label>
          <input
            type="number"
            class="input-field"
            v-model="maxResults"
            placeholder="例如：10"
            min="1"
          />
          <p class="hint">最多显示的结果数量</p>
        </div>

        <div class="input-group">
          <label>搜索范围</label>
          <input
            type="number"
            class="input-field"
            v-model="maxDistance"
            placeholder="例如：1000"
            min="0"
          />
          <p class="hint">单位为米</p>
        </div>

        <button class="nav-button" @click="searchPlaces">搜索附近</button>

        <div class="search-results">
          <h3>搜索结果</h3>
          <div v-if="searchResults.length === 0" class="no-results">
            暂无搜索结果
          </div>
          <div 
            v-for="(place, index) in searchResults"
            :key="index"
            class="place-item"
          >
            <h4>{{ place.name }}</h4>
            <p>距离：{{ place.distance }}米</p>
            <p>类型：{{ place.type }}</p>
            <p v-if="place.polularity">人气值：{{ place.polularity }}</p>
          </div>
        </div>
      </div>

      <!-- 室内导航模式 -->
      <div v-if="currentMode === 'indoor'" class="mode-content">
        <div class="input-group">
          <label>当前楼层</label>
          <div class="floor-control">
            <button 
              v-for="floor in availableFloors" 
              :key="floor"
              @click="switchFloor(floor)"
              :class="{ active: currentFloor === floor }"
            >
              {{ floor }}楼
            </button>
          </div>
        </div>

        <div class="input-group">
          <label>起点位置</label>
          <input
            type="text"
            class="input-field"
            v-model="startIndoorLocation"
            placeholder="例如：DIOR"
          />
        </div>

        <div class="input-group">
          <label>终点位置</label>
          <input
            type="text"
            class="input-field"
            v-model="endIndoorLocation"
            placeholder="例如：DIOR"
          />
        </div>

        <button class="nav-button" @click="startIndoorNavigation">开始室内导航</button>

        <div class="route-info">
          <h3>室内路线信息</h3>
          <p>🗺️ 当前楼层距离: {{ indoorDistance }} m</p>
          <p>🚩 途径: {{ indoorPoints }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref, computed, onBeforeUnmount } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";
import axios from 'axios';

export default {
  name: "MapComponent",
  setup() {
    const areaMode = ref("campus");
    const multiAreaMode = ref("campus");
    const strategy = ref("shortest_path");
    const startLocation = ref("");
    const endLocation = ref("");
    const totalDistance = ref(0);
    const estimatedTime = ref(0);
    const points = ref("");
    const map = ref(null);
    const selectedMode = ref(1);

    const currentMode = ref('navigation');
    const selectedServiceType = ref('超市');
    const currentPosition = ref(null);
    const searchResults = ref([]);
    const maxResults = ref(10);
    const maxDistance = ref(1000);

    const multiPoints = ref([{name: ""}]);
    const multiTotalDistance = ref(0);
    const multiEstimatedTime = ref(0);

    const startSuggestions = ref([]);
    const endSuggestions = ref([]);
    const showStartSuggestions = ref(false);
    const showEndSuggestions = ref(false);
    const multiSuggestions = ref([[]]);
    const activeSuggestionIndex = ref(null);
    const suggestionTimeout = ref(null);

    // 室内导航相关变量
    const buildingId = ref("B000A856LJ");
    const startIndoorLocation = ref("");
    const endIndoorLocation = ref("");
    const indoorPoints = ref("");
    const indoorDistance = ref(0.0);
    const currentFloor = ref("1L");
    const availableFloors = ref(["1L", "2L", "3L"]);
    let indoorMapInstance = null;

    // 用来存当前绘制到地图上的点和线
    let routeMarkers = [];
    let routePolyline = null;

    // 用于保存室内路径数据
    const indoorRouteData = ref(null);
    
    // 室内路径覆盖物
    let indoorRouteMarkers = [];
    let indoorRoutePolyline = null;

    let AMapInstance = null;

    onMounted(() => {
      window._AMapSecurityConfig = { securityJsCode: "ea176f2888ff519f13260e12af956fe6" };
      AMapLoader.load({
        key: "aeefd3c2789d4655bbc8596c2131a8b7",
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
      document.addEventListener('click', handleGlobalClick);
    });

    onBeforeUnmount(() => {
      // 组件卸载时移除监听
      document.removeEventListener('click', handleGlobalClick);
    });

    const initIndoorMap = () => {
      window._AMapSecurityConfig = { securityJsCode: "ea176f2888ff519f13260e12af956fe6" };
      AMapLoader.load({
        key: "aeefd3c2789d4655bbc8596c2131a8b7",
        version: "2.0",
        plugins: ['AMap.IndoorMap']
      }).then((AMap) => {
        indoorMapInstance = new AMap.Map('indoor-map-container', {
          center:[116.518542, 39.924677],
          zoom: 18,
          viewMode: '3D',
          pitch: 40,
          showIndoorMap: true
        });

        new AMap.IndoorMap({
          map: indoorMapInstance,
          zIndex: 1000,
        });

        console.log("加载室内地图");
      });
    }

    function handleGlobalClick(event) {
      const isInput = event.target.classList.contains('input-field');
      const isSuggestion = event.target.classList.contains('suggestion-item');
      const isSuggestionBox = event.target.classList.contains('suggestion-box');
 
      
      if (!isInput && !isSuggestion && !isSuggestionBox) {
        showStartSuggestions.value = false;
        showEndSuggestions.value = false;
        activeSuggestionIndex.value = null;
      }
    }

    async function startNavigation() {
      if (!startLocation.value || !endLocation.value) {
        alert("请填写起点和终点位置！");
        return;
      }

      let apiUrl = '';
      let request = ref({});
      if(strategy.value === 'shortest_path') {
        apiUrl = 'http://localhost:8000/map/path_plan/one_to_one_shortest_path';
        request.value = {
          start: startLocation.value,
          end: endLocation.value
        };
      } else {
        let mode = ref("");
        if(selectedMode.value === 0) mode = 'walk'; 
        else if(selectedMode.value === 1 && areaMode === 'campus') mode = 'bike'; 
        else if(selectedMode.value === 1 && areaMode === 'scenic') mode = 'ebike';
        else if(selectedMode.value === 2 && areaMode === 'campus') mode = 'walk_bike'; 
        else if(selectedMode.value === 2 && areaMode === 'scenic') mode = 'walk_ebike';
        apiUrl = 'http://localhost:8000/map/path_plan/one_to_one_shortest_time';
        request.value = {
          start: startLocation.value,
          end: endLocation.value,
          mode: mode
        };
      }
      axios.post(apiUrl,request.value)
      .then(res => {
        const data = res.data;
        console.log("路径规划结果:", data);
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

       // —— 组装坐标数组 ——
       const coords = route.map(p => [p.longitude, p.latitude]);

       // —— 画连线 —— 
       routePolyline = new AMapInstance.Polyline({
         path: coords,
         strokeColor: "#FF0000",
         strokeWeight: 4,
         strokeOpacity: 0.8,
         lineJoin: "round",
         map: map.value
       });

       const startPoint = route[0];
       const endPoint = route[route.length - 1];


      // 绘制起点标记（绿色）
      const startMarker = new AMapInstance.Marker({
        position: [startPoint.longitude, startPoint.latitude],
        map: map.value,
        title: startPoint.name, 
      });
      
      startMarker.setLabel({
        offset: new AMapInstance.Pixel(-10, -28),
        content: `<div style="
          background: #4CAF50;
          color: #fff;
          padding: 2px 4px;
          border-radius: 3px;
          font-size: 12px;
        ">起点: ${startPoint.name}</div>`
      });
      routeMarkers.push(startMarker);

      // 绘制终点标记（红色）
      const endMarker = new AMapInstance.Marker({
        position: [endPoint.longitude, endPoint.latitude],
        map: map.value,
        title: endPoint.name,
        
      });
      
      endMarker.setLabel({
        offset: new AMapInstance.Pixel(-10, -28),
        content: `<div style="
          background: #F44336;
          color: #fff;
          padding: 2px 4px;
          border-radius: 3px;
          font-size: 12px;
        ">终点: ${endPoint.name}</div>`
      });
      routeMarkers.push(endMarker);
      
       // —— 自动缩放视野到所有点和线 —— 
      map.value.setFitView();

        console.log("已绘制路径和标记");
      })
      .catch(err => {
        console.error("路径规划失败：", err);
      });
    }

    // 添加模式切换方法
    function switchMode(mode) {
      currentMode.value = mode;
      clearMapOverlays();
      
      if (mode === 'search') {
        setupMapClickListener();
      } else {
        removeMapClickListener();
      }

      if (mode === 'indoor' && !indoorMapInstance) {
        console.log('初始化室内地图')
        initIndoorMap();
      }
    }

    // 添加地图点击监听
    let mapClickListener = null;
    function setupMapClickListener() {
      if (map.value) {
        mapClickListener = map.value.on('click', (e) => {
          currentPosition.value = {
            lng: e.lnglat.getLng(),
            lat: e.lnglat.getLat()
          };
          addPositionMarker(e.lnglat);
        });
      }
    }

    function removeMapClickListener() {
      if (mapClickListener) {
        map.value.off('click', mapClickListener);
        mapClickListener = null;
      }
    }

    // 添加位置标记
    let positionMarker = null;
    function addPositionMarker(lnglat) {
      if (positionMarker) {
        positionMarker.setMap(null);
      }
      
      positionMarker = new AMapInstance.Marker({
        position: [lnglat.lng, lnglat.lat],
        map: map.value,
        title: "当前位置"
      })
      positionMarker.setLabel({
        offset: new AMapInstance.Pixel(-10, -28),
        content: `<div style="
          background: #f33;
          color: #fff;
          padding: 2px 4px;
          border-radius: 3px;
          font-size: 12px;
        ">当前位置</div>`
      });

    }

    let searchResultMarkers = [];
    function showSearchResultsOnMap(results) {
      // 清除之前的搜索结果标记
      searchResultMarkers.forEach(marker => marker.setMap(null));
      searchResultMarkers = [];

      results.forEach(place => {
        // 创建标记
        const marker = new AMapInstance.Marker({
          position: [place.longitude, place.latitude],
          map: map.value,
          title: place.name
        });

        marker.setLabel({
           offset: new AMapInstance.Pixel(-10, -28),
           content: `<div style="
             background: #f33;
             color: #fff;
             padding: 2px 4px;
             border-radius: 3px;
             font-size: 12px;
           ">${place.name}</div>`
         });

        // 创建信息窗体
        const infoWindow = new AMapInstance.InfoWindow({
          content: `
            <div style="padding: 10px;">
              <h4 style="margin: 0 0 5px 0;">${place.name}</h4>
              <p style="margin: 0;">距离：${place.distance.toFixed(0)}米</p>
            </div>
          `,
          offset: new AMapInstance.Pixel(0, -30)
        });

        // 点击标记时显示信息窗体
        marker.on('click', () => {
          infoWindow.open(map.value, marker.getPosition());
        });

        searchResultMarkers.push(marker);
      });

      // 调整地图视野以包含所有标记
      if (searchResultMarkers.length > 0) {
        map.value.setFitView(searchResultMarkers);
      }
    }

    function focusPlace(place) {
      map.value.setZoomAndCenter(18, [place.longitude, place.latitude]);

      const marker = searchResultMarkers.find(m => 
        m.getPosition().lng === place.longitude && 
        m.getPosition().lat === place.latitude
      );

      if (marker) {
        marker.emit('click');
      }
    }

    // 添加搜索方法
    async function searchPlaces() {
      if (!currentPosition.value) {
        alert('请先在地图上选择当前位置');
        return;
      }
      routeMarkers.forEach(marker => marker.setMap(null));
      routeMarkers = [];

      try {
        console.log('搜索类型:', selectedServiceType.value);
        console.log('当前位置:', currentPosition.value);
        console.log('最大结果数:', maxResults.value);
        console.log('最大距离:', maxDistance.value);
        const response = await axios.post('http://localhost:8000/map/search_places', {
          longitude: currentPosition.value.lng,
          latitude: currentPosition.value.lat,
          query_type: selectedServiceType.value,
          max_results: maxResults.value,
          max_distance: maxDistance.value
        });
        console.log("搜索结果：", response.data.places);
        searchResults.value = response.data.places;
        showSearchResultsOnMap(response.data.places);
      } catch (error) {
        console.error('搜索失败:', error);
        alert('搜索失败，请稍后重试');
      }
    }

    // 在地图展示搜索结果
    function showSearchResultsOnMap(results) {
      results.forEach(place => {
        const marker = new AMapInstance.Marker({
          position: [place.longitude, place.latitude],
          map: map.value,
          title: place.name,
          content: `<div class="custom-marker">${place.name}</div>`
        });
        routeMarkers.push(marker);
      });
      map.value.setFitView();
    }

    // 计算属性显示当前位置文本
    const currentPositionText = computed(() => {
      return currentPosition.value 
        ? `经度: ${currentPosition.value.lng.toFixed(4)}, 纬度: ${currentPosition.value.lat.toFixed(4)}`
        : '未选择位置';
    });

    const modeOptions = computed(() => {
      if (currentMode.value === 'navigation') {
        // 两点导航选项
        if (areaMode.value === 'campus') {
          return [
            { text: '步行', value: 'walk' },
            { text: '自行车', value: 'bike' },
            { text: '混合', value: 'walk_bike' }
          ];
        } else {
          return [
            { text: '步行', value: 'walk' },
            { text: '电动车', value: 'ebike' },
            { text: '混合', value: 'walk_ebike' }
          ];
        }
      } else {
        // 多点导航选项
        if (multiAreaMode.value === 'campus') {
          return [
            { text: '步行', value: 'walk' },
            { text: '自行车', value: 'bike' },
            { text: '混合', value: 'walk_bike' }
          ];
        } else {
          return [
            { text: '步行', value: 'walk' },
            { text: '电动车', value: 'ebike' },
            { text: '混合', value: 'walk_ebike' }
          ];
        }
      }
    });


    // 清理地图覆盖物时同时清理搜索标记
    function clearMapOverlays() {
      // 保留原有清理逻辑，增加：
      if (positionMarker) {
        positionMarker.setMap(null);
        positionMarker = null;
      }
      searchResults.value = [];
    }

    //多点导航相关函数
    const addPoint = () => {
      multiPoints.value.push({name: ""});
      multiSuggestions.value.push([]);
    };

    const removePoint = (index) => {
      multiPoints.value.splice(index, 1);
      multiSuggestions.value.splice(index, 1);
    };

    const movePointUp = (index) => {
      if (index > 0) {
        const temp = multiPoints.value[index];
        multiPoints.value[index] = multiPoints.value[index - 1];
        multiPoints.value[index - 1] = temp;
      }
    };

    const movePointDown = (index) => {
      if (index < multiPoints.value.length - 1) {
        const temp = multiPoints.value[index];
        multiPoints.value[index] = multiPoints.value[index + 1];
        multiPoints.value[index + 1] = temp;
      }
    };

    const fetchSuggestions = async (query, target) => {
      if (!query.trim()) {
        if (target === 'start') {
          startSuggestions.value = [];
        } else if (target === 'end') {
          endSuggestions.value = [];
        } else if (typeof target === 'number') {
          multiSuggestions.value[target] = [];
        }
        return;
      }
      
      try {
        const response = await axios.get(`http://localhost:8000/map/search_nodes?name=${query}`);
        const suggestions = response.data || [];
        console.log('获取搜索建议成功:', suggestions);
        
        if (target === 'start') {
          startSuggestions.value = suggestions;
        } else if (target === 'end') {
          endSuggestions.value = suggestions;
        } else if (typeof target === 'number') {
          multiSuggestions.value[target] = suggestions;
        }
      } catch (error) {
        console.error('获取搜索建议失败:', error);
      }
    };

    // 防抖处理
    const debounce = (func, delay) => {
      return (...args) => {
        clearTimeout(suggestionTimeout.value);
        suggestionTimeout.value = setTimeout(() => {
          func.apply(this, args);
        }, delay);
      };
    };

    const debouncedFetchSuggestions = debounce(fetchSuggestions, 300);

    // 起点输入处理
    const handleStartInput = (event) => {
      const query = event.target.value;
      debouncedFetchSuggestions(query, 'start');
    };
    
    // 终点输入处理
    const handleEndInput = (event) => {
      const query = event.target.value;
      debouncedFetchSuggestions(query, 'end');
    };
    
    // 多点输入处理
    const handleMultiInput = (index, event) => {
      const query = event.target.value;
      debouncedFetchSuggestions(query, index);
    };
    
    // 选择起点建议
    const selectStartSuggestion = (suggestion) => {
      startLocation.value = suggestion;
      showStartSuggestions.value = false;
    };
    
    // 选择终点建议
    const selectEndSuggestion = (suggestion) => {
      endLocation.value = suggestion;
      showEndSuggestions.value = false;
    };
    
    // 选择多点建议
    const selectMultiSuggestion = (index, suggestion) => {
      multiPoints.value[index].name = suggestion;
      activeSuggestionIndex.value = null;
    };
    
    // 设置当前活跃的多点输入索引
    const setActiveSuggestionIndex = (index) => {
      activeSuggestionIndex.value = index;
      if (multiPoints.value[index].name) {
        debouncedFetchSuggestions(multiPoints.value[index].name, index);
      }
    };
    
    // 输入框失去焦点处理
    const onInputBlur = (type) => {
      setTimeout(() => {
        if (type === 'start') showStartSuggestions.value = false;
        if (type === 'end') showEndSuggestions.value = false;
      }, 200);
    };
    
    // 多点输入框失去焦点处理
    const onMultiInputBlur = (index) => {
      setTimeout(() => {
        if (activeSuggestionIndex.value === index) {
          activeSuggestionIndex.value = null;
        }
      }, 200);
    };
    
    // 多点导航API调用
    async function startMultiNavigation() {
      if (multiPoints.value.length < 2) {
        alert("请至少添加两个地点");
        return;
      }

      // 检查所有地点是否已填写
      if (multiPoints.value.some(point => !point.name.trim())) {
        alert("请填写所有地点");
        return;
      }

      try {
        console.log("start:", multiPoints.value[0]);
        console.log("end:", multiPoints.value.slice(1));
        const response = await axios.post('http://localhost:8000/map/path_plan/one_to_many_shortest_path', {
          start: multiPoints.value[0].name,
          end: multiPoints.value.slice(1).map(point => point.name)
        });
        
        const data = response.data;
        console.log("多点路径规划结果:", data);
        
        if (data.path.length === 0) {
          alert("未找到路线");
          return;
        }

        // 更新路线信息
        multiTotalDistance.value = data.distance;
        multiEstimatedTime.value = data.time;

        if (!AMapInstance) {
          alert("地图加载失败，请稍后再试！");
          return;
        }

        // 清除旧覆盖物
        routeMarkers.forEach(m => m.setMap(null));
        routeMarkers = [];
        if (routePolyline) {
          routePolyline.setMap(null);
          routePolyline = null;
        }

        // 组装坐标数组
        const coords = data.path.map(p => [p.longitude, p.latitude]);

        // 绘制用户输入的点（带序号）
        const userPoints = data.path.filter((p, index) => 
          index === 0 || index === data.path.length - 1 || 
          multiPoints.value.some(mp => mp.name === p.name)
        );

        // 绘制路径点
        userPoints.forEach((p, index) => {
          const marker = new AMapInstance.Marker({
            position: [p.longitude, p.latitude],
            map: map.value,
            title: p.name
          });
          
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

        // 画连线
        routePolyline = new AMapInstance.Polyline({
          path: coords,
          strokeColor: "#FF0000",
          strokeWeight: 4,
          strokeOpacity: 0.8,
          lineJoin: "round",
          map: map.value,
          showDir: true, // 添加方向箭头
          dirColor: "#FFFFFF", // 箭头颜色
          dirSize: 16 // 箭头大小
        });

        // 自动缩放视野
        map.value.setFitView();

        console.log("已绘制多点路径");
      } catch (error) {
        console.error("多点导航失败:", error);
        alert("多点导航失败，请重试");
      }
    }

    function loadIndoorMap() {
      if (!map.value) {
        alert('地图尚未初始化完成，请稍后再试');
        return;
      }
      
      const bid = buildingId.value;
      if (!bid) {
        alert('请输入建筑物ID');
        return;
      }

      // 监听室内地图创建事件
      map.value.on('indoor_create', () => {
        indoorMap = map.value.indoormap;
        indoorMap.showIndoorMap(bid, () => {
          console.log('室内地图加载完成');
          
          // 监听楼层变化
          indoorMap.on('floor_change', (event) => {
            currentFloor.value = event.floor;
            fetchIndoorRoute();
          });
          
          // 获取可用楼层
          availableFloors.value = indoorMap.getFloors();
          currentFloor.value = indoorMap.getFloor();
        });
      });
    }


    function switchFloor(floor) {
      currentFloor.value = floor;
      fetchIndoorRoute();
    }

    // 绘制室内路径
    const drawIndoorRoute = (route) => {
      // 清除旧的覆盖物
      indoorRouteMarkers.forEach(m => m.setMap(null));
      indoorRouteMarkers = [];
      
      if (indoorRoutePolyline) {
        indoorRoutePolyline.setMap(null);
        indoorRoutePolyline = null;
      }

      if (!route || route.length === 0) {
        alert("未找到当前楼层的室内路径");
        return;
      }

      // 组装坐标数组
      const coords = route.map(p => [p.longitude, p.latitude]);

      // 画连线
      indoorRoutePolyline = new AMap.Polyline({
        path: coords,
        strokeColor: "#4169E1", // 使用不同的颜色区分室内路径
        strokeWeight: 6,
        strokeOpacity: 0.8,
        lineJoin: "round",
        map: indoorMapInstance
      });

      // 绘制起点和终点标记
      const startPoint = route[0];
      const startMarker = new AMap.Marker({
        position: [startPoint.longitude, startPoint.latitude],
        map: indoorMapInstance,
        title: startPoint.name,
      });
      
      startMarker.setLabel({
        offset: new AMap.Pixel(-10, -28),
        content: `<div style="
          background: #4CAF50;
          color: #fff;
          padding: 2px 4px;
          border-radius: 3px;
          font-size: 12px;
        ">起点: ${startPoint.name}</div>`
      });
      indoorRouteMarkers.push(startMarker);

      const endPoint = route[route.length - 1];
      const endMarker = new AMap.Marker({
        position: [endPoint.longitude, endPoint.latitude],
        map: indoorMapInstance,
        title: endPoint.name,
      });
      
      endMarker.setLabel({
        offset: new AMap.Pixel(-10, -28),
        content: `<div style="
          background: #F44336;
          color: #fff;
          padding: 2px 4px;
          border-radius: 3px;
          font-size: 12px;
        ">终点: ${endPoint.name}</div>`
      });
      indoorRouteMarkers.push(endMarker);
      
      // 自动缩放视野到所有点和线
      indoorMapInstance.setFitView();
    }

    async function startIndoorNavigation() {
      if (!startIndoorLocation.value || !endIndoorLocation.value) {
        alert("请填写起点和终点位置！");
        return;
      }

      try {
        console.log("startIndoorNavigation");
        const response = await axios.post('http://localhost:8000/map/path_plan/indoor_shortest_path', {
            start: startIndoorLocation.value,
            end: endIndoorLocation.value
        });
        console.log("获取室内导航结果成功:", response.data);
        if(response.data.success !== true) {
          alert("无法规划 indoor 路径，请检查输入的 indoor 位置！");
        }
        console.log("室内导航成功");
        // 开始导航后自动获取当前楼层路径
        fetchIndoorRoute();
      } catch (error) {
        console.error("室内导航失败:", error);
        alert("室内导航失败，请重试");
      }
    }

    async function fetchIndoorRoute() {
      console.log("当前楼层： " +  currentFloor.value);
      try {
        const response = await axios.get(`http://localhost:8000/map/path_plan/indoor_shortest_path?floor=${currentFloor.value}`);
        const data = response.data;
        console.log("室内导航结果:", data.path);
        console.log(data.distance);
        indoorRouteData.value = data;
        const currentFloorRoute = indoorRouteData.value.path.filter(
          point => point.floor === currentFloor.value
        );
        indoorPoints.value = currentFloorRoute.map(p => p.name).join(" → ");
        indoorDistance.value = data.distance;
        drawIndoorRoute(currentFloorRoute);
      } catch (error) {
        console.error("获取室内路径失败:", error);
      }
    }



    return { 
      startLocation, 
      endLocation, 
      totalDistance, 
      estimatedTime, 
      points, 
      startNavigation,
      currentMode,
      selectedServiceType,
      searchResults,
      currentPositionText,
      switchMode,
      searchPlaces,
      maxResults,
      maxDistance,
      focusPlace,
      multiPoints,
      multiTotalDistance,
      multiEstimatedTime,
      addPoint,
      removePoint,
      movePointUp,
      movePointDown,
      startMultiNavigation,
      modeOptions,
      areaMode,
      multiAreaMode,
      strategy,
      startSuggestions,
      endSuggestions,
      showStartSuggestions,
      showEndSuggestions,
      multiSuggestions,
      activeSuggestionIndex,
      handleStartInput,
      handleEndInput,
      handleMultiInput,
      selectStartSuggestion,
      selectEndSuggestion,
      selectMultiSuggestion,
      setActiveSuggestionIndex,
      onInputBlur,
      onMultiInputBlur,
      buildingId,
      startIndoorLocation,
      endIndoorLocation,
      indoorPoints,
      loadIndoorMap,
      startIndoorNavigation,
      currentFloor,
      availableFloors,
      switchFloor,
      indoorDistance
     };
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

.mode-switch {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.mode-switch button {
  flex: 1;
  padding: 0.8rem;
  border: 2px solid #ddd;
  background: #f8f9fa;
  color: #333;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.mode-switch button.active {
  border-color: var(--primary-color);
  background: var(--primary-color);
  color: white;
}

.hint {
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.5rem;
}

.search-results {
  margin-top: 2rem;
  max-height: 400px;
  overflow-y: auto;
}

.place-item {
  background: #f8f9fa;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.place-item:hover {
  background: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.place-item h4 {
  margin: 0 0 0.5rem;
  color: var(--primary-color);
}

.place-item p {
  margin: 0.25rem 0;
  color: #666;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.custom-marker {
  background: white;
  padding: 4px 8px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

#map-container, #indoor-map-container {
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

input-group .hint {
  font-size: 0.75rem;
  color: #999;
  margin-top: 0.25rem;
  line-height: 1.4;
}

.input-field[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
}
.input-field::-webkit-outer-spin-button,
.input-field::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.mode-buttons, .strategy-buttons {
  display: flex;
  gap: 10px;
  margin-top: 5px;
}

.mode-buttons button, .strategy-buttons button {
  flex: 1;
  padding: 8px 12px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.mode-buttons button.active, .strategy-buttons button.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.suggestion-container {
  position: relative;
  width: 100%;
}

.suggestion-box {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 1000; /* 确保在最顶层 */
  max-height: 200px;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 8px 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background 0.2s;
}

.suggestion-item:hover {
  background-color: #f5f5f5;
}

.point-item {
  position: relative;
  margin-bottom: 15px;
}

.input-group {
  overflow: visible;
}

.floor-control {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.floor-control button {
  padding: 6px 12px;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.floor-control button.active {
  background: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

</style>  
