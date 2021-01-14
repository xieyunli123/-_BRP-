"""
Ranking阶段对Matching后的视频采用更精细的特征计算user-item之间的排序分，作为最终输出推荐结果的依据。
"""
from collections import defaultdict, deque

import numpy as np

from recommendation.algorithms.common.constants import RankAlgorithmEnum
from recommendation.dao.memory import Memory


class Ranking(object):
    def __init__(self):
        self.group_size = 5
        self.memory = Memory()

    def rank(self, user, num, matched_poems):
        """
        :param user: User Object
        :param matched_poems: list of ResultPoem
        :return: list of ResultPoem Object
        """
        if user is None:
            return matched_poems
        ranked_poems = self.rank_score(user=user, matched_poems=matched_poems)  # rank策略暂时不用
        result_poems = self.merge(user, num, ranked_poems)
        return result_poems

    def rank_score(self, user, matched_poems):
        """
        :param user: User Object
        :param matched_poems: list of ResultPoem
        :return: list of ResultPoem
        """
        # for result_poem in matched_poems:
        #     pass
        return matched_poems

    def merge(self, user, num, ranked_poems):
        """
        来自各个推荐算法的结果按规则组合排序;
            视频按算法比例设置分配到每一组
            5首诗词为一组，每组：
                (1)、同一作者只能出现1首诗词；
        :param user: User Object
        :param ranked_poems:  list of ResultPoem
        :return: list of ResultPoem
        """
        result_poems = []
        result_poems_queue = defaultdict(deque)  # {"RB": [ResultPoem,ResultPoem], "UC": [ResultPoem，ResultPoem]}
        for _video in ranked_poems:  # 比列表解析更快
            result_poems_queue[_video.rank_algorithm].append(_video)
        queue_empty_count = 0
        illegal_result_videos = defaultdict(list)
        while len(result_poems) < num and queue_empty_count < len(result_poems_queue):
            # 先处理上一组被过滤下来的视频; 重新加到队列末尾; append进去，反转后添加回原队列，高分在末尾，保持顺序
            for _rank_algorithm, _result_videos in illegal_result_videos.items():
                result_poems_queue[_rank_algorithm].extendleft(reversed(_result_videos))
                # _result_videos 从高到低 ，extendleft 会反转_result_videos添加到队列头
            # 每一组各个算法按比例分配，一组一组往外取视频,每次循环取出一组; 顺序即是优先级，若某一算法视频缺失，使用高优先级算法填补
            this_group_count = defaultdict(int)
            illegal_result_videos = defaultdict(list)  # 这一组的，非法视频队列，置空
            while sum(this_group_count.values()) < self.group_size and queue_empty_count < len(result_poems_queue):
                queue_empty_count = 0
                for _algorithm, _proportion in RankAlgorithmEnum:  # 按照算法和比例遍历4个队列
                    if not _proportion:
                        continue
                    count = np.ceil(self.group_size * _proportion).astype("int32")  # 当前算法按比例应该取出多少视频
                    while count and sum(this_group_count.values()) < self.group_size:
                        if len(result_poems_queue[_algorithm]) == 0:  # 此队列已空
                            # print("** _algorithm :{} 队列已空".format(_algorithm))
                            queue_empty_count += 1
                            break
                        result_poem = result_poems_queue[_algorithm].popleft()  # 队头，score最高
                        # if poem_id not in result_poem_ids 必然不在，March 步已经去重了
                        poem = self.memory.all_poems_dict[result_poem.poem_id]
                        is_legal = False  # 视频是否满足要求
                        if this_group_count[poem.poet_id] < 1:  # 1、同一诗人作品只能出现1个视频
                            is_legal = True
                            this_group_count[poem.poet_id] += 1
                        if is_legal:  # 视频满足要求
                            result_poems.append(result_poem)
                            count -= 1
                        else:  # 不满足要求，user_id多 或者 is_feature多
                            illegal_result_videos[result_poem.rank_algorithm].append(result_poem)  # 被过滤的视频
        return result_poems
