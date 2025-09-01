from .synonyms import Synonyms
class SynonymsMatcher:

    def __init__(self):
        self.vectors = list()

    def check_rank(self, list_of_Synonyms):
        for i in len(list_of_Synonyms):
            for j in list_of_Synonyms[i].synonyms_set:
                for k in range(i+1,len(j)):
                    if list_of_Synonyms[k]==j:
                        raise ValueError('秩不为最大值')

    def get_vectors(self, list_of_Synonyms):
        if not isinstance(list_of_Synonyms, list):
            raise TypeError('list_of_Synonyms must be a list')
        for syn in list_of_Synonyms:
            if not isinstance(syn, Synonyms):
                raise TypeError(f"列表中有错误类型:{syn},类型: {type(syn)}")
        self.check_rank(list_of_Synonyms)
        self.vectors = list_of_Synonyms
        return self

    def pop_vector(self, list_of_Synonyms):
        pass




