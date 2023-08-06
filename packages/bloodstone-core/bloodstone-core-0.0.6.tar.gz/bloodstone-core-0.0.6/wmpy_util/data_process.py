#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-11-20 10:57
@File    : data_process.py
@Software: PyCharm
@Desc    : 数据预处理函数
"""
import pandas as pd
from collections import Counter
import random
import os
import sys
from sklearn.base import BaseEstimator, TransformerMixin
from wmpy_util import timer
from wmpy_util.json_util import *
import numpy as np
from wmpy_util.print_util import *
import math


def _observe_from_data_iter(data_iter, deepth=10, field_map=dict()):
    field_dict = dict()
    for datas in data_iter:
        columns = datas.columns
        for field in columns:
            if field == "id":
                continue
            field_dict.setdefault(field, dict())
            field_series = datas[field]
            if field in field_map:
                map_func = field_map[field]
                field_series = field_series.map(map_func)
            field_counter = Counter(field_series)
            for k, v in field_counter.items():
                field_dict[field].setdefault(k, 0)
                field_dict[field][k] += v
    # 按照字段的稀疏程度进行排序，dense feature排在前面进行显示
    field_dict_sort = sorted(field_dict.items(), key=lambda x: len(x[1]))
    for field, counter in field_dict_sort:
        print("-" * 10, "field: {}".format(field), "-" * 10)
        print("Set size = {}".format(len(counter)))
        _rank = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        print("Most frequency value")
        _num = deepth
        if len(counter) < deepth:
            _num = len(counter)
        for i in range(_num):
            print(_rank[i])
    return field_dict


def _create_data_iter_from_files(files):
    chunksize = 100000
    iter_num = 0
    for file in files:
        if not os.path.isfile(file):
            print("{} is not a file".format(file), file=sys.stderr)
            continue
        data_iter = pd.read_csv(file, chunksize=chunksize)
        try:
            while True:
                data = data_iter.__next__()
                yield data
                iter_num += 1
                if iter_num % 10 == 0:
                    print("{} data processed".format(iter_num * chunksize))
        except StopIteration as error:
            continue


def observe_data_file(data_file, deepth=10, field_map=dict()):
    """
    观察各字段的取值情况
    :param data_file:
    :param deepth: 观察每个字段频率最高的前deepth个取值
    :return:
    """
    data_iter = _create_data_iter_from_files((data_file,))
    return _observe_from_data_iter(data_iter, deepth=deepth, field_map=field_map)


def observe_data_files(data_files, deepth=10, field_map=dict()):
    """
    将多个文件联合统计
    :param data_files:
    :param deepth: 观察每个字段频率最高的前deepth个取值
    :return:
    """
    if not (isinstance(data_files, tuple) or isinstance(data_files, list)):
        raise ValueError("Data files must be a tuple")
    data_iter = _create_data_iter_from_files(data_files)
    return _observe_from_data_iter(data_iter, deepth=deepth, field_map=field_map)


def random_drop_negative(from_file, to_file, field="click", positive=1, negative=0, drop=0.5, seed=100):
    """
    用于处理正负样本不均衡的方式之一
    随机丢弃一部分负样本
    :param from_file: 源文件
    :param to_file: 写入目标文件
    :param field: 标签字段名称
    :param positive: 正样本标签值
    :param negative: 负样本标签值
    :param drop: 丢弃比例
    :param seed: 随机种子
    :return:
    """
    chunksize = 10000
    if not os.path.isfile(from_file):
        print("From_file {} is not a file".format(from_file), file=sys.stderr)
        return
    data_iter = pd.read_csv(from_file, chunksize=chunksize)
    random.seed = seed
    for index, data_frame in enumerate(data_iter):
        flag = data_frame.apply(_random_drop_negative_filter, axis=1, field=field, positive=positive, negative=negative,
                                drop=drop)
        data_frame = data_frame[flag]
        if index == 0:
            header = True
            mode = "w"
        else:
            header = False
            mode = "a"
        data_frame.to_csv(to_file, mode=mode, header=header, index=False, float_format="%.0f")
        if (index + 1) % 10 == 0:
            print("{} data processed".format((index + 1) * chunksize))


def _random_drop_negative_filter(data, *args, field='click', positive=1, negative=0, drop=0.5, **kwargs):
    value = data[field]
    if value == positive:
        # 正例全部保留
        return True
    elif value == negative:
        # 负样本抛弃drop比例的数据
        if random.random() < drop:
            return False
        else:
            return True
    else:
        # 数值在取值范围之外的直接抛弃（只处理二分类问题）
        return False


def form_endless_batch(file_path, func, batch_size=100, cache=False):
    """
    针对大数据集过大而内存有限的情况，无法将所有数据一次性读取到内存当中，所以需要进行分段读取
    该函数通过重复读取文件来产生'无穷无尽'的数据
    同时通过每次跳过随机函数来达到各个epoch之间略微的不同
    :param file_path:
    :param func:
    :param batch_size:
    :return:
    """
    cache_list = []
    # skip_rows = int(random.random() * batch_size)
    data_iter = pd.read_csv(file_path, chunksize=batch_size)
    for data in data_iter:
        gen_data = func(data)
        if cache:
            cache_list.append(gen_data)
        yield gen_data
    while True:
        if cache:
            for gen_data in cache_list:
                yield gen_data
        else:
            data_iter = pd.read_csv(file_path, chunksize=batch_size)
            for data in data_iter:
                yield func(data)


class SimpleLabelEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self._class = None
        self._val_map = None
        self._key_type = None
        # 统计编码时没有发现的字段
        self._statistic_not_found = 0

    @timer
    def fit(self, y):
        assert y is not None, "参数不能为空"
        self._class = set()
        self._val_map = dict()
        for y_index, y_val in enumerate(y):
            if self._key_type is None:
                self._key_type = type(y_val)
            else:
                y_val = self._key_type(y_val)
                if y_val not in self._class:
                    self._class.add(y_val)
                    self._val_map[y_val] = y_index
        # 未出现的值统一转换为-1
        self._val_map[None] = -1

    def transform(self, y):
        if self._key_type is None:
            self._key_type, _ = get_dict_type(self._val_map)
        if self._class is None:
            raise ValueError("Encoder not fit yet")
        ret = [self.get_value(val) for val in y]
        return ret

    def get_value(self, y):
        y = self._key_type(y)
        if y in self._val_map:
            return self._val_map[y]
        else:
            self._statistic_not_found += 1
            # 数量每增长10的倍数打印一次，也就是1，10，100次出现找不到的字段时打印，避免少量错误不打印，也避免过多打印
            if math.log(self._statistic_not_found, 10) % 1 == 0:
                print("%d 个字段没有找到编码" % self._statistic_not_found)
            return self._val_map[None]

    def is_fit(self):
        return not not self._class

    def fit_transform(self, X, y=None, **fit_params):
        if not self._class:
            self.fit(X)
        return self.transform(X)


class CommaSplitDataEncoder(SimpleLabelEncoder):
    def __init__(self, col_name="CSDE", max_length=1):
        """
        对逗号分隔字段进行编码
        特殊性在于，不是对字段直接进行编码
        而是先基于逗号将字段进行分割，然后对分割后的每一个字符进行编码

        最终编码后新的字段名将设置为：
        <col_name>_0,<col_name>_1,<col_name>_2.......<col_name>_<max_length-1>
        :param col_name: 需要编码的列标签
        :param max_length: 因为对逗号进行分割后得到的列表长度可能是任意长的，
                        这里如果超过max_length将统一到该值表示最大长度。
        """
        super().__init__()
        self.col_name = col_name
        self.max_length = max_length

    @timer(name=UseStyle("Transform", font_color=color_cyan), batch=10 * 1000)
    def transform(self, y):
        """
        CommaSplitDataEncoder.transform timeSpend 8.11 s/57.8 s on 10000/70000 iterations, average cost=0.81 ms
        # after
        Transform timeSpend 6.74 s/6.74 s on 10000/10000 iterations, average cost=0.67 ms

        :param y:
        :return:
        """
        if self._class is None:
            raise ValueError("Encoder not fit yet")
        data_list = list()
        cache = dict()
        for val in y:
            if val in cache:
                vals = cache[val]
            else:
                # 防止长度超过最大长度
                vals = val.split(",")[:self.max_length]
                vals = [self.get_value(val) for val in vals]
                vals = extend_array(vals, length=self.max_length, fill=-1)
                cache[val] = vals
            data_list.append(vals)
        data_array = np.asarray(np.asarray(data_list, dtype=float), dtype=int)
        kwarg = dict(("{:s}_{:d}".format(self.col_name, i), data_array[:, i]) for i in range(self.max_length))
        return pd.DataFrame(kwarg)


def extend_array(arr, length=8, fill=-1):
    if len(arr) >= length:
        return arr[:length]
    else:
        arr_len = len(arr)
        arr = [arr[i] if i < arr_len else fill for i in range(length)]
        return arr


def arg_sort(sort, *args, reverse=True):
    """
    根据首个参数的排序结果，对后续arg列表进行相同的顺序调整
    :param sort:
    :param args:
    :param reverse: True:sort列表从大到小，  False:sort列表从小到大
    :return:
    """
    if args is None or len(args) < 1:
        return None
    if sort is None or len(sort) < 1:
        return args
    data_len = len(sort)
    args = [np.asarray(arg) for arg in args]
    for arg in args:
        if not len(arg) == data_len:
            raise ValueError("Data length of args must match the sort data")
    sort_array = sorted(zip(sort, *args), key=lambda x: x[0], reverse=reverse)
    sort_arg = np.array(sort_array)[:, 1:]
    if len(args) == 1:
        ret = np.asarray(sort_arg[:, 0], dtype=args[0].dtype)
    else:
        ret = tuple(np.asarray(sort_arg[:, i], dtype=args[i].dtype) for i in range(len(args)))
    return ret


def trans_mean_and_var(x_array, mean=0, var=1):
    """
    将数据调整为指定的均值方差
    调整方式为
    x' = (x-u)/t
    其中
    t = sqrt(Sx / var)
    u = Ex - t * mean
    :param x_array:
    :param mean:
    :param var:
    :return:
    """
    x_array = np.asarray(x_array, dtype=float)
    _sx = np.var(x_array)
    _ex = np.mean(x_array)
    _t = np.sqrt(_sx / var)
    _u = _ex - _t * mean
    x_array = (x_array - _u) / _t
    return x_array


def get_sparsity(data):
    non_zero = 0
    if isinstance(data, dict):
        for k, items in data.items():
            non_zero += len(items)
        cell_num = len(data) * len(data)
    else:
        data = np.abs(np.array(data))
        non_zero = np.sum(data > 0)
        h, w = data.size
        cell_num = h * w
    sparsity = 1.0 * non_zero / cell_num
    print("Data sparsity {:.2f}%  {:d}/{:d}".format(sparsity * 100, non_zero, cell_num))
    return sparsity, cell_num


def float_equal(x, y):
    if x == y:
        return True
    x, y = abs(x), abs(y)
    min_xy = min(x, y)
    if min_xy == 0:
        min_xy = 1
    flag = abs(x - y) / min_xy
    return flag < 0.001


def exp_trans():
    """

    :return:
    """
    for i in range(100):
        x = np.random.random(10) * 10
        mean = random.randint(0, 10)
        var = random.randint(1, 10)
        y = trans_mean_and_var(x, mean, var)
        y_mean = np.mean(y)
        y_var = np.var(y)
        flag = float_equal(mean, y_mean)
        flag &= float_equal(var, y_var)
        assert flag


if __name__ == '__main__':
    exp_trans()
