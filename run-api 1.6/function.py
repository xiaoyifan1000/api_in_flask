#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as Et
import re
import os


def replace_all_blank(value):
    """
    去除value中的所有非字母内容，包括标点符号、空格、换行、下划线等
    :param value: 需要处理的内容
    :return: 返回处理后的内容
    """
    # \W 表示匹配非数字字母下划线
    result = re.sub(r'\W+', '', value).replace("_", '')
    return result


def dict_to_xml(tag: str, d):  # 字典转Element
    if not tag:
        tag = 'home'
    tag = replace_all_blank(tag)
    tag = tag.replace(' ', '_')
    elem = Element('当前搜索'+tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem


def write_xml(obj, file_name: str):  # 写入

    if not os.path.exists(file_name):
        tree_w = Et.Element('nyaa')
        tree_ = Et.ElementTree(tree_w)
        tree_.write(file_name, 'utf-8')

    tree = Et.parse(file_name)
    root = tree.getroot()

    root.append(obj)
    tree__ = Et.ElementTree(root)
    tree__.write(file_name, 'utf-8')


def categories(criteria: str, category: str, content: str, page: str):
    return f"/?f={criteria}&c={category}&q={content}&p={page}"


def filter_name(return_):
    if 'comment' not in return_:
        return True

