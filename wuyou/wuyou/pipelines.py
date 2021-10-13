# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ZhilianPipeline(object):
    def process_item(self, item, spider):
        item['c_Location'] = item['c_Location'].replace(r'\xa0', '')
        item['f_Require'] = item['f_Require'].replace(r'\xa0', '')
        item['h_Info'] = item['h_Info'].replace(r'\t', '')
        item['k_CompInfo'] = item['k_CompInfo'].replace(r'\xa0', '')

        return '数据处理完成'
