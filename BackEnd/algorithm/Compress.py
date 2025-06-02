import json
import base64
import heapq
from collections import defaultdict

class HuffmanCompressor:
    """自定义哈夫曼编码压缩器"""
    """使用的模块: file_utils.py"""
    
    @staticmethod
    def _build_frequency_dict(data):
        """构建字符频率字典"""
        frequency = defaultdict(int)
        for char in data:
            frequency[char] += 1
        return frequency
    
    @staticmethod
    def _build_huffman_tree(frequency):
        """构建哈夫曼树"""
        heap = [[weight, [char, ""]] for char, weight in frequency.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        
        return heap[0][1:]
    
    @staticmethod
    def _build_code_dict(huffman_tree):
        """构建编码字典"""
        return {char: code for char, code in huffman_tree}
    
    @staticmethod
    def _serialize_tree(huffman_tree):
        """序列化哈夫曼树"""
        return json.dumps(huffman_tree)
    
    @staticmethod
    def _deserialize_tree(serialized_tree):
        """反序列化哈夫曼树"""
        return json.loads(serialized_tree)
    
    @staticmethod
    def compress(data):
        """压缩数据"""
        if not data:
            return b''
        
        frequency = HuffmanCompressor._build_frequency_dict(data)
        huffman_tree = HuffmanCompressor._build_huffman_tree(frequency)
        code_dict = HuffmanCompressor._build_code_dict(huffman_tree)
        
        encoded_bits = ''.join([code_dict[char] for char in data])
        
        # 填充位数使长度为8的倍数
        padding = 8 - (len(encoded_bits) % 8)
        encoded_bits += '0' * padding
        
        # 将比特串转换为字节
        bytes_list = []
        for i in range(0, len(encoded_bits), 8):
            byte = encoded_bits[i:i+8]
            bytes_list.append(int(byte, 2))
        
        # 构建压缩数据: 树信息 + 填充位数 + 压缩数据
        compressed_data = {
            'tree': HuffmanCompressor._serialize_tree(huffman_tree),
            'padding': padding,
            'data': base64.b64encode(bytes(bytes_list)).decode('ascii')  # 转为Base64字符串
        }
        
        return json.dumps(compressed_data).encode('utf-8')
    
    @staticmethod
    def decompress(compressed_data):
        """解压数据"""
        if not compressed_data:
            return ''
        
        compressed_dict = json.loads(compressed_data.decode('utf-8'))
        huffman_tree = HuffmanCompressor._deserialize_tree(compressed_dict['tree'])
        padding = compressed_dict['padding']
        byte_data = base64.b64decode(compressed_dict['data'])  # 解码Base64
        
        # 重建编码字典
        code_dict = {code: char for char, code in huffman_tree}
        
        # 将字节转换为比特串
        bit_str = ''
        for byte in byte_data:
            bits = bin(byte)[2:].rjust(8, '0')
            bit_str += bits
        
        # 移除填充的0
        bit_str = bit_str[:-padding] if padding > 0 else bit_str
        
        # 解码数据
        current_code = ''
        decoded_data = []
        for bit in bit_str:
            current_code += bit
            if current_code in code_dict:
                decoded_data.append(code_dict[current_code])
                current_code = ''
        
        return ''.join(decoded_data)