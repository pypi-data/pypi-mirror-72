#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : schedule_util.py
@Desc    : 定时任务
"""
import schedule
import logging
import threading
import time
from datetime import datetime
from functools import wraps
import calendar
import re

logger = logging.getLogger(__name__)
"""
cron expression说明 （年 月 日 时 分 秒）

年 最小值：1970，最大值：9999 可用符号：*,-/
月 最小值：1，最大值：12 可用符号：*,-/
日 最小值：1，最大值：31（基于不同的年份和月份有所改变，如闰年2月最大天数为29） 可用符号：*,-/
时 最小值：0，最大值：23 可用符号：*,-/
分 最小值：0，最大值：59 可用符号：*,-/
秒 最小值：0，最大值：59 可用符号：*,-/
/ 表示从某个时刻开始，每增加一次的数值，如2018/3 表示从2018年开始每隔3年
* 表示任意时刻开始，如果后续有/递增符号，表示每增加一次的数值，没有则默认为1，如* * * * * */5，表示每5秒
, 表示分隔多个值，如2018，2021，2022，表示2018年，2021年，2022年
- 表示多个值的范围，如2018-2022，表示2018年至2022年，即2018，2019，2020，2021，2022

举例说明
* * * * * */5 每隔5秒
* * * * 15-40 5/10 每小时的15分钟至40分钟内从第5秒开始，每隔10秒增加一次

scheduler task说明，在需要启动定时任务的方法上增加方法注解 @scheduler(cron, retry_times, retry_interval)

参数cron即cron expression
retry_times 如果执行过程产生异常，重试的次数
retry_interval 如果执行过程产生异常，重试执行时间的时间间隔，单位为秒
"""


class ScheduleManger:
    def __init__(self, interval=1):
        self._quaz_flag = True
        self._interval = interval
        self._thread = None

    def __do_work(self):
        while self._quaz_flag:
            time.sleep(self._interval)
            schedule.run_pending()

    def start_time(self):
        if self._thread is None:
            self._thread = threading.Thread(target=self.__do_work)
            self._thread.daemon = True
        if not self._thread.is_alive():
            self._thread.start()

    def stop_timer(self):
        self._quaz_flag = False

    def add_schedule(self, every, job, args=(), kwargs={}):
        """
        增加定时任务
        :param every: 时间间隔：秒
        :param job:
        :param args:
        :param kwargs:
        :return:
        """
        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = dict()
        if not isinstance(args, list) and not isinstance(args, tuple):
            args = (args,)
        schedule.every(every).seconds.do(job, *args, **kwargs)

    def add_schedule_at_time(self, time_str, job, args=(), kwargs={}):
        schedule.every().days.at(time_str).do(job, *args, **kwargs)


schedule_manager = ScheduleManger()

month_mappings = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10,
                  "NOW": 11, "DEC": 12}

re_year = "(?P<years>(19[789]\d{1}|[2-9]\d{3}|\*)(/[1-9]\d*)?|(19[789]\d{1}|[2-9]\d{3})-(19[789]\d{1}|[2-9]\d{3})|(19[789]\d{1}|[2-9]\d{3})(-(19[789]\d{1}|[2-9]\d{3}))?(,(19[789]\d{1}|[2-9]\d{3})(-(19[789]\d{1}|[2-9]\d{3}))?)+)"
re_month = "(?P<months>((0?[1-9]|1[012])|\*)(/[1-9]\d*)?|(0?[1-9]|1[012])-(0?[1-9]|1[012])|(0?[1-9]|1[012])(-(0?[1-9]|1[012]))?(,(0?[1-9]|1[012])(-(0?[1-9]|1[012]))?)+|(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC)|(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC)-(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC)|(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC)(-(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC))?(,(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC)(-(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC))?)+)"
re_day = "(?P<days>((0?[1-9]|[12]\d|3[01])|\*)(/[1-9]\d*)?|(0?[1-9]|[12]\d|3[01])-(0?[1-9]|[12]\d|3[01])|(0?[1-9]|[12]\d|3[01])(-(0?[1-9]|[12]\d|3[01]))?(,(0?[1-9]|[12]\d|3[01])(-(0?[1-9]|[12]\d|3[01]))?)+)"
re_hour = "(?P<hours>(([01]?\d|2[0123])|\*)(/[1-9]\d*)?|([01]?\d|2[0123])-([01]?\d|2[0123])|([01]?\d|2[0123])(-([01]?\d|2[0123]))?(,([01]?\d|2[0123])(-([01]?\d|2[0123]))?)+)"
re_minute = "(?P<minutes>([0-5]?\d|\*)(/[1-9]\d*)?|[0-5]?\d-[0-5]?\d|[0-5]?\d(-[0-5]?\d)?(,[0-5]?\d(-[0-5]?\d)?)+)"
re_second = "(?P<seconds>([0-5]?\d|\*)(/[1-9]\d*)?|[0-5]?\d-[0-5]?\d|[0-5]?\d(-[0-5]?\d)?(,[0-5]?\d(-[0-5]?\d)?)+)"

cron_expression = "^%s\s+%s\s+%s\s+%s\s+%s\s+%s$" % (re_year, re_month, re_day, re_hour, re_minute, re_second)

re_range = ".*[-,].*"
re_star = "\*"
re_forward_flash = "/"

min_year, min_month, min_day, min_hour, min_minute, min_second = 1970, 1, 1, 0, 0, 0
max_year, max_month, max_day, max_hour, max_minute, max_second = 10000, 13, 32, 24, 60, 60


class CronError(Exception):

    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return repr(self.error_msg)


class Cron:

    def __init__(self, cron, init_datetime=datetime.now()):
        self.__init_year = init_datetime.year
        self.__init_month = init_datetime.month
        self.__init_day = init_datetime.day
        self.__init_hour = init_datetime.hour
        self.__init_minute = init_datetime.minute
        self.__init_second = init_datetime.second

        match = re.match(cron_expression, cron)
        if match is not None:
            years = match.group("years")
            self.__years = self.__resolve(years, min_year, max_year)

            months = match.group("months")
            for key, value in month_mappings.items():
                months = months.replace(key, str(value))
            self.__months = self.__resolve(months, min_month, max_month)

            days = match.group("days")
            self.__days = self.__resolve(days, min_day, max_day)

            hours = match.group("hours")
            self.__hours = self.__resolve(hours, min_hour, max_hour)

            minutes = match.group("minutes")
            self.__minutes = self.__resolve(minutes, min_minute, max_minute)

            seconds = match.group("seconds")
            self.__seconds = self.__resolve(seconds, min_second, max_second)
        else:
            raise CronError('Cron Expression Format Error')

    def __resolve(self, field_value, min_value, max_value):
        if re.match(re_range, field_value):
            points = self.__flatten(field_value)
        else:
            values = re.split(re_forward_flash, field_value)
            if re.match(re_star, field_value):
                period = 1 if len(values) == 1 else int(values[1])
                points = [i for i in range(min_value, max_value, period)]
            else:
                period = None if len(values) == 1 else int(values[1])
                if period is None:
                    points = [int(values[0])]
                else:
                    points = [i for i in range(int(values[0]), max_value, period)]
        return points

    def __flatten(self, ranges=""):
        values = []
        for r in [re.split("-", i) for i in re.split(",", ranges)]:
            if len(r) == 2:
                values += [i for i in range(int(r[0]), int(r[1]) + 1)]
            elif len(r) == 1:
                values.append(int(r[0]))
        return sorted(set(values))

    def next_execute_time(self):
        for year in self.__years:
            if year < self.__init_year:
                continue
            for month in self.__months:
                if year <= self.__init_year and month < self.__init_month:
                    continue
                current_max_day = calendar.monthrange(year, month)[1] + 1
                days = [i for i in filter(lambda x: x < current_max_day, self.__days)]
                for day in days:
                    if year <= self.__init_year and month <= self.__init_month and day < self.__init_day:
                        continue
                    for hour in self.__hours:
                        if year <= self.__init_year and month <= self.__init_month and day <= self.__init_day and hour < self.__init_hour:
                            continue
                        for minute in self.__minutes:
                            if year <= self.__init_year and month <= self.__init_month and day <= self.__init_day and hour <= self.__init_hour and minute < self.__init_minute:
                                continue
                            for second in self.__seconds:
                                if year <= self.__init_year and month <= self.__init_month and day <= self.__init_day and hour <= self.__init_hour and minute <= self.__init_minute and second < self.__init_second:
                                    continue
                                yield datetime(year, month, day, hour, minute, second)


def scheduler(cron, retry_times=3, retry_interval=5, excludes=(), includes=()):
    """
    调用样例
    @scheduler("* * * * 0/5 0")
    def func():
        ...
    每隔5分钟调用一次指定函数

    :param cron:
    :param retry_times:
    :param retry_interval:
    :param excludes:
    :param includes:
    :return:
    """
    scheduler_cron = Cron(cron)
    execute_datetime = scheduler_cron.next_execute_time()

    def decorator(func):

        @wraps(func)
        def wrapper():
            try:
                next_interval = (next(execute_datetime) - datetime.now()).total_seconds()
                threading.Timer(interval=next_interval, function=wrapper).start()
            except StopIteration:
                logger.warning("there is no next-execution-datetime found")

            executed_times = 0
            while executed_times <= retry_times:
                try:
                    logger.debug("start to execute the task %s", func.__name__)
                    func()
                    logger.debug("finish to execute the task %s", func.__name__)
                except Exception as e:
                    logger.error("it is failure to execute the task %s, the error is %s", func.__name__, str(e))

                    is_exclude = False
                    for exclude in excludes:
                        if isinstance(e, exclude):
                            is_exclude = True
                    if is_exclude:
                        raise e

                    is_include = False
                    for include in includes:
                        if isinstance(e, include):
                            is_include = True

                    if is_include or len(includes) == 0:
                        if executed_times < retry_times:
                            time.sleep(retry_interval)
                        executed_times += 1
                    else:
                        raise e

                    if executed_times > retry_times:
                        raise e
                else:
                    break

        try:
            next_execution_datetime = next(execute_datetime)
            while not (next_execution_datetime - datetime.now()).total_seconds() > 0:
                next_execution_datetime = next(execute_datetime)
            interval = (next_execution_datetime - datetime.now()).total_seconds()
            threading.Timer(interval=interval, function=wrapper).start()
            return wrapper
        except StopIteration:
            logger.warning("there is no next-execution-datetime found")

    return decorator


def add_scheduler_task(func, cron, retry_times=3, retry_interval=5, excludes=(), includes=()):
    scheduler(cron, retry_times, retry_interval, excludes, includes)(func)


if __name__ == '__main__':
    def my_job(name, *args, **kwargs):
        print(args, kwargs)
        print("my name is %s, at %.2f" % (name, time.time()))


    s = ScheduleManger()
    s.add_schedule(6, my_job, ("zww", "haha", 123), dict(a=1, b=2))
    s.add_schedule(3, my_job, ("ly", "lala", "456"), dict(jaja=1))
    time.sleep(10)
    s.add_schedule(1, my_job, ("yx", "jiji", 222), dict(bibi=2))
    a = input()
    s.stop_timer()
    time.sleep(100)
