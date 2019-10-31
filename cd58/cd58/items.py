# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Cd58Item(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # 静态数据
    aTitle = Field()
    bSalary = Field()
    cPos = Field()
    dWelfare = Field()
    eRequire = Field()
    fAddress = Field()
    gDesc = Field()
    hCom_intr = Field()
    iCompany = Field()
    # 名企，网邻通
    jCom_sign = Field()
    # 医疗/保健  服务业 etc.
    kCom_belong = Field()
    lCom_num = Field()
    mCom_iden = Field()
    nCom_detail = Field()
    # 加入 58 多少个月
    oJoin_58 = Field()

    # 动态数据
    pPos_time = Field()
    qView = Field()
    rApply = Field()
    sFeedback = Field()
    tApply_num = Field()
    uCommentCount = Field()


