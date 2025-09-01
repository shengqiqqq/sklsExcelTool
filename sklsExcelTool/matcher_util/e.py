from fuzzywuzzy import fuzz, process
import jieba
from collections import defaultdict


class ChineseSynonymMatcher:

    def __init__(self):
        self.synonym_dict = defaultdict(set)
        # 初始化jieba分词
        jieba.initialize()

    def add_synonyms(self, words):
        """添加一组中文同义词"""
        if not words:
            return

        # 对每个词进行分词，确保同义词组的分词结果一致
        word_tokens = {word: ' '.join(jieba.cut(word)) for word in words}

        # 创建同义词组
        synonym_set = set(words)
        for word in words:
            self.synonym_dict[word] = synonym_set
            # 同时存储分词结果
            self.synonym_dict[word + "_tokens"] = word_tokens[word]

    def get_synonyms(self, word):
        """获取一个词的所有同义词(包括自己)"""
        return self.synonym_dict.get(word, {word})

    def expand_query_with_synonyms(self, query):
        """将中文查询字符串分词后扩展为同义词组合"""
        # 先对查询进行分词
        query_tokens = list(jieba.cut(query))

        # 初始化扩展查询列表
        expanded_queries = [""]

        for token in query_tokens:
            synonyms = self.get_synonyms(token)
            new_expanded = []
            for synonym in synonyms:
                for existing in expanded_queries:
                    new_query = f"{existing} {synonym}".strip()
                    new_expanded.append(new_query)
            expanded_queries = new_expanded

        return expanded_queries


def chinese_best_match(query, choices, synonym_matcher=None, scorer=fuzz.WRatio, cutoff=70, return_score=False):
    """
    中文最佳匹配函数，支持分词和同义词扩展

    参数:
        query (str): 要匹配的中文查询字符串
        choices (list): 候选字符串列表(全集)
        synonym_matcher (ChineseSynonymMatcher, 可选): 中文同义词处理器
        scorer (function, 可选): 使用的模糊匹配算法
        cutoff (int, 可选): 匹配分数阈值
        return_score (bool, 可选): 是否返回匹配分数

    返回:
        匹配结果，格式取决于return_score参数
    """
    # 处理同义词扩展
    queries_to_try = [query]
    if synonym_matcher:
        queries_to_try.extend(synonym_matcher.expand_query_with_synonyms(query))

    best_score = 0
    best_choice = None

    # 尝试所有可能的查询变体(原始查询+同义词扩展)
    for q in queries_to_try:
        result = process.extractOne(q, choices, scorer=scorer)
        if result:
            choice, score = result
            if score > best_score:
                best_score = score
                best_choice = choice

    if best_score < cutoff:
        return (None, 0) if return_score else None

    return (best_choice, best_score) if return_score else best_choice


# 示例用法
if __name__ == "__main__":
    # 创建中文同义词匹配器
    synonym_matcher = ChineseSynonymMatcher()
    synonym_matcher.add_synonyms(["苹果", "红富士", "Apple"])
    synonym_matcher.add_synonyms(["香蕉", "芭蕉"])
    synonym_matcher.add_synonyms(["汽车", "轿车", "小汽车"])

    candidates = ["苹果", "香蕉", "橙子", "葡萄", "菠萝", "汽车销售"]

    # 基本用法(无同义词)
    print(chinese_best_match("苹", candidates))  # 输出: 苹果

    # 使用同义词匹配
    print(chinese_best_match("红富士", candidates, synonym_matcher=synonym_matcher))  # 输出: 苹果
    print(chinese_best_match("轿车销售", candidates, synonym_matcher=synonym_matcher))  # 输出: 汽车销售

    # 返回分数
    result = chinese_best_match("小汽车销售", candidates,
                                synonym_matcher=synonym_matcher,
                                return_score=True)
    print(result)  # 输出: ('汽车销售', 90)
