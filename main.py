import json
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher
from irr_spider import IrrSpider

process = CrawlerProcess(Settings({'ITEM_PIPELINES': {'pipelines.JsonWriterPipeline'}}))

items = []

def item_passed(item):
    items.append(item)

dispatcher.connect(item_passed, signals.item_passed)

json_data = open('irr_config.json').read()
config = json.loads(json_data)

process.crawl(IrrSpider, **config)
process.start()

print len(items)