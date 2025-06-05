class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        """将元素及其优先级加入优先队列"""
        # 创建一个元组，包含优先级和元素
        entry = (priority, item)
        # 将新元素添加到堆的末尾
        self.heap.append(entry)
        # 调整堆，使其满足最小堆的性质
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        """弹出优先级最高的元素"""
        if not self.heap:
            raise KeyError('pop from an empty priority queue')
        # 将堆顶元素与最后一个元素交换
        self._swap(0, len(self.heap) - 1)
        # 弹出最后一个元素（原堆顶元素）
        priority, item = self.heap.pop()
        # 调整堆，使其满足最小堆的性质
        self._sift_down(0)
        return item

    def peek(self):
        """查看优先级最高的元素，但不移除"""
        if not self.heap:
            raise KeyError('peek from an empty priority queue')
        return self.heap[0][1]

    def is_empty(self):
        """检查优先队列是否为空"""
        return len(self.heap) == 0

    def __len__(self):
        """返回优先队列中元素的数量"""
        return len(self.heap)

    def _sift_up(self, index):
        """向上调整堆"""
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[parent_index][0] > self.heap[index][0]:
                self._swap(parent_index, index)
                index = parent_index
            else:
                break

    def _sift_down(self, index):
        """向下调整堆"""
        size = len(self.heap)
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest = index

            if left_child_index < size and self.heap[left_child_index][0] < self.heap[smallest][0]:
                smallest = left_child_index

            if right_child_index < size and self.heap[right_child_index][0] < self.heap[smallest][0]:
                smallest = right_child_index

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _swap(self, i, j):
        """交换堆中的两个元素"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

# 示例使用
pq = PriorityQueue()
pq.push('task1', priority=3)
pq.push('task2', priority=1)
pq.push('task3', priority=2)

print(pq.pop())  # 输出 task2，优先级最高（数值最小）
print(pq.pop())  # 输出 task3
print(pq.pop())  # 输出 task1

print(pq.is_empty())  # 输出 True