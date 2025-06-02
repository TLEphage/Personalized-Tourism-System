def partial_selection_sort(lst, sort_key=None, sort_order='asc', max_number=None):
    """
    对列表进行部分选择排序
    使用该函数的模块: spot_service
    :param lst: 待排序的列表
    :param sort_key: 排序依据的键（函数），默认为None，即直接比较元素
    :param sort_order: 排序顺序，'asc'表示升序，'desc'表示降序，默认为'asc'
    :param max_number: 最多排序的元素数量，默认为None，即对整个列表排序
    :return: 部分排序后的列表
    """
    # 如果没有指定max_number或max_number大于列表长度，则对整个列表排序
    if max_number is None or max_number >= len(lst):
        max_number = len(lst)

    # 定义比较函数
    def compare(a, b):
        if sort_key is None:
            key_a = a
            key_b = b
        else:
            key_a = sort_key(a)
            key_b = sort_key(b)
        
        if sort_order == 'asc':
            return key_a < key_b
        else:
            return key_a > key_b

    # 部分选择排序
    for i in range(max_number):
        # 找到未排序部分的最小（或最大）元素的索引
        min_or_max_index = i
        for j in range(i + 1, len(lst)):
            if compare(lst[j], lst[min_or_max_index]):
                min_or_max_index = j
        
        # 交换元素
        lst[i], lst[min_or_max_index] = lst[min_or_max_index], lst[i]

    return lst[:max_number]

def quick_sort(lst, sort_key=None, sort_order='asc'):
    """
    使用快速排序算法对列表进行排序
    使用该函数的模块: diary_service, map_service
    :param lst: 待排序的列表
    :param sort_key: 排序依据的键（函数），默认为None，即直接比较元素
    :param sort_order: 排序顺序，'asc'表示升序，'desc'表示降序，默认为'asc'
    :return: 排序后的列表
    """
    # 如果列表为空或只有一个元素，直接返回
    if len(lst) <= 1:
        return lst

    # 定义比较函数
    def compare(a, b):
        if sort_key is None:
            key_a = a
            key_b = b
        else:
            key_a = sort_key(a)
            key_b = sort_key(b)
        
        if sort_order == 'asc':
            return key_a < key_b
        else:
            return key_a > key_b

    # 选择基准元素
    pivot = lst[len(lst) // 2]

    # 根据基准元素划分列表
    left = [x for x in lst if compare(x, pivot)]
    middle = [x for x in lst if (sort_key(x) if sort_key else x) == (sort_key(pivot) if sort_key else pivot)]
    right = [x for x in lst if compare(pivot, x)]

    # 递归排序左右子列表
    return quick_sort(left, sort_key, sort_order) + middle + quick_sort(right, sort_key, sort_order)