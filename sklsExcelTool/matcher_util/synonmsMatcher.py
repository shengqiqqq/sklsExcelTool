

from .synonyms import Synonyms
class SynonymsMatcher:

    def __init__(self):
        self.vectors = list()

    def check_rank(self, list_of_Synonyms):
        '''确保每个向量指向语义不同，也许可以改成合并'''
        for i in range(len(list_of_Synonyms)):
            '''list_of_Synonyms应该传入只包含Synonyms对象'''
            for j in list_of_Synonyms[i].synonyms_set:
                for k in range(i+1,len(list_of_Synonyms)):
                    if list_of_Synonyms[k]==j:
                        raise ValueError('秩不为最大值')

    def get_vectors(self, list_of_Synonyms):
        '''将每个Synonyms作为一个向量，应只想同一个语义'''
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

    def expand_query(self, query_l):
        '''扩展所有可能短语，以来Synonyms乘法'''
        if not isinstance(query_l, (list, tuple,set)):
            raise TypeError(f'错误的类型:{type(query_l)}')
        list_to_multiply = list()
        for element in query_l:
            for vector in self.vectors:
                if vector == element:
                    list_to_multiply.append(vector)
        list_to_output = list_to_multiply[0]
        for i in range (1,len(list_to_multiply)):
            list_to_output = list_to_multiply[i]*list_to_output
        return list_to_output







