## scrapy_nc

### 安装

```
pip install scrapy_nc
```

### 使用

目前提供以下基础数据:

- scrapy_nc.item.BaseItem 基础 item
- scrapy_nc.pipelines.AMQPPipeline 发送队列 pipeline
- scrapy_nc.pipelines.OSSPipeline 保存 OSS pipeline
- scrapy_nc.pipelines.MongoPipeline 保存 OSS pipeline
  <!-- - scrapy_nc.pipelines.RedisDuplicatesPipeline Redis 去重 Pipeline -->
- scrapy_nc.middlewares.ProxyDownloaderMiddleware 代理下载器


### BaseItem

目前由以下三个 Field 是默认包含的

```

crawled_at = scrapy.Field()  #爬虫时间
oss_filename = scrapy.Field() # oss 路径
unique_id = scrapy.Field()   # 资源唯一id
```

示例：

```

from scrapy_nc.item import BaseItem

class XiaoyusanItem(BaseItem):
    pass
```

### OSSPipeline

OSSPipeline 会将 item 内容保存在 oss 中，如果 oss_filename 如果为空则使用默认规则 {spider_name}/{url_host}/{md5(url)}

安装 oss2

```
pip install oss2
```

settings 配置

```
ITEM_PIPELINES = {
    'scrapy_nc.pipelines.OSSPipeline': 600,
}
```

### MongoPipeline

安装 pymongo

```
pip install pymongo
```

MongoPipeline 初始化会读取以下  mongodb 连接设置

```
MONGO_HOST = os.environ.get('CRAWLAB_MONGO_HOST')
MONGO_PORT = int(os.environ.get('CRAWLAB_MONGO_PORT', '27017'))
MONGO_DB = os.environ.get('CRAWLAB_MONGO_DB')
MONGO_USERNAME = os.environ.get('CRAWLAB_MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('CRAWLAB_MONGO_PASSWORD')
MONGO_AUTHSOURCE = os.environ.get('CRAWLAB_MONGO_AUTHSOURCE')
```

collection_name 是 spider 的 name

手动获取 mongodb collection 操作数据：

```
from scrapy_nc.db import mongo_db
spider_collection = mongo_db.get_collection(name) if mongo_db else None
```

mongo_db.get_collection(xxx) name 可以设置任何 collecton 的名称操作数据

保存数据逻辑：

1. 默认 ENSURE_UNIQUE_INDEX=False unique_id 和 task_id 联合唯一索引

2. 设置 unique_id 唯一索引 需要在 spider 中设置 ENSURE_UNIQUE_INDEX=True 如：
```
class ConsistencyEvaluationDrugsSpider(scrapy.Spider):
    name = 'spider_name'
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_nc.pipelines.ItemCheckPipeline': 100,
            'scrapy_nc.pipelines.MongoPipeline': 800
        },
        'ENSURE_UNIQUE_INDEX': True,
    }
```


### AMQPPipeline

安装 pika

```
pip install pika
```

settings 配置

```
ITEM_PIPELINES = {
    'scrapy_nc.pipelines.AMQPPipeline': 700,
}
```

配置 items.py 添加 queue_names 函数

```

from scrapy_nc.item import BaseItem

class XiaoyusanItem(BaseItem):
    test = scrapy.Field()

    def queue_names(self):
        return ['spider.medical.ncov_community.xiaoyusan'] # 默认发送到线上和线下两个队列，'.dev'或'.prod'结尾的队列只会发送其中一个

```

### RequestPipeline

安装 request


settings 配置

```
ITEM_PIPELINES = {
    'scrapy_nc.pipelines.RequestPipeline': 700,
}
```

在 spider 的 custom_settings 中配置

```json
REQUEST_ADDR 请求地址 必须
REQUEST_TRY_COUNT 请求重试次数 非必须 默认是5
REQUEST_TIMEOUT 请求超时 非必须 默认是5(单位是秒)
REQUEST_SUCCESS_STATUS_CODE 请求成功状态码 非必须 默认是200
REQUEST_VERIFY 请求是否验证证书 非必须 默认是 False
```

示例
```python
class NmpaDrugNewsSpider(scrapy.Spider):
    name = 'nmpa_drug_news'
    custom_settings = {
        'REQUEST_ADDR': f'{os.environ.get("MEDICAL_BASE_FLOW_HOST")}/medicalbase/flow/cfdaDrugNews',
    }

```


### ProxyDownloaderMiddleware

安装 requests

```
pip install requests
```

setting 配置

```
DOWNLOADER_MIDDLEWARES = {
        'scrapy_nc.middlewares.ProxyDownloaderMiddleware': 100,
        'scrapy_splash.SplashCookiesMiddleware': 723,
        'scrapy_splash.SplashMiddleware': 725,
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

如果也使用了 splash，ProxyDownloaderMiddleware 需要在它提供的 middlewares 之前执行。即，数值比它的要小。

公网服务地址 https://spider-proxy.nocode-tech.com
内网服务地址 http://spider-proxy-rest-svc.backend-base:21030


```

##本地开发

```
pip uninstall -y  scrapy_nc && python setup.py install
```