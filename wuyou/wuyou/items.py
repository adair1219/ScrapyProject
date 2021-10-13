# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ZhilianItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    a_JobName = Field()  # 职位
    b_ComName = Field()  # 公司名
    c_Location = Field()  # 地点
    d_Salary = Field()  # 薪水
    e_PubDate = Field()  # 发布时间
    f_Require = Field()  # 要求
    g_Walfare = Field()  # 福利
    h_Info = Field()  # 职位信息
    i_Type = Field()  # 职位类别
    j_keyword = Field()  # 关键字
    k_CompInfo = Field()  # 公司信息
    

