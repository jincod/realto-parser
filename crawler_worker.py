from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher
from irr_spider import IrrSpider

class CrawlerWorker():
    def __init__(self):
        self.process = CrawlerProcess(Settings({
            'ITEM_PIPELINES': {
                'pipelines.MongoDBPipeline': 1
            },
            'MONGO_URI': 'mongodb://localhost:27017/',
            'MONGO_DATABASE': 'realto'
        }))

        self.items = []
        dispatcher.connect(self.item_passed, signals.item_passed)

    def item_passed(self, item):
        self.items.append(item)

    def run(self, config):
        self.process.crawl(IrrSpider, **config)
        self.process.start()
        return self.items