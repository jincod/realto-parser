import json
import uuid
from crawler_worker import CrawlerWorker


with open('irr_config.json', 'r') as json_data:
    config = json.loads(json_data.read())
    config['id'] = str(uuid.uuid4())

wokrer = CrawlerWorker()
items = wokrer.run(config)

print len(items)
