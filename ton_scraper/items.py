#######################################################################
#                               imports                               #
#######################################################################

import scrapy

#######################################################################
#                                items                                #
#######################################################################

class Course(scrapy.Item):
    number = scrapy.Field()
    title = scrapy.Field()
    instructors = scrapy.Field()
    description = scrapy.Field()
    #terms = scrapy.Field()
    units = scrapy.Field()
    subject_title = scrapy.Field()
    subject_code = scrapy.Field()

class Textbook(scrapy.Item):
    isbn10 = scrapy.Field()
    isbn13 = scrapy.Field()
    course = scrapy.Field()
    school = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    edition = scrapy.Field()
    image_url = scrapy.Field()
    amazon_link = scrapy.Field()
    #ebay_link = scrapy.Field()
    #chegg_link = scrapy.Field()
