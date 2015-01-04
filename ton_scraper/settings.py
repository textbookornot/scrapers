BOT_NAME = 'ton_scraper'

SPIDER_MODULES = ['ton_scraper.spiders']
NEWSPIDER_MODULE = 'ton_scraper.spiders'

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'jerry',
            'database': 'ton_dev'}

ITEM_PIPELINES = ['ton_scraper.pipelines.TonScraperPipeline']
