from .amqp_pipeline import AMQPPipeline
from .mongo_pipeline import MongoPipeline
from .item_check_pipeline import ItemCheckPipeline
from .filter_pipeline import FilterCheckPipeline, FilterSavePipeline
from .request import RequestPipeline


ITEM_CHECK_PIPELINE = 'scrapy_nc.pipelines.ItemCheckPipeline'
FILTER_CHECK_PIPELINE = 'scrapy_nc.pipelines.FilterCheckPipeline'
AMQP_PIPELINE = 'scrapy_nc.pipelines.AMQPPipeline'
MONGO_PIPELINE = 'scrapy_nc.pipelines.MongoPipeline'
FILTER_SAVE_PIPELINE = 'scrapy_nc.pipelines.FilterSavePipeline'
REQUEST_PIPELINE = 'scrapy_nc.pipelines.RequestPipeline'

DEFAULT_PIPELINES = {
    ITEM_CHECK_PIPELINE: 500,
    MONGO_PIPELINE: 700,
    REQUEST_PIPELINE: 760,
}
