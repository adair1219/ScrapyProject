# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class JingdongItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    a_Loc = Field()  # 原产地
    b_Title = Field()  # 商品标题
    c_Mall = Field()  # 店铺
    d_Mall_url = Field()  # 店铺网址
    e_Brand = Field()  # 商品品牌
    Z_Url = Field()  # 商品链接，方便查询
    f_Sortable = Field()  # 商品类别
    g_Ads = Field()  # 商家广告
    h_StartCity = Field()  # 商品配送出发地, ！因不知购买者地址，所以配送远近因素可以忽略
    i_State = Field()  # 商品状态，如现货，无货
    # j_CashDesc = Field()  # 额外说明，如在线支付免运费
    k_JdPrice = Field()  # 京东商品价格
    # k_JdPrice_min = Field()  # 商品最小价格
    # l_JdPrice_max = Field()  # 商品最大价格
    # l_PromiseMark = Field()  # 商家承诺
    # m_PromiseResult = Field()  # 承诺具体内容

# class CommentsItem(Item):
    A_comments = Field()  # 评论内容
    B_hottag = Field()  # 商品标签
    C_hottag_number = Field()  # 标签数量
    D_commentCount = Field()  # 评论总数
    E_afterCount = Field()  # 追加数量
    F_generalCount = Field()  # 一般评论数量
    G_goodCount = Field()  # 好评数
    H_goodRate = Field()  # 好评率
    I_poorCount = Field()   # 差评数
    J_score1Count = Field()  # 一星评论数
    K_score2Count = Field()  # 二星
    L_score3Count = Field()  # 三星
    M_score4Count = Field()  # 四星
    N_score5Count = Field()  # 五星

    venderId = Field()

