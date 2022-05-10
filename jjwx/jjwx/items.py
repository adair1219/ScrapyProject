# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class JjwxItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    作品库类型 = Field()
    a_作者 = Field()
    a_作者_url = Field()
    b_作品 = Field()
    b_作品_url = Field()
    c_类型 = Field()
    d_风格 = Field()
    e_进度 = Field()
    f_字数 = Field()
    g_作品积分 = Field()
    h_发表时间 = Field()

class AuthorItem(Item):
    a_作者 = Field()
    a_被收藏数 = Field()
    a_最近更新作品 = Field()
    a_作品状态 = Field()
    a_作品字数 = Field()
    a_最后更新时间 = Field()
    a_作者所发送红包数 = Field()
    a_小说完本数 = Field()
    a_小说连载数 = Field()
    a_小说暂停数 = Field()

class PieceItems(Item):
    piece_url = Field()
    文章类型 = Field()
    作品视角 = Field()
    作品风格 = Field()
    文章进度 = Field()
    全文字数 = Field()
    签约状态 = Field()
    文章名称 = Field()
    总书评数 = Field()
    文章当前被收藏数 = Field()
    营养液数 = Field()
    文章积分 = Field()

    霸王票全站排行 = Field()
    前进一名所需地雷数 = Field()
    总共地雷数量 = Field()

    总点击量 = Field()

class AllItems(Item):
    author_url = Field()
    a_作者 = Field()
    a_被收藏数 = Field()
    a_最近更新作品 = Field()
    a_作品状态 = Field()
    a_作品字数 = Field()
    a_最后更新时间 = Field()
    a_作者所发送红包数 = Field()
    a_小说完本数 = Field()
    a_小说连载数 = Field()
    a_小说暂停数 = Field()

    piece_url = Field()
    b_文章类型 = Field()
    b_作品视角 = Field()
    b_作品风格 = Field()
    b_文章进度 = Field()
    b_全文字数 = Field()
    b_签约状态 = Field()
    b_文章名称 = Field()
    b_总书评数 = Field()
    b_文章当前被收藏数 = Field()
    b_营养液数 = Field()
    b_文章积分 = Field()

    b_霸王票全站排行 = Field()
    b_前进一名所需地雷数 = Field()
    b_总共地雷数量 = Field()

    b_总点击量 = Field()


class ScoreItems(Item):
    piece_url = Field()
    b_评分 = Field()




