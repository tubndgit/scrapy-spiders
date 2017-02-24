# -*- coding: utf-8 -*-

# Scrapy settings for scrapyx project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import os
import sys
import random
import requests
from scrapy import log
from requests.exceptions import (Timeout as ReqTimeout,
                                 ProxyError as ReqProxyError, SSLError,
                                 ContentDecodingError, ConnectionError)
                                 
                                 
BOT_NAME = 'scrapyx'

SPIDER_MODULES = ['scrapyx.spiders']
NEWSPIDER_MODULE = 'scrapyx.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyx (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapyx.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapyx.middlewares.MyCustomDownloaderMiddleware': 543,
#}


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'scrapyx.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

#################################################################################################

#LOG_FILE = 'log.txt'

DOWNLOADER_MIDDLEWARES = {
    #'scrapy.downloadermiddlewares.useragent': None,
    #'random_useragent.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    # Fix path to this module
    'scrapyx.randomproxy.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy_crawlera.CrawleraMiddleware': 610,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}
USER_AGENT_LIST = "resources/useragents.txt"

#DOWNLOADER_CLIENTCONTEXTFACTORY = 'scrapyx.CustomContext.CustomClientContextFactory'

ITEM_PIPELINES = {
    #'scrapyx.pipelines.CustomFilesPipeline',
    #'scrapyx.pipelines.CustomImagesPipeline',
    'scrapyx.pipelines.ScrapyxPipeline' : 300,
}

##################################################################
#PROXY
CRAWLERA_ENABLED = False  # false by default
CRAWLERA_APIKEY = ''

# Retry many times since proxies often fail
RETRY_TIMES = 3
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 401, 403, 404, 408]

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...
PROXY_LIST = 'resources/proxy_list.txt'

##################################################################
#Download
FILES_STORE = 'files'
# 90 days of delay for files expiration
FILES_EXPIRES = 90

DOWNLOAD_TIMEOUT = 3600
DOWNLOAD_HANDLERS = {'s3': None}
a='''
CWD = os.path.dirname(os.path.abspath(__file__))

def _check_if_proxies_available(http_proxy_path, timeout=10):
    if not os.path.exists(http_proxy_path):
        return False

    with open(http_proxy_path, 'r') as fh:
        proxies = [l.strip() for l in fh.readlines() if l.strip()]

    hosts = ['google.com', 'bing.com', 'ya.ru', 'yahoo.com']
    for h in hosts:
        prox = random.choice(proxies)
        try:
            requests.get(
                'http://'+h,
                proxies={'http': prox, 'https': prox},
                timeout=timeout
            )
            print('successfully fetched host %s using proxy %s' % (h, prox))
            return True
        except (ReqTimeout, ConnectionError):
            print('failed to fetch host %s using proxy %s' % (h, prox))
            pass  # got timeout - proxy not available
        except (ReqProxyError, SSLError, ContentDecodingError):
            print('proxy %s - failed to fetch host %s' % (prox, h))

if not os.path.exists('/tmp/_stop_proxies'):    
    if (os.path.exists(PROXY_LIST)            
            and _check_if_proxies_available(PROXY_LIST)):
        log.msg('USING PROXIES')
        print('USING PROXIES')
        #DOWNLOADER_MIDDLEWARES['scrapyx.randomproxy.RandomProxy'] = 100
    else:
        log.msg('NOT USING PROXIES')
        print('NOT USING PROXIES')'''