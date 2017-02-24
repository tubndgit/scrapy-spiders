# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ContactItem(scrapy.Item):
	PropertyName = scrapy.Field()      
	link = scrapy.Field()      
	rating = scrapy.Field()         
	review = scrapy.Field()     
	date = scrapy.Field()  
	reviewer = scrapy.Field()