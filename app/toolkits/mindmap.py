#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================================
#
# Copyright (c) 2020 <> All Rights Reserved
#
#
# File: /c/Users/Administrator/git/fid/fid/toolkits/xmind.py
# Author: Hai Liang Wang
# Date: 2022-11-04:13:17:19
#
# ===============================================================================

"""
思维导图
"""
__copyright__ = "Copyright (c) 2020 . All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2022-11-04:13:17:19"

import os, sys

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curdir, os.pardir))

if sys.version_info[0] < 3:
    raise RuntimeError("Must be using Python 3")
else:
    unicode = str

# Get ENV
ENVIRON = os.environ.copy()

from common.logger import Logger, LN

logger = Logger(LN(__name__))

import json
from toolkits import xmind
from toolkits.xmind.core.markerref import MarkerId
from toolkits.xmind.core.topic import TopicElement
from common.utils import get_substring_as_tail


def add_priority_marker_based_on_content_length(tp, content_length):
    '''
    根据文字多少添加优先级
    '''
    if content_length and content_length > 5000:
        tp.addMarker(MarkerId.priority1)
        return
    if content_length and content_length > 4000:
        tp.addMarker(MarkerId.priority2)
        return
    if content_length and content_length > 3000:
        tp.addMarker(MarkerId.priority3)
        return
    if content_length and content_length > 2000:
        tp.addMarker(MarkerId.priority4)
        return
    if content_length and content_length > 1000:
        tp.addMarker(MarkerId.priority5)
        return
    if content_length and content_length > 500:
        tp.addMarker(MarkerId.priority6)
        return
    if content_length and content_length > 100:
        tp.addMarker(MarkerId.priority7)
        return


def add_file_toc_as_topics(root_topic: TopicElement, file_name, toc_data):
    '''
    Add topics as ToC into Root
    '''
    file_root_tp = root_topic.addSubTopic()
    file_root_title = get_substring_as_tail(file_name, 20)
    file_root_tp.setTitle(file_root_title)
    file_root_tp.setPlainNotes("Filename: %s" % file_name)
    file_root_tp.addMarker(MarkerId.starGreen)

    current_h1_tp = None
    current_h2_tp = None
    current_h3_tp = None
    current_h4_tp = None

    for heading in toc_data:
        if heading["level"] == 1:
            # 创建一级标题
            current_h1_tp = file_root_tp.addSubTopic()
            current_h1_tp.setTitle("%s %s" % (
                heading["text"], "【%s字】" % heading["sub_content_length"] if heading["sub_content_length"] > 0 else ""))
            current_h1_tp.setPlainNotes("Filename: %s" % file_name)
            add_priority_marker_based_on_content_length(current_h1_tp, heading["sub_content_length"])

        if heading["level"] == 2:
            # 创建二级标题
            if current_h1_tp is None:
                # 一级标题还不存在，创建一个默认的一级标题
                current_h1_tp = file_root_tp.addSubTopic()
                current_h1_tp.setTitle("[WARN] Not Found H1")
                current_h1_tp.setPlainNotes("Filename: %s" % file_name)

            current_h2_tp = current_h1_tp.addSubTopic()
            current_h2_tp.setTitle("%s %s" % (
                heading["text"], "【%s字】" % heading["sub_content_length"] if heading["sub_content_length"] > 0 else ""))
            current_h2_tp.setPlainNotes("Filename: %s" % file_name)
            add_priority_marker_based_on_content_length(current_h2_tp, heading["sub_content_length"])

        if heading["level"] == 3:
            # 创建三级标题
            if current_h1_tp is None:
                # 一级标题还不存在，创建一个默认的一级标题
                current_h1_tp = file_root_tp.addSubTopic()
                current_h1_tp.setTitle("[WARN] Not Found H1")
                current_h1_tp.setPlainNotes("Filename: %s" % file_name)

            if current_h2_tp is None:
                # 二级标题还不存在，创建一个默认的二级标题
                current_h2_tp = file_root_tp.addSubTopic()
                current_h2_tp.setTitle("[WARN] Not Found H2")
                current_h2_tp.setPlainNotes("Filename: %s" % file_name)

            current_h3_tp = current_h2_tp.addSubTopic()
            current_h3_tp.setTitle("%s %s" % (
                heading["text"], "【%s字】" % heading["sub_content_length"] if heading["sub_content_length"] > 0 else ""))
            current_h3_tp.setPlainNotes("Filename: %s" % file_name)
            add_priority_marker_based_on_content_length(current_h3_tp, heading["sub_content_length"])

        if heading["level"] == 4:
            # 创建四级标题
            if current_h1_tp is None:
                # 一级标题还不存在，创建一个默认的一级标题
                current_h1_tp = file_root_tp.addSubTopic()
                current_h1_tp.setTitle("[WARN] Not Found H1")
                current_h1_tp.setPlainNotes("Filename: %s" % file_name)

            if current_h2_tp is None:
                # 二级标题还不存在，创建一个默认的二级标题
                current_h2_tp = current_h1_tp.addSubTopic()
                current_h2_tp.setTitle("[WARN] Not Found H2")
                current_h2_tp.setPlainNotes("Filename: %s" % file_name)

            if current_h3_tp is None:
                # 二级标题还不存在，创建一个默认的二级标题
                current_h3_tp = current_h2_tp.addSubTopic()
                current_h3_tp.setTitle("[WARN] Not Found H3")
                current_h3_tp.setPlainNotes("Filename: %s" % file_name)

            current_h4_tp = current_h3_tp.addSubTopic()
            current_h4_tp.setTitle("%s %s" % (
                heading["text"], "【%s字】" % heading["sub_content_length"] if heading["sub_content_length"] > 0 else ""))
            current_h4_tp.setPlainNotes("Filename: %s" % file_name)
            add_priority_marker_based_on_content_length(current_h4_tp, heading["sub_content_length"])

        if heading["level"] == 5:
            # 创建四级标题
            if current_h1_tp is None:
                # 一级标题还不存在，创建一个默认的一级标题
                current_h1_tp = file_root_tp.addSubTopic()
                current_h1_tp.setTitle("[WARN] Not Found H1")
                current_h1_tp.setPlainNotes("Filename: %s" % file_name)

            if current_h2_tp is None:
                # 二级标题还不存在，创建一个默认的二级标题
                current_h2_tp = current_h1_tp.addSubTopic()
                current_h2_tp.setTitle("[WARN] Not Found H2")
                current_h2_tp.setPlainNotes("Filename: %s" % file_name)

            if current_h3_tp is None:
                # 二级标题还不存在，创建一个默认的二级标题
                current_h3_tp = current_h2_tp.addSubTopic()
                current_h3_tp.setTitle("[WARN] Not Found H3")
                current_h3_tp.setPlainNotes("Filename: %s" % file_name)

            if current_h4_tp is None:
                # 二级标题还不存在，创建一个默认的二级标题
                current_h4_tp = current_h3_tp.addSubTopic()
                current_h4_tp.setTitle("[WARN] Not Found H4")
                current_h4_tp.setPlainNotes("Filename: %s" % file_name)

            current_h5_tp = current_h4_tp.addSubTopic()
            current_h5_tp.setTitle("%s %s" % (
                heading["text"], "【%s字】" % heading["sub_content_length"] if heading["sub_content_length"] > 0 else ""))
            current_h5_tp.setPlainNotes("Filename: %s" % file_name)
            add_priority_marker_based_on_content_length(current_h5_tp, heading["sub_content_length"])


def generate_xmind_with_toc_data(toc_result_path, output_file_path, root_title=None, tpl=None):
    '''
    Generate xmind file with toc data
    '''
    logger.info("toc_result_path %s --> %s" % (toc_result_path, output_file_path))
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    # init file
    w = xmind.load(output_file_path if tpl is None else tpl)
    primary_sheet = w.getPrimarySheet()  # get the first sheet
    root = primary_sheet.getRootTopic()  # 创建根节点
    root.setTitle(get_substring_as_tail(root_title, 10) if not root_title is None else "Root")
    if not root_title is None: root.setPlainNotes(root_title)

    # some sample codes
    #   more sample code https://github.com/hailiang-wang/xmind-sdk-python3/blob/master/example.py
    # s1 = w.getPrimarySheet()  # get the first sheet
    # s1.setTitle("first sheet")  # set its title
    # r1 = s1.getRootTopic()  # 创建根节点
    # r1.setTitle("ToC111")  # 给根节点命名
    # r2 = r1.addSubTopic()  # 创建二级节点
    # r2.setTitle("枝叶")  # 命名
    # r2.setPlainNotes("fooo\nbar...")
    # r2.addMarker(MarkerId.starBlue)

    # load toc result data
    toc_result = dict()
    with open(toc_result_path, "r", encoding='utf-8') as fh:
        toc_result = json.load(fh)

    #######################################
    # 第一步，对 KEY 进行排序
    #######################################
    files = list(toc_result.keys())
    # rank with elements num, from largest to smallest
    files = sorted(files, key=lambda x: len(toc_result[x]), reverse=True)

    for file in files:
        toc_data = toc_result[file]
        add_file_toc_as_topics(root, file, toc_data)

    # stream output
    xmind.save(w, output_file_path)


##########################################################################
# Testcases
##########################################################################
import unittest


# run testcase: python /c/Users/Administrator/git/fid/fid/toolkits/xmind.py Test.testExample
class Test(unittest.TestCase):
    '''
    
    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        print("test_001")
        generate_xmind_with_toc_data("/c/Users/Administrator/git/fid/demo/.fid/toc_result.json",
                                     "/c/Users/Administrator/git/fid/demo/.fid/toc_result.xmind",
                                     "My Root",
                                     "/c/Users/Administrator/git/fid/assets/toc_result_tpl.xmind")


def test():
    suite = unittest.TestSuite()
    suite.addTest(Test("test_001"))
    runner = unittest.TextTestRunner()
    runner.run(suite)


def main():
    test()


if __name__ == '__main__':
    main()
