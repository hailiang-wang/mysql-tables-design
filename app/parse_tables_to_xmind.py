#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================================
#
# Copyright (c) 2020 <> All Rights Reserved
#
#
# File: /c/Users/Administrator/git/mysql_tables_xmind/app/parse_tables_to_xmind.py
# Author: Hai Liang Wang
# Date: 2022-12-29:12:56:12
#
# ===============================================================================

"""
   
"""
__copyright__ = "Copyright (c) 2020 . All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2022-12-29:12:56:12"

import os, sys

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    raise RuntimeError("Must be using Python 3")
else:
    unicode = str

# Get ENV
ENVIRON = os.environ.copy()

MYSQL_USERNAME = ENVIRON['MYSQL_USERNAME']
MYSQL_PASSWORD = ENVIRON['MYSQL_PASSWORD']
MYSQL_DATABASE = ENVIRON['MYSQL_DATABASE']
MYSQL_HOST = ENVIRON['MYSQL_HOST']
MYSQL_PORT = ENVIRON['MYSQL_PORT']
OUTPUT_FILENAME_XMIND = ENVIRON['OUTPUT_FILENAME_XMIND']

import json
import mysql.connector
from toolkits import xmind
from toolkits.xmind.core.markerref import MarkerId
from toolkits.xmind.core.topic import TopicElement

MYSQL_UNIQUE_INDEX = '''
select stat.table_name,
       stat.index_name,
       group_concat(stat.column_name
            order by stat.seq_in_index separator ', ') as columns,
       tco.constraint_type
from information_schema.statistics stat
join information_schema.table_constraints tco
     on stat.table_schema = tco.table_schema
     and stat.table_name = tco.table_name
     and stat.index_name = tco.constraint_name
where stat.non_unique = 0
      and stat.table_schema = '%s'
			and tco.constraint_type = 'UNIQUE'
group by stat.table_schema,
         stat.table_name,
         stat.index_name,
         tco.constraint_type
order by stat.table_schema,
         stat.table_name;
'''

MYSQL_FOREIGN_KEYS = '''
select fks.table_name as foreign_table,
       '->' as rel,
       fks.referenced_table_name as primary_table,
       fks.constraint_name,
       group_concat(kcu.column_name
            order by position_in_unique_constraint separator ', ') 
             as fk_columns
from information_schema.referential_constraints fks
join information_schema.key_column_usage kcu
     on fks.constraint_schema = kcu.table_schema
     and fks.table_name = kcu.table_name
     and fks.constraint_name = kcu.constraint_name
where fks.constraint_schema = '%s'
group by fks.constraint_schema,
         fks.table_name,
         fks.unique_constraint_schema,
         fks.referenced_table_name,
         fks.constraint_name
order by fks.constraint_schema,
         fks.table_name;
'''


def get_unique_index_def(record):
    '''
    Unique Index Def
    '''
    lis = list(record)
    return dict({
        "table": lis[0],
        "index_name": lis[1],
        "columns": lis[2],
    })


def get_foreign_key_def(record):
    '''
    Get foreign key info
    '''
    lis = list(record)
    return dict({
        "foreign_table": lis[0],
        "primary_table": lis[2],
        "constraint_name": lis[3],
        "fk_columns": lis[4],
        "pr_columns": "id"  # fixed value for primary table
    })


def get_table_column(record):
    '''
    Get table column
    '''
    lis = list(record)
    return dict({
        "name": lis[3],
        "pos": lis[4],
        "default": lis[5],
        "is_nullable": lis[6],
        "data_type": lis[7],
        "varchar_max": lis[8],
        "charset": lis[13],
        "collation_name": lis[14],
        "column_type": lis[15]
    })


def get_table_info(record):
    '''
    Get table description
    '''
    lis = list(record)
    return dict({
        "name": lis[2],
        "comment": lis[20],
        "charset": lis[17],
        "createddate": lis[14].strftime('%Y-%m-%d %H:%M:%S')
    })


def generate_output_file(tables, table_info, table_columns, table_foreign_keys, table_unique_indexes):
    '''
    Generate XMIND File
    '''
    w = xmind.load(OUTPUT_FILENAME_XMIND)
    primary_sheet = w.getPrimarySheet()  # get the first sheet
    root = primary_sheet.getRootTopic()  # 创建根节点
    root.setTitle(MYSQL_DATABASE)

    # create tables
    level1 = dict()
    for table in tables:
        node = root.addSubTopic()
        node.setTitle(table)
        node.setPlainNotes(json.dumps(table_info[table], indent=2))
        level1[table] = node

    # create fields
    level2 = dict()
    for table in tables:
        columns = table_columns[table]
        parent = level1[table]
        for column in columns:
            node = parent.addSubTopic()
            node.setTitle(column["name"])
            if column["name"] == "id":
                node.addMarker(MarkerId.starGreen)
            node.setPlainNotes(json.dumps(column, indent=2))
            level2["%s:%s" % (table, column["name"])] = node

    # create rel
    for foreign_key in table_foreign_keys:
        foreign_table_name = foreign_key["foreign_table"]
        primary_table_name = foreign_key["primary_table"]
        constraint_name = foreign_key["constraint_name"]
        fk_columns_name = foreign_key["fk_columns"]
        pr_columns_name = foreign_key["pr_columns"]

        fk_columns_content = level2["%s:%s" % (foreign_table_name, fk_columns_name)].getNotes().getContent()
        try:
            level2["%s:%s" % (foreign_table_name, fk_columns_name)].addMarker(MarkerId.arrowRight)
        except: pass
        level2["%s:%s" % (foreign_table_name, fk_columns_name)].setPlainNotes(
            "%s\n\nforeign key [%s] linked primary key:\n    %s.%s" % (fk_columns_content, constraint_name, primary_table_name, pr_columns_name))

        pr_columns_content = level2["%s:%s" % (primary_table_name, pr_columns_name)].getNotes().getContent()
        # level2["%s:%s" % (primary_table_name, pr_columns_name)].addMarker(MarkerId.arrowLeft)
        level2["%s:%s" % (primary_table_name, pr_columns_name)].setPlainNotes(
            "%s\n\nprimary key [%s] linked foreign key:\n    %s.%s" % (pr_columns_content, constraint_name, foreign_table_name, fk_columns_name))

        # primary_sheet.createRelationship(level2["%s:%s" % (foreign_table_name, fk_columns_name)],
        #                                  level2["%s:%s" % (primary_table_name, pr_columns_name)], constraint_name)

    # create unique constraints
    for unique_index in table_unique_indexes:
        table_name = unique_index["table"]
        index_name = unique_index["index_name"]
        columns = unique_index["columns"]
        content = level1[table_name].getNotes().getContent()
        content += "\nunique constraint: %s\n    fields: %s" % (index_name, columns)
        level1[table_name].setPlainNotes(content)

    # save file
    xmind.save(w, OUTPUT_FILENAME_XMIND)


def parse_mysql_tables_to_xmind():
    '''
    Connect MySQL, print tables into xmind
    '''
    cnx = mysql.connector.connect(user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  port=MYSQL_PORT,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    cursor.execute("SET NAMES utf8")

    tables = []
    cursor.execute("show tables")
    for table in cursor:
        print(table[0])
        tables.append(table[0])

    table_info = dict()
    for table in tables:
        sql = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE table_name = '%s' AND table_schema = '%s'" % (
            table, MYSQL_DATABASE)
        cursor.execute(sql)
        for x in cursor:
            info = get_table_info(x)
            print("table %s" % table)
            print(info)
            table_info[table] = info

    table_columns = dict()
    for table in tables:
        sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '%s' AND table_schema = '%s'" % (
            table, MYSQL_DATABASE)
        cursor.execute(sql)
        print("-- %s --" % table)
        columns = []
        for x in cursor:
            # print(x)
            # print(len(list(x)))
            column = get_table_column(x)
            columns.append(column)
        table_columns[table] = columns
    print(table_columns)

    table_foreign_keys = []
    cursor.execute(MYSQL_FOREIGN_KEYS % (MYSQL_DATABASE))
    for fkey in cursor:
        print(fkey)
        print(len(list(fkey)))
        fkey_def = get_foreign_key_def(fkey)
        table_foreign_keys.append(fkey_def)
    print(table_foreign_keys)

    table_unique_indexes = []
    cursor.execute(MYSQL_UNIQUE_INDEX % (MYSQL_DATABASE))
    for unique in cursor:
        print(unique)
        print(len(list(unique)))
        unique_def = get_unique_index_def(unique)
        table_unique_indexes.append(unique_def)
    print(table_unique_indexes)

    generate_output_file(tables,
                         table_info,
                         table_columns,
                         table_foreign_keys,
                         table_unique_indexes)


##########################################################################
# Testcases
##########################################################################
import unittest


# run testcase: python /c/Users/Administrator/git/mysql_tables_xmind/app/parse_tables_to_xmind.py Test.testExample
class Test(unittest.TestCase):
    '''
    
    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        print("parse_mysql_tables_to_xmind ...")
        parse_mysql_tables_to_xmind()


def test():
    suite = unittest.TestSuite()
    suite.addTest(Test("test_001"))
    runner = unittest.TextTestRunner()
    runner.run(suite)


def main():
    test()


if __name__ == '__main__':
    main()
