"""基于规则的推荐"""
from flask import g  # 引入g对象

from recommendation.algorithms.common.constants import MatchAlgorithmEnum
from recommendation.dao.memory import Memory
from recommendation.dao.mysql_utils import MysqlDB
from recommendation.objects import ResultPoem
from recommendation.utils.tools import try_catch_with_logging


class RuleBase(object):
    def __init__(self):
        self.memory = Memory()
        self.mysql_db = MysqlDB()

    @try_catch_with_logging(default_response=[])
    def get_popular_poems(self, user=None, num=None):
        """
        :type user: User Object
        :type num int 返回数目
        :return:  list of ResultFeed Object
        """
        result_poems = [ResultPoem(poem_id, MatchAlgorithmEnum.rule_base, MatchAlgorithmEnum.rule_base, 0)
                        for poem_id in self.memory.popular_poem_ids[:num]]
        return result_poems

    @try_catch_with_logging(default_response=[])
    def get_match_tag_poems(self, user=None, num=None):
        """标签召回"""
        tags = set(g.tags)
        result_poems = []
        for poem_id, poem in self.memory.all_poems_dict.items():
            match_tags = poem.tags & tags  # 交集
            # print("match_tags:{},\n poem.tags:{}\n, tags : {}\n".format(match_tags, poem.tags, tags))
            if match_tags and len(result_poems) < num:
                result_poem = ResultPoem(poem_id, MatchAlgorithmEnum.tag_base, MatchAlgorithmEnum.tag_base, 0,
                                         reasons={"match_tags": list(match_tags)})
                result_poems.append(result_poem)
        result_poems = sorted(result_poems, key=lambda result_poem: len(result_poem.reasons["match_tags"]),
                              reverse=True)
        return result_poems
