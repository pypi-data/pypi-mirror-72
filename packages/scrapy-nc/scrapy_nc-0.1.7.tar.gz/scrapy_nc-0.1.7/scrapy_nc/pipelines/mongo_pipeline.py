from scrapy_nc.db import mongo_db
import datetime
import json


class MongoPipeline(object):
    def process_item(self, item, spider):
        if not self.spider_collection:
            spider.logger.warn(f'mongodb not collected, ignore save')
            return item
        item['crawled_at'] = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc)
        my_item = item.deepcopy()
        item_dict = dict(my_item)
        self.spider_collection.update_one({
            'unique_id':   my_item.get('unique_id')
        }, {"$set": item_dict}, upsert=True)
        return item

    def open_spider(self, spider):
        if not mongo_db:
            self.spider_collection = None
            spider.logger.error('mongodb no configuration')
            return
        self.spider_collection = mongo_db.get_collection(spider.name)
        spider.collection = self.spider_collection
        res = json.dumps(self.spider_collection.index_information())
        spider.logger.info(
            f'index_information {res}')
        index_name = 'unique_id'
        if index_name not in self.spider_collection.index_information():
            self.spider_collection.create_index(
                'unique_id', unique=True, name=index_name)
            spider.logger.info(f"create unique index {index_name}")
        ttl = spider.settings.get('DATA_TTL')
        if ttl is None:
            ttl = 86400 * 30 # 默认过期时间 30 天
            spider.logger.info(f'not found data_ttl,  set ttl 30 days')
        if ttl == -1:
            return
        if ttl > 0:
            expire_index_name = "crawled_at"
            if expire_index_name not in self.spider_collection.index_information():
                self.spider_collection.create_index(
                    "crawled_at", name=expire_index_name, expireAfterSeconds=ttl,
                )
                spider.logger.info(f'create ttl index {expire_index_name}, ttl: {ttl}')
