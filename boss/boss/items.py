# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BossItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    a_status = Field() # 招聘状态
    b_title = Field() #
    c_salary = Field() #
    d_fuli = Field() #
    e_city  = Field() #
    f_rq1 = Field() #
    f_rq2 = Field() #
    g_name = Field() #
    h_info = Field() #
    i_jobDes = Field() #
    j_comName = Field() #
    k_address = Field() #
