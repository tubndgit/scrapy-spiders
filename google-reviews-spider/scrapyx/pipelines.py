# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import sys
import csv
#import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
#from scrapy.pipelines.images import ImagesPipeline
import json

class ScrapyxPipeline(object):
    def __init__(self):
        self.fieldNames = ['PropertyName', 'link', 'rating', 'review', 'date', 'reviewer']
        self.csvfile = open('result.csv', 'wb');
        self.csvwriter = csv.DictWriter(self.csvfile, fieldnames = self.fieldNames)
        self.csvwriter.writeheader()
        
    def process_item(self, item, spider): 
        self.csvwriter.writerow(item)        
        return item
        