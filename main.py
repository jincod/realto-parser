import json
import uuid
from crawler_worker import CrawlerWorker


json_data = open('irr_config.json').read()
config = json.loads(json_data)
config['id'] = str(uuid.uuid4())

wokrer = CrawlerWorker()
items = wokrer.run(config)

print len(items)