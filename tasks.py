import json
import uuid
from celery import Celery
from crawler_worker import CrawlerWorker

BROKER_URL = 'mongodb://localhost:27017/realto'

celery = Celery('tasks', broker=BROKER_URL)

celery.conf.update(
	CELERY_TASK_SERIALIZER = 'json',
	CELERY_RESULT_SERIALIZER = 'json',
	CELERY_ACCEPT_CONTENT = ['json']
)

@celery.task
def process_new_config():
    json_data = open('irr_config.json').read()
    config = json.loads(json_data)
    config['id'] = str(uuid.uuid4())

    wokrer = CrawlerWorker()
    items = wokrer.run(config)

    print len(items)