# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CommentsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    b_brand = Field()
    a_location = Field()
    c_sortable = Field()
    d_comments = Field()
    e_hottag = Field()
    f_afterCount = Field()
    g_commentCount = Field()
    h_generalCount = Field()
    i_goodCount = Field()
    j_generalCount = Field()
    k_goodRate = Field()
    l_poorCount = Field()
