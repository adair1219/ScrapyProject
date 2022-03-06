# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class Job51Item(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = Field()
    jt = Field()
    tags = Field()
    ad_track = Field()
    jobid = Field()
    coid = Field()
    effect = Field()
    is_special_job = Field()
    job_href = Field()
    job_name = Field()
    job_title = Field()
    company_href = Field()
    company_name = Field()
    providesalary_text = Field()
    workarea = Field()
    workarea_text = Field()
    updatedate = Field()
    iscommunicate = Field()
    companytype_text = Field()
    degreefrom = Field()
    workyear = Field()
    issuedate = Field()
    isFromXyz = Field()
    isIntern = Field()
    jobwelf = Field()
    jobwelf_list = Field()
    isdiffcity = Field()
    attribute_text = Field()
    companysize_text = Field()
    companyind_text = Field()
    adid = Field()

