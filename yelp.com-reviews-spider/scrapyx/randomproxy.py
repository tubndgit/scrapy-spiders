# Copyright (C) 2013 by Aivars Kalvans <aivars.kalvans@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
import random
import base64
from scrapy import log


class RandomProxy(object):
    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        fin = open(self.proxy_list)

        self.proxies = {}
        for line in fin.readlines():
            if not line.strip():
                continue
            parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line)

            # Cut trailing @
            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else:
                user_pass = ''

            self.proxies[parts.group(1) + parts.group(3)] = user_pass

        fin.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def _insert_proxy_into_request(self, request):
        proxy_address = random.choice(self.proxies.keys())
        proxy_user_pass = self.proxies[proxy_address]
        #print 'xxxxxxxxxxxxxxx', proxy_address, proxy_user_pass

        request.meta['proxy'] = proxy_address
        if proxy_user_pass:
            basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = basic_auth

        log.msg('using proxy %s' % proxy_address)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        # if 'proxy' in request.meta:
        #     return
        if not getattr(spider, 'use_proxies', None):
            log.msg('use_proxies is OFF for this spider - not using proxy...')
            return        
        self._insert_proxy_into_request(request)

    def process_exception(self, request, exception, spider):
        log.msg('---------------process_exception---------------')
        print str(exception)
        proxy = request.meta.get('proxy', None)
        if proxy:
            log.msg('Removing failed proxy <%s>, %d proxies left' % (
                        proxy, len(self.proxies)))
            try:
                del self.proxies[proxy]
            except ValueError:
                pass
            except KeyError:
                pass
            self._insert_proxy_into_request(request)
