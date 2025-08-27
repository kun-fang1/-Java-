# -*- coding: utf-8 -*-

"""
@Time : 2022-02-28
@Author : Robin Luo
@File : 练习
@Description : 
"""
import xlrd
import json
path = r'思政元素数据.xlsx'
sheet_name= 'Sheet1'

bk=xlrd.open_workbook(path)
sh = bk.sheet_by_name(sheet_name)
row_num = sh.nrows
data_list = []
for i in range(1, row_num):
    row_data = sh.row_values(i)
    # print(row_data)
    data={}
    for index,key in enumerate(sh.row_values(0)):
        data[key]=row_data[index]
    data_list.append(data)
# print(data_list)

f = open('data/思政元素数据.json', 'w', encoding="utf-8")
for data_dict in data_list:
    data_str = json.dumps(data_dict, ensure_ascii=False)
    print(data_str)
    f.write(data_str)
    f.write('\n')
f.close()
# json_str = '/n'.join(data_list)

# f = open('release_note.json', 'w')
# f.write(json_str)
# f.close()
