#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import html.parser
import logging
import os
import re

import diskcache as dc

from ipcn.format import ip2long, long2ip

_logger = logging.getLogger(__name__)
_default_expire = None
try:
    _cache_obj = dc.Cache()
except Exception as err:
    _cache_obj = None
    _logger.warning("init cache obj failed, %s", err)
    pass


class _parser_cls(html.parser.HTMLParser, abc.ABC):
    """parser"""

    def __init__(self):
        super(_parser_cls, self).__init__()
        self._deep = 0
        self._ret_list = []
        self._in_code = False

    def get_ret_list(self):
        return self._ret_list

    def handle_starttag(self, tag, attrs):
        if self._deep > 0:
            self._deep += 1
        elif tag == 'div':
            attr_dict = dict([at for at in attrs if len(at) == 2])
            attr_id = attr_dict.get('id') or ''
            if attr_id == 'result':
                self._deep += 1

        if self._deep > 0 and tag == 'code':
            self._in_code = True

    def handle_data(self, data):
        if self._deep > 0 and self._in_code:
            self._ret_list.append(str.strip(data))

    def handle_endtag(self, tag):
        if self._deep > 0:
            self._deep -= 1
            if tag == 'code':
                self._in_code = False


def _query_from_ip_cn(ip_str: str):
    command = """curl
    'https://ip.cn/?ip=%(ip)s'
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
  -H 'sec-fetch-site: same-origin'
  -H 'sec-fetch-mode: navigate'
  -H 'sec-fetch-user: ?1'
  -H 'sec-fetch-dest: document'
  -H 'referer: https://ip.cn/?ip=%(ip)s'
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8'
  --compressed
  -s
  """

    result = dict()

    try:
        ips = ip_str
        str_command = command % dict(ip=ips)
        str_command = " ".join(filter(lambda x: x, map(str.strip, str_command.split("\n"))))
        with os.popen(str_command) as inf:
            ctx = inf.read()

        parser = _parser_cls()
        parser.feed(ctx)
        parser.close()
        ret_list = parser.get_ret_list()
        # result['ip'] = ret_list[0]
        result['desc_zh'] = ret_list[1]
        cpc = str.split(ret_list[2], ',') if len(ret_list) > 2 else []
        result['city'] = str.strip(cpc[-3] if len(cpc) >= 3 else '')
        result['province'] = str.strip(cpc[-2] if len(cpc) >= 2 else '')
        result['country'] = str.strip(cpc[-1] if len(cpc) >= 1 else '')
    except Exception as err:
        result['error'] = str(err)
        pass

    return result


def query_ip_location(ip_str):
    if isinstance(ip_str, int) or re.match(r"^\d+$", ip_str):
        long_ip = int(ip_str)
        raw_ip = long2ip(long_ip)
    else:
        raw_ip = ip_str
        long_ip = ip2long(ip_str)

    result = dict(ip=raw_ip, ip_long=long_ip)

    if _cache_obj:
        loc_cache = _cache_obj.get(long_ip)
        if loc_cache:
            result.update(loc_cache)
            return result

    loc = _query_from_ip_cn(raw_ip)

    try:
        if _cache_obj:
            _cache_obj.set(long_ip, loc, expire=_default_expire)
    except Exception as ex:
        _logger.error("Cache ip loc for %s failed, Error: %s", raw_ip, ex)

    result.update(loc)
    return result
