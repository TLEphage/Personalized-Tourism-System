
const renderGraphElements = () => {
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
      cursor: 'pointer',
      icon: new AMapInstance.Icon({
        image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
        size: new AMapInstance.Size(20, 20),
        imageSize: new AMapInstance.Size(20, 20)
      })
    });

    // 为当前 marker 添加点击事件
    marker.on('click', () => {
      if (mode.value === 'addEdge') {
        if (!edgeStartPoint.value) {
          edgeData.value.start_node = node.id;
          edgeStartPoint.value = { lng: node.longitude, lat: node.latitude };
          
          if (edgeStartMarker) edgeStartMarker.setMap(null);
          edgeStartMarker = new AMapInstance.Marker({
            position: [node.longitude, node.latitude],
            map: map.value,
            icon: new AMapInstance.Icon({
              image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png',
              size: new AMapInstance.Size(20, 20),
              imageSize: new AMapInstance.Size(20, 20)
            })
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
    }
  });
  console.log("节点和边渲染完成");
}
