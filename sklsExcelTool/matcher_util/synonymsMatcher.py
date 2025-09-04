

from .synonyms import Synonyms
class SynonymsMatcher:

    def __init__(self):
        self.vectors = list()

    def check_rank(self, list_of_Synonyms: list['Synonyms']):  # 添加类型提示
        """
        确保列表中每个Synonyms对象所包含的同义词集合是互不重叠的。
        如果发现任何同义词在多个Synonyms对象中出现，则抛出ValueError。
        """
        seen_synonyms = set()
        for i, syn_obj in enumerate(list_of_Synonyms):
            # 确保传入的确实是Synonyms对象，虽然get_vectors已经检查过，但这里再加一层防御性检查也无妨
            if not isinstance(syn_obj, Synonyms):
                raise TypeError(f"列表中有错误类型:{syn_obj},类型: {type(syn_obj)}")

            for synonym in syn_obj.synonyms_set:
                if synonym in seen_synonyms:
                    raise ValueError(f"秩不为最大值：同义词 '{synonym}' 在多个Synonyms对象中重复。")
                seen_synonyms.add(synonym)

    def get_vectors(self, list_of_Synonyms: list['Synonyms']) -> 'SynonymsMatcher':
        """
        设置SynonymsMatcher的向量列表。每个Synonyms对象被视为一个向量，
        代表一个语义单元。在设置前会进行秩检查以确保语义独立性。

        Args:
            list_of_Synonyms: 包含Synonyms对象的列表。

        Returns:
            SynonymsMatcher实例本身，支持链式调用。

        Raises:
            TypeError: 如果输入不是列表，或列表中包含非Synonyms对象。
            ValueError: 如果Synonyms对象之间存在同义词重叠（秩不为最大值）。
        """
        if not isinstance(list_of_Synonyms, list):
            raise TypeError('list_of_Synonyms must be a list')
        for syn in list_of_Synonyms:
            if not isinstance(syn, Synonyms):
                raise TypeError(f"列表中有错误类型:{syn},类型: {type(syn)}")
        self.check_rank(list_of_Synonyms)
        self.vectors = list_of_Synonyms
        return self

    def find_vector(self, string):
        '''寻找向量，依赖Synonyms等于计算'''
        if not isinstance(string, str):
            raise TypeError(f'错误的类型:{type(string)}')
        for vector in self.vectors:
            if vector == string:
                return vector

    def expand_query(self, query_l: list[str] | tuple[str, ...] | set[str]) -> Synonyms | None:  # 添加类型提示
        """
        根据查询列表扩展所有可能的短语组合。
        它会查找查询列表中每个元素对应的Synonyms向量，然后将这些向量进行“乘法”操作（字符串拼接的笛卡尔积）。

        Args:
            query_l: 包含字符串的列表、元组或集合，表示查询的各个部分。

        Returns:
            一个包含所有扩展短语的Synonyms对象。
            如果查询列表为空或没有找到任何匹配的向量，则返回一个空的Synonyms对象。

        Raises:
            TypeError: 如果输入不是列表、元组或集合。
        """
        if not isinstance(query_l, (list, tuple, set)):
            raise TypeError(f'错误的类型:{type(query_l)}')

        list_to_multiply = []
        for element in query_l:
            # 使用find_vector来查找匹配的Synonyms对象
            vector = self.find_vector(element)  # 假设find_vector已优化或明确返回None
            if vector:  # 只有找到匹配的向量才添加到列表中
                list_to_multiply.append(vector)

        if not list_to_multiply:
            # 如果没有找到任何匹配的向量，返回一个空的Synonyms对象
            # 或者根据需求返回 None
            return Synonyms(set())  # 返回一个空的Synonyms对象

        # 确认乘法顺序：S0 * S1 * ... * Sn
        list_to_output = list_to_multiply[0]
        for i in range(1, len(list_to_multiply)):
            list_to_output = list_to_output * list_to_multiply[i]  # 修正为 S0 * S1 * S2... 的顺序

        return list_to_output







