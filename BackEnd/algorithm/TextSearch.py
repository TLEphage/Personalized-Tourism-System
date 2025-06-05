def kmp(text, pattern):
    def build_prefix_table(pattern):
        # 构建部分匹配表（Prefix Table）
        m = len(pattern)
        table = [0] * m
        length = 0  # length 是最长相等前后缀的长度
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                table[i] = length
                i += 1
            else:
                if length != 0:
                    length = table[length - 1]
                else:
                    table[i] = 0
                    i += 1
        return table

    def search(text, pattern):
        m = len(pattern)
        n = len(text)
        prefix_table = build_prefix_table(pattern)
        i = 0  # i 是文本串的索引
        j = 0  # j 是模式串的索引

        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
            if j == m:  # 如果完全匹配
                return i - j  # 返回匹配的起始位置
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = prefix_table[j - 1]
                else:
                    i += 1
        return -1  # 如果没有找到匹配的子串

    # 调用搜索函数
    return search(text, pattern) != -1

def boyer_moore(text, pattern):
    def build_bad_char_table(pattern):
        # 构建坏字符表，记录每个字符在模式串中的最后出现位置
        table = {}
        for i in range(len(pattern)):
            table[pattern[i]] = i
        return table

    def search(text, pattern):
        m = len(pattern)
        n = len(text)
        bad_char_table = build_bad_char_table(pattern)
        i = 0  # i 是文本串的索引

        while i <= n - m:
            j = m - 1  # 从模式串的末尾开始匹配
            while j >= 0 and pattern[j] == text[i + j]:
                j -= 1
            if j < 0:  # 如果完全匹配
                return i  # 返回匹配的起始位置
            else:
                # 计算坏字符的跳过距离
                bad_char_shift = j - bad_char_table.get(text[i + j], -1)
                i += max(1, bad_char_shift)
        return -1  # 如果没有找到匹配的子串

    # 调用搜索函数
    return search(text, pattern) != -1

def binary_search_by_attribute(data_list, attribute, target_value):
    """
    使用二分查找在有序列表中查找具有特定属性值的字典元素。
    
    参数:
        data_list (list): 包含字典的列表，字典的指定属性是有序的。
        attribute (str): 字典中的属性名，用于查找。
        target_value: 要查找的目标值。
    
    返回:
        dict: 如果找到匹配的字典，返回该字典；否则返回None。
    """
    # 初始化二分查找的左右边界
    left = 0
    right = len(data_list) - 1

    # 开始二分查找
    while left <= right:
        mid = (left + right) // 2  # 计算中间索引
        mid_value = data_list[mid].get(attribute)  # 获取中间元素的属性值

        if mid_value == target_value:  # 如果找到目标值
            return data_list[mid]  # 返回匹配的字典
        elif mid_value < target_value:  # 如果中间值小于目标值
            left = mid + 1  # 调整左边界
        else:  # 如果中间值大于目标值
            right = mid - 1  # 调整右边界

    return None  # 如果未找到目标值，返回None

# 示例使用
if __name__ == "__main__":
    # 示例数据列表，假设按"age"属性有序
    data = [
        {"name": "Alice", "age": 20},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 30},
        {"name": "David", "age": 35},
        {"name": "Eve", "age": 40}
    ]

    # 要查找的属性和目标值
    attribute_to_search = "age"
    target_value_to_search = 30

    # 调用二分查找函数
    result = binary_search_by_attribute(data, attribute_to_search, target_value_to_search)

    # 输出结果
    if result:
        print("找到匹配的字典:", result)
    else:
        print("未找到匹配的字典")