from scrapy import Item, Field

class IrrItem(Item):
    id = Field()
    title = Field()