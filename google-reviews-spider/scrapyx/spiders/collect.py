# -*- coding: utf-8 -*-
#!/bin/sh
import sys
import re
import string
import scrapy
import csv
import logging
import json
import urllib
from scrapyx.utils import * 
from scrapy.selector import Selector
from scrapyx.items import ContactItem
from scrapy.http import TextResponse 
import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class ColectSpider(scrapy.Spider):
	name = "collect"
	allowed_domains = []
	start_urls = []    
	proxyOpt = None
	r = []
	input = []

	def __init__(self, proxy_opt = None, *args, **kwargs):
		super(ColectSpider, self).__init__(*args, **kwargs)
		with open('config.json', 'r') as ip:
			config = json.loads(ip.read())
			
		self.allowed_domains.append(config['domain'])
		self.start_urls.append(config['url'])

		self.proxyOpt = int(proxy_opt)					
		
		self.r = init_web_driver(self.proxyOpt)
		self.driver = self.r[0]
		
		with open("list.csv", "rb") as f:
			reader = csv.reader(f, delimiter=",")
			for i, line in enumerate(reader):
				self.input.append(line)

	def parse(self, response):
		#print response.body
		iCnt = len(self.input)
		index = 0
		while index < iCnt:
			print 'Review: ', index
			items = self.input[index]
			self.driver.get(items[1])
			
			# View all Google reviews
			view_reviews = self.driver.find_elements_by_xpath("//*[contains(text(), 'View all Google reviews')]")
			#view_reviews = self.driver.find_elements_by_xpath("//a[contains(@data-async-trigger, 'reviewDialog')]")
			if len(view_reviews):
				try:
					view_reviews[0].click()
				except:
					print "Cannot click!"
			
			wait = WebDriverWait(self.driver, 300).until(
						EC.presence_of_element_located((By.ID ,"reviewSort"))
						)
						
			elem = self.driver.find_element_by_class_name("loris")
			while len(self.driver.find_elements_by_id("lor-nmr")) == 0:
				self.driver.execute_script("return arguments[0].scrollIntoView();", elem)
			
			response = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')		
			for div in response.xpath('.//div[@class="_D7k"]'):
				item = {}
				item['PropertyName'] = items[0]
				item['date'] = div.xpath('.//div[@class="_Q7k"]//span[1]//text()').extract_first()
				item['link'] = items[1]
				item['rating'] = div.xpath('.//g-review-stars//span[1]//@aria-label').extract_first().replace('Rated', '').replace('out of 5,', '').strip()
				if div.xpath('.//span[@class="review-full-text"]'):
					item['review'] = div.xpath('.//span[@class="review-full-text"]//text()').extract_first().encode('utf-8').strip()
				else:
					item['review'] = ''.join([x for x in div.xpath('.//div[@class="_ucl"]//span[1]//text()').extract() if x]).encode('utf-8').strip()
					
				if div.xpath('.//a[@class="_e8k"]'):
					item['reviewer'] = div.xpath('.//a[@class="_e8k"]//text()').extract_first().encode('utf-8')
				
				yield item
				
			index = index + 1
			time.sleep(3)
											  

	def closed(self, reason):
		closeConnection()

					
				
				   
							
		
		
		