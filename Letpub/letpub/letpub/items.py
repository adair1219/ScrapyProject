# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LetpubItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    principal = Field()
    unit = Field()
    amount = Field()
    project_item = Field()
    numbering = Field()
    department = Field()
    year = Field()
    topic = Field()
    classification = Field()
    coding = Field()
    excutionTime = Field()
