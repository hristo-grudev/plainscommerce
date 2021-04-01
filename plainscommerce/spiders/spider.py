import scrapy

from scrapy.loader import ItemLoader

from ..items import PlainscommerceItem
from itemloaders.processors import TakeFirst


class PlainscommerceSpider(scrapy.Spider):
	name = 'plainscommerce'
	start_urls = ['https://www.plainscommerce.com/news']

	def parse(self, response):
		post_links = response.xpath('//div[@class="news-buttons"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="content-block"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="post-date"]/text()').get()

		item = ItemLoader(item=PlainscommerceItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
