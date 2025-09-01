class Synonyms:
    def __init__(self, l):
        """初始化同义词集合"""
        if not isinstance(l, (list, tuple, set)):
            raise TypeError(f'错误的类型:{type(l)}，请使用类型:list,tuple,set')
        l = self.check_element(l)
        self.synonyms_set = set(l)

    def check_element(self, l):
        """确保输入对象所有元素都是字符串"""
        for ele in l:
            if not isinstance(ele, str):
                raise TypeError(f'对象中有非文本内容:{ele},类型为{type(ele)}')
        return l  # 移到循环外面

    def expend_synonyms(self, l):
        """拓展同义词集合"""
        if not isinstance(l, (list, tuple, set)):
            # 修复参数引用错误
            raise TypeError(f'错误的类型:{type(l)}，请使用类型:list,tuple,set')
        l = self.check_element(l)  # 增加元素检查
        self.synonyms_set.update(set(l))  # 使用update更高效
        return self

    def __str__(self):
        return f"{';'.join(self.synonyms_set)}"

    def __repr__(self):
        return f"Synonyms:{';'.join(self.synonyms_set)}"

    def __iadd__(self, other):
        return self.expend_synonyms(other)

    def is_contains(self, s):
        if not isinstance(s, str):
            raise TypeError(f'错误的类型{type(s)},仅支持str类型')
        return s in self.synonyms_set

    def __eq__(self, other):
        """从设计上讲仅支持与字符串比较"""
        return self.is_contains(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __mul__(self, other):
        if not isinstance(other, Synonyms):
            raise TypeError(f'不支持的类型:{type(other)}')
        newset = set()
        for ele_x in self.synonyms_set:
            for ele_y in other.synonyms_set:
                newset.add(ele_x + ele_y)
        return Synonyms(newset)






if __name__ == '__main__':
    syn = Synonyms(['wwwwwwwww'])
    either = syn.expend_synonyms(['w','ww','www'])
    print(either)


