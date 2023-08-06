#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2020-06-16 17:47
@File    : es_util.py
@Software: PyCharm
@Desc    : 包括一些ES的常用操作
"""
from elasticsearch import Elasticsearch
from elasticsearch.client.utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH, _escape
from elasticsearch.exceptions import *
import logging
import random
import re
from wmpy_util.time_util import SimpleTimer
import traceback
import json

logger = logging.getLogger()


class ESClient:
    def __init__(self, host="localhost", port="9200", index=None, headers=None):
        """
        ES连接管理对象
        :param host:域名/地址
        :param port:端口
        :param index:请求的默认index
        :param headers:请求的默认headers
        """
        self.host = host
        self.port = port
        self.es_client = Elasticsearch("http://{HOST}:{PORT}".format(**dict(
            HOST=host, PORT=port
        )))
        self.default_index = index
        self.default_headers = headers
        self.transport = self.es_client.transport

    def create_index(self, index, settings=None, mapping=None):
        """
        创建索引，mapping和setting
        :param index:
        :param settings:
        :param mapping;
        :return:
        """
        if index in SKIP_IN_PATH:
            index = self.default_index
        _body = dict()
        if settings is not None:
            if "settings" in settings.keys():
                _body["settings"] = settings["settings"]
            else:
                _body["settings"] = settings
        include_type_name = False
        if mapping is not None:
            if "mappings" in mapping:
                _body["mappings"] = mapping["mappings"]
            else:
                _body["mappings"] = mapping
            if "properties" not in _body["mappings"].keys():
                # mappings下面接doc_type然后再接properties的情况
                include_type_name = True
        ret = self.perform_request(
            "PUT", _make_path(index),
            params=dict(include_type_name=include_type_name),
            body=_body
        )
        return ret

    def create_mapping(self, index=None, mapping=None):
        """
        创建索引，mapping和setting
        :param index:
        :param mapping;
        :return:
        """
        if index in SKIP_IN_PATH:
            index = self.default_index
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")
        if mapping is SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'mappings'.")
        include_type_name = "false"
        path_list = [index, "_mapping"]
        if "properties" not in mapping.keys():
            doc_type = list(mapping.keys())[0]
            include_type_name = "true"
            path_list.append(doc_type)
        params = dict(include_type_name=include_type_name)
        return self.perform_request(
            "PUT", _make_path(*path_list), params=params, body=mapping
        )

    def get_mapping(self, index=None):
        """
        获取索引的映射
        :param index:
        :return:
        """
        if index in SKIP_IN_PATH:
            index = self.default_index

        ret = self.perform_request(
            "GET", _make_path(index, "_mapping")
        )
        if index in ret:
            return ret[index]["mappings"]
        else:
            for key, item in ret.items():
                return item["mappings"]

    def get_settings(self, index=None, name=None):
        """
        获取索引的映射
        :param index:
        :param name
        :return:
        """
        if index in SKIP_IN_PATH:
            index = self.default_index
        ret = self.perform_request(
            "GET", _make_path(index, "_settings", name)
        )
        if index in ret:
            return ret[index]["settings"]
        else:
            for key, item in ret.items():
                return item["settings"]

    def change_read_only(self, index="_all"):
        """
        修改因为磁盘空间不足导致的ES只读状态
        该方法只能暂时改变只读状态，如果磁盘使用率依然过高，一段时间后es会重新设置状态为只读。
        :param index:
        :return:
        """
        if index in SKIP_IN_PATH:
            index = self.default_index
        _body = {"index.blocks.read_only_allow_delete": "false"}
        ret = self.perform_request(
            "PUT", _make_path(index, "_settings"), params=None, body=_body
        )
        print("change_read_only", ret)
        return ret

    def delete_index(self, index):
        """
        删除index
        :param index:
        :return:
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")
        try:
            ret = self.es_client.indices.delete(index=index)
            print("delete_index", ret)
            return ret
        except Exception as error:
            logger.error(error)

    def add_similarity(self, index=None, similarity=None):
        """
        添加自定义相似度
        如果index已经存在
        需要先关闭index，才能够添加，添加完后自动开启index
        :param index:
        :param similarity:
        :return:
        """
        if index in SKIP_IN_PATH:
            index = self.default_index
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")
        if similarity is SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'similarity'.")
        exist = self.es_client.indices.exists(index)
        settings = dict()
        settings["index"] = dict(similarity=similarity)
        if exist:
            # 如果已经存在则关闭后再操作
            self._do_with_index_close(index, "PUT", _make_path(index, "_settings"), body=settings)
        else:
            # 如果不存在则创建索引
            self.create_index(index, settings=settings)

    def _do_with_index_close(self, index, method, url, headers=None, params=None, body=None):
        """
        先关闭index，然后再index关闭的情况下进行指定操作，然后重新开启index
        :param method:
        :param url:
        :param headers:
        :param params:
        :param body:
        :return:
        """
        self.close_index(index)
        try:
            self.es_client.transport.perform_request(
                method, url, headers=headers, params=params, body=body
            )
        except Exception as error:
            logger.error(error)
            if isinstance(error, TransportError):
                info = error.info
                import json
                info_str = json.dumps(info)
                logger.error(info_str)
                logger.error(info)
        finally:
            self.open_index(index)

    def reindex(self, old_index, new_index):
        if old_index in SKIP_IN_PATH:
            old_index = self.default_index
        if old_index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'old_index'.")
        if new_index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'new_index'.")
        _body = {
            "source": {
                "index": old_index
            },
            "dest": {
                "index": new_index
            }
        }
        ret = self.es_client.reindex(_body, wait_for_completion="false")
        print("reindex", ret)
        return ret

    def close_index(self, index=None):
        if index in SKIP_IN_PATH:
            index = self.default_index
        ret = self.es_client.indices.close(index)
        print("close_index", ret)

    def open_index(self, _index=None):
        if _index in SKIP_IN_PATH:
            _index = self.default_index
        ret = self.es_client.indices.open(_index)
        print("open_index", ret)

    def get_task(self, _task_id):
        params = dict(human="true",
                      detailed="true")
        params = None
        return self.es_client.tasks.get(_task_id, params=params)

    def get_task_1(self, _task_id):
        params = dict(human="true")
        _url = _make_path("_tasks", _escape(_task_id))
        print("url =", _url)
        ret = self.es_client.transport.perform_request(
            "GET", _url, params=params
        )
        return ret

    def get_scroll(self, index, body, scroll_id, size):
        """
        基于scroll接口扫描公司索引
        :param index:
        :param body:
        :param scroll_id:
        :param size:
        :return:
        """
        if scroll_id is None:
            if index in SKIP_IN_PATH:
                index = self.default_index
            if index in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument 'index'.")
            resp = self.es_client.search(
                index=index,
                body=body,
                size=size,
                scroll='1m',  # time value for search
            )
        else:
            resp = self.es_client.scroll(
                scroll_id=scroll_id,
                scroll='1m',  # time value for search
            )
        try:
            return resp["_scroll_id"], resp["hits"]["hits"]
        except Exception as error:
            return None, None

    def get_scroll_iter(self, index=None, body=None, size=200):
        """
        基于scroll搜索接口生成数据结果的迭代器
        :param index:
        :param body:
        :param size:
        :return:
        """
        scroll_total = 0
        scroll_id = None
        is_end = False
        while not is_end:
            scroll_id, data = self.get_scroll(index=index, body=body, scroll_id=scroll_id, size=size)
            if data is None:
                is_end = True
            else:
                data_len = len(data)
                scroll_total += data_len
                if data_len < 200:
                    is_end = True
            yield data
        logger.info("Total scrolled data size={:d}".format(scroll_total))

    def search(self, index=None, doc_type=None, body=None, params=None):
        index = self.check_index(index)
        if params is None:
            params = dict()
        return self.es_client.search(index=index,
                                     doc_type=doc_type,
                                     body=body,
                                     params=params)

    def check_index(self, index):
        if index in SKIP_IN_PATH:
            index = self.default_index
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")
        return index

    def perform_request(self, method, url, headers=None, params=None, body=None):
        if headers is None:
            headers = self.default_headers
        request_str = "{} {}".format(method, url)
        if body is not None:
            request_str += "\n{}".format(json.dumps(body))
        logger.debug(request_str)
        return self.transport.perform_request(
            method, url, headers=headers, params=params, body=body
        )

    def clear_cache(self, index=None, headers=None):
        index = self.check_index(index)
        ret = self.transport.perform_request(
            "POST", _make_path(index, "_cache", "clear"), params=None, headers=headers
        )
        print("Clear cache: {}".format(ret))

    def bulk(self, body, index=None, params=None):
        index = self.check_index(index)
        if params is None:
            params = {}
        ret = self.es_client.bulk(body, index=index, params=params)
        return ret


    def update_by_query(self, index, doc_type=None, body=None, params=None):
        """
        基于查询进行更新
        :param index:
        :param doc_type:
        :param body:
        :param params:
        :return:
        """
        index = self.check_index(index)
        return self.es_client.update_by_query(
            index, doc_type, body, params)


def change_similarity(mapping, similarity_dict):
    """
    修改指定字段的相似度评分规则
    :param mapping: 索引映射字典
    :param similarity_dict: 字段相似度字典 {"field_name":"BM25"}
    :return:
    """
    properties = mapping["properties"]
    for field, value in similarity_dict.items():
        if field in properties:
            properties[field]["similarity"] = value
        else:
            logger.error("Field = {} not found".format(field))
    return mapping


class EsSpeedTest:
    def __init__(self):
        """
        es查询速度测试
        目的是为了
        使用不同的查询方式和查询词进行组合进行的
        """
        self.last_multi_method_result = None

    def exp_on_multi_method(self, word_list, methods=()):
        """
        将词表随机分配给测试方法，并且按照随机顺序执行，最终统计各个方法的耗时
        主要为了避免es缓存带来的影响
        :param word_list:
        :param methods:
        :return:
        """
        # 对所有的测试方法进行包装
        methods = [method_decorator(method) for method in methods]
        # 打乱初始顺序，保证配对是随机的
        random.shuffle(word_list)
        random.shuffle(methods)
        method_len = len(methods)
        method_word_list = list()
        # 将方法和带处理数据进行配对分组
        for i, word in enumerate(word_list):
            method = methods[i % method_len]
            method_word_list.append((method, word))
        # 对执行顺序进行打乱
        random.shuffle(method_word_list)
        method_ret_dict = dict()
        for method, word in method_word_list:
            if isinstance(word, str):
                response, method_result = method(word)
            elif isinstance(word, number_classes):
                response, method_result = method(word)
            elif isinstance(word, (list, tuple)):
                response, method_result = method(*word)
            elif isinstance(word, dict):
                response, method_result = method(**word)
            else:
                logger.error("Unknown type for word={}".format(word))
                continue
            method_ret_dict[method.__name__] = method_result
        self.last_multi_method_result = method_ret_dict
        return method_ret_dict

    def analyze_result(self, result=None, detail=False):
        """
        分析制定的测试结果，或者最近一次的测试结果
        :param result:
        :param detail:
        :return:
        """
        if result is None:
            result = self.last_multi_method_result
        if result is None:
            return
        # 对键值排序，保证每次试验输出结果的顺序是一致的
        items = list(result.items())
        items = sorted(items, key=lambda x: x[0], reverse=False)
        for key, val in items:
            print("***** {} result *****".format(key))
            if detail:
                print(val.get_detail())
            else:
                print(val.get_brief())


es_speed_test = EsSpeedTest()
exp_on_multi_method = es_speed_test.exp_on_multi_method


class MethodResult:
    def __init__(self, name):
        self.name = name
        # 实际计时
        self.spend_total = 0
        # es返回的耗时
        self.took_total = 0
        # 测试详情
        self.exp_details = []

        # 实验总次数
        self.count = 0

    def add_result(self, spend, query, es_response):
        self.spend_total += spend
        took = es_response["took"]
        total_hits = es_response["hits"]["total"]["value"]
        self.took_total += took
        self.count += 1
        self.exp_details.append(dict(
            took=took,
            spend=spend,
            total=total_hits,
            query=query
        ))

    def __str__(self):
        return self.get_brief()

    def get_brief(self):
        msg = "{} exp {} times, avg took={:.2f}ms; avg spend={:.2f}ms"
        msg = msg.format(self.name, self.count, self.took_total / self.count,
                         self.spend_total / self.count)
        return msg

    def get_detail(self):
        msg = ""
        for detail in self.exp_details:
            append = "query={query}, took={took:.0f}ms, spend={spend:.0f}ms, total_hits={total}\n"
            append = append.format(**detail)
            msg += append
        msg += self.get_brief()
        return msg


class EsMethod:
    def __init__(self, name, client: ESClient, method, url, headers=None, params=None, body=None):
        self.client = client
        self.method = method
        self.url = url
        self.headers = headers
        self.params = params
        self.body = body
        self.__name__ = name
        self.__qualname__ = name

    def __call__(self, *args, **kwargs):
        # 根据传递的参数修改body
        body_build = build_body(self.body, *args, **kwargs)
        params = self.params
        if params is None:
            params = dict()
        params["timeout"] = "60s"
        ret = self.client.transport.perform_request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            params=self.params,
            body=body_build
        )
        return ret


class EsSearchMethod(EsMethod):
    def __init__(self, name, client: ESClient, index=None, headers=None, params=None, body=None):
        _method = "POST"
        _index = client.check_index(index)
        _url = _make_path(_index, "_search")
        super(EsSearchMethod, self).__init__(name=name,
                                             client=client,
                                             method=_method,
                                             url=_url,
                                             headers=headers,
                                             params=params,
                                             body=body)


def method_decorator(method):
    _name = method.__name__
    _qname = method.__qualname__
    method_result = MethodResult(_name)

    def wrapper(*args, **kwargs):
        stimer = SimpleTimer(quiet=True)
        try:
            query = ""
            if len(args) > 0:
                query += str(args)
            if len(kwargs) > 0:
                query += str(kwargs)
            ret = method(*args, **kwargs)
            spend = stimer.check()
            method_result.add_result(spend, query, ret)
            print(method_result.get_brief())
            return ret, method_result
        except Exception as error:
            print(traceback.format_exc())
            return None, method_result

    wrapper.__name__ = _name
    wrapper.__qualname__ = _qname
    return wrapper


number_classes = (int, float, bool)


def build_body(body, *args, **kwargs):
    """
    基于参数构建搜索body
    body格式需求如下
    body = {
        "query":{
            "match":{
                "{0}":"{1}"
            }
        }
    }
    构建body调用如下
    body_build = build_body(body, "job_title", "工程师")

    或者
    body格式需求如下
    body = {
        "query":{
            "match":{
                "{field}":"{query}"
            }
        }
    }
    构建body调用如下
    body_build = build_body(body, field="job_title", query="工程师")


    :param body:
    :param args:
    :param kwargs:
    :return:
    """
    if body is None:
        return body
    elif isinstance(body, dict):
        return _build_body_dict(body, *args, **kwargs)
    elif isinstance(body, list):
        return _build_body_list(body, *args, **kwargs)
    elif isinstance(body, str):
        return _build_body_str(body, *args, **kwargs)
    elif isinstance(body, number_classes):
        return body
    else:
        raise ValueError("Unknown body type={}".format(body))


def _build_body_list(body_list, *args, **kwargs):
    body_list_build = list()
    for part in body_list:
        part_build = build_body(part, *args, **kwargs)
        body_list_build.append(part_build)
    return body_list_build


def _build_body_dict(body_dict, *args, **kwargs):
    body_dict_build = dict()
    for key, val in body_dict.items():
        key_build = build_body(key, *args, **kwargs)
        val_build = build_body(val, *args, **kwargs)
        body_dict_build[key_build] = val_build
    return body_dict_build


sub_pattern = re.compile(r'\{[\w:.]+\}')


def _build_body_str(body_str, *args, **kwargs):
    match = re.search(sub_pattern, body_str)
    if match is not None:
        body_str = body_str.format(*args, **kwargs)
    return body_str


if __name__ == '__main__':
    task_id = "vwIZg_VtRge6MO7WpTR1AA:511566128"
    url = _make_path("_task", task_id)
    print(url)
