import math

import numpy as np


def gaussian(x=0, sigma=1, mean=0):
    """
    :param x: 变量；偏离均值越大，值越小
    :param mean: 即均值，决定了图像位置，关于μ对称，并在μ处取最大值
    :param sigma: 方差; 越大越平滑，衰减越慢，1为标准正态分布
    :return:  e^( -(x-mean)^2 / (2*sigma^2) ) # standard normal distribution sigma=1 and mean=0
    """
    return math.exp(- (x - mean) ** 2 / (2 * sigma ** 2))


def largest_indices(ary, k):
    """
    :param ary: flatten numpy ndarray
    :param k:  top k largest
    :return: the ordered k largest indices from a numpy array. O(n + k*log k)
    """
    indices = np.argpartition(ary, -k)[-k:]
    indices = indices[np.argsort(-ary[indices])]
    return indices
