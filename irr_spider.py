import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from irr_item import IrrItem

class IrrSpider(CrawlSpider):
    name = 'IRR.RU'
    advert_selector = '.productGrid a.productBlock::attr("href")'

    follow_link = ''
    parse_link = ''

    def __init__(self, *args, **kwargs):
        super(IrrSpider, self).__init__(*args, **kwargs)

        self.start_urls = kwargs['config']['start_urls']
        self.advert_id_extractor = kwargs['config']['item']['id']['extractor']
        self.advert_title_extractor = kwargs['config']['item']['title']['extractor']
        self.allowed_domains = kwargs['config']['allowed_domains']

        self.follow_link = kwargs['config']['link_extractors']['follow_link']
        self.parse_link = kwargs['config']['link_extractors']['parse_link']
        self.config_id = kwargs['id']

    def parse(self, response):
        for url in response.css(self.advert_selector).extract():
            yield scrapy.Request(response.urljoin(url), self.parse_item)

    # rules = (
        # Rule(LinkExtractor(allow=(follow_link))),
    #     Rule(LinkExtractor(allow=(parse_link)), callback='parse_item', follow=False),
    # )

    def parse_item(self, response):
        id = response.xpath('string(//body)').re_first(self.advert_id_extractor)
        # title = str(response.xpath('string(//body)').re_first(re.compile(self.advert_title_extractor, re.DOTALL))).strip()
        title = response.css('.productName::text').extract_first().strip()
        item = IrrItem()
        item['id'] = id
        item['title'] = title
        item['config_id'] = self.config_id
        return item
