#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sql_in_query.py
@Time    :   2024/05/31 11:58:54
@Author  :   renjiepu 
@Contact :   renjiepu@tencent.com
@Desc    :   构建sql in查询语句
输入：sql_in.txt 每行一个查询项目
输出：sql_in_out.txt in查询语句

示例：
sql_in.txt
123
456

sql_in_out.txt
("123","456")
'''

# here put the import lib


res = ""
with open("sql_in.txt", 'r') as f:
    ids = f.readlines()
id_list = []
for id in ids:
    id_list.append("\"{0}\"".format(id.strip()))
res = res + "(" + ",".join(id_list) + ")"
print(res)
print(len(id_list))
with open("sql_in_out.txt", "w") as f:
    f.write(res)