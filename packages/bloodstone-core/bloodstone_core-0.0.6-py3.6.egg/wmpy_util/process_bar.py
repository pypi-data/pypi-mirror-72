#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2020-06-18 12:07
@File    : process_bar.py
@Software: PyCharm
@Desc    : 实现一个方便的进度条方案
"""
import time
import sys


def method1():
    for i in range(1, 101):
        print('\rhello', end=' ')
        print("\r下载进度：%.2f%%" % (float(i / 100 * 100)), end=' ')
        time.sleep(0.01)


class ShowProcess():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    i = 0  # 当前的处理进度
    max_steps = 0  # 总共需要处理的次数
    max_arrow = 50  # 进度条的长度
    infoDone = 'done'

    # 初始化函数，需要知道总共的处理次数
    def __init__(self, max_steps, infoDone='Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone

    # 显示函数，根据当前的处理进度i显示进度
    # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps)  # 计算显示多少个'>'
        num_line = self.max_arrow - num_arrow  # 计算显示多少个'-'
        percent = self.i * 100.0 / self.max_steps  # 计算完成进度，格式为xx.xx%
        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']' \
                      + '%.2f' % percent + '%'   # 带输出的字符串，'\r'表示不换行回到最左边
        print(process_bar, end="\r")  # 这两句打印字符到终端
        sys.stdout.flush()
        if self.i >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0


if __name__ == '__main__':
    max_steps = 100
    process_bar = ShowProcess(max_steps, 'OK')
    print("start")
    for i in range(max_steps):
        process_bar.show_process(i)
        time.sleep(0.1)
