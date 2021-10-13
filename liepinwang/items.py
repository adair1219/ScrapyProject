# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LiepinwangItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    a_JobName = Field()  # 职位
    b_ComName = Field()  # 公司名
    c_Location = Field()  # 地点
    d_Salary = Field()  # 薪水
    e_PubDate = Field()  # 发布时间
    f_Require = Field()  # 要求
    g_tags = Field()  # 标签
    h_Info = Field()  # 职位信息
    i_Belong = Field()  # 所属部门
    j_Duixiang = Field()  # 汇报对象
    k_Xiashu = Field() # 下属人数
    l_CompInfo = Field()  # 公司介绍
    m_Hangye = Field() # 行业
    n_Guimo = Field() # 公司规模
    o_Address = Field() # 公司地址
    p_Time = Field() # 注册时间
    q_Ziben = Field() # 注册资本
    r_Date = Field() # 经营期限
    s_Range = Field() # 经营范围

