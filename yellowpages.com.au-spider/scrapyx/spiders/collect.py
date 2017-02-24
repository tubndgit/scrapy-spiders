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
from scrapy import Request
import scrapy
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.common.action_chains import ActionChains
#import winsound
from PIL import Image
from time import sleep, time
from random import uniform, randint
#import deathbycaptcha
import ast
import hashlib

class ColectSpider(scrapy.Spider):
	name = "collect"
	allowed_domains = []
	start_urls = []    	
	lines = None	
	format_url = "https://www.yellowpages.com.au/search/listings?clue={}&locationClue={}&lat=&lon=&selectedViewMode=list"
	maps = {}
	list_urls = []

	def __init__(self, proxy_opt = None, *args, **kwargs):
		super(ColectSpider, self).__init__(*args, **kwargs)
		with open('config.json', 'r') as ip:
			config = json.loads(ip.read())
			
		self.allowed_domains.append(config['domain'])
		if config['url'] <> "":
			self.start_urls.append(config['url']) 
		
		self.proxyOpt = int(proxy_opt)                  		
		self.driver = init_web_driver(self.proxyOpt)

		f = open('keywords.txt', 'r+')
		self.lines = f.readlines()         
		f.close() 
		
		for line in self.lines:
			keyword = line.strip().replace(' ', '+')
			suburb = '4227'
			url = self.format_url.format(keyword, suburb)
			self.list_urls.append(url)
			key = hashlib.md5(url.encode('utf-8'))
			self.maps[key]= [suburb, keyword]		
			
	def parse(self, response):
		for url in self.list_urls:
			self.driver.get(url)
			self.wait_between(1.5, 3.0)            
			iLoop = True
				
			while iLoop:                           
				CheckBox = WebDriverWait(self.driver, 3000).until(
					EC.presence_of_element_located((By.CSS_SELECTOR ,".emphasise"))
					)
				response = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')            
							  
				current_url = self.driver.current_url
				aParts = (current_url.split('?')[1]).split('&')
				for x in aParts:
					params = x.split('=')
					if params[0] == 'clue':
						keyword = params[1].replace('%20', ' ').replace('+', ' ')
					if params[0] == 'locationClue':
						suburb = params[1]
						
				for div in response.xpath('.//div[@class="flow-layout outside-gap-large inside-gap inside-gap-large vertical"]//div[@class="cell in-area-cell middle-cell"]'):					
					if div.xpath('.//a[@class="listing-name"]//text()').extract_first():
						if div.xpath('.//a[@title="Phone"]'):
							phone = div.xpath('.//a[@title="Phone"]//@href').extract_first()
							if phone:
								sphone = phone.replace('tel:', '')
								if self.checkDuplicates(sphone) == False:
									item = {}
									item['Phone'] = sphone								
									item['Suburb'] = suburb
									item['Keyword'] = keyword
									item['CompanyName'] = div.xpath('.//a[@class="listing-name"]//text()').extract_first().strip().encode('utf-8')
									if div.xpath('.//p[@class="listing-short-description"]'):
										item['Description'] = div.xpath('.//p[@class="listing-short-description"]//text()').extract_first().encode('utf-8')
									if div.xpath('.//p[@class="listing-address mappable-address"]'):
										item['Address'] = div.xpath('.//p[@class="listing-address mappable-address"]//text()').extract_first().encode('utf-8')
									if div.xpath('.//p[@class="listing-address mappable-address mappable-address-with-poi"]'):
										item['Address'] = div.xpath('.//p[@class="listing-address mappable-address mappable-address-with-poi"]//text()').extract_first().encode('utf-8')
									
									if div.xpath('.//a[@class="contact contact-main contact-email "]'):
										item['Email'] = div.xpath('.//a[@class="contact contact-main contact-email "]//@data-email').extract_first()
									if div.xpath('.//a[@class="contact contact-main contact-url "]'):
										item['Website'] = div.xpath('.//a[@class="contact contact-main contact-url "]//@href').extract_first()
									
									yield item
				
				# parse next page
				if response.xpath('.//a[contains(@class, "pagination navigation") and contains(text(), "Next")]'):
					next_url = response.xpath('.//a[contains(@class, "pagination navigation") and contains(text(), "Next")]//@href').extract_first()
					self.driver.get(response.urljoin(next_url))					
					self.wait_between(1.5, 3.0)
				else:
					iLoop = False						
				
	def wait_between(self, a,b):
		rand=uniform(a, b) 
		sleep(rand)

	def saveUrl(self, file, url):        
		f = open(file, 'a')
		f.write(url.encode('utf-8') + '\n')            
		f.close()   

	def checkDuplicates(self, phone):
		bReturn = False
		f = open('phone.txt', 'r+')
		lines = f.readlines()
		f.seek(0)
		f.truncate()
		
		for line in lines: 
			line = line.strip()
			f.write(line + '\n')
			if phone == line:
				bReturn = True                
													  
		if bReturn == False:
			f.write(phone + '\n')
			
		f.close()
		
		return bReturn