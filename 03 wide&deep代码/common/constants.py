from recommendation.utils.enum import Enum


class MatchAlgorithmEnum(Enum):
    """ name key proportion
    顺序即是优先级，若某一算法视频缺失，使用高优先级算法填补
    """
    tag_base = ("TG", 0.5)  # 标签
    rule_base = ("HT", 0.5)  # 热度


class RankAlgorithmEnum(Enum):
    """ name key proportion
    顺序即是优先级，若某一算法视频缺失，使用高优先级算法填补
    """
    tag_base = ("TG", 0.5)  # 标签
    rule_base = ("HT", 0.5)  # 热度
