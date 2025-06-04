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