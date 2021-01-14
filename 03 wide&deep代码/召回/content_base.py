"""基于内容的推荐算法 content based filtering ，内容关联算法(Content-Based) CB"""

from recommendation.dao.memory import Memory
from recommendation.utils.tools import try_catch_with_logging


class ContentBase(object):
    def __init__(self):
        self.memory = Memory()

    @try_catch_with_logging(default_response=[])
    def fit(self, user=None, num=None):
        """
        :type user: User Object
        :type num int 返回数目
        :return:  list of ResultPoem Object
        """
        if user is None:
            return []

        return []
