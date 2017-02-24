# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ContactItem(scrapy.Item):
	Suburb = scrapy.Field()
	Keyword = scrapy.Field()      
	CompanyName = scrapy.Field()      
	Description = scrapy.Field()
	Address = scrapy.Field()         
	Phone = scrapy.Field()        
	Website = scrapy.Field()  
	Email = scrapy.Field()    