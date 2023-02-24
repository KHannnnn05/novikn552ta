import scrapy


class OptlistItem(scrapy.Item):
    url = scrapy.Field()
    date = scrapy.Field()
    cardname = scrapy.Field()
    region = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
