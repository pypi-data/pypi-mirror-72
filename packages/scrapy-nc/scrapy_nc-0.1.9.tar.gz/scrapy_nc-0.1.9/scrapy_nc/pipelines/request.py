from scrapy.exceptions import DropItem
import requests
import os
import json


class RequestPipeline(object):

    def __init__(self, crawler, request_addr, request_try_count, request_timeout, request_success_status_code,
                 request_verify):
        self.crawler = crawler
        self.request_addr = request_addr
        self.request_try_count = request_try_count or 5
        self.request_timeout = request_timeout or 5
        self.request_success_status_code = request_success_status_code or 200
        self.request_verify = request_verify or False

    def process_item(self, item, spider):
        if self.request_addr == '':
            spider.logger.info(f'spider {spider.name} no REQUEST_ADDR setting')
            return item

        unique_id = item['unique_id']
        if not unique_id:
            raise DropItem('unique_id is None')

        data = item.deepcopy().to_dict()
        # convert datetime to str before serialize
        data['crawled_at'] = data['crawled_at'].isoformat()
        # compatible with old codes
        if self.request_addr:
            for retry_count in range(self.request_try_count):
                response = requests.post(self.request_addr, json=data, timeout=self.request_timeout,
                                         verify=self.request_verify)
                if int(response.status_code) == self.request_success_status_code:
                    spider.logger.info(f'req addr: {self.request_addr}  {unique_id} request success')
                    return item
                spider.logger.info(f'req addr: {self.request_addr} {unique_id} request fail, {response.status_code} {data}')
        flow_urls = item.get('flow_urls', None)
        if not flow_urls:
            flow_urls = spider.settings.get('FLOW_URLS')
        if flow_urls:
            data_helper_url = spider.settings.get('DATA_HELPER_URL')
            if not data_helper_url:
                data_helper_url = os.environ.get('DATA_HELPER_URL')
            if not data_helper_url:
                spider.logger.error(f'data helper url not found, config url to settings')
                return item
            else:
                config_type = type(flow_urls)
                flows = []
                if config_type == str:
                    flows.append(flow_urls)
                elif config_type == list:
                    flows = flow_urls
                else:
                    spider.logger.error(f'flow urls config type error, make sure the type must be an array or string')
                    return item
                response = requests.post(data_helper_url, json={
                    'flow_urls': flows,
                    'payload': json.dumps(data),
                }, timeout=5)
                if response.status_code == 200:
                    spider.logger.info(f'send data to helper success: {item.get("unique_id")}')
                else:
                    spider.logger.warn(f'send data to helper fail: {item.get("unique_id")} {response.status_code}')
                return item
        return item


    @classmethod
    def from_crawler(cls, crawler):
        if crawler.spider is None:
            return
        request_addr = crawler.spider.settings.get('REQUEST_ADDR')
        request_try_count = crawler.spider.settings.get('REQUEST_TRY_COUNT')
        request_timeout = crawler.spider.settings.get('REQUEST_TIMEOUT')
        request_success_status_code = crawler.spider.settings.get('REQUEST_SUCCESS_STATUS_CODE')
        request_verify = crawler.spider.settings.get('REQUEST_VERIFY')
        return cls(
            crawler,
            request_addr,
            request_try_count,
            request_timeout,
            request_success_status_code,
            request_verify
        )
