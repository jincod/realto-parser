from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from irr_item import IrrItem


class IrrSpider(CrawlSpider):
    name = 'irr'

    def __init__(self, *args, **kwargs):
        follow_link = kwargs['config']['link_extractors']['follow_link']
        parse_link = kwargs['config']['link_extractors']['parse_link']

        IrrSpider.rules = (
            Rule(LinkExtractor(allow=(follow_link))),
            Rule(LinkExtractor(allow=(parse_link)), callback='parse_item'),
        )
        super(IrrSpider, self).__init__(*args, **kwargs)

        self.start_urls = kwargs['config']['start_urls']
        self.advert_id_extractor = kwargs['config']['item']['id']['extractor']
        self.advert_title_extractor = kwargs['config']['item']['title']['extractor']
        self.allowed_domains = kwargs['config']['allowed_domains']

        self.config_id = kwargs['id']

    def parse_item(self, response):
        id = response.xpath('string(//body)').re_first(self.advert_id_extractor)
        title = response.css(self.advert_title_extractor + '::text').extract_first().strip()

        item = IrrItem()
        item['id'] = id
        item['title'] = title
        item['config_id'] = self.config_id
        return item
