# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook

class LetpubPipeline(object):

    def __init__(self):
        self.wb = Workbook()  # 创建 excel，填写表头
        self.ws = self.wb.active

        self.ws.append(['负责人', '单位', '金额(万)', '项目编号', '项目类型', '所属学院', '批准年份', '题目', '学科分类',
                        '学科代码', '执行时间'])  # 设置表头

    def process_item(self, item, spider):
        line = [item['principal'], item['unit'], item['amount'], item['numbering'], item['project_item'],
                item['department'], item['year'], item['topic'], item['classification'], item['coding'],
                item['excutionTime']]
        self.ws.append(line)
        self.wb.save('sci.xls')
        return item
